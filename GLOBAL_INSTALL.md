# Global Installation with uv

## ✅ Installation Complete!

`gq` has been installed globally using `uv tool install`. This gives you:

- **Fast execution**: Uses `uv`'s optimized environment
- **Isolated dependencies**: No conflicts with other Python packages
- **Easy updates**: Just run `uv tool upgrade groq-cli`
- **Clean uninstall**: `uv tool uninstall groq-cli` if needed

## 📍 Installation Location

Your `gq` command is installed at:
```
C:\Users\Josh\.local\bin\gq.exe
```

## 🚀 To Use Globally

You need to restart your terminal/PowerShell for the PATH changes to take effect.

After restarting:
```bash
# Use from anywhere!
gq -q "What's the weather today?"
gq -q "Calculate 15% tip on $45"
gq -t -f audio.mp3
```

## 🔧 If `gq` is not found after restart

Add to your PATH manually:

### Option 1: PowerShell (Temporary)
```powershell
$env:Path += ";C:\Users\Josh\.local\bin"
```

### Option 2: Windows Settings (Permanent)
1. Open System Properties → Environment Variables
2. Edit PATH (User variables)
3. Add: `C:\Users\Josh\.local\bin`
4. OK and restart terminal

### Option 3: PowerShell Profile (Permanent)
Add to your PowerShell profile (`$PROFILE`):
```powershell
$env:Path = "C:\Users\Josh\.local\bin;" + $env:Path
```

## 📦 Managing with uv

### Update to latest version
```bash
cd C:\Users\Josh\Projects\GroqWhisperCheck
uv tool install --from . --force --python 3.12 groq-cli
```

### Or from the project directory
```bash
uv tool upgrade groq-cli
```

### Uninstall
```bash
uv tool uninstall groq-cli
```

### List installed tools
```bash
uv tool list
```

## 🎯 Benefits of uv tool install

1. **No pip conflicts**: Isolated from global Python packages
2. **Fast startup**: uv's optimized Python runtime
3. **Auto-updates**: Easy to upgrade when you update the project
4. **Clean PATH**: Only adds one directory to PATH
5. **Multiple versions**: Can have different versions for different projects

## 💡 Pro Tips

- The tool runs in its own isolated environment (no `venv` activation needed)
- Dependencies are managed separately from your global Python
- Updates are instant with `uv tool upgrade`
- Works alongside other Python tools without conflicts

## 🔍 Troubleshooting

If you see errors about missing packages:
```bash
# Reinstall fresh
uv tool uninstall groq-cli
uv tool install --from C:\Users\Josh\Projects\GroqWhisperCheck --python 3.12 groq-cli
```

---

**Remember**: After installation, restart your terminal for PATH changes to take effect!