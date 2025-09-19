# Add uv tools directory to PATH permanently

# Check if .local\bin is already in PATH
$uvPath = "C:\Users\Josh\.local\bin"
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")

if ($currentPath -notlike "*$uvPath*") {
    Write-Host "Adding $uvPath to user PATH..." -ForegroundColor Green

    # Add to user PATH environment variable
    $newPath = "$uvPath;$currentPath"
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")

    Write-Host "✓ Added to permanent user PATH" -ForegroundColor Green
    Write-Host ""
    Write-Host "Please restart your PowerShell/Terminal for changes to take effect." -ForegroundColor Yellow
} else {
    Write-Host "✓ $uvPath is already in PATH" -ForegroundColor Green
}

# Also check if it's in the current session
if ($env:Path -notlike "*$uvPath*") {
    $env:Path = "$uvPath;" + $env:Path
    Write-Host "✓ Added to current session PATH" -ForegroundColor Green
}

Write-Host ""
Write-Host "You can now test with:" -ForegroundColor Cyan
Write-Host "  gq -q 'Hello world'" -ForegroundColor White