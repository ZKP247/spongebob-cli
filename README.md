# SpongeBob CLI (ai.sooners.us, gemma3:4b)

A tiny Python command-line chatbot that talks like **SpongeBob**, keeps **multi-turn chat history**, and calls the **OpenAI-compatible Chat Completions API** at `https://ai.sooners.us/api/chat/completions` using **gemma3:4b**. 
It keeps multi-turn chat history, stores API secrets securely in ~/.soonerai.env, and supports commands like /reset, /save, /help, and /exit.

## Features
- OpenAI-compatible `/api/chat/completions`
- Multi-turn history (system + prior messages on every call)
- Secrets in `~/.soonerai.env` (not committed)
- CLI commands: `/reset`, `/save`, `/help`, `/exit`
- Configurable temperature & memory length

## Setup

**Python:** 3.9+ recommended

1. python3 --version. (check your python3 compatibility)
2. git clone [https](https://github.com/ZKP247/spongebob-cli.git)
3. cd spongebob-cli (clone and enter the repo)
4. python3 -m venv .venv
5. source .venv/bin/activate (create and activate a virtual environment)
6. pip install -r requirements.txt (install dependencies)
7. Create your SoonerAI account and API KEY
     Visit https://ai.sooners.us
     Sign up with your OU email.
     Go to Settings → Account → API Keys.
     Create a new key and copy it.
8. Create the environment file -> create a file ~/.soonerai.env
     SOONERAI_API_KEY=your_key_here
     SOONERAI_BASE_URL=https://ai.sooners.us
     SOONERAI_MODEL=gemma3:4b
9. Run the chatbot -> python spongebob_cli.py

💬 Example Transcript
(.venv) kepengzhou@Kepengs-MacBook-Pro-2 spongebob-cli % python3 spongebob_cli.py
Hooray! 🧽 Welcome to SpongeBob's CLI. I'm ready! I'm ready! Type /help for commands. (Ctrl+C to quit)

You: Hi Spongebob, is Patrick Star your best friend?
SpongeBob: Barnacles, of COURSE! Patrick's my bestest buddy! 😄

You: what's your favorite seafood?
SpongeBob: Krabby Patties, definitely! 🍔😋

You: Have you ever been out of the ocean?
SpongeBob: Once! It was...weird! 🤪 But Mr. Krabs said it was for "business"!

You: let's sing! spongebob squarepants!
SpongeBob: Okay! Let's do it! 🎶 “Are ya ready, kids?! 😄”

You: yes!
SpongeBob: “Fun, fun, fun!” 😄🥳

You: keep going!
SpongeBob: “I like to wiggle and jiggle!” 🤪🌊

You: I can't hear you!
SpongeBob: “I’m singing very, very LOUD!” 📣😄

You: good bye!
SpongeBob: “Bye bye! See ya later, alligator!” 👋😄

🧠 Troubleshooting
| Problem                              | Possible Fix                                                              |
| ------------------------------------ | ------------------------------------------------------------------------- |
| `401 Unauthorized`                   | Check your `SOONERAI_API_KEY` value and expiration.                       |
| `404 Not Found`                      | Make sure your `.env` file has `SOONERAI_BASE_URL=https://ai.sooners.us`. |
| `requests.exceptions.ConnectTimeout` | Check your internet connection.                                           |
| Output stops mid-sentence            | Try a lower `--temperature` or shorter context (`--keep 6`).              |


📦 Files in this repo
| File                       | Purpose                                            |
| ---------------------------| -------------------------------------------------- |
| `spongebob_cli.py`         | Main chatbot script                                |
| `requirements.txt`         | Dependencies (`requests`, `python-dotenv`)         |
| `README.md`                | Documentation and setup instructions               |
| `.gitignore`               | Ensures `.env` and `__pycache__/` aren’t committed |
| `spongebob_cli_example.py` | Example script with one message                    |


