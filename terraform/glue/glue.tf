provider "aws" {
  region = "us-east-1" # change to your AWS region
}

# IAM Role for Glue Job
resource "aws_iam_role" "glue_role" {
  name = "glue-etl-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "glue.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

# Attach necessary policies
resource "aws_iam_role_policy_attachment" "glue_service_policy" {
  role       = aws_iam_role.glue_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

resource "aws_iam_role_policy_attachment" "glue_s3_access" {
  role       = aws_iam_role.glue_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

# Glue Job
resource "aws_glue_job" "clean_data" {
  name     = "clean_data_job"
  role_arn = aws_iam_role.glue_role.arn

  command {
    name            = "glueetl"
    python_version  = "3"
    script_location = "s3://nigeria-food-prices-bucket110112211/scripts/clean_data.py"
  }

  default_arguments = {
    "--TempDir"             = "s3://nigeria-food-prices-bucket110112211/tmp/"
    "--job-language"        = "python"
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-metrics"      = ""
  }

  max_retries  = 0
  glue_version = "3.0"
  number_of_workers = 2
  worker_type       = "Standard"
}
