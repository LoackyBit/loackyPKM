#!/bin/bash
# watch.sh - Second Brain Inbox Watcher daemon with dynamic path resolution
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VAULT_PATH="$(cd "$SCRIPT_DIR/../.." && pwd)"
INBOX_PATH="$VAULT_PATH/03 - Inbox"
DASHBOARD_FILE="$INBOX_PATH/Review Dashboard.md"
LOG_DIR="$VAULT_PATH/99 - Meta/logs"
LOG_FILE="$LOG_DIR/watch.log"

mkdir -p "$LOG_DIR"
export PATH="/Users/lorenzo/.local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

echo "$(date '+%Y-%m-%d %H:%M:%S') - Starting Second Brain Watcher daemon on $VAULT_PATH" >> "$LOG_FILE"

OPENED_FLAG="/tmp/obsidian_dashboard_opened"
rm -f "$OPENED_FLAG"

while true; do
    shopt -s nullglob
    has_work=false

    # Check for pending approvals/rejections in Review Dashboard
    if [ -f "$DASHBOARD_FILE" ]; then
        if grep -q "\- \[x\] Approva" "$DASHBOARD_FILE" || grep -q "\- \[\-\] Approva" "$DASHBOARD_FILE"; then
            has_work=true
        fi
    fi

    if [ "$has_work" = true ]; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') - Dashboard review activity detected. Invoking brain_ingest.py..." >> "$LOG_FILE"
        python3 "$VAULT_PATH/99 - Meta/Scripts/brain_ingest.py" --process-approvals >> "$LOG_FILE" 2>&1
    fi

    # Obsidian Launch Integration
    if pgrep -x "Obsidian" >/dev/null; then
        if [ -f "$DASHBOARD_FILE" ] && grep -q "\- \[ \]" "$DASHBOARD_FILE" && [ ! -f "$OPENED_FLAG" ]; then
            echo "$(date '+%Y-%m-%d %H:%M:%S') - Obsidian running with pending reviews. Opening dashboard..." >> "$LOG_FILE"
            open "obsidian://open?vault=loackyPKM&file=03%20-%20Inbox%2FReview%20Dashboard"
            touch "$OPENED_FLAG"
        fi
    else
        if [ -f "$OPENED_FLAG" ]; then
            rm -f "$OPENED_FLAG"
        fi
    fi

    sleep 5
done
