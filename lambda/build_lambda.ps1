$BuildDir = Join-Path $PSScriptRoot "build"
$ZipFile  = Join-Path $PSScriptRoot "lambda_package.zip"

# Ensure build directory exists fresh
if (Test-Path $BuildDir) {
    Remove-Item -Recurse -Force $BuildDir
}
New-Item -ItemType Directory -Path $BuildDir | Out-Null

# Copy source code
Copy-Item -Recurse -Force "$PSScriptRoot\*" $BuildDir

# Install dependencies into build folder
pip install -r "$PSScriptRoot\requirements.txt" -t $BuildDir

# Create zip
Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::CreateFromDirectory($BuildDir, $ZipFile)
