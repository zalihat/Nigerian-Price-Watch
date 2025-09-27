variable "function_name" {
  description = "Name of the Lambda function"
  type        = string
}

variable "runtime" {
  description = "Lambda runtime (e.g. python3.9)"
  type        = string
  default     = "python3.9"
}

variable "handler" {
  description = "Lambda handler (e.g. app.lambda_handler)"
  type        = string
}

variable "package_file" {
  description = "Path to prebuilt Lambda deployment package zip"
  type        = string
}

variable "timeout" {
  description = "Lambda timeout in seconds"
  type        = number
  default     = 900
}

variable "s3_bucket_arn" {
  description = "ARN of the S3 bucket the Lambda needs access to"
  type        = string
}

variable "s3_bucket_name" {
  description = "Name of the S3 bucket the Lambda needs access to"
  type        = string
}
