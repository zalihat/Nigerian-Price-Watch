output "lambda_function_name" {
  description = "The name of the Lambda function"
  value       = module.lambda_ingest.lambda_function_name
}

output "lambda_role_arn" {
  description = "The ARN of the IAM role associated with the Lambda"
  value       = module.lambda_ingest.lambda_role_arn
}

output "lambda_function_arn" {
  description = "The ARN of the Lambda function"
  value       = module.lambda_ingest.lambda_function_arn
}