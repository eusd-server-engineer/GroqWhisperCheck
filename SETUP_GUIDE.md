# Setup Guide for New Machines

## Quick Start (Any Machine)

```bash
# 1. Clone the repository
git clone https://github.com/eusd-server-engineer/GroqWhisperCheck.git
cd GroqWhisperCheck

# 2. Install with uv
uv tool install --from . --python 3.12 groq-cli

# 3. Set your API key (choose one method):
```

## Method 1: Environment Variable (Persistent)

### Windows (PowerShell as Admin)
```powershell
[Environment]::SetEnvironmentVariable("GROQ_API_KEY", "your_key_here", "User")
# Restart terminal
```

### Windows (Command Prompt)
```cmd
setx GROQ_API_KEY "your_key_here"
# Restart terminal
```

### Linux/Mac
```bash
echo 'export GROQ_API_KEY="your_key_here"' >> ~/.bashrc
source ~/.bashrc
```

## Method 2: .env File (Per Project)

```bash
# Create .env in project directory
echo GROQ_API_KEY=your_key_here > .env
```

## Method 3: Windows Credential Manager (Most Secure)

```powershell
# Store credential
cmdkey /generic:GROQ_API_KEY /user:groq /pass:your_key_here

# The app can retrieve it (future feature)
```

## Method 4: Personal Setup Script

Create your own `my_setup.ps1` (ignored by Git):

```powershell
# my_setup.ps1
$env:GROQ_API_KEY = "your_actual_key_here"
uv tool install --from . --python 3.12 groq-cli
uv tool update-shell
Write-Host "Setup complete! Restart terminal and use 'gq'"
```

Then run:
```powershell
.\my_setup.ps1
```

## For Multiple Machines (Your Use Case)

### Option 1: Secure Sync Service
Use a password manager that syncs (1Password, Bitwarden, etc.):
1. Store API key in password manager
2. Copy to each machine during setup

### Option 2: Encrypted File
Create an encrypted `.env.gpg`:
```bash
# Encrypt (on main machine)
gpg -c .env  # Creates .env.gpg

# Decrypt (on new machine)
gpg -d .env.gpg > .env
```

### Option 3: Private Gist
Store your setup script in a private GitHub Gist:
```bash
# Create private gist with your API key
gh gist create my_setup.ps1 --private

# On new machine, get the gist
gh gist view GIST_ID > my_setup.ps1
.\my_setup.ps1
```

## GitHub Secrets - What They're Actually For

GitHub Secrets are for **GitHub Actions** (CI/CD), not for distributing keys to users:

```yaml
# .github/workflows/test.yml
name: Test
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: |
          export GROQ_API_KEY=${{ secrets.GROQ_API_KEY }}
          python test_groq.py
```

They're useful for:
- Running tests in CI/CD
- Automated deployments
- Building releases

But they DON'T:
- Get downloaded with `git clone`
- Automatically set up on user machines
- Provide keys to end users

## Recommended Approach for You

Since you have multiple workstations:

1. **Use a private Gist** for your personal setup:
   ```bash
   # Create once
   echo "GROQ_API_KEY=your_key" > .env
   gh gist create .env --private -d "Groq API key"

   # On each new machine
   gh gist view YOUR_GIST_ID > .env
   ```

2. **Or use Windows Credential Manager**:
   - Store once per machine
   - Very secure
   - Survives reinstalls

3. **Or use environment variable**:
   - Set once per machine
   - Works everywhere
   - Simple and reliable

## Security Best Practices

✅ **DO**:
- Keep API keys in `.env` files (gitignored)
- Use environment variables
- Store in password managers
- Use credential managers

❌ **DON'T**:
- Commit keys to Git
- Put keys in code
- Share keys in issues/PRs
- Include in documentation

## Testing Your Setup

After setup, test with:
```bash
gq -q "Hello, is my API key working?"
```

If it responds, you're all set!