"""Whisper transcription module for Groq API."""

import os
import json
from pathlib import Path
from typing import Optional, Dict, Any, Literal
from groq import Groq, GroqError, RateLimitError, APIError
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn

console = Console()

# Supported audio formats
SUPPORTED_FORMATS = {'.flac', '.mp3', '.mp4', '.mpeg', '.mpga', '.m4a', '.ogg', '.wav', '.webm'}

# File size limits in MB
FILE_SIZE_LIMITS = {
    'free': 25,
    'developer': 100
}

ResponseFormat = Literal["json", "text", "verbose_json", "srt", "vtt"]

class WhisperTranscriber:
    """Handles audio transcription using Groq's Whisper API."""

    def __init__(self, api_key: Optional[str] = None, tier: str = 'free'):
        """
        Initialize the transcriber with API credentials.

        Args:
            api_key: Groq API key (defaults to GROQ_API_KEY env var)
            tier: Account tier ('free' or 'developer')
        """
        self.api_key = api_key or os.environ.get('GROQ_API_KEY')
        if not self.api_key:
            raise ValueError("API key required. Set GROQ_API_KEY or pass api_key parameter.")

        self.client = Groq(api_key=self.api_key)
        self.tier = tier
        self.max_file_size = FILE_SIZE_LIMITS.get(tier, 25) * 1024 * 1024  # Convert to bytes

    def validate_file(self, file_path: Path) -> None:
        """
        Validate audio file format and size.

        Args:
            file_path: Path to the audio file

        Raises:
            ValueError: If file is invalid
        """
        if not file_path.exists():
            raise ValueError(f"File not found: {file_path}")

        # Check file format
        if file_path.suffix.lower() not in SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported format: {file_path.suffix}. "
                f"Supported formats: {', '.join(SUPPORTED_FORMATS)}"
            )

        # Check file size
        file_size = file_path.stat().st_size
        if file_size > self.max_file_size:
            size_mb = file_size / (1024 * 1024)
            max_mb = self.max_file_size / (1024 * 1024)
            raise ValueError(
                f"File too large: {size_mb:.1f}MB. "
                f"Maximum size for {self.tier} tier: {max_mb}MB"
            )

    def transcribe(
        self,
        file_path: Path,
        model: str = "whisper-large-v3-turbo",
        language: Optional[str] = None,
        response_format: ResponseFormat = "verbose_json",
        temperature: float = 0.0,
        include_timestamps: bool = True
    ) -> Dict[str, Any]:
        """
        Transcribe an audio file using Groq's Whisper API.

        Args:
            file_path: Path to the audio file
            model: Whisper model to use
            language: Optional language code (ISO-639-1)
            response_format: Output format
            temperature: Sampling temperature (0-1)
            include_timestamps: Include word/segment timestamps

        Returns:
            Transcription response dictionary
        """
        file_path = Path(file_path).resolve()
        self.validate_file(file_path)

        # Prepare timestamp granularities if needed
        timestamp_granularities = None
        if include_timestamps and response_format == "verbose_json":
            timestamp_granularities = ["word", "segment"]

        console.print(f"[blue]Transcribing {file_path.name} using {model}...[/blue]")

        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TimeRemainingColumn(),
                console=console
            ) as progress:
                task = progress.add_task("Uploading and processing...", total=None)

                with open(file_path, "rb") as audio_file:
                    # Create transcription request
                    params = {
                        "file": (file_path.name, audio_file.read()),
                        "model": model,
                        "response_format": response_format,
                        "temperature": temperature
                    }

                    if language:
                        params["language"] = language

                    if timestamp_granularities:
                        params["timestamp_granularities"] = timestamp_granularities

                    transcription = self.client.audio.transcriptions.create(**params)

                progress.update(task, completed=True)

            # Convert response to dictionary if needed
            if hasattr(transcription, 'model_dump'):
                result = transcription.model_dump()
            elif hasattr(transcription, 'text'):
                # It's a transcription object with text attribute
                result = {'text': transcription.text}
            elif isinstance(transcription, str):
                # It's just a string
                result = transcription
            else:
                result = transcription

            console.print("[green]✓ Transcription completed successfully![/green]")
            return result

        except RateLimitError as e:
            console.print(f"[red]Rate limit exceeded. Please wait and try again.[/red]")
            raise
        except APIError as e:
            console.print(f"[red]API Error: {e}[/red]")
            raise
        except Exception as e:
            console.print(f"[red]Unexpected error: {e}[/red]")
            raise

    def save_transcript(
        self,
        transcript_data: Dict[str, Any],
        output_path: Optional[Path] = None,
        format: str = "text"
    ) -> Path:
        """
        Save transcription to a file.

        Args:
            transcript_data: Transcription response data
            output_path: Optional output file path
            format: Output format ('text', 'json', 'srt', 'vtt')

        Returns:
            Path to saved file
        """
        if output_path is None:
            output_path = Path(f"transcript.{format if format != 'text' else 'txt'}")

        output_path = Path(output_path).resolve()

        if format == "text":
            # Save plain text
            text = transcript_data.get('text', '')
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)

        elif format == "json":
            # Save full JSON response
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(transcript_data, f, indent=2, ensure_ascii=False)

        elif format == "srt":
            # Convert to SRT format
            srt_content = self._convert_to_srt(transcript_data)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(srt_content)

        elif format == "vtt":
            # Convert to WebVTT format
            vtt_content = self._convert_to_vtt(transcript_data)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(vtt_content)

        else:
            raise ValueError(f"Unsupported format: {format}")

        console.print(f"[green]Transcript saved to: {output_path}[/green]")
        return output_path

    def _convert_to_srt(self, transcript_data: Dict[str, Any]) -> str:
        """Convert transcript to SRT subtitle format."""
        segments = transcript_data.get('segments', [])
        if not segments:
            return ""

        srt_lines = []
        for i, segment in enumerate(segments, 1):
            start_time = self._seconds_to_srt_time(segment.get('start', 0))
            end_time = self._seconds_to_srt_time(segment.get('end', 0))
            text = segment.get('text', '').strip()

            srt_lines.append(f"{i}")
            srt_lines.append(f"{start_time} --> {end_time}")
            srt_lines.append(text)
            srt_lines.append("")  # Empty line between subtitles

        return "\n".join(srt_lines)

    def _convert_to_vtt(self, transcript_data: Dict[str, Any]) -> str:
        """Convert transcript to WebVTT subtitle format."""
        segments = transcript_data.get('segments', [])
        if not segments:
            return "WEBVTT\n\n"

        vtt_lines = ["WEBVTT", ""]
        for segment in segments:
            start_time = self._seconds_to_vtt_time(segment.get('start', 0))
            end_time = self._seconds_to_vtt_time(segment.get('end', 0))
            text = segment.get('text', '').strip()

            vtt_lines.append(f"{start_time} --> {end_time}")
            vtt_lines.append(text)
            vtt_lines.append("")  # Empty line between subtitles

        return "\n".join(vtt_lines)

    def _seconds_to_srt_time(self, seconds: float) -> str:
        """Convert seconds to SRT time format (HH:MM:SS,mmm)."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

    def _seconds_to_vtt_time(self, seconds: float) -> str:
        """Convert seconds to WebVTT time format (HH:MM:SS.mmm)."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"


# Convenience function for quick transcription
def transcribe_audio(
    file_path: str,
    api_key: Optional[str] = None,
    model: str = "whisper-large-v3-turbo",
    save_to_file: bool = True
) -> Dict[str, Any]:
    """
    Quick transcription function.

    Args:
        file_path: Path to audio file
        api_key: Optional API key
        model: Whisper model to use
        save_to_file: Whether to save transcript to file

    Returns:
        Transcription data
    """
    transcriber = WhisperTranscriber(api_key=api_key)
    file_path = Path(file_path)

    result = transcriber.transcribe(file_path, model=model)

    if save_to_file:
        # Save as text file next to original
        output_path = file_path.with_suffix('.txt')
        transcriber.save_transcript(result, output_path, format="text")

    return result