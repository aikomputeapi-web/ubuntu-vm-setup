#!/usr/bin/env python3
"""
free-models-watch.py | Watch free AI models across 5 coding-agent gateways.

Providers monitored:
  1. OpenRouter   GET https://openrouter.ai/api/v1/models    (public, no auth)
  2. OpenCode Zen GET https://opencode.ai/zen/v1/models      (public, no auth)
  3. Kilo         GET https://api.kilo.ai/api/gateway/models  (public, no auth)
  4. Cline        GET https://api.cline.bot/api/v1/models     (requires CLINE_API_KEY env var)
  5. Ollama Cloud GET https://ollama.com/api/tags             (requires OLLAMA_CLOUD_API_KEY env var)

Usage:
  python free-models-watch.py              # one-shot snapshot
  python free-models-watch.py --watch      # refresh every 5 min, show deltas
  python free-models-watch.py --watch --interval 60
  python free-models-watch.py --json        # machine-readable JSON output
  python free-models-watch.py --provider openrouter kilo

Requires: requests (pip install requests)
For Cline: set CLINE_API_KEY environment variable
For Ollama: set OLLAMA_CLOUD_API_KEY environment variable
For OpenRouter: optionally set OPENROUTER_API_KEY (increases rate limits)
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone

try:
    import requests
except ImportError:
    sys.stderr.write(
        "Error: 'requests' not installed. Run: pip install requests\n"
    )
    sys.exit(1)

# ---------------------------------------------------------------------------
# ANSI colors
# ---------------------------------------------------------------------------
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
RED = "\033[31m"
BLUE = "\033[34m"

# Windows: enable ANSI escape codes + UTF-8 stdout
if sys.platform == "win32":
    os.system("")  # enables VT100 processing on Windows 10+
    # Force UTF-8 on stdout to avoid UnicodeEncodeError on em-dashes, etc.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# ---------------------------------------------------------------------------
# Provider fetchers
# ---------------------------------------------------------------------------

HTTP_TIMEOUT = 20  # seconds
USER_AGENT = "free-models-watch/1.0"


def _safe_get(url, headers=None):
    """GET with error handling. Returns (json_data, error_str)."""
    hdrs = {"User-Agent": USER_AGENT}
    if headers:
        hdrs.update(headers)
    try:
        resp = requests.get(url, headers=hdrs, timeout=HTTP_TIMEOUT)
        resp.raise_for_status()
        return resp.json(), None
    except requests.exceptions.HTTPError as e:
        return None, f"HTTP {resp.status_code}: {e}"
    except requests.exceptions.ConnectionError:
        return None, "connection error"
    except requests.exceptions.Timeout:
        return None, "timeout"
    except Exception as e:
        return None, str(e)


def fetch_openrouter():
    """
    OpenRouter: public endpoint, no auth needed.
    Free = pricing.prompt == "0" AND pricing.completion == "0".
    Model IDs ending in ':free' are the canonical free variants.
    """
    data, err = _safe_get("https://openrouter.ai/api/v1/models")
    if err:
        return [], f"OpenRouter: {err}"

    free_models = []
    seen = set()
    for m in data.get("data", []):
        pricing = m.get("pricing", {})
        prompt_price = str(pricing.get("prompt", "0") or "0")
        completion_price = str(pricing.get("completion", "0") or "0")

        is_free = (
            float(prompt_price) == 0.0 and float(completion_price) == 0.0
        )
        if not is_free:
            continue

        model_id = m.get("id", "")
        if model_id in seen or model_id.startswith("~"):
            continue
        seen.add(model_id)

        free_models.append({
            "id": model_id,
            "name": m.get("name", model_id),
            "context_length": m.get("context_length"),
        })

    free_models.sort(key=lambda x: x["name"].lower())
    return free_models, None


def fetch_opencode_zen():
    """
    OpenCode Zen: public endpoint, no auth needed.
    The API list doesn't include pricing, so we identify free models by the
    known naming convention (model IDs containing 'free') plus hardcoded
    additional free models from the docs (e.g. 'big-pickle').
    """
    data, err = _safe_get("https://opencode.ai/zen/v1/models")
    if err:
        return [], f"OpenCode Zen: {err}"

    # Models documented as free on https://opencode.ai/docs/zen/
    known_free_names = {
        "big-pickle",
        "mimo-v2.5-free",
        "hy3-free",
        "nemotron-3-ultra-free",
        "nemotron-3.5-lightning-free",
        "muse-spark-1.2-contributor-free",
        "deepseek-v4-flash-free",
        "laguna-s-2.1-free",
    }

    free_models = []
    for m in data.get("data", []):
        model_id = m.get("id", "")
        if "free" in model_id.lower() or model_id in known_free_names:
            free_models.append({
                "id": model_id,
                "name": model_id,  # Zen API doesn't return display names
            })

    free_models.sort(key=lambda x: x["id"])
    return free_models, None


def fetch_kilo():
    """
    Kilo Gateway: public endpoint, no auth needed.
    Uses isFree flag on each model.
    """
    data, err = _safe_get("https://api.kilo.ai/api/gateway/models")
    if err:
        return [], f"Kilo: {err}"

    free_models = []
    for m in data.get("data", []):
        if m.get("isFree"):
            free_models.append({
                "id": m.get("id", ""),
                "name": m.get("name", m.get("id", "")),
                "context_length": m.get("context_length"),
            })

    free_models.sort(key=lambda x: x["name"].lower())
    return free_models, None


def fetch_cline():
    """
    Cline API: requires authentication (CLINE_API_KEY env var).
    Falls back to documented free models if no key or endpoint fails.
    """
    api_key = os.environ.get("CLINE_API_KEY", "")
    if not api_key:
        # Fallback: document what we know from the docs/cline.bot/models
        return (
            [{
                "id": "minimax/minimax-m2.5",
                "name": "MiniMax: MiniMax M2.5 (documented free tier)",
                "context_length": None,
            }],
            "Cline: no CLINE_API_KEY set, showing documented free model only",
        )

    headers = {"Authorization": f"Bearer {api_key}"}
    data, err = _safe_get(
        "https://api.cline.bot/api/v1/models", headers=headers
    )
    if err:
        # Fallback on error
        return (
            [{
                "id": "minimax/minimax-m2.5",
                "name": "MiniMax: MiniMax M2.5 (documented free tier)",
                "context_length": None,
            }],
            f"Cline: {err}, showing documented free model only",
        )

    free_models = []
    if isinstance(data, dict) and "data" in data:
        model_list = data["data"]
    elif isinstance(data, list):
        model_list = data
    else:
        model_list = []

    for m in model_list:
        pricing = m.get("pricing", {})
        prompt_price = str(pricing.get("prompt", "0") or "0")
        completion_price = str(pricing.get("completion", "0") or "0")
        is_free = (
            float(prompt_price) == 0.0
            and float(completion_price) == 0.0
        )
        # Also check explicit free flag if present
        if m.get("isFree"):
            is_free = True
        if not is_free:
            continue
        free_models.append({
            "id": m.get("id", ""),
            "name": m.get("name", m.get("id", "")),
            "context_length": m.get("context_length"),
        })

    if not free_models:
        return (
            [{
                "id": "minimax/minimax-m2.5",
                "name": "MiniMax: MiniMax M2.5 (documented free tier)",
                "context_length": None,
            }],
            "Cline: no free models in API response, showing documented one",
        )

    free_models.sort(key=lambda x: x["name"].lower())
    return free_models, None


def fetch_ollama():
    """
    Ollama Cloud: uses https://ollama.com/api/tags with Bearer auth.
    All cloud models are accessible on the Free plan (light usage),
    so all returned models are listed.
    Requires OLLAMA_CLOUD_API_KEY env var.
    """
    api_key = os.environ.get("OLLAMA_CLOUD_API_KEY", "")
    if not api_key:
        return (
            [],
            "Ollama: no OLLAMA_CLOUD_API_KEY set",
        )

    headers = {"Authorization": f"Bearer {api_key}"}
    data, err = _safe_get("https://ollama.com/api/tags", headers=headers)
    if err:
        return [], f"Ollama: {err}"

    # All cloud models are free-tier accessible
    free_models = []
    for m in data.get("models", []):
        model_name = m.get("name", m.get("model", ""))
        free_models.append({
            "id": model_name,
            "name": model_name,
            "context_length": None,
        })

    free_models.sort(key=lambda x: x["name"].lower())
    return free_models, None


# ---------------------------------------------------------------------------
# Provider registry
# ---------------------------------------------------------------------------

PROVIDERS = {
    "openrouter":   {"label": "OpenRouter",   "fetch": fetch_openrouter,   "color": BLUE},
    "opencode":     {"label": "OpenCode Zen", "fetch": fetch_opencode_zen, "color": MAGENTA},
    "kilo":         {"label": "Kilo",         "fetch": fetch_kilo,         "color": CYAN},
    "cline":        {"label": "Cline",        "fetch": fetch_cline,        "color": GREEN},
    "ollama":       {"label": "Ollama Cloud", "fetch": fetch_ollama,       "color": YELLOW},
}


def fetch_all(provider_keys=None):
    """Fetch free models from all (or subset of) providers.
    Returns dict: provider_key -> {models, error, label, color}."""
    results = {}
    keys = provider_keys or list(PROVIDERS.keys())
    for key in keys:
        prov = PROVIDERS[key]
        models, err = prov["fetch"]()
        results[key] = {
            "models": models,
            "error": err,
            "label": prov["label"],
            "color": prov["color"],
        }
    return results


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def print_snapshot(results, as_json=False):
    if as_json:
        output = {}
        for key, r in results.items():
            output[key] = {
                "label": r["label"],
                "count": len(r["models"]),
                "error": r["error"],
                "models": [{"id": m["id"], "name": m.get("name", m["id"])}
                           for m in r["models"]],
            }
        print(json.dumps(output, indent=2))
        return

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    total = sum(
        len(r["models"]) for r in results.values() if not r["error"]
    )
    print(f"\n{BOLD}{'='*70}{RESET}")
    print(f"{BOLD}  Free AI Models Watch  {DIM}| {now}{RESET}")
    print(f"{BOLD}{'='*70}{RESET}")
    print(f"{DIM}  Total free models across all providers: {total}{RESET}")
    print(f"{BOLD}{'='*70}{RESET}")

    for key in PROVIDERS:
        if key not in results:
            continue
        r = results[key]
        color = r["color"]
        label = r["label"]

        if r["error"]:
            print(f"\n  {color}{BOLD}● {label}{RESET} {DIM}({len(r['models'])} models){RESET}")
            print(f"    {RED}⚠ {r['error']}{RESET}")
        else:
            count = len(r["models"])
            print(f"\n  {color}{BOLD}● {label}{RESET} {DIM}({count} free models){RESET}")

        if r["models"]:
            for m in r["models"]:
                name = m.get("name", m["id"])
                mid = m["id"]
                ctx = m.get("context_length")
                ctx_str = ""
                if ctx:
                    if ctx >= 1_000_000:
                        ctx_str = f" {DIM}[{ctx/1_000_000:.0f}M ctx]{RESET}"
                    elif ctx >= 1000:
                        ctx_str = f" {DIM}[{ctx//1000}K ctx]{RESET}"
                print(f"    {color}  {name}{RESET}{ctx_str}")
                if mid != name:
                    print(f"    {DIM}      {mid}{RESET}")

    print(f"\n{BOLD}{'='*70}{RESET}")


def compute_deltas(old_results, new_results):
    """Compare two snapshots. Returns list of (provider, added/removed, model_id)."""
    deltas = []
    for key in PROVIDERS:
        old = old_results.get(key, {}).get("models", [])
        new = new_results.get(key, {}).get("models", [])
        if old_results.get(key, {}).get("error") or new_results.get(key, {}).get("error"):
            # Skip delta if either side had an error
            continue
        old_ids = {m["id"] for m in old}
        new_ids = {m["id"] for m in new}
        added = new_ids - old_ids
        removed = old_ids - new_ids
        label = PROVIDERS[key]["label"]
        color = PROVIDERS[key]["color"]
        for mid in sorted(added):
            # Find name
            name = next((m.get("name", mid) for m in new if m["id"] == mid), mid)
            deltas.append((label, color, "added", mid, name))
        for mid in sorted(removed):
            name = next((m.get("name", mid) for m in old if m["id"] == mid), mid)
            deltas.append((label, color, "removed", mid, name))
    return deltas


def print_deltas(deltas, prev_total, new_total):
    if not deltas:
        return
    now = datetime.now(timezone.utc).strftime("%H:%M:%S UTC")
    print(f"\n{YELLOW}{BOLD}CHANGES DETECTED {DIM}| {now}{RESET}")
    for label, color, action, mid, name in deltas:
        if action == "added":
            arrow = f"{GREEN}+ added{RESET}"
        else:
            arrow = f"{RED}- removed{RESET}"
        print(f"  {arrow}  {color}{label}: {name}{RESET}")
        if mid != name:
            print(f"           {DIM}{mid}{RESET}")
    print(f"  {DIM}Total: {prev_total} → {new_total}{RESET}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Watch free AI models across coding-agent gateways.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Providers:
  openrouter   OpenRouter (https://openrouter.ai)
  opencode     OpenCode Zen (https://opencode.ai/zen)
  kilo         Kilo Gateway (https://api.kilo.ai)
  cline        Cline API (https://cline.bot) | needs CLINE_API_KEY
  ollama       Ollama Cloud (https://ollama.com) | needs OLLAMA_CLOUD_API_KEY

Examples:
  %(prog)s                          # one-shot snapshot
  %(prog)s --watch                  # refresh every 5 minutes, show deltas
  %(prog)s --watch -i 120           # refresh every 2 minutes
  %(prog)s --json                   # JSON output for piping
  %(prog)s -p openrouter kilo       # only OpenRouter + Kilo
  %(prog)s --watch -p kilo cline    # watch only Kilo + Cline

Environment:
  CLINE_API_KEY         Optional. Cline API key for live model fetching.
  OLLAMA_CLOUD_API_KEY  Optional. Ollama Cloud API key.
  OPENROUTER_API_KEY    Optional. OpenRouter key for higher rate limits.
        """,
    )
    parser.add_argument(
        "-w", "--watch",
        action="store_true",
        help="Watch mode: continuously refresh and show deltas.",
    )
    parser.add_argument(
        "-i", "--interval",
        type=int, default=300,
        help="Refresh interval in seconds (default: 300 = 5 min).",
    )
    parser.add_argument(
        "-j", "--json",
        action="store_true",
        help="Output as JSON (one-shot mode only).",
    )
    parser.add_argument(
        "-p", "--provider",
        nargs="+",
        choices=list(PROVIDERS.keys()),
        help="Only watch specific providers.",
    )
    args = parser.parse_args()

    provider_keys = args.provider or list(PROVIDERS.keys())

    # --- One-shot mode ---
    if not args.watch:
        results = fetch_all(provider_keys)
        print_snapshot(results, as_json=args.json)
        return

    # --- Watch mode ---
    prev_results = None
    prev_total = 0
    cycle = 0

    print(f"{DIM}Watching free models every {args.interval}s. Press Ctrl+C to stop.{RESET}")

    while True:
        cycle += 1
        now = datetime.now(timezone.utc).strftime("%H:%M:%S UTC")
        print(f"\n{DIM}[{now}] Refresh #{cycle}...{RESET}", end="", flush=True)

        results = fetch_all(provider_keys)
        new_total = sum(
            len(r["models"]) for r in results.values() if not r["error"]
        )

        if prev_results is not None:
            deltas = compute_deltas(prev_results, results)
            if deltas:
                print()  # newline after the "Refresh #N..." line
                print_deltas(deltas, prev_total, new_total)
            else:
                print(f" {GREEN}no changes{RESET} {DIM}(total: {new_total}){RESET}")
        else:
            print()  # newline
            print_snapshot(results)

        prev_results = results
        prev_total = new_total

        try:
            time.sleep(args.interval)
        except KeyboardInterrupt:
            print(f"\n{DIM}Stopped.{RESET}")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{DIM}Interrupted.{RESET}")
        sys.exit(0)
