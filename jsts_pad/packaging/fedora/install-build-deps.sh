#!/usr/bin/env bash
set -euo pipefail

# JSTS Pad deliberately does not install host packages or elevate privileges.
# This helper only reports which host-side commands the non-privileged AppImage
# builder expects to find already installed.

required=(python3 gcc objcopy strip patchelf file curl)
optional=(desktop-file-validate appstreamcli)
missing=0

echo "JSTS Pad AppImage host prerequisite check"
for command_name in "${required[@]}"; do
    if command -v "$command_name" >/dev/null 2>&1; then
        printf '  [OK] %s\n' "$command_name"
    else
        printf '  [MISSING] %s\n' "$command_name"
        missing=1
    fi
done
for command_name in "${optional[@]}"; do
    if command -v "$command_name" >/dev/null 2>&1; then
        printf '  [OK] %s (optional validation)\n' "$command_name"
    else
        printf '  [INFO] %s unavailable (optional validation skipped)\n' "$command_name"
    fi
done

if (( missing )); then
    echo "Install the missing host tools with your normal system administration workflow, then rerun this check." >&2
    exit 1
fi
