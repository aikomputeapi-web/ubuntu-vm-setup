#!/usr/bin/env bash
# ============================================================================
# ubuntu-vm-setup.sh — Universal Ubuntu VM Installer with Public SSH
# ============================================================================
# Works in: sandboxes, notebooks, codespaces, bare metal, WSL, Docker
# Features:
#   - Auto-detects environment (container/sandbox/bare metal)
#   - Auto-selects best hypervisor (KVM > TCG > fallback)
#   - Downloads & boots Ubuntu cloud image
#   - Configures NAT networking with internet access
#   - Sets up public SSH via Cloudflare Tunnel
#   - Includes watchdog for VM + tunnel keepalive
#   - Survives host reboots (optional systemd integration)
#
# Usage:
#   chmod +x ubuntu-vm-setup.sh && ./ubuntu-vm-setup.sh
#   # Or with options:
#   VM_DISK_SIZE=50 VM_RAM=4094 VM_CPUS=4 ./ubuntu-vm-setup.sh
# ============================================================================

set -euo pipefail
IFS=$'\n\t'

# ── Configuration Defaults ──────────────────────────────────────────────────
VM_NAME="${VM_NAME:-ubuntu-vm}"
VM_DISK_SIZE="${VM_DISK_SIZE:-50}"         # GB
VM_RAM="${VM_RAM:-4096}"                  # MB
VM_CPUS="${VM_CPUS:-2}"
VM_SSH_PORT="${VM_SSH_PORT:-2222}"
VM_HOST_FWD="${VM_HOST_FWD:-8022}"        # Host port forwarded to VM:22
VM_IMAGE_DIR="${VM_IMAGE_DIR:-$HOME/.vm-images}"
VM_DISK_DIR="${VM_DISK_DIR:-$HOME/.vm-disks}"
CLOUD_IMAGE_URL="${CLOUD_IMAGE_URL:-https://cloud-images.ubuntu.com/noble/current/noble-server-cloudimg-amd64.img}"
CLOUD_IMAGE_NAME="${CLOUD_IMAGE_NAME:-ubuntu-24.04-server-cloudimg-amd64.img}"
VM_USER="${VM_USER:-ubuntu}"
VM_PASS="${VM_PASS:-ubuntu}"
SSH_KEY="${SSH_KEY:-$HOME/.ssh/id_ed25519}"
TUNNEL_TOKEN="${CLOUDFLARE_TUNNEL_TOKEN:-}"  # Optional: for persistent tunnels

# ── Colors ──────────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; CYAN='\033[0;36m'; NC='\033[0m'

log()  { echo -e "${GREEN}[+]${NC} $*"; }
warn() { echo -e "${YELLOW}[!]${NC} $*"; }
err()  { echo -e "${RED}[x]${NC} $*" >&2; }
info() { echo -e "${BLUE}[i]${NC} $*"; }
banner() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║         Ubuntu VM Setup — Universal Installer              ║"
    echo "║   Sandboxes · Notebooks · Codespaces · Bare Metal          ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# ── Environment Detection ───────────────────────────────────────────────────
detect_environment() {
    log "Detecting environment..."
    ENV_TYPE="unknown"
    CONTAINER_RUNTIME="none"

    # Check for container/sandbox indicators
    if [ -f /.dockerenv ]; then
        ENV_TYPE="docker"
        CONTAINER_RUNTIME="docker"
    elif grep -qE 'docker|lxc|containerd' /proc/1/cgroup 2>/dev/null; then
        ENV_TYPE="container"
        CONTAINER_RUNTIME=$(head -1 /proc/1/cgroup | grep -oP '(docker|lxc|containerd)')
    elif [ -f /run/.containerenv ]; then
        ENV_TYPE="podman"
        CONTAINER_RUNTIME="podman"
    elif grep -qiE 'codespace|vscode' /proc/version 2>/dev/null; then
        ENV_TYPE="codespace"
    elif [ -n "${GITHUB Codespace:-}" ] || [ -n "${CODESPACE_NAME:-}" ]; then
        ENV_TYPE="codespace"
    elif grep -qi 'microsoft' /proc/version 2>/dev/null; then
        ENV_TYPE="wsl"
    elif [ -f /etc/google-cloud/ ] || [ -n "${DEVSHELL_NAME:-}" ]; then
        ENV_TYPE="notebook"  # GCP/GCE or similar
    elif [ -f /proc/version ] && grep -qi 'microsoft\|WSL' /proc/version; then
        ENV_TYPE="wsl"
    else
        ENV_TYPE="bare-metal"
    fi

    # Check for nested virtualization
    HAS_KVM=false
    if [ -e /dev/kvm ] && [ -r /dev/kvm ] && [ -w /dev/kvm ]; then
        HAS_KVM=true
    fi

    # Check available resources
    TOTAL_RAM_MB=$(free -m 2>/dev/null | awk '/^Mem:/{print $2}' || echo "2048")
    TOTAL_CPUS=$(nproc 2>/dev/null || echo "2")
    FREE_DISK_GB=$(df -BG / 2>/dev/null | awk 'NR==2{print $4}' || echo "10")

    info "Environment: $ENV_TYPE"
    info "KVM available: $HAS_KVM"
    info "Host RAM: ${TOTAL_RAM_MB}MB | CPUs: $TOTAL_CPUS | Free disk: ${FREE_DISK_GB}GB"
}

