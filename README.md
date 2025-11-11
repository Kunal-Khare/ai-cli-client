# CLI AI Client

Terminal interface for chatting with multiple AI providers from a single, consistent CLI.

Supported providers out of the box:

* **Groq** (default)
* **Google Gemini**
* **OpenAI**
* **Anthropic Claude**

> One script, one command, many models.

---

## Features

* 🔁 **Unified chat interface** across providers (messages/history abstracted for you)
* 🧠 **System prompts** supported (where the API allows)
* 💾 **Local, ephemeral conversation history** per session
* 🔐 **Simple credential management** via `~/.ai_cli_config.json` (0600 perms)
* 🧪 **Single-shot** or **interactive** REPL-like chat modes
* 🧰 **Pluggable provider + model selection** with sensible defaults

---

## Requirements

* Python **3.8+**
* Provider SDKs (install only what you need):

  * `pip install groq`  (for Groq)
  * `pip install google-generativeai`  (for Gemini)
  * `pip install openai`  (for OpenAI)
  * `pip install anthropic`  (for Claude)

> You can install them all safely; the script imports each one conditionally.

---

## Installation

```bash
# 1) Clone your repo
git clone <your-repo-url>
cd <your-repo-folder>

# 2) (Optional) Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate

# 3) Install provider SDKs you plan to use
pip install groq google-generativeai openai anthropic

# 4) Make the script executable (optional)
chmod +x ai_cli.py
```

> Replace `ai_cli.py` with your file name if different.

---

## Quick Start

Configure your API keys once:

```bash
python ai_cli.py --configure
```

This creates/updates `~/.ai_cli_config.json` and sets secure permissions. You may also set environment variables instead of (or in addition to) the file:

* `GEMINI_API_KEY`
* `OPENAI_API_KEY`
* `ANTHROPIC_API_KEY`
* `GROQ_API_KEY`

Run an interactive chat (defaults to Groq):

```bash
python ai_cli.py
```

Ask a one-off question (default provider = Groq):

```bash
python ai_cli.py "Explain Python decorators with examples"
```

Use a different provider & model:

```bash
python ai_cli.py -p openai -m gpt-4-turbo-preview "Give me 3 refactoring tips"
python ai_cli.py -p anthropic -m claude-3-5-sonnet-20241022 "Rewrite this more clearly"
python ai_cli.py -p gemini -m gemini-pro "Summarize: attention is all you need"
python ai_cli.py -p groq -m llama-3.3-70b-versatile "Write a haiku about CLIs"
```

Start interactive mode explicitly and set a system prompt:

```bash
python ai_cli.py --system "You are a concise, helpful assistant." --interactive
```

---

## Usage

```
usage: ai_cli.py [-h] [-p {gemini,openai,anthropic,groq}] [-m MODEL]
                 [-i] [-s SYSTEM] [--configure]
                 [query ...]

Chat with AI models in your terminal

positional arguments:
  query                 Your question or prompt (omit to enter interactive mode)

options:
  -h, --help            Show this help message and exit
  -p, --provider        AI provider to use (default: groq)
  -m, --model           Specific model to use
  -i, --interactive     Start interactive chat mode
  -s, --system          System prompt / instructions
  --configure           Configure API keys interactively
```

### Examples

```bash
# Interactive (Groq default)
python ai_cli.py

# One-off with Anthropic
python ai_cli.py -p anthropic "Draft an apology email for a missed meeting"

# OpenAI with system prompt
python ai_cli.py -p openai -s "You are a strict proof checker." "Is this proof valid?"

# Gemini quick question
python ai_cli.py -p gemini "List 5 creative study techniques"
```

---

## Provider Defaults (as implemented in code)

| Provider      | SDK Import                        | Default Model                | Notes                                        |
| ------------- | --------------------------------- | ---------------------------- | -------------------------------------------- |
| **Groq**      | `from groq import Groq`           | `llama-3.3-70b-versatile`    | CLI default provider                         |
| **Gemini**    | `google.generativeai`             | `gemini-pro`                 | System prompt is prepended to first user msg |
| **OpenAI**    | `from openai import OpenAI`       | `gpt-4-turbo-preview`        | Uses Chat Completions API                    |
| **Anthropic** | `from anthropic import Anthropic` | `claude-3-5-sonnet-20241022` | Uses Messages API with `system` when given   |

> You can always override the model with `-m/--model`.

---

## How It Works (High-level)

1. **Config**: On startup, keys are loaded from `~/.ai_cli_config.json` and/or environment variables.
2. **Provider Init**: The chosen provider client is initialized lazily with your API key and default model (if none specified).
3. **Message Flow**:

   * For **OpenAI** & **Groq**: messages history is sent as Chat Completions.
   * For **Anthropic**: history is sent to Messages API, optionally with a `system` string.
   * For **Gemini**: a single `generate_content` call; if this is the first turn and a system prompt exists, it’s prepended to your message.
4. **History**: In-memory only. Use `clear` in interactive mode to reset. Exiting the program also clears history.

---

## Security Notes

* Your config file is saved at `~/.ai_cli_config.json` with permissions set to **0600**.
* Never commit API keys to version control.
* Consider using an isolated virtual environment and a secrets manager for production usage.

---

## Troubleshooting

* **ImportError: SDK not installed**

  * Install the missing SDK, e.g. `pip install groq`.
* **ValueError: API key not found**

  * Run `python ai_cli.py --configure` or set the relevant `*_API_KEY` env var.
* **HTTP / auth errors**

  * Confirm your key is valid and has access to the requested model.
* **Model not found**

  * Pass a valid `-m` for that provider, or switch provider.
* **Unicode / terminal issues**

  * Try a different terminal font or ensure your locale is UTF-8.

---

## Extending

* Add a new provider by implementing a new branch in `initialize_client()` and `chat()`.
* Mirror the structure used for Groq/OpenAI/Anthropic/Gemini.
* Optionally, refactor providers into separate modules/classes if the file grows.

---

## Roadmap Ideas

* Streamed tokens output
* Persistent transcript save/export (`--save transcript.md`)
* Tool/function calling
* Image input/output where supported
* Multi-turn system prompts and per-session profiles

---

## Legal

This project is provided "as is" with no warranty. You are responsible for compliance with each provider’s terms of service and usage policies.

---

## License

Consider adding an open-source license (e.g., MIT) to clarify reuse.
