#!/usr/bin/env bash
set -euo pipefail

ARCHIVE="${1:-familyos-engineering-epics.zip}"
TARGET="${2:-.}"

if [[ ! -f "$ARCHIVE" ]]; then
    echo "Archive introuvable : $ARCHIVE" >&2
    exit 1
fi

mkdir -p "$TARGET"
unzip -o "$ARCHIVE" -d "$TARGET"

echo
echo "EPIC installés dans : $TARGET/docs/epics"
find "$TARGET/docs/epics" -type f -name '*.md' | sort
