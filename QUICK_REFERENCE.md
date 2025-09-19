# gq - Quick Reference

## Most Common Commands

```bash
# Quick question
gq -q "your question here"

# Interactive chat
gq

# Transcribe audio
gq -t -f audio.mp3
```

## Real-World Examples

### Current Information (Web Search)
```bash
gq -q "What's the weather in San Francisco?"
gq -q "Latest news about renewable energy"
gq -q "Current stock price of NVDA"
```

### Calculations (Code Execution)
```bash
gq -q "Calculate 18% tip on $85.50"
gq -q "What's the monthly payment on a 300k mortgage at 6.5% for 30 years"
gq -q "Convert 72 fahrenheit to celsius"
```

### Creative & Static Knowledge
```bash
gq -q "Write a haiku about coding" -m llama-3.1-8b-instant
gq -q "Explain quantum computing simply" -m llama-3.3-70b-versatile
```

### Audio Transcription
```bash
# Basic transcription
gq -t -f recording.mp3

# Save to file
gq -t -f recording.wav --output transcript.txt

# Generate subtitles
gq -t -f video.mp4 --format srt --output subtitles.srt
```

## Model Selection

| Use Case | Model | Command Flag |
|----------|-------|-------------|
| Research, current info | groq/compound | (default) |
| Single tool, fast | groq/compound-mini | `-m groq/compound-mini` |
| Creative writing | llama-3.1-8b-instant | `-m llama-3.1-8b-instant` |
| Complex reasoning | llama-3.3-70b-versatile | `-m llama-3.3-70b-versatile` |

## Tips

1. **Default is smart**: `groq/compound` automatically uses web search and code
2. **Be specific**: "Calculate..." triggers code execution
3. **Ask for current**: "What's the latest..." triggers web search
4. **Speed matters**: Use `-m llama-3.1-8b-instant` for quick responses
5. **Transcription**: Supports MP3, WAV, M4A, and more up to 100MB

## Setup Reminder

```bash
# Set API key once
set GROQ_API_KEY=your_key_here

# Or use .env file
echo GROQ_API_KEY=your_key_here > .env
```

---
*Command: `gq` | Help: `gq --help` | Version: 0.1.0*