variable "region" {
  description = "AWS region"
  type        = string
}

variable "cluster_name" {
  description = "Name of ECS cluster"
  type        = string
}

variable "service_name" {
  description = "Name of ECS service"
  type        = string
}

variable "container_name" {
  description = "Name of container"
  type        = string
}

variable "container_port" {
  description = "Port the container listens on"
  type        = number
}

variable "cpu" {
  description = "CPU units for task"
  type        = number
  default     = 256
}

variable "memory" {
  description = "Memory (MB) for task"
  type        = number
  default     = 512
}

# variable "desired_count" {
#   description = "How many tasks to run"
#   type        = number
#   default     = 1
# }

variable "image_url" {
  description = "ECR image URL"
  type        = string
}
