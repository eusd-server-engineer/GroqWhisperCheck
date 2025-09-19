"""Utility functions for the Groq CLI tool."""

import os
import sys
from pathlib import Path
from typing import Optional, Union
from rich.console import Console

console = Console()


def validate_api_key(api_key: Optional[str] = None) -> str:
    """
    Validate and return API key.

    Args:
        api_key: Optional API key

    Returns:
        Valid API key

    Raises:
        SystemExit: If no valid API key found
    """
    key = api_key or os.environ.get('GROQ_API_KEY')

    if not key:
        console.print("[red]Error: GROQ_API_KEY not found.[/red]")
        console.print("[yellow]Please set your API key:[/yellow]")
        console.print("  1. Set environment variable: set GROQ_API_KEY=your_key_here")
        console.print("  2. Create .env file with: GROQ_API_KEY=your_key_here")
        console.print("  3. Pass via command line: groq --api-key your_key_here")
        sys.exit(1)

    return key


def safe_path_handling(file_path: Union[str, Path]) -> Path:
    """
    Safely handle file paths on Windows.

    Args:
        file_path: File path as string or Path object

    Returns:
        Resolved Path object

    Raises:
        FileNotFoundError: If file doesn't exist
    """
    # Convert to Path object - handles forward/backward slashes
    path = Path(file_path)

    # Resolve to absolute path
    path = path.resolve()

    # Verify file exists
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    return path


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.

    Args:
        size_bytes: Size in bytes

    Returns:
        Formatted string
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def get_audio_file_info(file_path: Path) -> dict:
    """
    Get information about an audio file.

    Args:
        file_path: Path to audio file

    Returns:
        Dictionary with file information
    """
    stat = file_path.stat()
    return {
        'name': file_path.name,
        'path': str(file_path),
        'size': stat.st_size,
        'size_formatted': format_file_size(stat.st_size),
        'extension': file_path.suffix.lower(),
        'modified': stat.st_mtime
    }


def is_supported_audio_format(file_path: Path) -> bool:
    """
    Check if file has a supported audio format.

    Args:
        file_path: Path to file

    Returns:
        True if supported, False otherwise
    """
    supported = {'.flac', '.mp3', '.mp4', '.mpeg', '.mpga', '.m4a', '.ogg', '.wav', '.webm'}
    return file_path.suffix.lower() in supported


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to specified length.

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add when truncated

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def create_default_env_file() -> None:
    """Create a default .env file if it doesn't exist."""
    env_path = Path('.env')
    if not env_path.exists():
        env_content = """# Groq API Configuration
GROQ_API_KEY=your_api_key_here

# Optional settings
# GROQ_DEFAULT_MODEL=groq/compound
# GROQ_DEFAULT_WHISPER_MODEL=whisper-large-v3-turbo
# GROQ_ACCOUNT_TIER=free
"""
        env_path.write_text(env_content)
        console.print("[green]Created .env file. Please add your API key.[/green]")
    else:
        console.print("[yellow].env file already exists.[/yellow]")


def get_system_info() -> dict:
    """Get system information for debugging."""
    import platform
    return {
        'os': platform.system(),
        'os_version': platform.version(),
        'python_version': platform.python_version(),
        'machine': platform.machine(),
        'processor': platform.processor()
    }