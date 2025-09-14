#!/bin/bash
set -euo pipefail

# Always run from the script's directory
cd "$(dirname "$0")"

# Get repository URL from Terraform output
RepoUrl=$(terraform -chdir="../infrastructure/services/ecr" output -raw repository_url)

echo "✅ Using ECR repo: $RepoUrl"

# Define image name and tag
ImageName="clean-food-price-data"
Tag=${1:-latest}   # pass version like ./build_and_push.sh v1.0.0

echo "🚀 Building Docker image: $ImageName:$Tag"

# Build the Docker image
docker build -t "$ImageName:$Tag" .

# Full image name for ECR
FullImageName="$RepoUrl:$Tag"

# Tag the image for ECR
docker tag "$ImageName:$Tag" "$FullImageName"

# Authenticate Docker to ECR
aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin "${RepoUrl%/*}"

# Push the image to ECR
docker push "$FullImageName"

echo "🎉 Successfully pushed $FullImageName"
