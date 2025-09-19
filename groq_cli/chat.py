"""Chat completion module with streaming support for Groq API including compound model capabilities."""

import os
from typing import Optional, List, Dict, Generator, Any
from groq import Groq, GroqError, RateLimitError, APIError
from rich.console import Console
import sys
from rich.live import Live
from rich.text import Text
from rich.markdown import Markdown

# Force UTF-8 encoding for Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

console = Console(force_terminal=True, legacy_windows=False)


class ChatCompleter:
    """Handles chat completions with streaming support."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize chat completer with API credentials.

        Args:
            api_key: Groq API key (defaults to GROQ_API_KEY env var)
        """
        self.api_key = api_key or os.environ.get('GROQ_API_KEY')
        if not self.api_key:
            raise ValueError("API key required. Set GROQ_API_KEY or pass api_key parameter.")

        self.client = Groq(api_key=self.api_key)
        self.conversation_history: List[Dict[str, str]] = []

    def stream_completion(
        self,
        query: str,
        model: str = "groq/compound",
        temperature: float = 0.7,
        max_tokens: int = 2000,
        system_prompt: Optional[str] = None,
        maintain_history: bool = False,
        include_domains: Optional[List[str]] = None,
        exclude_domains: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Stream a chat completion response.

        Args:
            query: User query
            model: Model to use
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            system_prompt: Optional system prompt
            maintain_history: Whether to maintain conversation history

        Returns:
            Complete response text
        """
        messages = []

        # Add system prompt if provided
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        # Add conversation history if maintaining
        if maintain_history:
            messages.extend(self.conversation_history)

        # Add current query
        messages.append({"role": "user", "content": query})

        try:
            # Build parameters
            params = {
                "messages": messages,
                "model": model,
                "stream": True,
                "temperature": temperature,
                "max_tokens": max_tokens
            }

            # Add domain filtering for compound models
            if "compound" in model:
                if include_domains:
                    params["include_domains"] = include_domains
                if exclude_domains:
                    params["exclude_domains"] = exclude_domains

            # Create streaming chat completion
            stream = self.client.chat.completions.create(**params)

            response_text = ""
            executed_tools = []

            # Stream tokens to console
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    response_text += content
                    print(content, end="", flush=True)

                # Check for executed tools (compound models)
                if hasattr(chunk.choices[0], 'message') and hasattr(chunk.choices[0].message, 'executed_tools'):
                    executed_tools = chunk.choices[0].message.executed_tools

            # Add to history if maintaining
            if maintain_history:
                self.conversation_history.append({"role": "user", "content": query})
                self.conversation_history.append({"role": "assistant", "content": response_text})

                # Keep history size manageable (last 10 exchanges)
                if len(self.conversation_history) > 20:
                    self.conversation_history = self.conversation_history[-20:]

            # Display tools used if compound model
            if executed_tools and "compound" in model:
                console.print(f"\n[dim]Tools used: {', '.join(executed_tools)}[/dim]")

            return {"text": response_text, "tools_used": executed_tools}

        except RateLimitError as e:
            console.print(f"\n[red]Rate limit exceeded. Please wait and try again.[/red]")
            raise
        except APIError as e:
            console.print(f"\n[red]API Error: {e}[/red]")
            raise
        except Exception as e:
            console.print(f"\n[red]Unexpected error: {e}[/red]")
            raise

    def stream_completion_rich(
        self,
        query: str,
        model: str = "groq/compound",
        temperature: float = 0.7,
        max_tokens: int = 2000,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Stream a chat completion with Rich live display.

        Args:
            query: User query
            model: Model to use
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            system_prompt: Optional system prompt

        Returns:
            Complete response text
        """
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": query})

        try:
            stream = self.client.chat.completions.create(
                messages=messages,
                model=model,
                stream=True,
                temperature=temperature,
                max_tokens=max_tokens
            )

            response_text = ""

            # Use Rich Live for smooth updating
            with Live(console=console, refresh_per_second=10, transient=False) as live:
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        response_text += content

                        # Update display with accumulated text
                        text = Text(response_text)
                        live.update(text)

            return response_text

        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")
            raise

    def interactive_chat(
        self,
        model: str = "groq/compound",
        temperature: float = 0.7,
        system_prompt: Optional[str] = None
    ) -> None:
        """
        Start an interactive chat session.

        Args:
            model: Model to use
            temperature: Sampling temperature
            system_prompt: Optional system prompt
        """
        console.print(f"[green]Starting interactive chat with {model}[/green]")
        console.print("[dim]Type 'exit', 'quit', or 'bye' to end the session[/dim]")
        console.print("[dim]Type 'clear' to clear conversation history[/dim]\n")

        # Initialize with system prompt if provided
        if system_prompt:
            self.conversation_history = [{"role": "system", "content": system_prompt}]
        else:
            self.conversation_history = []

        while True:
            try:
                # Get user input
                query = console.input("[bold blue]You:[/bold blue] ")

                # Check for exit commands
                if query.lower() in ['exit', 'quit', 'bye']:
                    console.print("[yellow]Goodbye![/yellow]")
                    break

                # Check for clear command
                if query.lower() == 'clear':
                    self.conversation_history = []
                    if system_prompt:
                        self.conversation_history = [{"role": "system", "content": system_prompt}]
                    console.print("[yellow]Conversation history cleared.[/yellow]\n")
                    continue

                if not query.strip():
                    continue

                # Display assistant header
                console.print("[bold green]Assistant:[/bold green] ", end="")

                # Stream the response with history
                response = self.stream_completion(
                    query,
                    model=model,
                    temperature=temperature,
                    maintain_history=True
                )

                console.print()  # New line after response

            except KeyboardInterrupt:
                console.print("\n[yellow]Chat interrupted. Goodbye![/yellow]")
                break
            except Exception as e:
                console.print(f"\n[red]Error: {e}[/red]")
                console.print("[yellow]Let's continue...[/yellow]\n")

    def clear_history(self) -> None:
        """Clear conversation history."""
        self.conversation_history = []

    def get_history(self) -> List[Dict[str, str]]:
        """Get current conversation history."""
        return self.conversation_history

    def set_history(self, history: List[Dict[str, str]]) -> None:
        """Set conversation history."""
        self.conversation_history = history


# Convenience function for quick chat
def quick_chat(
    query: str,
    api_key: Optional[str] = None,
    model: str = "groq/compound",
    stream: bool = True,
    include_domains: Optional[List[str]] = None
) -> str:
    """
    Quick chat completion function.

    Args:
        query: User query
        api_key: Optional API key
        model: Model to use
        stream: Whether to stream the response

    Returns:
        Response text
    """
    chat = ChatCompleter(api_key=api_key)

    if stream:
        return chat.stream_completion(query, model=model)
    else:
        # Non-streaming version
        client = Groq(api_key=api_key or os.environ.get('GROQ_API_KEY'))
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": query}],
            model=model,
            stream=False,
            temperature=0.7
        )
        return response.choices[0].message.content