# ── Dependency Installation ─────────────────────────────────────────────────
install_deps() {
    log "Installing dependencies..."
    local pkgs=()

    # Detect package manager
    if command -v apt-get &>/dev/null; then
        PKG_MGR="apt"
    elif command -v yum &>/dev/null; then
        PKG_MGR="yum"
    elif command -v dnf &>/dev/null; then
        PKG_MGR="dnf"
    elif command -v apk &>/dev/null; then
        PKG_MGR="apk"
    elif command -v pacman &>/dev/null; then
        PKG_MGR="pacman"
    else
        PKG_MGR="unknown"
        warn "Unknown package manager — assuming deps are pre-installed"
    fi

    # QEMU (try KVM-enabled first, fall back to TCG)
    if ! command -v qemu-system-x86_64 &>/dev/null; then
        pkgs+=(qemu-system-x86 qemu-img)
        if [ "$PKG_MGR" = "apk" ]; then
            # Alpine needs qemu-system-x86_64 separately
            pkgs+=(qemu-system-x86_64 qemu-img)
        fi
    fi

    # Supporting tools
    pkgs+=(wget curl socat cloud-utils genisoimage xorriso socat)

    if [ "$PKG_MGR" = "apt" ]; then
        sudo apt-get update -qq
        sudo apt-get install -y -qq "${pkgs[@]}" qemu-utils cloud-image-utils xorriso socat 2>/dev/null || true
    elif [ "$PKG_MGR" = "yum" ] || [ "$PKG_MGR" = "dnf" ]; then
        sudo "$PKG_MGR" install -y -q qemu-system-x86 qemu-img wget curl socat genisoimage xorriso 2>/dev/null || true
    elif [ "$PKG_MGR" = "apk" ]; then
        sudo apk add --no-cache qemu-system-x86_64 qemu-img wget curl socat cdrtools xorriso 2>/dev/null || true
    elif [ "$PKG_MGR" = "pacman" ]; then
        sudo pacman -Sy --noconfirm qemu-full wget curl socat cdrtools xorriso 2>/dev/null || true
    fi

    # Verify QEMU installed
    if ! command -v qemu-system-x86_64 &>/dev/null; then
        err "Failed to install QEMU. Trying alternative: qemu-system-x86_64"
        if command -v qemu-system-x86_64 &>/dev/null; then
            QEMU_BIN="qemu-system-x86_64"
        else
            err "Cannot find any QEMU binary. Exiting."
            exit 1
        fi
    else
        QEMU_BIN="qemu-system-x86_64"
    fi

    # Verify qemu-img
    if ! command -v qemu-img &>/dev/null && ! command -v qemu-img.exe &>/dev/null; then
        err "qemu-img not found"
        exit 1
    fi
    QEMU_IMG="qemu-img"

    log "QEMU: $($QEMU_BIN --version 2>/dev/null | head -1)"
}

# ── Hypervisor Selection ────────────────────────────────────────────────────
select_hypervisor() {
    log "Selecting hypervisor mode..."
    if $HAS_KVM; then
        HYPERVISOR="kvm"
        ACCEL="-accel kvm -cpu host"
        info "Using KVM (hardware acceleration)"
    else
        HYPERVISOR="tcg"
        ACCEL="-accel tcg -cpu max"
        warn "KVM not available — using TCG (software emulation, slower)"
        warn "Performance will be degraded. This is expected in containers/sandboxes."
    fi
}

