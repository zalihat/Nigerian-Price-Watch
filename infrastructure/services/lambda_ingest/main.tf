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

data "terraform_remote_state" "s3" {
  backend = "local"
  config = {
    path = "../s3/terraform.tfstate"
  }
}

module "lambda_ingest" {
  source = "../../modules/lambda"

  function_name   = "ingest_lambda_test"
  runtime         = "python3.13"
  handler         = "lambda_function.lambda_handler"

  package_file    = "${path.module}/../../../lambda/lambda_package.zip"

  # Use attributes of the existing bucket
  s3_bucket_name  = data.terraform_remote_state.s3.outputs.bucket_name
  s3_bucket_arn   = data.terraform_remote_state.s3.outputs.bucket_arn
  timeout         = 900
} 
