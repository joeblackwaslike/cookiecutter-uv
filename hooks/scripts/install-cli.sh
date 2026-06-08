#!/usr/bin/env bash
# Installs the create-py-project CLI into the session environment.
# Called by the Claude Code plugin SessionStart hook.

if command -v create-py-project &>/dev/null; then
  echo '{"continue": true, "suppressOutput": true, "status": "ready"}'
  exit 0
fi

cd "$CLAUDE_PLUGIN_ROOT" || {
  echo '{"continue": true, "suppressOutput": false, "status": "install failed — CLAUDE_PLUGIN_ROOT not set or not a directory"}'
  exit 1
}

# Suppress installer stdout (it would corrupt the JSON status line) but let
# stderr through so a non-obvious failure is visible before we fall through.
if command -v uv &>/dev/null && uv tool install --editable . >/dev/null; then
  echo '{"continue": true, "suppressOutput": true, "status": "installed via uv tool"}'
  exit 0
fi

if command -v pipx &>/dev/null && pipx install --editable . >/dev/null; then
  echo '{"continue": true, "suppressOutput": true, "status": "installed via pipx"}'
  exit 0
fi

if pip install -e . --quiet >/dev/null; then
  echo '{"continue": true, "suppressOutput": true, "status": "installed via pip"}'
  exit 0
fi

echo "{\"continue\": true, \"suppressOutput\": false, \"status\": \"install failed — run: uv tool install --editable $CLAUDE_PLUGIN_ROOT\"}"
