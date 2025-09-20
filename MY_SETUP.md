# Personal Setup Instructions

## Your Private Gist

Your API key is stored in a secret GitHub Gist:
- **Gist URL**: https://gist.github.com/eusd-server-engineer/9427f691835ffb213cea084826753d45
- **Gist ID**: `9427f691835ffb213cea084826753d45`

## Quick Setup on Any Machine

### Method 1: Using the Setup Script

```powershell
# Clone the repo
git clone https://github.com/eusd-server-engineer/GroqWhisperCheck.git
cd GroqWhisperCheck

# Run the setup script
.\setup_from_gist.ps1

# Restart terminal, then use
gq -q "Hello world"
```

### Method 2: Manual Setup

```powershell
# Clone the repo
git clone https://github.com/eusd-server-engineer/GroqWhisperCheck.git
cd GroqWhisperCheck

# Install gq
uv tool install --from . --python 3.12 groq-cli

# Get your API key from gist
gh gist view 9427f691835ffb213cea084826753d45 > .env

# Update PATH
uv tool update-shell

# Restart terminal and use
gq -q "test"
```

## Prerequisites

Make sure you have these installed on each machine:
1. **GitHub CLI**: `winget install GitHub.cli` or download from github.com/cli/cli
2. **UV**: `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`
3. **Python 3.10+**: Should come with uv

## Logging into GitHub CLI

If you're not logged in:
```powershell
gh auth login
# Choose: GitHub.com
# Choose: HTTPS
# Choose: Login with web browser
```

## Viewing Your Gist

To see or edit your API key:
```powershell
# View
gh gist view 9427f691835ffb213cea084826753d45

# Edit (opens in editor)
gh gist edit 9427f691835ffb213cea084826753d45

# View in browser
Start-Process "https://gist.github.com/eusd-server-engineer/9427f691835ffb213cea084826753d45"
```

## Security Notes

- ✅ The gist is **secret** (not listed publicly)
- ✅ Only accessible when logged into your GitHub account
- ✅ The `.env` file is gitignored (won't be committed)
- ✅ The setup script can be shared (doesn't contain the key)

## If You Need to Update Your API Key

```powershell
# Edit the gist
gh gist edit 9427f691835ffb213cea084826753d45

# Or create a new .env and update the gist
echo "GROQ_API_KEY=new_key_here" > .env
gh gist edit 9427f691835ffb213cea084826753d45 .env
```

## Complete Fresh Setup Commands

Copy and paste this block on any new Windows machine:

```powershell
# One-liner to install prerequisites
winget install GitHub.cli; powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Clone and setup
git clone https://github.com/eusd-server-engineer/GroqWhisperCheck.git
cd GroqWhisperCheck
gh auth login  # If not already logged in
.\setup_from_gist.ps1

# Restart terminal then test
gq -q "What's the weather?"
```

---

*Note: This file is safe to commit since it only contains the gist ID, not the actual API key.*