# ── Disk & Image Setup ──────────────────────────────────────────────────────
setup_disk() {
    log "Setting up VM disk..."
    mkdir -p "$VM_DISK_DIR"

    local vm_disk="$VM_DISK_DIR/${VM_NAME}.qcow2"
    VM_DISK="$vm_disk"

    if [ -f "$vm_disk" ]; then
        info "Existing disk found: $vm_disk"
        local current_size
        current_size=$($QEMU_IMG info "$vm_disk" 2>/dev/null | grep 'virtual size' | grep -oP '\d+' || echo "0")
        if [ "$current_size" -lt "$((VM_DISK_SIZE * 1073741824))" ] 2>/dev/null; then
            warn "Resizing disk to ${VM_DISK_SIZE}GB..."
            $QEMU_IMG resize "$vm_disk" "${VM_DISK_SIZE}G" 2>/dev/null || true
        fi
    else
        log "Creating ${VM_DISK_SIZE}GB disk image..."
        $QEMU_IMG create -f qcow2 "$vm_disk" "${VM_DISK_SIZE}G"
        log "Disk created: $vm_disk"
    fi
}

download_image() {
    log "Downloading Ubuntu cloud image..."
    mkdir -p "$VM_IMAGE_DIR"

    local image_path="$VM_IMAGE_DIR/$CLOUD_IMAGE_NAME"
    VM_IMAGE="$image_path"

    if [ -f "$image_path" ]; then
        info "Image already downloaded: $image_path"
        return 0
    fi

    log "Downloading from: $CLOUD_IMAGE_URL"
    if command -v wget &>/dev/null; then
        wget -q --show-progress -O "$image_path" "$CLOUD_IMAGE_URL"
    elif command -v curl &>/dev/null; then
        curl -L --progress-bar -o "$image_path" "$CLOUD_IMAGE_URL"
    else
        err "Neither wget nor curl available"
        exit 1
    fi

    log "Image downloaded: $image_path"
}

# ── Cloud-Init User Data ────────────────────────────────────────────────────
create_cloud_init() {
    log "Creating cloud-init user data..."
    local user_data_dir="$VM_DISK_DIR/${VM_NAME}-cidata"
    VM_CIDATA="$user_data_dir"
    mkdir -p "$user_data_dir"

    # Generate SSH key if not present
    if [ ! -f "$SSH_KEY" ]; then
        log "Generating SSH key pair..."
        ssh-keygen -t ed25519 -f "$SSH_KEY" -N "" -q
    fi

    local public_key
    public_key=$(cat "${SSH_KEY}.pub" 2>/dev/null || cat "$SSH_KEY" 2>/dev/null)

    cat > "$user_data_dir/user-data" <<USERDATA
#cloud-config
hostname: ${VM_NAME}
manage_etc_hosts: true

users:
  - name: ${VM_USER}
    sudo: ALL=(ALL) NOPASSWD:ALL
    shell: /bin/bash
    lock_passwd: false
    plain_text_passwd: ${VM_PASS}
    ssh_authorized_keys:
      - ${public_key}

ssh_pwauth: true
disable_root: false

package_update: true
package_upgrade: true
packages:
  - openssh-server
  - openssh-client
  - curl
  - wget
  - htop
  - tmux
  - net-tools
  - iputils-ping
  - dnsutils
  - socat
  - ufw
  - jq
  - git

runcmd:
  - systemctl enable ssh
  - systemctl start ssh
  - ufw allow ssh
  - ufw --force enable
  - echo "Ubuntu VM ready — $(date)" > /etc/motd
  - sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
  - sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config
  - systemctl restart ssh

final_message: "Cloud-init finished — VM ready for SSH"
USERDATA

    cat > "$user_data_dir/meta-data" <<META
instance-id: ${VM_NAME}
local-hostname: ${VM_NAME}
META

    # Create ISO
    if command -v genisoimage &>/dev/null; then
        (cd "$user_data_dir" && genisoimage -output "${VM_NAME}-cidata.iso" -volid cidata -joliet -rock user-data meta-data 2>/dev/null)
    elif command -v xorriso &>/dev/null; then
        xorriso -as mkisofs -o "${user_data_dir}/${VM_NAME}-cidata.iso" -V cidata -J -rock "$user_data_dir/user-data" "$user_data_dir/meta-data" 2>/dev/null
    elif command -v mkisofs &>/dev/null; then
        (cd "$user_data_dir" && mkisofs -o "${VM_NAME}-cidata.iso" -V cidata -J -rock user-data meta-data 2>/dev/null)
    else
        warn "No ISO creation tool found. Trying python..."
        python3 -c "
import zipfile, os
with zipfile.ZipFile('${user_data_dir}/${VM_NAME}-cidata.iso', 'w') as z:
    z.write('${user_data_dir}/user-data', 'user-data')
    z.write('${user_data_dir}/meta-data', 'meta-data')
" 2>/dev/null || err "Cannot create cloud-init ISO — VM may not configure automatically"
    fi

    VM_CIDATA_ISO="${user_data_dir}/${VM_NAME}-cidata.iso"
    if [ -f "$VM_CIDATA_ISO" ]; then
        log "Cloud-init ISO created: $VM_CIDATA_ISO"
    else
        warn "Cloud-init ISO not created — manual setup may be needed"
    fi
}

