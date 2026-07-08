#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
PLUGIN_ROOT="$ROOT/codex/agent-ticket-skills"

cd "$ROOT"

python3 -m unittest discover -s tests
python3 "$ROOT/skills/plane-ticket-reader/scripts/plane" --help >/dev/null
python3 "$ROOT/skills/plane-ticket-reader/scripts/plane" issues --help >/dev/null
python3 "$ROOT/skills/plane-ticket-reader/scripts/plane" comments --help >/dev/null

PLUGIN_VALIDATOR="${CODEX_PLUGIN_VALIDATOR:-${CODEX_HOME:-$HOME/.codex}/skills/.system/plugin-creator/scripts/validate_plugin.py}"
if [[ -f "$PLUGIN_VALIDATOR" ]]; then
  python3 "$PLUGIN_VALIDATOR" "$PLUGIN_ROOT"
else
  echo "Skipping Codex plugin schema validation; validator not found at $PLUGIN_VALIDATOR" >&2
fi

python3 - "$ROOT" "$PLUGIN_ROOT" <<'PY'
import json
import os
import sys
from pathlib import Path

root = Path(sys.argv[1])
plugin_root = Path(sys.argv[2])

for skill_path in sorted((root / "skills").glob("*/SKILL.md")):
    text = skill_path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise SystemExit(f"{skill_path}: missing YAML frontmatter")
    frontmatter = text.split("---", 2)[1]
    if "\nname:" not in "\n" + frontmatter:
        raise SystemExit(f"{skill_path}: missing name")
    if "\ndescription:" not in "\n" + frontmatter:
        raise SystemExit(f"{skill_path}: missing description")

manifest = json.loads((plugin_root / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
if manifest["name"] != "agent-ticket-skills":
    raise SystemExit("plugin name must be agent-ticket-skills")
if manifest.get("skills") != "./skills/":
    raise SystemExit("plugin skills path must be ./skills/")

for name in ("ba", "lead", "plane-ticket-reader", "ticket-workflow"):
    adapter_entry = plugin_root / "skills" / name
    source_entry = root / "skills" / name
    if not adapter_entry.exists():
        raise SystemExit(f"missing Codex skill adapter entry: {adapter_entry}")
    if os.path.realpath(adapter_entry) != str(source_entry):
        raise SystemExit(f"adapter entry does not resolve to source skill: {adapter_entry}")

print("Validation OK")
PY
