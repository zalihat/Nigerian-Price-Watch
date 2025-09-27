variable "project_name" {
  description = "Name of the project/pipeline"
  type        = string
}

variable "dashboard_name" {
  description = "Name of the CloudWatch dashboard"
  type        = string
  default     = "pipeline-dashboard"
}

variable "lambda_function_name" {
  description = "Lambda function name to monitor"
  type        = string
}

variable "ecs_cluster_name" {
  description = "ECS cluster name"
  type        = string
}

# variable "ecs_service_name" {
#   description = "ECS service name"
#   type        = string
# }

variable "step_function_arn" {
  description = "ARN of the Step Function state machine"
  type        = string
}

variable "glue_crawler_name" {
  description = "Glue crawler name"
  type        = string
}

variable "alert_email" {
  description = "Email address for alerts"
  type        = string
}
variable "ecs_log_group_name" {
  description = "CloudWatch Log Group name used by ECS tasks"
  type        = string
}
