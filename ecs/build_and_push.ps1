param (
    [string]$ServicePath = "ecs",
    [string]$Tag = "latest",
    [string]$Region = "eu-west-1",
    [string]$ImageName = "clean-food-price-data"
)

# Move into ECS folder (where Dockerfile lives)
Set-Location $PSScriptRoot

# Get repository URL from Terraform outputs
$RepoUrl = $(terraform -chdir="../infrastructure/services/ecr" output -raw repository_url)
$RepoUrl = $RepoUrl.Trim().Trim('"')

if (-not $RepoUrl) {
    Write-Error "❌ Could not retrieve ECR repository URL. Did you run 'terraform apply' inside infrastructure/services/ecr'?"
    exit 1
}

Write-Host "DEBUG: RepoUrl = '$RepoUrl'"

# Build image names explicitly (no inline : in vars)
$LocalImage = "$ImageName" + ":" + "$Tag"
$FullImageName = "$RepoUrl" + ":" + "$Tag"

Write-Host "🚀 Building Docker image: $FullImageName"

# Build the Docker image
docker build -t "$LocalImage" $ServicePath
if ($LASTEXITCODE -ne 0) { exit 1 }

# Tag the image for ECR
docker tag "$LocalImage" "$FullImageName"

# Authenticate Docker to ECR
Write-Host "🔑 Logging into ECR..."
$Registry = ($RepoUrl -split '/')[0]
aws ecr get-login-password --region $Region | docker login --username AWS --password-stdin $Registry
if ($LASTEXITCODE -ne 0) { exit 1 }

# Push the image
Write-Host "📦 Pushing image to ECR..."
docker push "$FullImageName"

Write-Host "✅ Image successfully pushed: $FullImageName"
