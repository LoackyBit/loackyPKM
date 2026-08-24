#!/bin/bash
# Second Brain Inbox Watcher loop with Obsidian integration
VAULT_PATH="/Users/lorenzo/Library/Mobile Documents/iCloud~md~obsidian/Documents/Ken vault"
INBOX_PATH="$VAULT_PATH/03 - Inbox"
DASHBOARD_FILE="$INBOX_PATH/Review Dashboard.md"
LOG_DIR="$VAULT_PATH/99 - Meta/logs"
LOG_FILE="$LOG_DIR/watch.log"

export PATH="/Users/lorenzo/.local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

echo "$(date '+%Y-%m-%d %H:%M:%S') - Starting Second Brain Inbox Watcher loop..." >> "$LOG_FILE"

# Flag file to track if we've already opened the dashboard in this Obsidian session
OPENED_FLAG="/tmp/obsidian_dashboard_opened"

# Clean up flag on startup
rm -f "$OPENED_FLAG"

while true; do
    shopt -s nullglob
    
    # Check for new raw files (any .md file in inbox that does not start with proposed- or raw-, is not the Dashboard, and has ready: true)
    raw_files=()
    for f in "$INBOX_PATH"/*.md; do
        basename_f=$(basename "$f")
        if [[ "$basename_f" != proposed-* && "$basename_f" != raw-* && "$basename_f" != seen-* && "$basename_f" != "Review Dashboard.md" ]]; then
            if grep -q -i "^ready:\s*true" "$f"; then
                raw_files+=("$f")
            fi
        fi
    done
    
    # Check for approvals (checked boxes [x] in Review Dashboard) or rejections ([-] in Review Dashboard)
    has_approvals=false
    has_rejections=false
    if [ -f "$DASHBOARD_FILE" ]; then
        if grep -q "\- \[x\] Approva" "$DASHBOARD_FILE"; then
            has_approvals=true
        fi
        if grep -q "\- \[\-\] Approva" "$DASHBOARD_FILE"; then
            has_rejections=true
        fi
    fi
    
    # Trigger ingest script if there is work to do
    if [ ${#raw_files[@]} -gt 0 ] || [ "$has_approvals" = true ] || [ "$has_rejections" = true ]; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') - Activity detected (Raw files: ${#raw_files[@]}, Approvals: $has_approvals, Rejections: $has_rejections). Invoking ingest manager..." >> "$LOG_FILE"
        python3 "$VAULT_PATH/99 - Meta/Scripts/ingest_manager.py"
    fi
    
    # Obsidian Launch Integration:
    # Check if Obsidian is running
    if pgrep -x "Obsidian" >/dev/null; then
        # If Obsidian is running, and we have pending reviews, and we haven't opened the dashboard yet:
        if [ -f "$DASHBOARD_FILE" ] && grep -q "\- \[ \]" "$DASHBOARD_FILE" && [ ! -f "$OPENED_FLAG" ]; then
            echo "$(date '+%Y-%m-%d %H:%M:%S') - Obsidian running with pending reviews. Opening dashboard..." >> "$LOG_FILE"
            # Open the dashboard in Obsidian using the Obsidian URL scheme
            open "obsidian://open?vault=Ken%20vault&file=03%20-%20Inbox%2FReview%20Dashboard"
            touch "$OPENED_FLAG"
        fi
    else
        # If Obsidian is not running, reset the opened flag so it triggers next time Obsidian starts
        if [ -f "$OPENED_FLAG" ]; then
            rm -f "$OPENED_FLAG"
        fi
    fi
    
    sleep 5
done