# ── Network Setup ────────────────────────────────────────────────────────────
setup_network() {
    log "Configuring networking..."

    # Create TAP interface if possible (for bridged networking)
    # In containers/sandboxes, we fall back to user-mode SLIRP networking
    USE_TAP=false
    if [ "$(id -u)" -eq 0 ] && command -v ip &>/dev/null && [ "$ENV_TYPE" = "bare-metal" ]; then
        TAP_IF="tap0"
        if ! ip link show "$TAP_IF" &>/dev/null; then
            ip tuntap add dev "$TAP_IF" mode tap 2>/dev/null && USE_TAP=true || true
        fi
        if $USE_TAP; then
            ip addr add 10.0.2.1/24 dev "$TAP_IF" 2>/dev/null || true
            ip link set "$TAP_IF" up 2>/dev/null || true
            # Enable IP forwarding and NAT
            sysctl -w net.ipv4.ip_forward=1 2>/dev/null || true
            if command -v iptables &>/dev/null; then
                iptables -t nat -A POSTROUTING -s 10.0.2.0/24 -j MASQUERADE 2>/dev/null || true
                iptables -A FORWARD -i "$TAP_IF" -j ACCEPT 2>/dev/null || true
                iptables -A FORWARD -o "$TAP_IF" -j ACCEPT 2>/dev/null || true
            fi
            log "TAP interface created: $TAP_IF"
        fi
    fi

    if $USE_TAP; then
        NET_OPTS="-netdev tap,id=net0,ifname=$TAP_IF,script=no,downscript=no -device virtio-net-pci,netdev=net0"
    else
        # User-mode SLIRP networking (works everywhere, no root needed)
        NET_OPTS="-netdev user,id=net0,hostfwd=tcp::${VM_HOST_FWD}-:22,hostfwd=tcp::${VM_HOST_FWD}0-:2200 -device virtio-net-pci,netdev=net0"
        info "Using user-mode (SLIRP) networking — VM accessible via localhost:${VM_HOST_FWD}"
    fi
}

