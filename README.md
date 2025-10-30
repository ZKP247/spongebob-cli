# SpongeBob CLI (ai.sooners.us, gemma3:4b)

A tiny Python command-line chatbot that talks like **SpongeBob**, keeps **multi-turn chat history**, and calls the **OpenAI-compatible Chat Completions API** at `https://ai.sooners.us/api/chat/completions` using **gemma3:4b**.

## Features
- OpenAI-compatible `/api/chat/completions`
- Multi-turn history (system + prior messages on every call)
- Secrets in `~/.soonerai.env` (not committed)
- CLI commands: `/reset`, `/save`, `/help`, `/exit`

## Setup

**Python:** 3.9+ recommended

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
