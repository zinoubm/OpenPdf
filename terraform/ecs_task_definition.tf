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
      environment = [
                    # backend
                    {
                      name  = "ENVIRONMENT"
                      value = var.ENVIRONMENT
                    },
                    {
                      name  = "PROJECT_NAME"
                      value = var.PROJECT_NAME
                    },
                    {
                      name  = "SERVER_HOST"
                      value = var.SERVER_HOST
                    },
                    {
                      name  = "DOMAIN"
                      value = var.DOMAIN
                    },
                    {
                      name  = "BACKEND_CORS_ORIGINS"
                      value = var.BACKEND_CORS_ORIGINS
                    },
                    {
                      name  = "FIRST_SUPERUSER"
                      value = var.FIRST_SUPERUSER
                    },
                    {
                      name  = "FIRST_SUPERUSER_PASSWORD"
                      value = var.FIRST_SUPERUSER_PASSWORD
                    },
                    {
                      name  = "EMAILS_FROM_EMAIL"
                      value = var.EMAILS_FROM_EMAIL
                    },
                    {
                      name  = "USERS_OPEN_REGISTRATION"
                      value = var.USERS_OPEN_REGISTRATION
                    },
                    {
                      name  = "SECRET_KEY"
                      value = var.SECRET_KEY
                    },

                    # postgres
                    {
                      name  = "POSTGRES_DB"
                      value = var.POSTGRES_DB
                    },
                    {
                      name  = "POSTGRES_PASSWORD"
                      value = var.POSTGRES_PASSWORD
                    },
                    {
                      name  = "POSTGRES_USER"
                      value = var.POSTGRES_USER
                    },
                    {
                      name  = "POSTGRES_SERVER"
                      value = aws_db_instance.openpdfai_db.endpoint
                    },

                    # google
                    {
                      name  = "GOOGLE_CLIENT_ID"
                      value = var.GOOGLE_CLIENT_ID
                    },

                    # aws
                    {
                      name  = "ACCESS_KEY_ID"
                      value = var.ACCESS_KEY_ID
                    },
                    {
                      name  = "SECRET_ACCESS_KEY"
                      value = var.SECRET_ACCESS_KEY
                    },
                    {
                      name  = "AWS_BUCKET_NAME"
                      value = var.AWS_BUCKET_NAME
                    },
                    {
                      name  = "AWS_REGION"
                      value = var.AWS_REGION
                    },

                    # openai
                    {
                      name  = "OPENAI_API_KEY"
                      value = var.OPENAI_API_KEY
                    },
                    {
                      name  = "OPENAI_ORGANIZATION"
                      value = var.OPENAI_ORGANIZATION
                    },
                    
                    # qdrant
                    {
                      name  = "COLLECTION_NAME"
                      value = var.COLLECTION_NAME
                    },
                    {
                      name  = "COLLECTION_SIZE"
                      value = var.COLLECTION_SIZE
                    },
                    {
                      name  = "QDRANT_API_KEY"
                      value = var.QDRANT_API_KEY
                    },
                    {
                      name  = "QDRANT_HOST"
                      value = var.QDRANT_HOST
                    },
                    {
                      name  = "QDRANT_PORT"
                      value = var.QDRANT_PORT
                    },
                    {
                      name  = "QDRANT_URL"
                      value = var.QDRANT_URL
                    },

                    # smtp
                    {
                      name  = "MAILTRAP_API_KEY"
                      value = var.MAILTRAP_API_KEY
                    },
                    {
                      name  = "SMTP_HOST"
                      value = var.SMTP_HOST
                    },
                    {
                      name  = "SMTP_PASSWORD"
                      value = var.SMTP_PASSWORD
                    },
                    {
                      name  = "SMTP_PORT"
                      value = var.SMTP_PORT
                    },
                    {
                      name  = "SMTP_TLS"
                      value = var.SMTP_TLS
                    },
                    {
                      name  = "SMTP_USER"
                      value = var.SMTP_USER
                    },

                    # stripe
                    {
                      name  = "STRIPE_ENDPOINT_SECRET"
                      value = var.STRIPE_ENDPOINT_SECRET
                    },
                    {
                      name  = "STRIPE_PUBLISHABLE_KEY"
                      value = var.STRIPE_PUBLISHABLE_KEY
                    },
                    {
                      name  = "STRIPE_SECRET_KEY"
                      value = var.STRIPE_SECRET_KEY
                    },
                    # services secrets
                    {
                      name  = "CRON_JOB_SECRET_KEY"
                      value = var.CRON_JOB_SECRET_KEY
                    },
                    {
                      name  = "DOCUMENT_PORECESSOR_SECRETE_KEY"
                      value = var.CRON_JOB_SECRET_KEY
                    },
                    # batch
                    {
                      name  = "AWS_BATCH_JOB_QUEUE_ARN"
                      value = aws_batch_job_queue.batch.arn
                    },
                    {
                      name  = "AWS_BATCH_JOB_DEFINITION_ARN"
                      value = aws_batch_job_definition.batch.arn
                    },
                    ]


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















# {
#   name  = "BACKEND_CORS_ORIGINS"
#   value = jsonencode([
#     "http://localhost",
#     "http://localhost:3000",
#     "https://localhost",
#     "https://localhost:3000",
#     "https://openpdf.vercel.app",
#     "https://www.openpdfai.com"
#   ])
# },