#!/usr/bin/env python3
"""
CLI AI Client - Terminal interface for multiple AI providers
Supports: Gemini, OpenAI, Anthropic Claude, Groq, and more
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Optional, List, Dict

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False


class AIClient:
    """Multi-provider AI client"""
    
    def __init__(self, provider: str = "groq", model: Optional[str] = None):
        self.provider = provider.lower()
        self.model = model
        self.conversation_history: List[Dict] = []
        self.config_file = Path.home() / ".ai_cli_config.json"
        self.load_config()
        self.initialize_client()
    
    def load_config(self):
        """Load API keys from config file or environment"""
        self.config = {}
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        
        # Load from environment if not in config
        self.config.setdefault('gemini_api_key', os.getenv('GEMINI_API_KEY', ''))
        self.config.setdefault('openai_api_key', os.getenv('OPENAI_API_KEY', ''))
        self.config.setdefault('anthropic_api_key', os.getenv('ANTHROPIC_API_KEY', ''))
        self.config.setdefault('groq_api_key', os.getenv('GROQ_API_KEY', ''))
    
    def save_config(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
        os.chmod(self.config_file, 0o600)  # Secure the config file
    
    def initialize_client(self):
        """Initialize the appropriate AI client"""
        if self.provider == "gemini":
            if not GEMINI_AVAILABLE:
                raise ImportError("google-generativeai not installed. Run: pip install google-generativeai")
            api_key = self.config.get('gemini_api_key')
            if not api_key:
                raise ValueError("Gemini API key not found. Set GEMINI_API_KEY or run --configure")
            genai.configure(api_key=api_key)
            self.model = self.model or "gemini-pro"
            self.client = genai.GenerativeModel(self.model)
            
        elif self.provider == "openai":
            if not OPENAI_AVAILABLE:
                raise ImportError("openai not installed. Run: pip install openai")
            api_key = self.config.get('openai_api_key')
            if not api_key:
                raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY or run --configure")
            self.client = OpenAI(api_key=api_key)
            self.model = self.model or "gpt-4-turbo-preview"
            
        elif self.provider == "anthropic":
            if not ANTHROPIC_AVAILABLE:
                raise ImportError("anthropic not installed. Run: pip install anthropic")
            api_key = self.config.get('anthropic_api_key')
            if not api_key:
                raise ValueError("Anthropic API key not found. Set ANTHROPIC_API_KEY or run --configure")
            self.client = Anthropic(api_key=api_key)
            self.model = self.model or "claude-3-5-sonnet-20241022"
            
        elif self.provider == "groq":
            if not GROQ_AVAILABLE:
                raise ImportError("groq not installed. Run: pip install groq")
            api_key = self.config.get('groq_api_key')
            if not api_key:
                raise ValueError("Groq API key not found. Set GROQ_API_KEY or run --configure")
            self.client = Groq(api_key=api_key)
            self.model = self.model or "llama-3.3-70b-versatile"

        else:
            raise ValueError(f"Unknown provider: {self.provider}")
    
    def chat(self, message: str, system_prompt: Optional[str] = None) -> str:
        """Send a message and get response"""
        if self.provider == "gemini":
            if system_prompt:
                # For Gemini, prepend system prompt to first message
                if not self.conversation_history:
                    message = f"{system_prompt}\n\n{message}"
            
            response = self.client.generate_content(message)
            return response.text
            
        elif self.provider == "openai":
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.extend(self.conversation_history)
            messages.append({"role": "user", "content": message})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            reply = response.choices[0].message.content
            
            # Update history
            self.conversation_history.append({"role": "user", "content": message})
            self.conversation_history.append({"role": "assistant", "content": reply})
            
            return reply
            
        elif self.provider == "anthropic":
            self.conversation_history.append({"role": "user", "content": message})
            
            kwargs = {"model": self.model, "max_tokens": 4096, "messages": self.conversation_history}
            if system_prompt:
                kwargs["system"] = system_prompt
            
            response = self.client.messages.create(**kwargs)
            reply = response.content[0].text
            
            self.conversation_history.append({"role": "assistant", "content": reply})
            
            return reply
            
        elif self.provider == "groq":
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.extend(self.conversation_history)
            messages.append({"role": "user", "content": message})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            reply = response.choices[0].message.content
            
            # Update history
            self.conversation_history.append({"role": "user", "content": message})
            self.conversation_history.append({"role": "assistant", "content": reply})
            
            return reply
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []


def configure_api_keys():
    """Interactive configuration of API keys"""
    config_file = Path.home() / ".ai_cli_config.json"
    config = {}
    
    if config_file.exists():
        with open(config_file, 'r') as f:
            config = json.load(f)
    
    print("=== AI CLI Configuration ===\n")
    print("Enter your API keys (press Enter to skip):\n")
    
    gemini_key = input(f"Gemini API Key [{config.get('gemini_api_key', '')[:10]}...]: ").strip()
    if gemini_key:
        config['gemini_api_key'] = gemini_key
    
    openai_key = input(f"OpenAI API Key [{config.get('openai_api_key', '')[:10]}...]: ").strip()
    if openai_key:
        config['openai_api_key'] = openai_key
    
    anthropic_key = input(f"Anthropic API Key [{config.get('anthropic_api_key', '')[:10]}...]: ").strip()
    if anthropic_key:
        config['anthropic_api_key'] = anthropic_key
    
    groq_key = input(f"Groq API Key [{config.get('groq_api_key', '')[:10]}...]: ").strip()
    if groq_key:
        config['groq_api_key'] = groq_key
    
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    os.chmod(config_file, 0o600)
    
    print(f"\n✓ Configuration saved to {config_file}")


def interactive_mode(client: AIClient, system_prompt: Optional[str] = None):
    """Run interactive chat mode"""
    print(f"\n=== AI Chat ({client.provider.upper()} - {client.model}) ===")
    print("Type 'exit' or 'quit' to end, 'clear' to reset conversation\n")
    
    while True:
        try:
            user_input = input("\n You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['exit', 'quit']:
                print("\nGoodbye!")
                break
            
            if user_input.lower() == 'clear':
                client.clear_history()
                print("\n✓ Conversation cleared")
                continue
            
            response = client.chat(user_input, system_prompt)
            print(f"\n  AI: {response}")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="CLI AI Client - Chat with AI models in your terminal",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                                    # Interactive mode with Groq
  %(prog)s -p openai "Explain Python"         # Single query with OpenAI
  %(prog)s -p anthropic -m claude-opus-4      # Use Claude Opus
  %(prog)s "Write a function"                 # Quick query with Groq (default)
  %(prog)s --configure                        # Configure API keys
  %(prog)s --system "You are a poet" -i       # Set system prompt

Providers: groq (default), gemini, openai, anthropic
        """
    )
    
    parser.add_argument('query', nargs='*', help='Your question or prompt')
    parser.add_argument('-p', '--provider', default='groq', 
                       choices=['gemini', 'openai', 'anthropic', 'groq'],
                       help='AI provider to use (default: groq)')
    parser.add_argument('-m', '--model', help='Specific model to use')
    parser.add_argument('-i', '--interactive', action='store_true',
                       help='Start interactive chat mode')
    parser.add_argument('-s', '--system', help='System prompt')
    parser.add_argument('--configure', action='store_true',
                       help='Configure API keys')
    
    args = parser.parse_args()
    
    if args.configure:
        configure_api_keys()
        return
    
    try:
        client = AIClient(provider=args.provider, model=args.model)
        
        if args.interactive or not args.query:
            interactive_mode(client, args.system)
        else:
            query = ' '.join(args.query)
            response = client.chat(query, args.system)
            print(response)
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
