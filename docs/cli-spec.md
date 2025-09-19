# CLI Tool Specification

## Project: Groq Command-Line Interface
**Priority: 2**
**Status: In Development**

## Overview
Create a globally accessible Windows CLI tool that provides both Whisper transcription and chat completion functionality through simple terminal commands.

## Command Structure

### Basic Syntax
```bash
groq [OPTIONS]
```

### Primary Options
- `-q, --query TEXT`: Submit a text query to the compound model
- `-t, --transcribe`: Enable Whisper transcription mode
- `-f, --file PATH`: Specify audio file path for transcription
- `-m, --model TEXT`: Chat model selection (default: groq/compound)
- `--whisper-model TEXT`: Whisper model selection (default: whisper-large-v3-turbo)
- `--api-key TEXT`: API key (alternative to environment variable)
- `-h, --help`: Show help message

### Usage Examples

#### Chat Completion
```bash
# Simple query
groq -q "Explain quantum computing in simple terms"

# With model selection
groq -q "Write a Python function" -m llama3-70b-8192

# Interactive mode (no query provided)
groq
```

#### Whisper Transcription
```bash
# Transcribe audio file
groq -t -f "C:\audio\meeting.mp3"

# With specific model
groq -t -f audio.wav --whisper-model whisper-large-v3

# Transcribe with output to file
groq -t -f audio.mp3 --output transcript.txt
```

## Features

### Chat Completion Mode
1. **Streaming Response**: Real-time token streaming to terminal
2. **Interactive Mode**: Multi-turn conversation when no query provided
3. **Model Selection**: Support for all Groq chat models
4. **Context Preservation**: Maintain conversation history in interactive mode
5. **Formatted Output**: Rich text formatting with colors

### Transcription Mode
1. **File Validation**: Check format and size before upload
2. **Progress Indicator**: Show upload and processing status
3. **Multiple Output Formats**: Console, text file, JSON
4. **Timestamp Support**: Optional word-level timestamps
5. **Error Recovery**: Graceful handling of API failures

### Common Features
1. **Environment Configuration**: Support .env files
2. **Global Installation**: Accessible from any directory
3. **Windows Path Handling**: Proper handling of Windows file paths
4. **Unicode Support**: Correct display of special characters
5. **Colored Output**: Enhanced readability with Rich library

## Technical Implementation

### Dependencies
- **click**: Command-line argument parsing
- **groq**: Official Groq Python SDK
- **rich**: Terminal formatting and colors
- **python-dotenv**: Environment variable management
- **pathlib**: Cross-platform path handling

### Installation Methods
1. **pip install**: Global installation via setuptools entry points
2. **Poetry**: Development and distribution management
3. **Batch wrapper**: Alternative Windows-specific approach

### Configuration Files
```
.env                 # API key and default settings
groq_config.json     # User preferences (optional)
```

### Error Handling
1. Missing API key detection
2. Invalid file path validation
3. Network timeout management
4. Rate limit handling
5. Graceful interrupt (Ctrl+C)

## Windows-Specific Requirements

### Path Registration
- Entry point in Scripts directory
- Automatic .exe wrapper creation
- PATH environment variable update

### File Path Handling
- Support both forward and backward slashes
- Handle spaces in paths
- UNC path support
- Relative to absolute path conversion

### Terminal Compatibility
- Windows Terminal full support
- PowerShell color rendering
- Command Prompt compatibility
- ConEmu/Cmder support

## User Experience

### First-Time Setup
```bash
# Install
pip install groq-cli

# Set API key
set GROQ_API_KEY=your_api_key_here

# Test
groq -q "Hello, world!"
```

### Help System
```bash
groq --help           # General help
groq -t --help        # Transcription help
```

### Progress Feedback
- Upload progress bar for large files
- Streaming tokens with color coding
- Clear error messages with suggestions
- Processing time display

## Testing Requirements
1. Command parsing validation
2. File path edge cases
3. Streaming output verification
4. Interactive mode testing
5. Error message clarity
6. Installation verification

## Success Criteria
1. Single command installation
2. Global accessibility from any directory
3. Smooth streaming output
4. Proper Windows path handling
5. Clear error messages
6. Interactive and non-interactive modes
7. Fast response time (<1s startup)

## Future Enhancements
1. Configuration file support
2. Output redirection options
3. Batch file processing
4. Custom prompt templates
5. Response caching
6. Auto-update mechanism
7. Shell completions (PowerShell/Bash)