# # Navigate to the folder containing ingestdata.py and utils.py

# Set-Location $PSScriptRoot
# python -c "
# import sys
# sys.path.insert(0, r'$PSScriptRoot')
# from utils import get_bucket_name
# bucket_name = get_bucket_name()
# file_path = 'test.py'
# with open(file_path, 'r') as f:
#     code = f.read()
# code = code.replace('REPLACE_BUCKET_NAME', bucket_name)
# with open(file_path, 'w') as f:
#     f.write(code)
# print(f'Inserted bucket name: {bucket_name} into {file_path}')
# "

# # Stop on error
# $ErrorActionPreference = "Stop"

# # --- 1. Get ECR Repo URL from Terraform ---
# $RepoUrl = $(terraform -chdir="../infrastructure/services/ecr" output -raw repository_url)
# $RepoUrl = $RepoUrl.Trim().Trim('"')

# if (-not $RepoUrl) {
#     Write-Error "❌ Could not retrieve ECR repository URL. Did you run 'terraform apply' inside infrastructure/services/ecr'?"
#     exit 1
# }

# Write-Host "DEBUG: RepoUrl = '$RepoUrl'"

# --- 2. Get S3 Bucket Name from Terraform ---
$BucketName = $(terraform -chdir="../infrastructure/services/s3" output -raw bucket_name)
$BucketName = $BucketName.Trim().Trim('"')

if (-not $BucketName) {
    Write-Error "❌ Could not retrieve S3 bucket name. Did you run 'terraform apply' inside infrastructure/services/s3'?"
    exit 1
}

Write-Host "DEBUG: BucketName = '$BucketName'"

# --- 3. Inject Bucket Name into clean.py ---
python -c "
file_path = 'test.py'
bucket_name = '$BucketName'

with open(file_path, 'r') as f:
    code = f.read()

code = code.replace('REPLACE_BUCKET_NAME', bucket_name)

with open(file_path, 'w') as f:
    f.write(code)

print(f'✅ Inserted bucket name: {bucket_name} into {file_path}')
"




