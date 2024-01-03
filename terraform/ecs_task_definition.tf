resource "aws_ecs_task_definition" "default" {
  family                   = "${var.namespace}_ecs_task_definition_${var.environment}"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  cpu                      = var.cpu_units
  memory                   = var.memory
  
  container_definitions = jsonencode([
    {
      name         = var.service_name
      image        = "${aws_ecr_repository.ecr.repository_url}:latest"
      cpu          = var.cpu_units
      memory       = var.memory
      essential    = true
      environment = concat(
          [
            for key, value in var.env_vars : {
              name  = key
              value = value
            }
          ],
          [
            {
              name  = "BACKEND_CORS_ORIGINS"
              value = jsonencode([
                "http://localhost",
                "http://localhost:3000",
                "https://localhost",
                "https://localhost:3000",
                "https://openpdf.vercel.app",
                "https://www.openpdfai.com"
              ])
            },
            {
              name  = "AWS_BATCH_JOB_QUEUE_ARN"
              value = aws_batch_job_queue.batch.arn
            },
            {
              name  = "AWS_BATCH_JOB_DEFINITION_ARN"
              value = aws_batch_job_definition.batch.arn
            }
          ]
        )
        
      portMappings = [
        {
          containerPort = var.container_port
          hostPort      = var.container_port
          protocol      = "tcp"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options   = {
          "awslogs-group"         = aws_cloudwatch_log_group.log_group.name
          "awslogs-region"        = var.region
          "awslogs-stream-prefix" = "${var.service_name}-log-stream-${var.environment}"
        }
      }
    }
  ])
}