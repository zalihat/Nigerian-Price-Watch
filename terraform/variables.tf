variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "eu-west-1"
}

variable "s3_bucket_name" {
  description = "S3 bucket name for storing ingested and processed data"
  type        = string
  default     = "nigeria-food-prices-bucket110112211"
}

variable "lambda_function_name" {
  description = "Lambda function name"
  type        = string
  default     = "ingest_data_lambda"
}

variable "lambda_runtime" {
  description = "Lambda runtime"
  type        = string
  default     = "python3.11"
}

variable "lambda_handler" {
  description = "Lambda handler (file.function)"
  type        = string
  default     = "lambda_function.lambda_handler"
}

variable "glue_job_name" {
  description = "Glue job name"
  type        = string
  default     = "clean_data_job"
}

variable "glue_script_key" {
  description = "Path (key) in S3 where Glue script will be uploaded"
  type        = string
  default     = "scripts/clean_data.py"
}

variable "glue_script_source" {
  description = "Local path to Glue script"
  type        = string
  default     = "../../scripts/clean_data.py"
}
