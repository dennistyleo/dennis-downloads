#!/bin/zsh
# PNL-COO MVP launcher (macOS)
# Double-click this file to start the demo server and open the browser.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# --------- config ---------
PORT="${PNL_COO_PORT:-8001}"
PYENV_PY="3.11.9"
VENV_DIR=".venv"
REQUIREMENTS_FILE="requirements.txt"
# --------------------------

echo "[PNL-COO] Launching from: $SCRIPT_DIR"

# Lock python via pyenv if available (non-fatal)
if command -v pyenv >/dev/null 2>&1; then
  pyenv local "$PYENV_PY" >/dev/null 2>&1 || true
fi

# Choose a python interpreter
PY_BIN=""
if command -v python3 >/dev/null 2>&1; then
  PY_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PY_BIN="python"
else
  echo "[ERROR] Python not found. Install Python 3.11+ (pyenv recommended)."
  exit 1
fi

# Create venv if needed
if [ ! -d "$VENV_DIR" ]; then
  echo "[PNL-COO] Creating venv ($VENV_DIR)…"
  "$PY_BIN" -m venv "$VENV_DIR"
fi

# Activate venv
source "$VENV_DIR/bin/activate"

# Install deps (skip if already satisfied is fine)
if [ -f "$REQUIREMENTS_FILE" ]; then
  echo "[PNL-COO] Installing deps…"
  python -m pip install --upgrade pip >/dev/null
  pip install -r "$REQUIREMENTS_FILE" >/dev/null
fi

# --- .env handling (no secrets in the repo) ---
# Preference order:
#   1) ENV_PATH (explicit)
#   2) .env next to dev.command
#   3) ~/Documents/PNL COO/.env
#   4) ~/Documents/PNL_COO/.env
ENV_SRC=""
if [ -n "${ENV_PATH:-}" ] && [ -f "${ENV_PATH}" ]; then
  ENV_SRC="${ENV_PATH}"
elif [ -f "${SCRIPT_DIR}/.env" ]; then
  ENV_SRC="${SCRIPT_DIR}/.env"
elif [ -f "${HOME}/Documents/PNL COO/.env" ]; then
  ENV_SRC="${HOME}/Documents/PNL COO/.env"
elif [ -f "${HOME}/Documents/PNL_COO/.env" ]; then
  ENV_SRC="${HOME}/Documents/PNL_COO/.env"
fi

# Link central env into project (non-fatal)
if [ -n "$ENV_SRC" ] && [ "$ENV_SRC" != "${SCRIPT_DIR}/.env" ]; then
  ln -sf "$ENV_SRC" "${SCRIPT_DIR}/.env" >/dev/null 2>&1 || true
fi

# Export vars from .env into this shell (so FastAPI can see them)
if [ -f "${SCRIPT_DIR}/.env" ]; then
  set -a
  source "${SCRIPT_DIR}/.env"
  set +a
fi

# Kill anything already on the port to avoid serving the wrong folder
if command -v lsof >/dev/null 2>&1; then
  OLD_PIDS=$(lsof -ti tcp:${PORT} || true)
  if [ -n "${OLD_PIDS}" ]; then
    echo "[PNL-COO] Port ${PORT} in use (PID: ${OLD_PIDS}). Stopping…"
    kill ${OLD_PIDS} >/dev/null 2>&1 || true
    sleep 0.5
  fi
fi

cleanup() {
  if [ -n "${SERVER_PID:-}" ]; then
    kill "$SERVER_PID" >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT

echo "[PNL-COO] Starting server on http://127.0.0.1:${PORT} …"
python -m uvicorn app.main:app --port ${PORT} &
SERVER_PID=$!

sleep 1
URL="http://127.0.0.1:${PORT}"
if command -v open >/dev/null 2>&1; then
  open "$URL" >/dev/null 2>&1 || true
fi

echo "[PNL-COO] Health: ${URL}/api/health"
echo "[PNL-COO] Press Ctrl+C to stop."
wait "$SERVER_PID"
