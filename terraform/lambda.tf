# ------------------------------
# Build Lambda package (Windows/PowerShell)
# ------------------------------
resource "null_resource" "build_lambda" {
  provisioner "local-exec" {
    interpreter = ["PowerShell", "-Command"]
    command     = <<EOT
      Remove-Item -Recurse -Force "${path.module}\build" -ErrorAction SilentlyContinue
      New-Item -ItemType Directory -Path "${path.module}\build" | Out-Null
      Copy-Item -Recurse -Force "${path.module}\..\lambda\*" "${path.module}\build\"
      python -m pip install -r "${path.module}\..\lambda\requirements.txt" -t "${path.module}\build" | Write-Output
    EOT
  }

  triggers = {
    ts       = timestamp()
    req_hash = filesha256("${path.module}/../lambda/requirements.txt")
  }
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/build"
  output_path = "${path.module}/lambda_package.zip"

  depends_on = [null_resource.build_lambda]
}

# ------------------------------
# Lambda Function
# ------------------------------
resource "aws_lambda_function" "ingest" {
  function_name = var.lambda_function_name
  role          = aws_iam_role.lambda_role.arn
  runtime       = var.lambda_runtime
  handler       = var.lambda_handler

  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  timeout = 900

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
