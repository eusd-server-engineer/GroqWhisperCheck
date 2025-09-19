# Changelog

## [0.1.0] - 2025-09-19

### Added
- **Groq Compound AI Model Integration** - Default model now supports:
  - Built-in web search for real-time information
  - Python code execution for calculations
  - Automatic tool selection based on queries
  - Domain filtering for targeted research

- **Short Command Name** - `gq` as primary command (also available: `groqchat`, `groq-cli`)

- **Global Installation via UV** - Fast, isolated installation using `uv tool install`

- **Whisper Transcription** - Support for audio file transcription using Groq's Whisper models:
  - `whisper-large-v3-turbo` (216x real-time, default)
  - `whisper-large-v3` (164x real-time)
  - Multiple output formats (text, JSON, SRT, VTT)

- **Streaming Chat Completions** - Real-time token streaming to terminal

- **Interactive Mode** - Conversational interface with history management

- **Windows Optimization** - Full compatibility with Windows Terminal, PowerShell, and Command Prompt

### Technical Improvements
- Updated to Python 3.10+ minimum requirement
- Fixed Unicode encoding issues for Windows terminals
- Enhanced error handling for API responses
- Added tool usage tracking for compound models
- Implemented domain filtering for web searches
- UTF-8 encoding forced for Windows compatibility

### Models
- Default: `groq/compound` (with tools)
- Alternative: `groq/compound-mini` (single-tool, lower latency)
- Standard models: `llama-3.3-70b-versatile`, `llama-3.1-8b-instant`
- Whisper: `whisper-large-v3-turbo`, `whisper-large-v3`

### Documentation
- Comprehensive README with usage examples
- CLAUDE.md for AI assistant guidance
- UV installation guide for global access
- Quick reference card for common commands
- Detailed update notes for September 2025

### Dependencies
- groq>=0.11.0
- click>=8.0.0
- rich>=13.0.0
- python-dotenv>=1.0.0
- aiohttp>=3.8.0

### Configuration
- Environment variable support (`GROQ_API_KEY`)
- .env file configuration
- Command-line API key option
- Tier selection for file size limits

### Breaking Changes
- Default model changed from `llama-3.3-70b-versatile` to `groq/compound`
- `stream_completion()` now returns dict with `text` and `tools_used` keys
- Minimum Python version increased to 3.10

### Known Issues
- Some Unicode characters may require special handling in older terminals
- File size limits: 25MB (free tier), 100MB (developer tier)
- Rate limits apply at organization level