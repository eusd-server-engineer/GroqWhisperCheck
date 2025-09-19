# Claude Code Subagent Configuration

This directory contains configuration files for Claude Code subagents used in the GroqWhisperCheck project.

## Available Agents

### 1. Research Agent (`research-agent.json`)
- **Purpose**: Research API documentation and best practices
- **Tools**: WebSearch, WebFetch
- **Use Case**: Gathering information about Groq API updates, finding implementation examples

### 2. Testing Agent (`testing-agent.json`)
- **Purpose**: Validate functionality and test edge cases
- **Tools**: Bash, Read, Write
- **Use Case**: Running test scripts, validating API responses, checking error handling

### 3. Summary Agent (`summary-agent.json`)
- **Purpose**: Generate comprehensive operation summaries
- **Tools**: Read, Write
- **Use Case**: Creating documentation from research, summarizing test results

## Usage

Subagents are invoked automatically when needed to:
- Keep context clean by offloading research tasks
- Perform specialized operations
- Generate consistent documentation

## Summary Output

All agent summaries are saved to `.claude/summaries/` with timestamps and agent identifiers for easy reference.

## Windows-Specific Notes

- Agents use PowerShell for command execution on Windows
- File paths are handled with `pathlib` for cross-platform compatibility
- JSON escaping is configured for Windows file paths