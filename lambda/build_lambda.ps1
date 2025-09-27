$BuildDir = Join-Path $PSScriptRoot "build"
$ZipFile  = Join-Path $PSScriptRoot "lambda_package.zip"

# Ensure build directory exists fresh
if (Test-Path $BuildDir) {
    Remove-Item -Recurse -Force $BuildDir
}
New-Item -ItemType Directory -Path $BuildDir | Out-Null


$BucketName = $(terraform -chdir="../infrastructure/services/s3" output -raw bucket_name)
$BucketName = $BucketName.Trim().Trim('"')

if (-not $BucketName) {
    Write-Error "❌ Could not retrieve S3 bucket name. Did you run 'terraform apply' inside infrastructure/services/s3'?"
    exit 1
}

Write-Host "DEBUG: BucketName = '$BucketName'"

# --- 3. Inject Bucket Name into ingest_to_s3.py ---
python -c "
import os, shutil

file_path = 'ingest_to_s3.py'
tmp_path = file_path + '.tmp'
bucket_name = '$BucketName'

# Read file safely
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# Replace placeholder
code = code.replace('REPLACE_BUCKET_NAME', bucket_name)

# Write to temp file
with open(tmp_path, 'w', encoding='utf-8') as f:
    f.write(code)

# Replace original atomically
shutil.move(tmp_path, file_path)

print(f'Inserted bucket name: {bucket_name} into {file_path}')
"


# Copy source code
Copy-Item -Recurse -Force "$PSScriptRoot\*" $BuildDir
# Copy-Item -Recurse -Force "$PSScriptRoot\*" $BuildDir -Exclude "build"

# Install dependencies into build folder
pip install -r "$PSScriptRoot\requirements.txt" -t $BuildDir

# Create zip
Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::CreateFromDirectory($BuildDir, $ZipFile)
