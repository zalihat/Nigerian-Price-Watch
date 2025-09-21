output "cluster_id" {
  value = aws_ecs_cluster.this.id
}

# output "service_name" {
#   value = aws_ecs_service.this.name
# }

output "security_group_id" {
  value = aws_security_group.ecs.id
}

output "subnet_ids" {
  value = [aws_subnet.public_a.id, aws_subnet.public_b.id]
}

output "vpc_id" {
  value = aws_vpc.this.id
}

# output "ecs_task_arn" {
#   value = aws_ecs_task.this.arn
# }

# output "ecs_task_id" {
#   value = aws_ecs_task.this.id
# }
