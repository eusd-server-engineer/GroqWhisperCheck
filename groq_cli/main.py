"""Main CLI interface for Groq tool."""

import os
import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from dotenv import load_dotenv

from groq_cli.transcriber import WhisperTranscriber
from groq_cli.chat import ChatCompleter

# Load environment variables
load_dotenv()

console = Console()


@click.command()
@click.argument('text', required=False, type=str)
@click.option('-q', '--query', type=str, help='Query for chat completion')
@click.option('-t', '--transcribe', is_flag=True, help='Switch to Whisper transcription mode')
@click.option('-f', '--file', type=click.Path(exists=True, path_type=Path), help='Audio file for transcription')
@click.option('-m', '--model', default='groq/compound', help='Model for chat (default: groq/compound - with web search and tools)')
@click.option('--whisper-model', default='whisper-large-v3-turbo', help='Whisper model (default: whisper-large-v3-turbo)')
@click.option('--api-key', envvar='GROQ_API_KEY', help='Groq API key (or set GROQ_API_KEY env var)')
@click.option('--output', type=click.Path(), help='Output file for transcription')
@click.option('--format', type=click.Choice(['text', 'json', 'srt', 'vtt']), default='text', help='Output format for transcription')
@click.option('--language', help='Language code for transcription (e.g., en, es, fr)')
@click.option('--temperature', type=float, default=0.7, help='Temperature for chat (0.0-1.0)')
@click.option('--max-tokens', type=int, default=2000, help='Maximum tokens for chat response')
@click.option('--system', help='System prompt for chat')
@click.option('--tier', type=click.Choice(['free', 'developer']), default='free', help='Account tier for file size limits')
def cli(
    text: Optional[str],
    query: Optional[str],
    transcribe: bool,
    file: Optional[Path],
    model: str,
    whisper_model: str,
    api_key: str,
    output: Optional[str],
    format: str,
    language: Optional[str],
    temperature: float,
    max_tokens: int,
    system: Optional[str],
    tier: str
):
    """
    Groq CLI tool for chat completions and Whisper transcription.

    Examples:

        # Chat completion (shorthand):
        groq "Explain quantum computing"

        # Chat completion (explicit):
        groq -q "Explain quantum computing"

        # Transcription:
        groq -t -f audio.mp3

        # Interactive chat:
        groq

        # Advanced transcription:
        groq -t -f audio.wav --whisper-model whisper-large-v3 --format srt --output subtitles.srt

        # Chat with custom model:
        groq "Write a poem" -m llama-3.3-70b-versatile --temperature 0.9

        # Use compound model for research:
        groq "What's the latest news about AI?" -m groq/compound
    """

    # If positional text argument is provided, use it as query
    if text and not query:
        query = text

    # Check for API key
    if not api_key:
        console.print("[red]Error: GROQ_API_KEY not found.[/red]")
        console.print("[yellow]Set it with:[/yellow]")
        console.print("  [dim]Windows:[/dim] set GROQ_API_KEY=your_api_key_here")
        console.print("  [dim]Or create a .env file with:[/dim] GROQ_API_KEY=your_api_key_here")
        sys.exit(1)

    try:
        if transcribe:
            # Transcription mode
            handle_transcription(
                file=file,
                api_key=api_key,
                model=whisper_model,
                output=output,
                format=format,
                language=language,
                tier=tier
            )

        elif query:
            # Chat completion mode
            handle_chat(
                query=query,
                api_key=api_key,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                system_prompt=system
            )

        else:
            # Interactive mode
            handle_interactive(
                api_key=api_key,
                model=model,
                temperature=temperature,
                system_prompt=system
            )

    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled.[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


def handle_transcription(
    file: Optional[Path],
    api_key: str,
    model: str,
    output: Optional[str],
    format: str,
    language: Optional[str],
    tier: str
) -> None:
    """Handle transcription mode."""
    if not file:
        console.print("[red]Error: --file is required when using --transcribe[/red]")
        console.print("[yellow]Usage: groq -t -f audio.mp3[/yellow]")
        sys.exit(1)

    # Initialize transcriber
    transcriber = WhisperTranscriber(api_key=api_key, tier=tier)

    # Perform transcription
    console.print(f"[blue]Processing: {file.name}[/blue]")
    console.print(f"[dim]Model: {model}[/dim]")
    if language:
        console.print(f"[dim]Language: {language}[/dim]")

    result = transcriber.transcribe(
        file_path=file,
        model=model,
        language=language,
        response_format="verbose_json" if format in ['srt', 'vtt', 'json'] else "text",
        include_timestamps=(format in ['srt', 'vtt', 'json'])
    )

    # Display transcript
    console.print("\n[green]Transcription:[/green]")
    console.print("-" * 50)

    # Handle both string and dict responses
    if isinstance(result, str):
        transcript_text = result
        # Convert to dict format for consistency
        result = {'text': transcript_text}
    else:
        transcript_text = result.get('text', '')

    if transcript_text:
        # Wrap long text for better display
        from textwrap import fill
        wrapped_text = fill(transcript_text, width=console.width - 4)
        console.print(wrapped_text)
    else:
        console.print("[yellow]No text found in transcription.[/yellow]")

    console.print("-" * 50)

    # Save to file if requested
    if output or format != 'text':
        if not output:
            # Generate default output filename
            output = file.with_suffix(f'.{format if format != "text" else "txt"}')
        else:
            output = Path(output)

        transcriber.save_transcript(result, output, format=format)

    # Display statistics if available
    if 'duration' in result:
        console.print(f"\n[dim]Duration: {result['duration']:.1f} seconds[/dim]")
    if 'language' in result:
        console.print(f"[dim]Detected language: {result['language']}[/dim]")


def handle_chat(
    query: str,
    api_key: str,
    model: str,
    temperature: float,
    max_tokens: int,
    system_prompt: Optional[str]
) -> None:
    """Handle single chat completion."""
    # Initialize chat completer
    chat = ChatCompleter(api_key=api_key)

    # Display model info
    console.print(f"[dim]Using model: {model}[/dim]")
    if system_prompt:
        console.print(f"[dim]System: {system_prompt}[/dim]")
    console.print()

    # Stream the response
    result = chat.stream_completion(
        query=query,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        system_prompt=system_prompt,
        maintain_history=False
    )

    console.print()  # Final newline

    # Show tools used if compound model
    if result.get("tools_used") and "compound" in model:
        console.print(f"[dim]Tools used: {', '.join(result['tools_used'])}[/dim]")


def handle_interactive(
    api_key: str,
    model: str,
    temperature: float,
    system_prompt: Optional[str]
) -> None:
    """Handle interactive chat mode."""
    # Display welcome message
    console.print("[bold green]Welcome to Groq Interactive Chat![/bold green]")
    console.print(f"[dim]Model: {model} | Temperature: {temperature}[/dim]")
    if system_prompt:
        console.print(f"[dim]System: {system_prompt}[/dim]")
    console.print()

    # Initialize chat and start interactive session
    chat = ChatCompleter(api_key=api_key)
    chat.interactive_chat(
        model=model,
        temperature=temperature,
        system_prompt=system_prompt
    )


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()