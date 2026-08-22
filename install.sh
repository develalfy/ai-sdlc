#!/usr/bin/env bash
# Install ai-sdlc SKILL.md into ~/.hermes/skills/ai-sdlc/.
# Local script: run after `git clone`. No network, no curl-pipe-bash.
set -euo pipefail

# REPLACE_AT_RELEASE with the SHA of the published SKILL.md bytes.
EXPECTED_SHA256="REPLACE_AT_RELEASE"

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
SRC="$REPO_ROOT/SKILL.md"
DEST_DIR="$HOME/.hermes/skills/ai-sdlc"
DEST="$DEST_DIR/SKILL.md"

if [ ! -f "$SRC" ]; then
  echo "error: $SRC not found" >&2
  exit 1
fi

ACTUAL_SHA256="$(sha256sum "$SRC" | awk '{print $1}')"
echo "computed sha256: $ACTUAL_SHA256"

if [ "$EXPECTED_SHA256" != "REPLACE_AT_RELEASE" ] && [ "$ACTUAL_SHA256" != "$EXPECTED_SHA256" ]; then
  echo "skipped (sha mismatch): expected $EXPECTED_SHA256, got $ACTUAL_SHA256" >&2
  exit 1
fi

mkdir -p "$DEST_DIR"
cp "$SRC" "$DEST"
echo "installed: $DEST (sha $ACTUAL_SHA256)"
