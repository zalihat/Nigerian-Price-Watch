# provider "aws" {
#   region = "eu-west-1"
# }

# resource "aws_s3_bucket" "example" {
#   bucket = "nigeria-food-prices0001"
#   tags = {
#     Project = "Test"
#   }
#   force_destroy = true
# }

terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "6.9.0"
    }
  }
}


provider "aws" {
  region = "eu-west-1" # change if needed
}

# ------------------------------
# S3 bucket for your ingested data
# ------------------------------
resource "aws_s3_bucket" "data_bucket" {
  bucket = "nigeria-food-prices-bucket110112211" # must be globally unique; change if needed
   lifecycle {
    prevent_destroy = true
  }
}

# ------------------------------
# IAM role for Lambda
# ------------------------------
data "aws_iam_policy_document" "assume_lambda" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "lambda_role" {
  name               = "ingest_lambda_role"
  assume_role_policy = data.aws_iam_policy_document.assume_lambda.json
}

# Basic execution for logs
resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# S3 access for this bucket
resource "aws_iam_role_policy" "lambda_s3" {
  name = "lambda_s3_access"
  role = aws_iam_role.lambda_role.id
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect   = "Allow",
      Action   = ["s3:PutObject", "s3:GetObject", "s3:ListBucket"],
      Resource = [
        aws_s3_bucket.data_bucket.arn,
        "${aws_s3_bucket.data_bucket.arn}/*"
      ]
    }]
  })
}

# ------------------------------
# Build Lambda package (Windows/PowerShell)
# ------------------------------
# This installs deps into a build folder, copies your lambda/ code, then we zip it.
resource "null_resource" "build_lambda" {
  provisioner "local-exec" {
    interpreter = ["PowerShell", "-Command"]
    command = <<EOT
      Remove-Item -Recurse -Force "${path.module}\build" -ErrorAction SilentlyContinue
      New-Item -ItemType Directory -Path "${path.module}\build" | Out-Null
      Copy-Item -Recurse -Force "${path.module}\..\lambda\*" "${path.module}\build\"
      python -m pip install -r "${path.module}\..\lambda\requirements.txt" -t "${path.module}\build" | Write-Output
    EOT
  }

  # Rebuild when requirements or code changes (timestamp ensures rebuild each apply)
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
# Lambda function
# ------------------------------
resource "aws_lambda_function" "ingest" {
  function_name = "ingest_data_lambda"
  role          = aws_iam_role.lambda_role.arn
  runtime       = "python3.11"
  handler       = "lambda_function.lambda_handler"  # file: lambda_function.py, function: lambda_handler

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

# ------------------------------
# Outputs
# ------------------------------
output "s3_bucket_name" {
  value = aws_s3_bucket.data_bucket.bucket
}

output "lambda_function_name" {
  value = aws_lambda_function.ingest.function_name
}
