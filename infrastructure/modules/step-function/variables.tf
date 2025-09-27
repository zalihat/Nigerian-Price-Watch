variable "state_machine_name" {
  type        = string
  description = "Name of the Step Function state machine"
}

variable "lambda_function_arn" {
  type        = string
  description = "ARN of the Lambda function to invoke"
}

variable "ecs_cluster_arn" {
  type        = string
  description = "ARN of the ECS cluster"
}

variable "ecs_task_definition_arn" {
  type        = string
  description = "ARN of the ECS Fargate task definition"
}

variable "ecs_subnet_ids" {
  type        = list(string)
  description = "List of subnet IDs for ECS Fargate tasks"
}

variable "ecs_security_group_ids" {
  type        = list(string)
  description = "List of security group IDs for ECS Fargate tasks"
}

variable "glue_crawler_name" {
  type        = string
  description = "Name of the Glue crawler to start"
}