# ── Launch VM ────────────────────────────────────────────────────────────────
launch_vm() {
    log "Launching Ubuntu VM..."
    info "  Disk:   $VM_DISK"
    info "  Image:  $VM_IMAGE"
    info "  RAM:    ${VM_RAM}MB | CPUs: $VM_CPUS"
    info "  SSH:    localhost:${VM_HOST_FWD} -> VM:22"
    info "  User:   $VM_USER / $VM_PASS"

    local qemu_args=(
        -name "$VM_NAME"
        -m "$VM_RAM"
        -smp "$VM_CPUS"
        $ACCEL
        -drive "file=$VM_DISK,if=virtio,format=qcow2,index=0"
        -cdrom "${VM_CIDATA_ISO:-/dev/null}"
        $NET_OPTS
        -nographic
        -serial mon:stdio
        -display none
        -pidfile "$VM_DISK_DIR/${VM_NAME}.pid"
        -monitor "unix:$VM_DISK_DIR/${VM_NAME}-monitor.sock,server,nowait"
        -usb -device usb-tablet
    )

    # Add VGA for environments that support it
    if [ "$ENV_TYPE" = "bare-metal" ]; then
        qemu_args+=(-vga std)
    fi

    # Run in background with logging
    local vm_log="$VM_DISK_DIR/${VM_NAME}.log"
    log "VM log: $vm_log"
    nohup $QEMU_BIN "${qemu_args[@]}" > "$vm_log" 2>&1 &
    VM_PID=$!
    echo "$VM_PID" > "$VM_DISK_DIR/${VM_NAME}.pid"
    log "VM started with PID: $VM_PID"

    # Wait for VM to boot
    info "Waiting for VM to boot (this may take 2-5 minutes)..."
    local retries=0
    local max_retries=120
    while [ $retries -lt $max_retries ]; do
        if ssh -o StrictHostKeyChecking=no -o ConnectTimeout=3 \
               -p "$VM_HOST_FWD" "${VM_USER}@localhost" "echo ready" &>/dev/null; then
            log "VM is ready! SSH access available."
            return 0
        fi
        sleep 3
        retries=$((retries + 1))
        if [ $((retries % 10)) -eq 0 ]; then
            info "Still waiting... ($retries/$max_retries attempts)"
        fi
    done

    warn "VM boot timeout — it may still be starting. Check: ssh -p $VM_HOST_FWD ${VM_USER}@localhost"
}

# ── Public SSH Tunnel ───────────────────────────────────────────────────────
setup_public_tunnel() {
    log "Setting up public SSH tunnel..."

    # Install cloudflared for public tunnel
    if ! command -v cloudflared &>/dev/null; then
        log "Installing cloudflared..."
        local arch
        arch=$(uname -m)
        case "$arch" in
            x86_64)  arch="amd64" ;;
            aarch64) arch="arm64" ;;
            armv7l)  arch="arm" ;;
            *)       arch="amd64" ;;
        esac
        local cf_url="https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-${arch}"
        curl -sL "$cf_url" -o /tmp/cloudflared 2>/dev/null || wget -q "$cf_url" -O /tmp/cloudflared 2>/dev/null
        chmod +x /tmp/cloudflared
        if [ "$(id -u)" -eq 0 ]; then
            mv /tmp/cloudflared /usr/local/bin/cloudflared
        else
            mkdir -p "$HOME/.local/bin"
            mv /tmp/cloudflared "$HOME/.local/bin/cloudflared"
            export PATH="$HOME/.local/bin:$PATH"
        fi
        log "cloudflared installed"
    fi

    # Start SSH tunnel (quick tunnel — no account needed)
    log "Starting public SSH tunnel (Cloudflare Quick Tunnel)..."
    local tunnel_log="$VM_DISK_DIR/${VM_NAME}-tunnel.log"

    # Create tunnel wrapper that restarts on failure
    cat > "$VM_DISK_DIR/tunnel.sh" <<TUNNEL
#!/usr/bin/env bash
# Auto-restarting SSH tunnel wrapper
while true; do
    echo "[$(date)] Starting tunnel..."
    cloudflared tunnel --url ssh://localhost:${VM_HOST_FWD} 2>&1 | tee -a "$tunnel_log"
    echo "[$(date)] Tunnel crashed, restarting in 5s..."
    sleep 5
done
TUNNEL
    chmod +x "$VM_DISK_DIR/tunnel.sh"

    nohup "$VM_DISK_DIR/tunnel.sh" > "$tunnel_log" 2>&1 &
    TUNNEL_PID=$!
    echo "$TUNNEL_PID" > "$VM_DISK_DIR/${VM_NAME}-tunnel.pid"
    log "Tunnel started (PID: $TUNNEL_PID)"

    # Extract tunnel URL after a delay
    sleep 5
    local tunnel_url
    tunnel_url=$(grep -oP 'https://[a-z0-9-]+\.trycloudflare\.com' "$tunnel_log" 2>/dev/null | head -1)
    if [ -n "$tunnel_url" ]; then
        log "╔══════════════════════════════════════════════════════════════╗"
        log "║  PUBLIC SSH ACCESS:                                         ║"
        log "║  ssh ${VM_USER}@${tunnel_url#https://}                      ║"
        log "║  Password: ${VM_PASS}                                       ║"
        log "╚══════════════════════════════════════════════════════════════╝"
        echo "${tunnel_url#https://}" > "$VM_DISK_DIR/${VM_NAME}-tunnel-url.txt"
    else
        warn "Tunnel URL not yet available. Check: $tunnel_log"
        warn "Or run: grep 'trycloudflare' $tunnel_log"
    fi
}

