output "cluster_id" {
  value = module.ecs_fargate.cluster_id
}
output "cluster_arn" {
  value = module.ecs_fargate.cluster_arn
}


output "cluster_name" {
  value = module.ecs_fargate.cluster_name
}

output "task_definition_arn" {
  value = module.ecs_fargate.task_definition_arn
}

# output "service_name" {
#   value = aws_ecs_service.this.name
# }

output "security_group_id" {
  value = module.ecs_fargate.security_group_id
}

output "subnet_ids" {
  value = module.ecs_fargate.subnet_ids
}

output "vpc_id" {
  value = module.ecs_fargate.vpc_id
}

# output "ecs_task_arn" {
#   value = aws_ecs_task.this.arn
# }

# output "ecs_task_id" {
#   value = aws_ecs_task.this.id
# }
output "ecs_log_group_name" {
  value = module.ecs_fargate.ecs_log_group_name
}
