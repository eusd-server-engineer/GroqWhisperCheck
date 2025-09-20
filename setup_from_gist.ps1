# Setup script that pulls API key from your private gist
# This file CAN be committed since it doesn't contain the key itself

Write-Host "Setting up GroqWhisperCheck from GitHub..." -ForegroundColor Cyan

# Your private gist ID
$GIST_ID = "9427f691835ffb213cea084826753d45"

# Install with uv
Write-Host "`nInstalling gq command with uv..." -ForegroundColor Green
uv tool install --from . --python 3.12 groq-cli --force

# Get API key from private gist
Write-Host "`nFetching API key from private gist..." -ForegroundColor Green
try {
    gh gist view $GIST_ID > .env
    Write-Host "✓ API key retrieved and saved to .env" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to fetch gist. Make sure you're logged in with: gh auth login" -ForegroundColor Red
    exit 1
}

# Update PATH
Write-Host "`nUpdating PATH..." -ForegroundColor Green
uv tool update-shell

Write-Host "`n✅ Setup complete!" -ForegroundColor Green
Write-Host "`nRestart your terminal, then test with:" -ForegroundColor Yellow
Write-Host "  gq -q 'Hello world'" -ForegroundColor White
Write-Host "`nYour gist ID for reference: $GIST_ID" -ForegroundColor DarkGray