#!/usr/bin/env bash
# Install ai-sdlc SKILL.md into ~/.hermes/skills/ai-sdlc/.
# Local script: run after `git clone`. No network, no curl-pipe-bash.
#
# v0.1 ships without SHA pinning. The maintainer can re-enable it by:
#   1. Setting EXPECTED_SHA256 below to the SHA of the published SKILL.md.
#   2. Re-enabling the mismatch branch (see the comment in the script).
set -euo pipefail

# EXPECTED_SHA256=""  # leave empty for v0.1; populate for v0.2+
EXPECTED_SHA256=""

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

# SHA verification is OFF in v0.1 (EXPECTED_SHA256 is empty).
# To re-enable: populate EXPECTED_SHA256 above, then change the guard to:
#   if [ "$ACTUAL_SHA256" != "$EXPECTED_SHA256" ]; then ... exit 1; fi
if [ -n "$EXPECTED_SHA256" ] && [ "$ACTUAL_SHA256" != "$EXPECTED_SHA256" ]; then
  echo "skipped (sha mismatch): expected $EXPECTED_SHA256, got $ACTUAL_SHA256" >&2
  exit 1
fi

mkdir -p "$DEST_DIR"
cp "$SRC" "$DEST"
echo "installed: $DEST (sha $ACTUAL_SHA256)"
