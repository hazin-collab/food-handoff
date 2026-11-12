#!/usr/bin/env bash
# Run from Git Bash on Windows or a Bash terminal on Linux/macOS.
set -euo pipefail
cd -- "$(dirname -- "$0")"

if command -v py >/dev/null 2>&1; then
    python_cmd=(py -3)
else
    python_cmd=(python3)
fi

batch_id=${1:-B-104}
deployment=$("${python_cmd[@]}" deploy_food_handoff.py)
printf '%s\n' "$deployment"
address=$(printf '%s\n' "$deployment" | sed -n 's/^Contract address: //p' | tr -d '\r')
if [[ ! $address =~ ^0x[[:xdigit:]]{40}$ ]]; then
    echo "Could not read the deployed contract address." >&2
    exit 1
fi

for action in register dispatch receive; do
    "${python_cmd[@]}" handoff.py "$action" "$address" "$batch_id"
done