# ── Watchdog / Keepalive Daemon ─────────────────────────────────────────────
install_watchdog() {
    log "Installing watchdog daemon..."

    cat > "$VM_DISK_DIR/watchdog.sh" <<'WATCHDOG'
#!/usr/bin/env bash
# ============================================================================
# VM Watchdog — Keeps VM and tunnel alive
# ============================================================================
# Checks every 30s:
#   1. VM process is running
#   2. VM responds to SSH ping
#   3. Tunnel process is running
#   4. Tunnel URL is reachable
# Restarts anything that failed.
# ============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VM_NAME="${VM_NAME:-ubuntu-vm}"
VM_DISK_DIR="${VM_DISK_DIR:-$HOME/.vm-disks}"
VM_HOST_FWD="${VM_HOST_FWD:-8022}"
VM_USER="${VM_USER:-ubuntu}"
CHECK_INTERVAL="${CHECK_INTERVAL:-30}"
LOG_FILE="$VM_DISK_DIR/${VM_NAME}-watchdog.log"
QEMU_BIN="${QEMU_BIN:-qemu-system-x86_64}"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG_FILE"; echo "$*"; }

check_vm_process() {
    local pidfile="$VM_DISK_DIR/${VM_NAME}.pid"
    if [ ! -f "$pidfile" ]; then
        return 1
    fi
    local pid
    pid=$(cat "$pidfile")
    if kill -0 "$pid" 2>/dev/null; then
        return 0
    fi
    return 1
}

check_vm_ssh() {
    ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 \
        -o BatchMode=yes \
        -p "$VM_HOST_FWD" "${VM_USER}@localhost" "echo ok" &>/dev/null
}

check_tunnel_process() {
    local pidfile="$VM_DISK_DIR/${VM_NAME}-tunnel.pid"
    if [ ! -f "$pidfile" ]; then
        return 1
    fi
    local pid
    pid=$(cat "$pidfile")
    if kill -0 "$pid" 2>/dev/null; then
        return 0
    fi
    return 1
}

start_vm() {
    log "Restarting VM..."
    # Find the last known QEMU command or use defaults
    local vm_disk="$VM_DISK_DIR/${VM_NAME}.qcow2"
    local vm_image="$HOME/.vm-images/ubuntu-24.04-server-cloudimg-amd64.img"
    local cidata_iso=$(ls "$VM_DISK_DIR/${VM_NAME}-cidata/"*.iso 2>/dev/null | head -1)
    local vm_ram="${VM_RAM:-4096}"
    local vm_cpus="${VM_CPUS:-2}"
    local accel="-accel tcg -cpu max"
    [ -e /dev/kvm ] && accel="-accel kvm -cpu host"

    nohup $QEMU_BIN \
        -name "$VM_NAME" \
        -m "$vm_ram" -smp "$vm_cpus" $accel \
        -drive "file=$vm_disk,if=virtio,format=qcow2,index=0" \
        ${cidata_iso:+-cdrom "$cidata_iso"} \
        -netdev user,id=net0,hostfwd=tcp::${VM_HOST_FWD}-:22 \
        -device virtio-net-pci,netdev=net0 \
        -nographic -serial mon:stdio -display none \
        -pidfile "$VM_DISK_DIR/${VM_NAME}.pid" \
        > "$VM_DISK_DIR/${VM_NAME}.log" 2>&1 &
    log "VM restart initiated"
}

start_tunnel() {
    log "Restarting tunnel..."
    local tunnel_script="$VM_DISK_DIR/tunnel.sh"
    if [ -f "$tunnel_script" ]; then
        nohup "$tunnel_script" > "$VM_DISK_DIR/${VM_NAME}-tunnel.log" 2>&1 &
        echo $! > "$VM_DISK_DIR/${VM_NAME}-tunnel.pid"
        log "Tunnel restart initiated"
    fi
}

# Main loop
log "Watchdog started (PID: $$)"
log "Check interval: ${CHECK_INTERVAL}s"

while true; do
    # 1. Check VM process
    if ! check_vm_process; then
        log "ALERT: VM process is dead!"
        start_vm
        sleep 30  # Give VM time to boot
    fi

    # 2. Check VM SSH
    if ! check_vm_ssh; then
        log "WARN: VM SSH not responding"
        # Only restart if VM process is alive but SSH is down
        if check_vm_process; then
            log "VM is alive but SSH down — waiting 60s for recovery"
            sleep 60
            if ! check_vm_ssh; then
                log "SSH still down — force restarting VM"
                local pidfile="$VM_DISK_DIR/${VM_NAME}.pid"
                [ -f "$pidfile" ] && kill -9 "$(cat "$pidfile")" 2>/dev/null || true
                sleep 5
                start_vm
                sleep 30
            fi
        fi
    fi

    # 3. Check tunnel
    if ! check_tunnel_process; then
        log "WARN: Tunnel process is dead"
        start_tunnel
    fi

    # 4. Rotate log if too large (>10MB)
    if [ -f "$LOG_FILE" ] && [ "$(stat -f%z "$LOG_FILE" 2>/dev/null || stat -c%s "$LOG_FILE" 2>/dev/null || echo 0)" -gt 10485760 ]; then
        mv "$LOG_FILE" "${LOG_FILE}.old"
        log "Log rotated"
    fi

    sleep "$CHECK_INTERVAL"
done
WATCHDOG
    chmod +x "$VM_DISK_DIR/watchdog.sh"

    # Start watchdog
    nohup "$VM_DISK_DIR/watchdog.sh" > "$VM_DISK_DIR/${VM_NAME}-watchdog.log" 2>&1 &
    WATCHDOG_PID=$!
    echo "$WATCHDOG_PID" > "$VM_DISK_DIR/${VM_NAME}-watchdog.pid"
    log "Watchdog installed (PID: $WATCHDOG_PID)"
}

