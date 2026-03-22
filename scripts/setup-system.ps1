# Ensure script stops on errors
$ErrorActionPreference = "Stop"

Write-Host "Installing pipx..."
python -m pip install --user pipx
python -m pipx ensurepath