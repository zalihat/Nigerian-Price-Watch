# ------------------------------
# Build Lambda package for clean_data
# ------------------------------
resource "null_resource" "build_lambda_clean" {
  provisioner "local-exec" {
    command     = <<EOT
      Remove-Item -Recurse -Force "${path.module}\build_clean" -ErrorAction SilentlyContinue
      New-Item -ItemType Directory -Path "${path.module}\build_clean" | Out-Null
      Copy-Item -Recurse -Force "${path.module}\..\lambda_clean\*" "${path.module}\build_clean\"
      python -m pip install -r "${path.module}\..\lambda_clean\requirements.txt" -t "${path.module}\build_clean" | Write-Output
    EOT
  }

  triggers = {
    ts       = timestamp()
    req_hash = filesha256("${path.module}/../lambda_clean/requirements.txt")
  }
}

data "archive_file" "lambda_clean_zip" {
  type        = "zip"
  source_dir  = "${path.module}/build_clean"
  output_path = "${path.module}/lambda_clean_package.zip"

  depends_on = [null_resource.build_lambda_clean]
}

# ------------------------------
# Lambda Function for clean_data
# ------------------------------
resource "aws_lambda_function" "clean_data" {
  function_name = "clean_data_lambda"
  role          = aws_iam_role.lambda_role.arn
  runtime       = "python3.9"
  handler       = "lambda_function.lambda_handler"

  filename         = data.archive_file.lambda_clean_zip.output_path
  source_code_hash = data.archive_file.lambda_clean_zip.output_base64sha256

  timeout = 900 # 15 minutes (max for Lambda)

  environment {
    variables = {
      S3_BUCKET = aws_s3_bucket.data_bucket.bucket
    }
  }

  depends_on = [
    aws_iam_role_policy_attachment.lambda_basic,
    aws_iam_role_policy.lambda_s3
  ]
}