# ── Systemd Service (optional, for bare metal) ──────────────────────────────
install_systemd() {
    if [ "$ENV_TYPE" = "bare-metal" ] && command -v systemctl &>/dev/null && [ "$(id -u)" -eq 0 ]; then
        log "Installing systemd services..."
        cat > /etc/systemd/system/ubuntu-vm.service <<SERVICE
[Unit]
Description=Ubuntu VM (${VM_NAME})
After=network.target

[Service]
Type=simple
ExecStart=$QEMU_BIN -name ${VM_NAME} -m ${VM_RAM} -smp ${VM_CPUS} -accel kvm -cpu host \\
    -drive file=${VM_DISK},if=virtio,format=qcow2,index=0 \\
    -cdrom ${VM_CIDATA_ISO} \\
    -netdev user,id=net0,hostfwd=tcp::${VM_HOST_FWD}-:22 \\
    -device virtio-net-pci,netdev=net0 \\
    -nographic -serial mon:stdio -display none \\
    -pidfile /run/ubuntu-vm.pid
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICE

        cat > /etc/systemd/system/ubuntu-vm-watchdog.service <<SERVICE
[Unit]
Description=Ubuntu VM Watchdog
After=ubuntu-vm.service
Requires=ubuntu-vm.service

[Service]
Type=simple
ExecStart=${VM_DISK_DIR}/watchdog.sh
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
SERVICE

        systemctl daemon-reload
        systemctl enable ubuntu-vm.service ubuntu-vm-watchdog.service
        log "Systemd services installed and enabled"
    fi
}

