#!/bin/bash
# watch.sh - Second Brain Inbox & Review Dashboard Watcher Daemon
# Implements full CLI lifecycle (start, stop, status, restart, run), PID tracking with auto-healing,
# 5MB log rotation (preserving watch.log.1..3), debounced polling, and non-invasive Obsidian focus.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VAULT_PATH="$(cd "$SCRIPT_DIR/../.." && pwd)"
INBOX_PATH="$VAULT_PATH/03 - Inbox"
DASHBOARD_FILE="$INBOX_PATH/Review Dashboard.md"
LOG_DIR="$VAULT_PATH/99 - Meta/logs"
LOG_FILE="$LOG_DIR/watch.log"
PID_FILE="${PID_FILE:-/tmp/brain_watcher.pid}"
OPENED_FLAG="/tmp/obsidian_dashboard_opened"

mkdir -p "$LOG_DIR"
export PATH="/Users/lorenzo/.local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

rotate_logs() {
    if [ -f "$LOG_FILE" ]; then
        FILE_SIZE=$(stat -f%z "$LOG_FILE" 2>/dev/null || stat -c%s "$LOG_FILE" 2>/dev/null || echo 0)
        if [ "$FILE_SIZE" -gt 5242880 ]; then
            mv -f "${LOG_FILE}.2" "${LOG_FILE}.3" 2>/dev/null || true
            mv -f "${LOG_FILE}.1" "${LOG_FILE}.2" 2>/dev/null || true
            mv -f "$LOG_FILE" "${LOG_FILE}.1" 2>/dev/null || true
            touch "$LOG_FILE"
        fi
    fi
}

log_msg() {
    rotate_logs
    local MSG="$(date '+%Y-%m-%d %H:%M:%S') - $1"
    echo "$MSG" >> "$LOG_FILE"
    if [ "${FOREGROUND:-0}" -eq 1 ]; then
        echo "$MSG"
    fi
}

is_running() {
    if [ -f "$PID_FILE" ]; then
        local PID
        PID=$(cat "$PID_FILE" 2>/dev/null)
        if [ -n "$PID" ] && kill -0 "$PID" 2>/dev/null; then
            return 0
        else
            # Stale PID auto-healing
            rm -f "$PID_FILE"
            return 1
        fi
    fi
    return 1
}

cleanup() {
    rm -f "$PID_FILE" "$OPENED_FLAG"
    log_msg "Watcher daemon stopped."
}

run_loop() {
    if is_running; then
        echo "Error: Watcher is already running with PID $(cat "$PID_FILE")." >&2
        exit 1
    fi

    echo "$$" > "$PID_FILE"
    trap cleanup EXIT SIGTERM SIGINT

    log_msg "Starting Second Brain Watcher daemon on $VAULT_PATH (PID $$)"

    while true; do
        shopt -s nullglob
        has_work=false

        # Check for pending approvals/rejections in Review Dashboard with debouncing
        if [ -f "$DASHBOARD_FILE" ]; then
            # Debounce: ensure file is not actively being flushed
            size1=$(stat -f%z "$DASHBOARD_FILE" 2>/dev/null || stat -c%s "$DASHBOARD_FILE" 2>/dev/null || echo 0)
            sleep 1
            size2=$(stat -f%z "$DASHBOARD_FILE" 2>/dev/null || stat -c%s "$DASHBOARD_FILE" 2>/dev/null || echo 0)

            if [ "$size1" -eq "$size2" ]; then
                if grep -q "\- \[x\] Approva" "$DASHBOARD_FILE" || grep -q "\- \[\-\] Approva" "$DASHBOARD_FILE"; then
                    has_work=true
                fi
            fi
        fi

        if [ "$has_work" = true ]; then
            log_msg "Dashboard review activity detected. Invoking brain_ingest.py..."
            python3 "$VAULT_PATH/99 - Meta/Scripts/brain_ingest.py" --process-approvals >> "$LOG_FILE" 2>&1
        fi

        # Obsidian Launch Integration (Non-stealing single notification per session)
        if pgrep -x "Obsidian" >/dev/null 2>&1; then
            if [ -f "$DASHBOARD_FILE" ] && grep -q "\- \[ \]" "$DASHBOARD_FILE" && [ ! -f "$OPENED_FLAG" ]; then
                log_msg "Obsidian running with pending reviews. Opening Review Dashboard..."
                open "obsidian://open?vault=loackyPKM&file=03%20-%20Inbox%2FReview%20Dashboard" 2>/dev/null || true
                touch "$OPENED_FLAG"
            fi
        else
            if [ -f "$OPENED_FLAG" ]; then
                rm -f "$OPENED_FLAG"
            fi
        fi

        sleep 4
    done
}

start_daemon() {
    if is_running; then
        echo "Watcher is already running with PID $(cat "$PID_FILE")."
        exit 0
    fi

    echo "Starting Second Brain Watcher daemon..."
    nohup "$0" run >/dev/null 2>&1 &
    sleep 1

    if is_running; then
        echo "Watcher daemon started successfully with PID $(cat "$PID_FILE")."
    else
        echo "Failed to start watcher daemon. Check $LOG_FILE for details." >&2
        exit 1
    fi
}

stop_daemon() {
    if [ -f "$PID_FILE" ]; then
        local PID
        PID=$(cat "$PID_FILE" 2>/dev/null)
        if [ -n "$PID" ] && kill -0 "$PID" 2>/dev/null; then
            echo "Stopping Watcher daemon (PID $PID)..."
            kill "$PID" 2>/dev/null || true
            for _ in {1..10}; do
                if ! kill -0 "$PID" 2>/dev/null; then
                    break
                fi
                sleep 0.5
            done
            if kill -0 "$PID" 2>/dev/null; then
                kill -9 "$PID" 2>/dev/null || true
            fi
            rm -f "$PID_FILE" "$OPENED_FLAG"
            echo "Watcher daemon stopped."
            return 0
        else
            rm -f "$PID_FILE" "$OPENED_FLAG"
            echo "Cleaned up stale PID file. Watcher is not running."
            return 0
        fi
    fi
    echo "Watcher is not running."
}

status_daemon() {
    if is_running; then
        echo "Watcher is running with PID $(cat "$PID_FILE")."
        exit 0
    else
        echo "Watcher is not running."
        exit 0
    fi
}

restart_daemon() {
    stop_daemon
    sleep 1
    start_daemon
}

# CLI Argument routing
case "${1:-run}" in
    start)
        start_daemon
        ;;
    stop)
        stop_daemon
        ;;
    status)
        status_daemon
        ;;
    restart)
        restart_daemon
        ;;
    run)
        run_loop
        ;;
    *)
        echo "Usage: $0 {start|stop|status|restart|run}"
        exit 1
        ;;
esac
