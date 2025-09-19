#!/usr/bin/env python
"""Simple test script for Groq CLI functionality."""

import os
import sys
from pathlib import Path
from groq_cli.transcriber import WhisperTranscriber, transcribe_audio
from groq_cli.chat import ChatCompleter, quick_chat
from rich.console import Console

console = Console()


def test_api_connection():
    """Test basic API connection."""
    console.print("[yellow]Testing API connection...[/yellow]")

    api_key = os.environ.get('GROQ_API_KEY')
    if not api_key:
        console.print("[red][X] GROQ_API_KEY not found in environment[/red]")
        return False

    try:
        # Test with a simple chat query
        response = quick_chat("Say 'API connection successful' in 5 words or less", stream=False)
        if response:
            console.print(f"[green][OK] API Response: {response}[/green]")
            return True
        else:
            console.print("[red][X] No response from API[/red]")
            return False
    except Exception as e:
        console.print(f"[red][X] API Error: {e}[/red]")
        return False


def test_transcription(audio_file: str = None):
    """Test Whisper transcription."""
    console.print("\n[yellow]Testing Whisper transcription...[/yellow]")

    if audio_file and Path(audio_file).exists():
        file_path = Path(audio_file)
    else:
        # Create a dummy test note
        console.print("[dim]Note: Provide an audio file path to test actual transcription[/dim]")
        console.print("[dim]Example: python test_groq.py sample.mp3[/dim]")
        return False

    try:
        transcriber = WhisperTranscriber()
        console.print(f"[blue]Testing with file: {file_path.name}[/blue]")

        # Validate file
        transcriber.validate_file(file_path)
        console.print("[green][OK] File validation passed[/green]")

        # Attempt transcription
        result = transcriber.transcribe(file_path, model="whisper-large-v3-turbo")

        if result and 'text' in result:
            text = result['text'][:100] + "..." if len(result.get('text', '')) > 100 else result.get('text', '')
            console.print(f"[green][OK] Transcription successful: {text}[/green]")
            return True
        else:
            console.print("[red][X] Transcription failed[/red]")
            return False

    except Exception as e:
        console.print(f"[red][X] Transcription Error: {e}[/red]")
        return False


def test_chat_streaming():
    """Test chat streaming."""
    console.print("\n[yellow]Testing chat streaming...[/yellow]")

    try:
        chat = ChatCompleter()
        console.print("[blue]Sending test query...[/blue]")
        response = chat.stream_completion(
            "Count from 1 to 5 slowly",
            model="llama-3.1-8b-instant",  # Use a current fast model for testing
            temperature=0.1,
            max_tokens=50
        )

        if response:
            console.print("\n[green][OK] Streaming completed successfully[/green]")
            return True
        else:
            console.print("[red][X] No streaming response[/red]")
            return False

    except Exception as e:
        console.print(f"[red][X] Streaming Error: {e}[/red]")
        return False


def main():
    """Run all tests."""
    console.print("[bold cyan]Groq CLI Test Suite[/bold cyan]")
    console.print("=" * 50)

    # Check for audio file argument
    audio_file = sys.argv[1] if len(sys.argv) > 1 else None

    # Run tests
    results = []
    results.append(("API Connection", test_api_connection()))

    if audio_file:
        results.append(("Whisper Transcription", test_transcription(audio_file)))
    else:
        console.print("\n[yellow]Skipping transcription test (no audio file provided)[/yellow]")

    results.append(("Chat Streaming", test_chat_streaming()))

    # Summary
    console.print("\n" + "=" * 50)
    console.print("[bold cyan]Test Results Summary:[/bold cyan]")
    for test_name, passed in results:
        status = "[green][PASSED][/green]" if passed else "[red][FAILED][/red]"
        console.print(f"  {test_name}: {status}")

    all_passed = all(result[1] for result in results)
    if all_passed:
        console.print("\n[bold green]All tests passed![/bold green]")
    else:
        console.print("\n[bold red]Some tests failed. Please check the errors above.[/bold red]")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())