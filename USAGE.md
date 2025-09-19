# GroqWhisperCheck Usage Guide

## Command Names

Since you have another `groq` command installed globally (from pocketgroq), our CLI tool is available as:

- **`gq`** - Primary command (shortest and easiest!)
- **`groqchat`** - Alternative name
- **`groq-cli`** - Alternative name

## Installation & Usage

### Option 1: Using uv (Recommended)
```bash
cd C:\Users\Josh\Projects\GroqWhisperCheck
uv run gq -q "Your query here"
```

### Option 2: Install Globally
```bash
cd C:\Users\Josh\Projects\GroqWhisperCheck
uv pip install -e .

# Then use from anywhere:
gq -q "What's the weather today?"
gq -q "Calculate 15% of 250"
```

## Quick Examples

### Research Query (Uses Web Search)
```bash
gq -q "What's the latest news about AI?"
```

### Calculation (Uses Code Execution)
```bash
gq -q "Calculate compound interest on 5000 at 7% for 10 years"
```

### Audio Transcription
```bash
gq -t -f "path\to\audio.mp3"
```

### Interactive Chat Mode
```bash
gq
```

### Use Different Model
```bash
# Fast model without web search
gq -q "Write a poem" -m llama-3.1-8b-instant

# Compound mini for single-tool tasks
gq -q "What's 2+2" -m groq/compound-mini
```

## Available Models

### Default: groq/compound
- Has web search, code execution, and other tools
- Best for research, current events, calculations

### Other Models
- `groq/compound-mini` - Faster, single-tool tasks
- `llama-3.1-8b-instant` - Fast responses, no tools
- `llama-3.3-70b-versatile` - Balanced performance

## Troubleshooting

### If you see pocketgroq errors
You're using the wrong `groq` command. Use `groqchat` or `groq-cli` instead.

### To check which command you're using
```bash
where groq      # Shows C:\Windows\groq.bat (pocketgroq)
where groqchat  # Shows our tool
```

### To always use our project version
```bash
# Create an alias in PowerShell
Set-Alias groq groqchat

# Or always use with uv
uv run groqchat [args]
```

## Features

- **Compound Model**: Automatic web search and code execution
- **Streaming**: Real-time response display
- **Whisper**: Audio transcription support
- **Multiple Formats**: Text, JSON, SRT, VTT for transcripts

---

*Note: The global `groq` command points to a different tool (pocketgroq). Use `groqchat` for this project.*