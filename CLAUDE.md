# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

GroqWhisperCheck is a Windows CLI tool that provides:
1. **Whisper audio transcription** via Groq API
2. **Streaming chat completions** with compound model support
3. **Global CLI access** through the `groq` command

## Common Development Tasks

### Installing and Testing
```bash
# Install in development mode
pip install -e .

# Run tests
python test_groq.py

# Test with audio file
python test_groq.py sample.mp3

# Test CLI directly
python -m groq_cli.main -q "test query"
```

### Building and Distribution
```bash
# Build distribution packages
python -m build

# Install globally
pip install dist/groq_cli-0.1.0-py3-none-any.whl
```

## Architecture

### Core Modules

1. **groq_cli/transcriber.py**: Whisper API integration
   - `WhisperTranscriber` class handles all transcription logic
   - Validates file size limits (25MB free, 100MB developer)
   - Supports multiple output formats (text, JSON, SRT, VTT)

2. **groq_cli/chat.py**: Chat completion with streaming
   - `ChatCompleter` class manages conversations
   - Real-time token streaming to terminal
   - Interactive and non-interactive modes

3. **groq_cli/main.py**: CLI entry point
   - Click-based command structure
   - Handles both `-q` (query) and `-t` (transcribe) modes
   - Environment variable and argument parsing

## API Integration Details (Updated September 2025)

### Authentication
- Primary: `GROQ_API_KEY` environment variable
- Fallback: `--api-key` command argument
- Config: `.env` file support via python-dotenv

### Rate Limiting
- Organization-level limits (not per-key)
- Exponential backoff implemented
- Production-grade stability for compound models
- Check limits at: console.groq.com/settings/limits

### Model Selection
- **Compound Models** (with built-in tools):
  - `groq/compound`: Multi-tool workflows, web search, code execution (default)
  - `groq/compound-mini`: Single-tool tasks, lower latency
- **Whisper Models**:
  - `whisper-large-v3-turbo`: 216x real-time, $0.04/hr (default)
  - `whisper-large-v3`: 164x real-time, $0.03/hr
- **Standard Chat Models**:
  - `llama-3.3-70b-versatile`: General purpose
  - `llama-4-scout`: 460+ tokens/s performance

### Compound Model Features
- Automatic tool selection (web search, code execution)
- Domain filtering with `include_domains` and `exclude_domains`
- Tool tracking via `executed_tools` field
- No additional setup required - tools run server-side

## Windows-Specific Considerations

### Path Handling
- Always use `pathlib.Path` for file operations
- Support both forward and backward slashes
- Handle spaces in paths with proper quoting

### Installation
- Entry points create `.exe` wrapper in Scripts directory
- Global command registration via setuptools
- PowerShell and Command Prompt compatibility

## Subagent System

### Available Agents
Located in `.claude/agents/`:
- **research-agent.json**: API documentation research
- **testing-agent.json**: Functionality validation
- **summary-agent.json**: Operation documentation

### Summary Generation
- All agent outputs saved to `.claude/summaries/`
- Timestamp-based naming convention
- Markdown format for easy reference

## Common Issues & Solutions

### File Size Limits
```python
# Check in transcriber.py
FILE_SIZE_LIMITS = {
    'free': 25,      # MB
    'developer': 100  # MB
}
```

### Streaming Output
- Use `flush=True` for real-time display
- Rich library handles Windows terminal colors
- Fall back to plain text if terminal doesn't support ANSI

### Error Handling
- Catch `GroqError`, `RateLimitError`, `APIError` separately
- Provide clear user feedback with Rich console
- Graceful degradation for network issues

## Testing Checklist

When modifying code, ensure:
- [ ] API key validation works
- [ ] File size limits are enforced
- [ ] Streaming displays properly in Windows terminals
- [ ] Error messages are clear and actionable
- [ ] Global `groq` command works after installation
- [ ] Both transcription and chat modes function

## Important Files

- **pyproject.toml**: Package configuration and entry points
- **test_groq.py**: Comprehensive test suite
- **docs/**: Project specifications and tracking
- **.claude/**: Subagent configurations and summaries
- **.env.example**: Template for API configuration

## Development Workflow

1. Make changes to relevant module
2. Test locally with `python -m groq_cli.main`
3. Run test suite with `python test_groq.py`
4. Install in development mode to test global command
5. Update specifications in `docs/` if needed
6. Use subagents for research when implementing new features

## Performance Considerations

- Whisper models: Balance speed vs accuracy
  - `whisper-large-v3-turbo`: 216x real-time, 12% WER
  - `whisper-large-v3`: 189x real-time, 10.3% WER
- Chat streaming: ~450 tokens/second for compound model
- File uploads: Progress indication for large files

## Security Notes

- Never log or commit API keys
- Sanitize file paths in error messages
- Validate file content matches extension
- Clean up temporary files after processing