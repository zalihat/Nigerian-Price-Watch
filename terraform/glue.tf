# ------------------------------
# Glue Job
# ------------------------------
resource "aws_glue_job" "clean_data" {
  depends_on = [aws_s3_object.clean_data_script]

  name     = var.glue_job_name
  role_arn = aws_iam_role.glue_role.arn

  command {
    name            = "glueetl"
    python_version  = "3"
    script_location = "s3://${aws_s3_object.clean_data_script.bucket}/${aws_s3_object.clean_data_script.key}"
  }

  default_arguments = {
    "--TempDir"                          = "s3://${aws_s3_bucket.data_bucket.bucket}/tmp/"
    "--job-language"                     = "python"
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-metrics"                   = ""
  }

  max_retries       = 0
  glue_version      = "3.0"
  number_of_workers = 2
  worker_type       = "Standard"
}
