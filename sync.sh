#!/usr/bin/env bash
# Pull the latest cheat sheet from m5's Desktop.
set -e
scp -o ConnectTimeout=5 -o BatchMode=yes m5:~/Desktop/m2-cheat-sheet.md /home/shemika2/cheat-sheet/cheat-sheet.md
echo "synced $(date -u +%Y-%m-%dT%H:%M:%SZ)"
ls -l /home/shemika2/cheat-sheet/cheat-sheet.md
