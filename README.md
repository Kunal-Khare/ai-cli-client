# CLI AI Client

A simple command-line tool to chat with multiple AI providers directly from your terminal.

## Supported Providers

* Groq (default)
* OpenAI
* Anthropic Claude
* Google Gemini

## Features

* Chat with AI from terminal (single or interactive mode)
* Supports multiple AI APIs in one tool
* Saves API keys securely in `~/.ai_cli_config.json`
* Works with environment variables too

## Setup

```bash
# Install dependencies
pip install groq openai anthropic google-generativeai

# (Optional) make it executable
chmod +x ai_cli.py
```

## Configure API Keys

```bash
python ai_cli.py --configure
```

Or set environment variables:

```
export GROQ_API_KEY="your_key"
export OPENAI_API_KEY="your_key"
export ANTHROPIC_API_KEY="your_key"
export GEMINI_API_KEY="your_key"
```

## Usage

```bash
# Interactive chat (default: Groq)
python ai_cli.py

# One-time query
python ai_cli.py "Explain recursion in simple words"

# Use different provider
python ai_cli.py -p openai "What is overfitting?"

# With system prompt
python ai_cli.py -p anthropic -s "You are a teacher" -i
```

## Example

```
You: Write a haiku about AI
AI: Machines learn softly
    Code whispers through endless loops
    Thoughts born of zeros
```

## Notes

* Config file is stored at `~/.ai_cli_config.json` (permissions 0600)
* Supports clearing history (`clear` in chat)
* Works with Python 3.8+

## License

MIT License (add if needed)
