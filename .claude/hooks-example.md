# Claude Code Hooks Configuration Example

## Overview
This document provides example hook configurations for Windows to automatically capture subagent outputs and generate summaries.

## Hook Types

### 1. SubagentStop Hook
Triggers when a subagent completes its task.

**Windows PowerShell Configuration:**
```powershell
# .claude/hooks/subagent-stop.ps1
param(
    [string]$AgentName,
    [string]$Output,
    [string]$TaskDescription
)

$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$summaryDir = ".claude/summaries"
$summaryFile = "$summaryDir/${AgentName}_${timestamp}.md"

# Create summary directory if it doesn't exist
if (!(Test-Path $summaryDir)) {
    New-Item -ItemType Directory -Path $summaryDir | Out-Null
}

# Write summary
@"
# Agent Summary: $AgentName
**Generated**: $timestamp
**Task**: $TaskDescription

## Output
$Output

---
"@ | Out-File -FilePath $summaryFile -Encoding UTF8

Write-Host "Summary saved to: $summaryFile"
```

### 2. PostToolUse Hook
Triggers after any tool is used.

**Example Configuration:**
```json
{
  "hooks": {
    "PostToolUse": {
      "command": "powershell.exe -NoProfile -ExecutionPolicy Bypass -File .claude/hooks/post-tool-use.ps1",
      "triggers": ["Task", "WebSearch", "WebFetch"],
      "capture_output": true
    }
  }
}
```

### 3. TaskComplete Hook
Custom hook for when a todo item is marked complete.

```powershell
# .claude/hooks/task-complete.ps1
param(
    [string]$TaskName,
    [string]$Status
)

$logFile = ".claude/task-log.md"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

"- [$timestamp] Task '$TaskName' marked as: $Status" |
    Add-Content -Path $logFile
```

## Implementation Steps

1. **Create hooks directory:**
   ```bash
   mkdir .claude/hooks
   ```

2. **Create PowerShell scripts** for each hook type needed

3. **Configure Claude Code settings** to use the hooks:
   - Open Claude Code settings
   - Navigate to Hooks configuration
   - Add hook configurations

4. **Test hooks** by invoking subagents or using tools

## Best Practices

1. **Always use UTF-8 encoding** for output files
2. **Include timestamps** in all summaries
3. **Create directories** if they don't exist
4. **Handle errors gracefully** with try-catch blocks
5. **Keep summaries concise** but comprehensive

## Example Summary Output

```markdown
# Agent Summary: research-agent
**Generated**: 2024-01-15_14-30-45
**Task**: Research Groq Whisper API rate limits

## Output
### Key Findings
- Organization-level rate limits apply
- Free tier: 25MB file size limit
- Developer tier: 100MB file size limit
- Rate limits: RPM and TPM based

### Recommendations
- Implement exponential backoff
- Cache frequently used responses
- Monitor usage with 15-minute delay

---
```

## Troubleshooting

### Common Issues
1. **Permission denied**: Run PowerShell as Administrator
2. **Execution policy**: Use `-ExecutionPolicy Bypass` flag
3. **Path not found**: Use absolute paths or verify working directory
4. **Encoding issues**: Explicitly set UTF-8 encoding

### Debug Commands
```powershell
# Test hook manually
powershell -NoProfile -ExecutionPolicy Bypass -File .claude/hooks/subagent-stop.ps1 -AgentName "test" -Output "test output" -TaskDescription "test task"

# Check hook output
Get-Content .claude/summaries/test_*.md
```