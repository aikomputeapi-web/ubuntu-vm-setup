#!/usr/bin/env bash
# ============================================================================
# vm-reconnect.sh — Quick reconnect to Ubuntu VM
# ============================================================================
# Usage:
#   ./vm-reconnect.sh              # Reconnect via local SSH
#   ./vm-reconnect.sh --public     # Reconnect via public tunnel
#   ./vm-reconnect.sh --restart    # Restart everything
#   ./vm-reconnect.sh --status     # Check status
# ============================================================================

set -euo pipefail

VM_NAME="${VM_NAME:-ubuntu-vm}"
VM_DISK_DIR="${VM_DISK_DIR:-$HOME/.vm-disks}"
VM_HOST_FWD="${VM_HOST_FWD:-8022}"
VM_USER="${VM_USER:-ubuntu}"
VM_PASS="${VM_PASS:-ubuntu}"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; NC='\033[0m'

log()  { echo -e "${GREEN}[+]${NC} $*"; }
warn() { echo -e "${YELLOW}[!]${NC} $*"; }
err()  { echo -e "${RED}[x]${NC} $*" >&2; }
info() { echo -e "${BLUE}[i]${NC} $*"; }

VM_SCRIPT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/ubuntu-vm-setup.sh"

check_vm_running() {
    local pidfile="$VM_DISK_DIR/${VM_NAME}.pid"
    [ -f "$pidfile" ] && kill -0 "$(cat "$pidfile")" 2>/dev/null
}

check_tunnel_running() {
    local pidfile="$VM_DISK_DIR/${VM_NAME}-tunnel.pid"
    [ -f "$pidfile" ] && kill -0 "$(cat "$pidfile")" 2>/dev/null
}

get_tunnel_url() {
    local log="$VM_DISK_DIR/${VM_NAME}-tunnel.log"
    grep -oP 'https://[a-z0-9-]+\.trycloudflare\.com' "$log" 2>/dev/null | tail -1
}

do_status() {
    echo ""
    info "═══ VM Status ═══"
    if check_vm_running; then
        log "VM: RUNNING (PID: $(cat "$VM_DISK_DIR/${VM_NAME}.pid"))"
    else
        err "VM: STOPPED"
    fi

    if check_tunnel_running; then
        log "Tunnel: RUNNING"
        local url
        url=$(get_tunnel_url)
        [ -n "$url" ] && info "Public URL: $url"
    else
        err "Tunnel: STOPPED"
    fi

    if [ -f "$VM_DISK_DIR/${VM_NAME}-watchdog.pid" ]; then
        if kill -0 "$(cat "$VM_DISK_DIR/${VM_NAME}-watchdog.pid")" 2>/dev/null; then
            log "Watchdog: RUNNING"
        else
            warn "Watchdog: STOPPED"
        fi
    else
        warn "Watchdog: NOT INSTALLED"
    fi
    echo ""
}

do_local_ssh() {
    if ! check_vm_running; then
        warn "VM not running. Starting..."
        bash "$VM_SCRIPT" --stop 2>/dev/null || true
        exec bash "$VM_SCRIPT"
    fi
    info "Connecting via local SSH..."
    ssh -o StrictHostKeyChecking=no -p "$VM_HOST_FWD" "${VM_USER}@localhost"
}

do_public_ssh() {
    if ! check_tunnel_running; then
        warn "Tunnel not running. Starting..."
        bash "$VM_DISK_DIR/tunnel.sh" &
        sleep 8
    fi
    local url
    url=$(get_tunnel_url)
    [ -z "$url" ] && url=$(cat "$VM_DISK_DIR/${VM_NAME}-tunnel-url.txt" 2>/dev/null)
    if [ -z "$url" ]; then
        err "Could not find tunnel URL. Check: tail -f $VM_DISK_DIR/${VM_NAME}-tunnel.log"
        exit 1
    fi
    local host="${url#https://}"
    if ! command -v cloudflared &>/dev/null; then
        err "cloudflared not installed on THIS machine. Install it first:"
        err "  https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/"
        exit 1
    fi
    info "Connecting via public tunnel (cloudflared ProxyCommand)..."
    info "ssh ${VM_USER}@${host}"
    ssh -o StrictHostKeyChecking=no \
        -o ProxyCommand="cloudflared access ssh --hostname %h" \
        "${VM_USER}@${host}"
}

do_restart() {
    log "Stopping everything..."
    bash "$VM_SCRIPT" --stop 2>/dev/null || true
    [ -f "$VM_DISK_DIR/${VM_NAME}-tunnel.pid" ] && kill "$(cat "$VM_DISK_DIR/${VM_NAME}-tunnel.pid")" 2>/dev/null || true
    [ -f "$VM_DISK_DIR/${VM_NAME}-watchdog.pid" ] && kill "$(cat "$VM_DISK_DIR/${VM_NAME}-watchdog.pid")" 2>/dev/null || true
    sleep 2
    log "Restarting..."
    exec bash "$VM_SCRIPT"
}

# Main
case "${1:-}" in
    --public|-p)
        do_public_ssh
        ;;
    --restart|-r)
        do_restart
        ;;
    --status|-s)
        do_status
        ;;
    --help|-h)
        echo "Usage: $0 [--local|--public|--restart|--status]"
        echo ""
        echo "  (no args)   Connect via local SSH"
        echo "  --public    Connect via public Cloudflare tunnel"
        echo "  --restart   Stop and restart everything"
        echo "  --status    Show VM/tunnel/watchdog status"
        ;;
    *)
        do_local_ssh
        ;;
esac
