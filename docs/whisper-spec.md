# Groq Whisper API Specification

## Project: Whisper Transcription via Groq
**Priority: 1 (Highest)**
**Status: In Development**

## Overview
Implement audio file transcription using Groq's Whisper API models. This module will handle file submission, transcription processing, and response parsing.

## API Specifications

### Endpoint
- **Transcription**: `https://api.groq.com/openai/v1/audio/transcriptions`
- **Translation**: `https://api.groq.com/openai/v1/audio/translations`

### Authentication
- Bearer token via `GROQ_API_KEY` environment variable
- Header: `Authorization: Bearer $GROQ_API_KEY`

### Available Models
1. **whisper-large-v3-turbo**
   - Speed: 216x real-time
   - Word Error Rate: 12%
   - Cost: $0.04/hour
   - Use Case: Speed-critical applications

2. **whisper-large-v3**
   - Speed: 189x real-time
   - Word Error Rate: 10.3%
   - Cost: $0.111/hour
   - Use Case: Highest accuracy requirements

### File Requirements
- **Supported Formats**: flac, mp3, mp4, mpeg, mpga, m4a, ogg, wav, webm
- **Size Limits**:
  - Free tier: 25MB maximum
  - Developer tier: 100MB maximum
- **Chunking**: Required for files exceeding limits

### Request Parameters
```python
{
    "file": binary,                    # Required: Audio file binary data
    "model": "whisper-large-v3-turbo", # Required: Model selection
    "language": "en",                   # Optional: ISO-639-1 language code
    "response_format": "verbose_json",  # Options: json, text, verbose_json, srt, vtt
    "temperature": 0.0,                 # Optional: 0-1, controls randomness
    "timestamp_granularities": ["word", "segment"]  # Optional: Timestamp detail level
}
```

### Response Format (verbose_json)
```json
{
    "task": "transcribe",
    "language": "english",
    "duration": 8.47,
    "text": "Transcribed text content",
    "words": [
        {
            "word": "The",
            "start": 0.56,
            "end": 0.64
        }
    ],
    "segments": [
        {
            "id": 0,
            "seek": 0,
            "start": 0.56,
            "end": 8.44,
            "text": " The transcribed segment text",
            "tokens": [50364, 440, ...],
            "temperature": 0.0,
            "avg_logprob": -0.286,
            "compression_ratio": 1.236,
            "no_speech_prob": 0.0001
        }
    ]
}
```

## Implementation Requirements

### Core Functions
1. **authenticate(api_key: str)** - Initialize Groq client
2. **validate_file(path: Path)** - Check format and size
3. **transcribe_audio(file_path: Path, model: str)** - Main transcription
4. **parse_response(response: dict)** - Extract and format results
5. **save_transcript(text: str, output_path: Path)** - Save to file

### Error Handling
- File size validation before upload
- Network timeout handling (30 seconds default)
- Rate limit management (exponential backoff)
- Invalid file format detection
- API error response parsing

### Output Options
1. Console display (default)
2. Text file (.txt)
3. JSON file with timestamps
4. SRT/VTT subtitle formats

## Testing Requirements
- Sample audio files in multiple formats
- Files at size boundaries (24MB, 26MB, 99MB, 101MB)
- Different language samples
- Poor quality audio handling
- Network failure simulation

## Success Criteria
1. Successfully transcribe audio files up to size limit
2. Proper error messages for oversized files
3. Support all documented audio formats
4. Handle API errors gracefully
5. Save transcripts in multiple formats
6. Accurate timestamp extraction when requested

## Rate Limits & Performance
- Organization-level rate limits (not per-key)
- Monitor RPM and TPM limits
- Implement retry logic with backoff
- Cache transcripts to avoid redundant API calls

## Security Considerations
- Never log API keys
- Sanitize file paths in error messages
- Validate file content matches extension
- Handle temporary file cleanup

## Future Enhancements
- Batch processing for multiple files
- Audio chunking for large files
- Language auto-detection
- Speaker diarization (if supported)
- Real-time streaming transcription