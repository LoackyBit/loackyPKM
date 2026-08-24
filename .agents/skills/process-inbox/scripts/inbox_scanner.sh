#!/bin/bash
# inbox_scanner.sh - Elenca i file markdown presenti in Inbox/ per la skill /process-inbox.

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VAULT_ROOT="$( cd "$SCRIPT_DIR/../../../.." && pwd )"

INBOX_DIR="$VAULT_ROOT/Inbox"

if [ ! -d "$INBOX_DIR" ]; then
    echo "Errore: La directory Inbox non esiste in $INBOX_DIR" >&2
    exit 1
fi

echo "--- Note in attesa di smistamento in Inbox ---"
find "$INBOX_DIR" -type f -name "*.md" ! -name ".*" | while read -r file; do
    # Stampa il percorso relativo rispetto alla root del vault
    python3 -c "import os; print(os.path.relpath('$file', '$VAULT_ROOT'))"
done
