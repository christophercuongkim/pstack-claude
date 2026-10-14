#!/usr/bin/env bash
# Move the upstream submodule to the latest cursor/plugins main, rebuild the plugin, and validate it.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"

git -C "$here" submodule update --init --remote --quiet upstream
echo "upstream at $(git -C "$here/upstream" log -1 --format='%h %s')"
python3 -I "$here/port.py"
claude plugin validate "$here/plugin"
git -C "$here" status --short -- upstream plugin | head -20
