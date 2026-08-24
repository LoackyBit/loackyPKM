#!/bin/bash
# discover.sh - Seleziona 3 note casuali da Atlas per la skill /dream.
# Portabile su macOS e Linux tramite fallback Python3.

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VAULT_ROOT="$( cd "$SCRIPT_DIR/../../../.." && pwd )"

python3 -c "
import os, random, sys
atlas_dir = os.path.join('$VAULT_ROOT', 'Atlas')
if not os.path.exists(atlas_dir):
    print(f'Errore: La directory {atlas_dir} non esiste.', file=sys.stderr)
    sys.exit(1)

md_files = []
for root, dirs, files in os.walk(atlas_dir):
    # Salta directory nascoste
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    for file in files:
        if file.endswith('.md') and not file.startswith('.'):
            md_files.append(os.path.join(root, file))

if not md_files:
    print('Nessun file markdown trovato in Atlas.', file=sys.stderr)
    sys.exit(0)

selected = random.sample(md_files, min(3, len(md_files)))
for f in selected:
    print(f)
"
