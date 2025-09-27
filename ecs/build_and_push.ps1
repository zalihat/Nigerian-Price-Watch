
param (
    [string]$ServicePath = "ecs",
    [string]$Tag = "latest",
    [string]$Region = "eu-west-1",
    [string]$ImageName = "clean-food-price-data"
)

# Move into ECS folder (where Dockerfile lives)
Set-Location $PSScriptRoot
$BucketName = $(terraform -chdir="../infrastructure/services/s3" output -raw bucket_name)
$BucketName = $BucketName.Trim().Trim('"')

if (-not $BucketName) {
    Write-Error "Could not retrieve S3 bucket name. Did you run 'terraform apply' inside infrastructure/services/s3'?"
    exit 1
}

Write-Host "DEBUG: BucketName = '$BucketName'"

# --- 3. Inject Bucket Name into clean.py ---
python -c "
import os, shutil

file_path = 'clean_data.py'
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



# Get repository URL from Terraform outputs
$RepoUrl = $(terraform -chdir="../infrastructure/services/ecr" output -raw repository_url)
$RepoUrl = $RepoUrl.Trim().Trim('"')

if (-not $RepoUrl) {
    Write-Error "Could not retrieve ECR repository URL. Did you run 'terraform apply' inside infrastructure/services/ecr'?"
    exit 1
}

Write-Host "DEBUG: RepoUrl = '$RepoUrl'"

# Build image names explicitly (no inline : in vars)
$LocalImage = "$ImageName" + ":" + "$Tag"
$FullImageName = "$RepoUrl" + ":" + "$Tag"

Write-Host "🚀 Building Docker image: $FullImageName"

# Build the Docker image
docker build -t "$LocalImage" .
if ($LASTEXITCODE -ne 0) { exit 1 }

# Tag the image for ECR
docker tag "$LocalImage" "$FullImageName"

# Authenticate Docker to ECR
# Write-Host "Logging into ECR..."
# $Registry = ($RepoUrl -split '/')[0]
# aws ecr get-login-password --region $Region | docker login --username AWS --password-stdin $Registry
# if ($LASTEXITCODE -ne 0) { exit 1 }
# Define the ECR repository URL and the AWS region.
# It's good practice to define these variables at the top of the script.
# $RepoUrl = "[554074174252.dkr.ecr.eu-west-1.amazonaws.com/your-repo-name](https://554074174252.dkr.ecr.eu-west-1.amazonaws.com/your-repo-name)"
# $Region = "eu-west-1"

# --- ECR Login Section ---
# Write-Host "Logging into ECR in region: $Region..."

# Extract the registry URL from the full repository URL.
# $Registry = ($RepoUrl -split '/')[0]

# Check if the AWS CLI is installed and configured.
# if (-not (Get-Command aws -ErrorAction SilentlyContinue)) {
#     Write-Error "AWS CLI not found. Please install and configure it."
#     exit 1
# }

# # Use the AWS CLI to get a temporary password and pipe it to docker login.
# # The --password-stdin flag is crucial for security as it prevents the password
# # from being exposed in process listings.
# aws ecr get-login-password --region $Region | docker login --username AWS --password-stdin $Registry

# # Check the exit code of the last command to see if it was successful.
# if ($LASTEXITCODE -ne 0) {
#     Write-Error "Failed to log in to ECR. Please check your AWS credentials and IAM permissions."
#     exit 1
# }
# --- Authenticate Docker to ECR robustly ---
Write-Host " Logging into ECR..."

try {
    # Use AWS CLI to get password
    $loginPassword = aws ecr get-login-password --region $Region 2>&1

    if ($loginPassword -match "error|cannot|fail") {
        Write-Error "Failed to get ECR login password: $loginPassword"
        exit 1
    }

    # Pipe into Docker login using cmd.exe to avoid PowerShell pipe quirks
    $loginCommand = "echo $loginPassword | docker login --username AWS --password-stdin $($RepoUrl.Split('/')[0])"
    cmd.exe /c $loginCommand
    if ($LASTEXITCODE -ne 0) { 
        Write-Error "Docker login failed"
        exit 1
    }

    Write-Host "Logged in to ECR successfully."
}
catch {
    Write-Error "Unexpected error during ECR login: $_"
    exit 1
}

Write-Host "Successfully logged in to ECR."
# Now you can add your `docker build` and `docker push` commands.

# Push the image
Write-Host "Pushing image to ECR..."
docker push "$FullImageName"

Write-Host "Image successfully pushed: $FullImageName"