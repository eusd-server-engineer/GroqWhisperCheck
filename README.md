# GroqWhisperCheck

A Windows CLI tool for Groq API integration featuring Whisper audio transcription, streaming chat completions, and the powerful Compound AI model with built-in web search and code execution capabilities.

## Features

- 🎙️ **Whisper Transcription**: Transcribe audio files using Groq's Whisper models
- 💬 **Chat Completion**: Stream responses from Groq's language models
- 🔍 **Compound AI Model**: Built-in web search, code execution, and tool use capabilities
- 🖥️ **Windows Optimized**: Fully compatible with Windows Terminal, PowerShell, and Command Prompt
- 🚀 **Global CLI Access**: Use `groq` command from anywhere after installation
- 📝 **Multiple Output Formats**: Support for text, JSON, SRT, and VTT formats
- ⚡ **Fast Inference**: Powered by Groq's LPU technology for industry-leading speed

## Installation

### Prerequisites
- Python 3.8 or higher
- Groq API key (get one at [console.groq.com](https://console.groq.com))

### Quick Install

1. Clone the repository:
```bash
git clone https://github.com/yourusername/GroqWhisperCheck.git
cd GroqWhisperCheck
```

2. Install the package:
```bash
pip install -e .
```

3. Set up your API key:
```bash
# Windows Command Prompt
set GROQ_API_KEY=your_api_key_here

# Or create a .env file
copy .env.example .env
# Edit .env and add your API key
```

## Command Name

The tool is available as **`gq`** (short and easy to type!). Alternative names: `groqchat`, `groq-cli`

## Usage

### Whisper Transcription

Transcribe an audio file:
```bash
gq -t -f "path\to\audio.mp3"
```

Advanced transcription with options:
```bash
gq -t -f audio.wav --whisper-model whisper-large-v3 --format srt --output subtitles.srt
```

### Chat Completion

Simple query (uses Compound model with web search by default):
```bash
gq -q "What's the latest news about AI today?"
```

Research with specific domains:
```bash
gq -q "Latest quantum computing breakthroughs" -m groq/compound
```

With specific model:
```bash
gq -q "Write a haiku" -m llama-3.1-8b-instant --temperature 0.9
```

Interactive chat mode:
```bash
gq
```

### Command Options

| Option | Description | Example |
|--------|-------------|---------|
| `-q, --query` | Text query for chat | `gq -q "Hello"` |
| `-t, --transcribe` | Enable transcription mode | `gq -t -f audio.mp3` |
| `-f, --file` | Audio file path | `gq -t -f "C:\audio\file.wav"` |
| `-m, --model` | Chat model selection | `gq -q "Test" -m groq/compound` |
| `--whisper-model` | Whisper model selection | `gq -t -f audio.mp3 --whisper-model whisper-large-v3` |
| `--format` | Output format (text/json/srt/vtt) | `gq -t -f audio.mp3 --format srt` |
| `--output` | Output file path | `gq -t -f audio.mp3 --output transcript.txt` |
| `--language` | Language code for transcription | `gq -t -f audio.mp3 --language en` |
| `--temperature` | Chat temperature (0-1) | `gq -q "Test" --temperature 0.5` |
| `--api-key` | API key (alternative to env var) | `gq -q "Test" --api-key your_key` |

## Supported Models

### Whisper Models (September 2025)
- `whisper-large-v3-turbo`: Fast, 216x real-time, $0.04/hour (default)
- `whisper-large-v3`: Higher accuracy, 164x real-time, $0.03/hour
- `distil-whisper`: Lightweight variant for faster processing

### Chat Models (September 2025)

#### Compound Models (with built-in tools)
- `groq/compound`: Multi-tool workflows with web search & code execution (default)
- `groq/compound-mini`: Single-tool tasks, 3x lower latency

#### Standard Models
- `llama-3.3-70b-versatile`: Llama 3.3 70B with enhanced capabilities
- `llama-3.1-8b-instant`: Llama 3.1 8B for fast responses
- `llama-4-scout`: 109B total params, 460+ tokens/s
- `mixtral-8x7b-32768`: Mixtral 8x7B
- `gemma2-9b-it`: Gemma 2 9B

## Compound Model Capabilities

The Compound AI model includes built-in tools:
- **Web Search**: Real-time internet research
- **Code Execution**: Python code execution for calculations
- **Website Access**: Direct website content extraction
- **Browser Automation**: Automated web interactions

### Example: Research Query
```bash
gq -q "Research the latest developments in renewable energy and summarize the top 3 innovations"
```

The model automatically decides when to use web search, making it perfect for:
- Current events and news
- Technical research
- Fact-checking
- Data analysis with calculations

## File Size Limits

- **Free Tier**: 25MB maximum file size
- **Developer Tier**: 100MB maximum file size

## Supported Audio Formats

- FLAC (.flac)
- MP3 (.mp3)
- MP4 (.mp4)
- MPEG (.mpeg, .mpga)
- M4A (.m4a)
- OGG (.ogg)
- WAV (.wav)
- WebM (.webm)

## Testing

Run the test suite:
```bash
# Basic tests (without audio file)
python test_groq.py

# Full tests (with audio file)
python test_groq.py sample.mp3
```

## Project Structure

```
GroqWhisperCheck/
├── groq_cli/
│   ├── __init__.py         # Package initialization
│   ├── main.py             # CLI entry point
│   ├── transcriber.py      # Whisper transcription module
│   ├── chat.py             # Chat completion module
│   └── utils.py            # Utility functions
├── docs/
│   ├── whisper-spec.md     # Whisper API specifications
│   ├── cli-spec.md         # CLI tool specifications
│   └── projects.md         # Project tracking
├── .claude/
│   ├── agents/             # Subagent configurations
│   └── summaries/          # Agent output summaries
├── tests/
│   └── test_files/         # Sample audio files
├── pyproject.toml          # Project configuration
├── requirements.txt        # Dependencies
├── test_groq.py           # Test script
└── README.md              # This file
```

## Troubleshooting

### Common Issues

1. **"GROQ_API_KEY not found"**
   - Set the environment variable: `set GROQ_API_KEY=your_key`
   - Or create a `.env` file with your key

2. **"File too large" error**
   - Free tier limit is 25MB
   - Consider upgrading to developer tier or splitting the file

3. **"Unsupported format" error**
   - Check that your file is in a supported format
   - Convert to WAV or MP3 if needed

4. **Installation issues**
   - Ensure Python 3.8+ is installed
   - Try: `pip install --upgrade pip setuptools wheel`

## Development

### Setting up for development:
```bash
# Clone repository
git clone https://github.com/yourusername/GroqWhisperCheck.git
cd GroqWhisperCheck

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install in development mode
pip install -e .[dev]
```

### Running with subagents:
The project includes Claude Code subagent configurations for:
- Research tasks
- Testing operations
- Summary generation

See `.claude/agents/README.md` for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- Built with [Groq API](https://groq.com)
- CLI powered by [Click](https://click.palletsprojects.com)
- Terminal formatting by [Rich](https://rich.readthedocs.io)

## Support

For issues or questions, please open an issue on GitHub or contact the maintainer.