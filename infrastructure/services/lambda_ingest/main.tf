terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "6.9.0"
    }
  }
}


provider "aws" {
  region = "eu-west-1"
}

# Reference an existing S3 bucket
data "aws_s3_bucket" "data" {
  bucket = "nigeria-food-prices-bucket110112211"
}

module "lambda_ingest" {
  source = "../../modules/lambda"

  function_name   = "ingest_lambda_test"
  runtime         = "python3.9"
  handler         = "app.lambda_handler"

  package_file    = "${path.module}/../../../lambda/lambda_package.zip"

  # Use attributes of the existing bucket
  s3_bucket_name  = data.aws_s3_bucket.data.bucket
  s3_bucket_arn   = data.aws_s3_bucket.data.arn

  timeout         = 900
}
