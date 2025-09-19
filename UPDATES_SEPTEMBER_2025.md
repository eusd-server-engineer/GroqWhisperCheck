# GroqWhisperCheck Updates - September 2025

## Major Updates

### 1. Compound AI Model Integration
The project now defaults to Groq's powerful **Compound AI model** (`groq/compound`), which includes:
- **Built-in Web Search**: Automatically searches the internet for current information
- **Code Execution**: Runs Python code for calculations and data processing
- **Website Access**: Directly extracts content from websites
- **Tool Auto-Selection**: AI decides which tools to use based on the query

### 2. Model Updates
- **Default model changed** from `llama-3.3-70b-versatile` to `groq/compound`
- Added `groq/compound-mini` for single-tool, low-latency tasks
- Updated model list to reflect September 2025 availability
- Fixed deprecated model references

### 3. Enhanced Features
- **Domain Filtering**: Control which websites the compound model can search
- **Tool Tracking**: See which tools were used for each query
- **Unicode Support**: Fixed encoding issues for Windows terminals
- **Python 3.10+**: Updated minimum Python version for better compatibility

### 4. API & SDK Updates
- Groq SDK version 0.31.1 confirmed working
- Added support for compound model parameters (`include_domains`, `exclude_domains`)
- Enhanced streaming to show tool usage
- Updated error handling for current API responses

## Usage Examples

### Basic Research Query
```bash
groq -q "What's happening in AI today?"
# Automatically uses web search to find current information
```

### Calculation with Code Execution
```bash
groq -q "Calculate the compound interest on 10000 dollars at 5% for 3 years"
# Uses Python code execution for accurate calculations
```

### Domain-Restricted Research
```bash
groq -q "Latest quantum computing papers" -m groq/compound
# Can be enhanced with domain filtering in code
```

### Traditional Chat (without tools)
```bash
groq -q "Write a haiku" -m llama-3.1-8b-instant
# Uses standard model without web search or tools
```

## Key Improvements

1. **Real-time Information**: Default model can now access current web data
2. **No Setup Required**: Tools work automatically without configuration
3. **Faster Performance**: Compound models leverage Groq's LPU for ~350 tokens/second
4. **Better Accuracy**: ~25% improvement in accuracy over previous versions
5. **Production Ready**: Compound models moved from beta to general availability

## Breaking Changes

- Default model changed to `groq/compound` (was `llama-3.3-70b-versatile`)
- `stream_completion()` now returns a dict with `text` and `tools_used` keys
- Minimum Python version increased to 3.10

## Files Modified

- `groq_cli/main.py`: Updated default model, added compound examples
- `groq_cli/chat.py`: Added compound model support, domain filtering, tool tracking
- `README.md`: Updated with compound model information
- `CLAUDE.md`: Added September 2025 API details
- `pyproject.toml`: Updated Python version requirement
- `test_groq.py`: Fixed unicode issues, updated test models

## Testing

All core functionality tested and working:
- ✅ Compound model web search
- ✅ Code execution capabilities
- ✅ Whisper transcription
- ✅ Standard chat models
- ✅ Streaming responses
- ✅ Windows compatibility

## Notes

- The Compound AI model represents a significant upgrade in capabilities
- No additional API keys or setup required for web search and code execution
- Tools run server-side on Groq's infrastructure
- Pricing is pass-through to underlying models plus tool usage
- Rate limits are generous for production use

## Recommendations

1. **Use Compound Model** for queries requiring current information
2. **Use Standard Models** for creative writing or static knowledge tasks
3. **Use Compound-Mini** for single-tool operations with lower latency
4. **Monitor Tool Usage** to understand and optimize costs

---

*Updated: September 19, 2025*