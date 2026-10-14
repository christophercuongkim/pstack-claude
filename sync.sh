#!/usr/bin/env bash
# Pull upstream pstack, rebuild the Claude Code plugin, and validate it.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
upstream="${PSTACK_UPSTREAM:-$HOME/repos/pstack}"

git -C "$upstream" pull --ff-only --quiet
echo "upstream at $(git -C "$upstream" log -1 --format='%h %s')"
python3 -I "$here/port.py" "$upstream/pstack"
claude plugin validate "$here/plugin"
git -C "$here" status --short -- plugin | head -20
