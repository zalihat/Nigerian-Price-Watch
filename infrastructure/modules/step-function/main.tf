# IAM role for Step Functions execution
resource "aws_iam_role" "sfn_execution_role" {
  name = "${var.state_machine_name}-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = { Service = "states.amazonaws.com" },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

# IAM policy for Lambda, ECS, Glue
resource "aws_iam_policy" "sfn_policy" {
  name   = "${var.state_machine_name}-policy"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "lambda:InvokeFunction"
        ],
        Resource = var.lambda_function_arn
      },
      {
        Effect = "Allow",
        Action = [
          "ecs:RunTask",
          "ecs:DescribeTasks",
          "iam:PassRole"
        ],
        Resource = "*"
      },
      {
        Effect = "Allow",
        Action = [
          "glue:StartCrawler"
        ],
        Resource = "arn:aws:glue:*:*:crawler/${var.glue_crawler_name}"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "attach_sfn_policy" {
  role       = aws_iam_role.sfn_execution_role.name
  policy_arn = aws_iam_policy.sfn_policy.arn
}

# Step Function definition using variables
locals {
  state_machine_definition = jsonencode({
    Comment = "State machine orchestrating Lambda → ECS → Glue"
    StartAt = "Lambda Invoke"
    States = {
      "Lambda Invoke" = {
        Type      = "Task"
        Resource  = "arn:aws:states:::lambda:invoke"
        Output    = "{% $states.result.Payload %}"
        Arguments = {
          FunctionName = var.lambda_function_arn
          Payload      = "{% $states.input %}"
        }
        Retry = [
          {
            ErrorEquals     = [
              "Lambda.ServiceException",
              "Lambda.AWSLambdaException",
              "Lambda.SdkClientException",
              "Lambda.TooManyRequestsException"
            ]
            IntervalSeconds = 1
            MaxAttempts     = 3
            BackoffRate     = 2
            JitterStrategy  = "FULL"
          }
        ]
        Next = "ECS RunTask"
      },
      "ECS RunTask" = {
        Type      = "Task"
        Resource  = "arn:aws:states:::ecs:runTask"
        Arguments = {
          LaunchType       = "FARGATE"
          Cluster          = var.ecs_cluster_arn
          TaskDefinition   = var.ecs_task_definition_arn
          NetworkConfiguration = {
            AwsvpcConfiguration = {
              Subnets        = var.ecs_subnet_ids
              SecurityGroups = var.ecs_security_group_ids
              AssignPublicIp = "ENABLED"
            }
          }
        }
        Next = "StartCrawler"
      },
      "StartCrawler" = {
        Type      = "Task"
        Resource  = "arn:aws:states:::aws-sdk:glue:startCrawler"
        Arguments = {
          Name = var.glue_crawler_name
        }
        End = true
      }
    },
    QueryLanguage = "JSONata"
  })
}

resource "aws_sfn_state_machine" "this" {
  name     = var.state_machine_name
  role_arn = aws_iam_role.sfn_execution_role.arn
  definition = local.state_machine_definition
}
