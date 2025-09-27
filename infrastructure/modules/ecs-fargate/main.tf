# ------------------------------
# Networking
# ------------------------------
resource "aws_vpc" "this" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = { Name = "${var.service_name}-vpc" }
}

resource "aws_internet_gateway" "this" {
  vpc_id = aws_vpc.this.id
  tags   = { Name = "${var.service_name}-igw" }
}

resource "aws_subnet" "public_a" {
  vpc_id                  = aws_vpc.this.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "${var.region}a"
  map_public_ip_on_launch = true

  tags = { Name = "${var.service_name}-subnet-a" }
}

resource "aws_subnet" "public_b" {
  vpc_id                  = aws_vpc.this.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "${var.region}b"
  map_public_ip_on_launch = true

  tags = { Name = "${var.service_name}-subnet-b" }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.this.id
  tags   = { Name = "${var.service_name}-public-rt" }
}

resource "aws_route" "internet" {
  route_table_id         = aws_route_table.public.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.this.id
}

resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.public_a.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "b" {
  subnet_id      = aws_subnet.public_b.id
  route_table_id = aws_route_table.public.id
}

resource "aws_security_group" "ecs" {
  name        = "${var.service_name}-sg"
  description = "Allow inbound traffic to ECS tasks"
  vpc_id      = aws_vpc.this.id

  ingress {
    from_port   = var.container_port
    to_port     = var.container_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Name = "${var.service_name}-sg" }
}

# ------------------------------
# ECS Cluster + IAM
# ------------------------------
resource "aws_ecs_cluster" "this" {
  name = var.cluster_name
}

resource "aws_iam_role" "ecs_task_exec" {
  name = "${var.service_name}-task-exec-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = { Service = "ecs-tasks.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_task_exec_policy" {
  role       = aws_iam_role.ecs_task_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# -----------------------------------------
# ECS Task Role (for container permissions)
# -------------------------------------------
resource "aws_iam_role" "ecs_task_role" {
  name = "${var.service_name}-task-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = { Service = "ecs-tasks.amazonaws.com" }
        Action   = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_task_s3_policy" {
  role       = aws_iam_role.ecs_task_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess" # or a restrictive custom policy
}


# ------------------------------
# ECS Task Definition
# ------------------------------
resource "aws_ecs_task_definition" "this" {
  family                   = var.service_name
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = var.cpu
  memory                   = var.memory
  execution_role_arn       = aws_iam_role.ecs_task_exec.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn 

  container_definitions = jsonencode([
    {
      name      = var.container_name
      image     = var.image_url
      essential = true
      portMappings = [
        {
          containerPort = var.container_port
          hostPort      = var.container_port
        }
      ]
         logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.ecs.name
          awslogs-region        = var.region
          awslogs-stream-prefix = var.container_name
        }
      }
    }
  ])
}


resource "aws_cloudwatch_log_group" "ecs" {
  name              = "/ecs/${var.service_name}"
  retention_in_days = 7
}


# ------------------------------
# ECS Service
# ------------------------------
# resource "aws_ecs_service" "this" {
#   name            = var.service_name
#   cluster         = aws_ecs_cluster.this.id
#   task_definition = aws_ecs_task_definition.this.arn
#   desired_count   = var.desired_count
#   launch_type     = "FARGATE"

#   network_configuration {
#     subnets          = [aws_subnet.public_a.id, aws_subnet.public_b.id]
#     security_groups  = [aws_security_group.ecs.id]
#     assign_public_ip = true
#   }

#   depends_on = [
#     aws_iam_role_policy_attachment.ecs_task_exec_policy,
#     aws_route.internet
#   ]
# }

# resource "aws_ecs_run_task" "one_off" {
#   cluster         = aws_ecs_cluster.this.id
#   task_definition = aws_ecs_task_definition.this.arn
#   launch_type     = "FARGATE"

#   network_configuration {
#     subnets          = [aws_subnet.public_a.id, aws_subnet.public_b.id]
#     security_groups  = [aws_security_group.ecs.id]
#     assign_public_ip = true
#   }
#     wait_for_completion = true
#     depends_on = [
#     aws_iam_role_policy_attachment.ecs_task_exec_policy,
#     aws_iam_role_policy_attachment.ecs_task_s3_policy,
#     aws_route.internet
#   ]
# }

