#!/usr/bin/env bash
set -euo pipefail

export OLLAMA_HOST="${OLLAMA_HOST:-http://127.0.0.1:11434}"
export OLLAMA_MODEL="${OLLAMA_MODEL:-llama3.2:latest}"
export OLLAMA_MODELS="${OLLAMA_MODELS:-/data/ollama}"
export FIELDFORM_DB_PATH="${FIELDFORM_DB_PATH:-/data/fieldform.db}"

mkdir -p "$(dirname "$FIELDFORM_DB_PATH")" "$OLLAMA_MODELS"

ollama serve &
OLLAMA_PID=$!

cleanup() {
    kill "$OLLAMA_PID" 2>/dev/null || true
}
trap cleanup EXIT

for _ in $(seq 1 60); do
    if ollama list >/dev/null 2>&1; then
        break
    fi
    sleep 1
done

ollama show "$OLLAMA_MODEL" >/dev/null 2>&1 || ollama pull "$OLLAMA_MODEL"

streamlit run app/app.py \
    --server.address=0.0.0.0 \
    --server.port="${PORT:-10000}" \
    --server.headless=true
