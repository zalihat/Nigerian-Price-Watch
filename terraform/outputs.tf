output "s3_bucket_name" {
  description = "S3 bucket name used for ingestion and Glue scripts"
  value       = aws_s3_bucket.data_bucket.bucket
}

output "lambda_function_name" {
  description = "Lambda function name"
  value       = aws_lambda_function.ingest.function_name
}

output "glue_job_name" {
  description = "Glue job name"
  value       = aws_glue_job.clean_data_shell.name
}