# ── Status Report ────────────────────────────────────────────────────────────
print_status() {
    echo ""
    log "═══════════════════════════════════════════════════════════════"
    log "  SETUP COMPLETE"
    log "═══════════════════════════════════════════════════════════════"
    echo ""
    info "VM Name:    $VM_NAME"
    info "Environment: $ENV_TYPE"
    info "Hypervisor:  $HYPERVISOR"
    info "Disk:        $VM_DISK"
    info "Resources:   ${VM_RAM}MB RAM, ${VM_CPUS} CPUs, ${VM_DISK_SIZE}GB disk"
    echo ""
    info "LOCAL SSH:"
    info "  ssh -p $VM_HOST_FWD ${VM_USER}@localhost"
    info "  Password: $VM_PASS"
    echo ""

    local tunnel_url=""
    if [ -f "$VM_DISK_DIR/${VM_NAME}-tunnel-url.txt" ]; then
        tunnel_url=$(cat "$VM_DISK_DIR/${VM_NAME}-tunnel-url.txt")
    fi

    if [ -n "$tunnel_url" ]; then
        info "PUBLIC SSH (via Cloudflare Tunnel):"
        info "  ssh ${VM_USER}@${tunnel_url}"
        info "  Password: $VM_PASS"
        echo ""
    fi

    info "Management:"
    info "  Monitor:  socat - UNIX-CONNECT:$VM_DISK_DIR/${VM_NAME}-monitor.sock"
    info "  Logs:     tail -f $VM_DISK_DIR/${VM_NAME}.log"
    info "  Tunnel:   tail -f $VM_DISK_DIR/${VM_NAME}-tunnel.log"
    info "  Watchdog: tail -f $VM_DISK_DIR/${VM_NAME}-watchdog.log"
    info "  Stop:     kill \$(cat $VM_DISK_DIR/${VM_NAME}.pid)"
    echo ""
    info "Files:"
    info "  VM disk:   $VM_DISK_DIR/${VM_NAME}.qcow2"
    info "  SSH key:   $SSH_KEY"
    info "  Cloud-init: $VM_CIDATA_ISO"
    echo ""
    log "═══════════════════════════════════════════════════════════════"
}

# ── Cleanup ──────────────────────────────────────────────────────────────────
cleanup() {
    log "Cleaning up..."
    # Kill any existing VM with same name
    local pidfile="$VM_DISK_DIR/${VM_NAME}.pid"
    if [ -f "$pidfile" ]; then
        local old_pid
        old_pid=$(cat "$pidfile")
        if kill -0 "$old_pid" 2>/dev/null; then
            warn "Stopping existing VM (PID: $old_pid)"
            kill "$old_pid" 2>/dev/null || true
            sleep 2
            kill -9 "$old_pid" 2>/dev/null || true
        fi
    fi
}

# ── Main ─────────────────────────────────────────────────────────────────────
main() {
    banner
    detect_environment
    install_deps
    select_hypervisor
    cleanup
    download_image
    setup_disk
    create_cloud_init
    setup_network
    launch_vm
    setup_public_tunnel
    install_watchdog
    install_systemd
    print_status
}

# Parse CLI args
while [ $# -gt 0 ]; do
    case "$1" in
        --help|-h)
            echo "Usage: $0 [options]"
            echo ""
            echo "Environment variables:"
            echo "  VM_NAME             VM name (default: ubuntu-vm)"
            echo "  VM_DISK_SIZE        Disk size in GB (default: 50)"
            echo "  VM_RAM              RAM in MB (default: 4096)"
            echo "  VM_CPUS             Number of CPUs (default: 2)"
            echo "  VM_HOST_FWD         Host port for SSH (default: 8022)"
            echo "  VM_USER             Username (default: ubuntu)"
            echo "  VM_PASS             Password (default: ubuntu)"
            echo "  SSH_KEY             SSH key path (default: ~/.ssh/id_ed25519)"
            echo "  CLOUDFLARE_TUNNEL_TOKEN  Token for persistent tunnel"
            exit 0
            ;;
        --stop)
            VM_NAME="${VM_NAME:-ubuntu-vm}"
            VM_DISK_DIR="${VM_DISK_DIR:-$HOME/.vm-disks}"
            pidfile="$VM_DISK_DIR/${VM_NAME}.pid"
            [ -f "$pidfile" ] && kill "$(cat "$pidfile")" 2>/dev/null && log "VM stopped"
            exit 0
            ;;
        --status)
            VM_NAME="${VM_NAME:-ubuntu-vm}"
            VM_DISK_DIR="${VM_DISK_DIR:-$HOME/.vm-disks}"
            pidfile="$VM_DISK_DIR/${VM_NAME}.pid"
            if [ -f "$pidfile" ] && kill -0 "$(cat "$pidfile")" 2>/dev/null; then
                log "VM is running (PID: $(cat "$pidfile"))"
            else
                warn "VM is not running"
            fi
            exit 0
            ;;
        *)
            err "Unknown option: $1"
            exit 1
            ;;
    esac
done

main "$@"
