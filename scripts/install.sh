#!/bin/bash
set -euo pipefail
host="${1:-}"
case "$host" in
  codex) dest="$HOME/.agents/skills/universal-agent-orchestrator" ;;
  claude) dest="$HOME/.claude/skills/universal-agent-orchestrator" ;;
  *) echo "Usage: bash scripts/install.sh codex|claude" >&2; exit 2 ;;
esac
src="$(cd "$(dirname "$0")/.." && pwd -P)"
if [[ -e "$dest" ]]; then
  echo "Refusing to overwrite existing skill: $dest" >&2
  exit 1
fi
mkdir -p "$(dirname "$dest")"
cp -R "$src" "$dest"
echo "Installed Skill at: $dest"
echo "No providers configured; no production orchestrator installed."
