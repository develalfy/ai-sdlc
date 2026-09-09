#!/usr/bin/env bash
# Install ai-sdlc SKILL.md into ~/.hermes/skills/ai-sdlc/.
# Local script: run after `git clone`. No network, no curl-pipe-bash.
#
# v0.1+ ships WITH SHA pinning enabled by default. The expected SHA256 of
# the canonical SKILL.md is published in PROTOCOL.md §9 ("Install integrity").
# The script computes the SHA of the LOCAL SKILL.md and refuses to install
# on mismatch — this fails closed if a third party has tampered with the
# clone before ./install.sh runs.
#
# To install an intentionally-different local SKILL.md (e.g. a fork),
# pass `--no-verify` to skip the SHA check. The script still prints the
# computed SHA so you can record the new baseline.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
SRC="$REPO_ROOT/SKILL.md"
DEST_DIR="$HOME/.hermes/skills/ai-sdlc"
DEST="$DEST_DIR/SKILL.md"
PROTOCOL="$REPO_ROOT/PROTOCOL.md"

if [ ! -f "$SRC" ]; then
  echo "error: $SRC not found" >&2
  exit 1
fi
if [ ! -f "$PROTOCOL" ]; then
  echo "error: $PROTOCOL not found (needed to read the published SHA baseline)" >&2
  exit 1
fi

VERIFY=1
for arg in "$@"; do
  case "$arg" in
    --no-verify) VERIFY=0 ;;
    -h|--help)
      echo "usage: $0 [--no-verify]" >&2
      echo "  --no-verify  install even if local SKILL.md SHA differs from PROTOCOL.md baseline" >&2
      exit 0
      ;;
    *) echo "error: unknown argument: $arg" >&2; exit 2 ;;
  esac
done

ACTUAL_SHA256="$(sha256sum "$SRC" | awk '{print $1}')"
echo "computed sha256: $ACTUAL_SHA256"

# Extract the canonical SHA from PROTOCOL.md §9. Format:
#   "SKILL.md expected SHA256: `<64-hex>`"
EXPECTED_SHA256="$(awk '
  /SKILL\.md expected SHA256:/ { print $NF }
' "$PROTOCOL" | tr -d '`')"

if [ -z "$EXPECTED_SHA256" ]; then
  echo "error: could not find SKILL.md SHA baseline in $PROTOCOL §9" >&2
  echo "       (maintainer must publish the SHA before shipping this release)" >&2
  exit 1
fi

if [ "$VERIFY" -eq 1 ] && [ "$ACTUAL_SHA256" != "$EXPECTED_SHA256" ]; then
  echo "error: SKILL.md sha mismatch" >&2
  echo "  expected (from PROTOCOL.md §9): $EXPECTED_SHA256" >&2
  echo "  actual   (from local SKILL.md): $ACTUAL_SHA256" >&2
  echo "" >&2
  echo "  refusing to install — pass --no-verify to install anyway" >&2
  exit 1
fi

mkdir -p "$DEST_DIR"
cp "$SRC" "$DEST"
echo "installed: $DEST (sha $ACTUAL_SHA256)"
