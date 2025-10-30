"""
SpongeBob CLI Chatbot (multi-turn) for ai.sooners.us (OpenAI-compatible)

- Uses Chat Completions API at: {BASE_URL}/api/chat/completions
- Default model: gemma3:4b
- Loads secrets from ~/.soonerai.env
- Maintains and sends chat history each turn
- Simple commands: /reset, /save <file>, /help, /exit

Run:
  python spongebob_cli.py
"""

import os
import sys
import json
import time
import argparse
from typing import List, Dict
import requests
from dotenv import load_dotenv

# ---------- Config & Env ----------

ENV_PATH = os.path.join(os.path.expanduser("~"), ".soonerai.env")
load_dotenv(ENV_PATH)

API_KEY = os.getenv("SOONERAI_API_KEY")
BASE_URL = os.getenv("SOONERAI_BASE_URL", "https://ai.sooners.us").rstrip("/")
MODEL = os.getenv("SOONERAI_MODEL", "gemma3:4b")

CHAT_URL = f"{BASE_URL}/api/chat/completions"

SYSTEM_STYLE = (
    "You are SpongeBob SquarePants. Speak cheerfully with nautical/ocean humor, "
    "enthusiastic optimism, and playful word choices. Keep replies concise for a CLI."
)

DEFAULT_TEMPERATURE = 0.6
DEFAULT_MAX_TURNS = 8  # keep last N user/assistant pairs (plus system)

# ---------- Helpers ----------

def ensure_api_key():
    if not API_KEY:
        raise RuntimeError(
            "Missing SOONERAI_API_KEY. Create ~/.soonerai.env with:\n"
            "SOONERAI_API_KEY=your_key_here\n"
            "SOONERAI_BASE_URL=https://ai.sooners.us\n"
            "SOONERAI_MODEL=gemma3:4b"
        )

def truncate_history(history: List[Dict[str, str]], keep_pairs: int) -> List[Dict[str, str]]:
    if not history:
        return history
    system = history[0:1]
    rest = history[1:]
    return system + rest[-2 * keep_pairs :]

def api_chat_completion(messages: List[Dict[str, str]], temperature: float) -> str:
    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": temperature,
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    try:
        resp = requests.post(CHAT_URL, headers=headers, json=payload, timeout=90)
    except requests.RequestException as e:
        raise RuntimeError(f"Network error calling {CHAT_URL}: {e}") from e

    if resp.status_code != 200:
        raise RuntimeError(f"Error {resp.status_code}: {resp.text}")

    data = resp.json()
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as e:
        raise RuntimeError(f"Unexpected API response: {json.dumps(data, indent=2)}") from e

def print_bot(t: str):
    print(f"SpongeBob: {t}")

def save_transcript(path: str, history: List[Dict[str, str]]):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for msg in history:
            role = msg.get("role", "?")
            content = msg.get("content", "")
            f.write(f"{role.upper()}: {content}\n\n")
    print(f"[Saved transcript to {path}]")

def build_argparser():
    p = argparse.ArgumentParser(description="SpongeBob CLI chatbot (ai.sooners.us, gemma3:4b)")
    p.add_argument("--temperature", type=float, default=DEFAULT_TEMPERATURE, help="Sampling temperature")
    p.add_argument("--keep", type=int, default=DEFAULT_MAX_TURNS, help="Keep last N user/assistant turns")
    p.add_argument("--system", type=str, default=SYSTEM_STYLE, help="Override system prompt")
    return p

# ---------- Main Loop ----------

def main():
    ensure_api_key()
    args = build_argparser().parse_args()

    history: List[Dict[str, str]] = [
        {"role": "system", "content": args.system.strip()},
    ]

    print("Ahoy! 🧽 Welcome to SpongeBob's CLI. Type /help for commands. (Ctrl+C to quit)")

    while True:
        try:
            user_text = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye-bye, barnacle buddy! 🌊")
            break

        if not user_text:
            continue

        if user_text.lower() in ("/exit", "/quit"):
            print("Bye-bye, barnacle buddy! 🌊")
            break
        if user_text.lower() == "/help":
            print(
                "Commands:\n"
                "  /reset              Clear chat history (keeps system prompt)\n"
                "  /save <file>        Save transcript to a text file\n"
                "  /help               Show this help\n"
                "  /exit               Quit"
            )
            continue
        if user_text.lower() == "/reset":
            history = [{"role": "system", "content": args.system.strip()}]
            print("[History reset]")
            continue
        if user_text.lower().startswith("/save"):
            parts = user_text.split(maxsplit=1)
            if len(parts) == 2:
                save_transcript(parts[1], history)
            else:
                ts = time.strftime("%Y%m%d-%H%M%S")
                save_transcript(f"transcript-{ts}.txt", history)
            continue

        history.append({"role": "user", "content": user_text})
        send_history = truncate_history(history, args.keep)

        try:
            reply = api_chat_completion(send_history, args.temperature)
        except Exception as e:
            print(f"[Error] {e}")
            history.pop()
            continue

        history.append({"role": "assistant", "content": reply})
        print_bot(reply)

if __name__ == "__main__":
    main()

