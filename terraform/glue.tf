# ------------------------------
# Glue Job: Python Shell
# ------------------------------

# Upload clean_data.py script to S3
resource "aws_s3_object" "clean_data_script" {
  bucket = aws_s3_bucket.data_bucket.bucket
  key    = "scripts/clean_data.py"
  source = "../scripts/clean_data.py"
}

# IAM Role for Glue Job
resource "aws_iam_role" "glue_role" {
  name = "glue-etl-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = { Service = "glue.amazonaws.com" },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

# Attach Glue service and S3 access policies
resource "aws_iam_role_policy_attachment" "glue_service_policy" {
  role       = aws_iam_role.glue_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

resource "aws_iam_role_policy_attachment" "glue_s3_access" {
  role       = aws_iam_role.glue_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_glue_job" "clean_data_shell" {
  name     = "clean_data_job_shell"
  role_arn = aws_iam_role.glue_role.arn

  command {
    name            = "pythonshell"
    python_version  = "3"
    script_location = "s3://${aws_s3_object.clean_data_script.bucket}/${aws_s3_object.clean_data_script.key}"
  }

  default_arguments = {
    "--TempDir" = "s3://${aws_s3_object.clean_data_script.bucket}/tmp/"
  }

  # For Python Shell jobs, only max_capacity is supported
  max_capacity = 1

  depends_on = [aws_s3_object.clean_data_script]
}
