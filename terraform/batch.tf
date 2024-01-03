resource "aws_batch_compute_environment" "batch" {
  compute_environment_name = "${var.namespace}_batch_compute_environment_${var.environment}"
  
  compute_resources {
    max_vcpus = 256
    security_group_ids = [
      aws_security_group.batch.id,
    ]
    subnets = aws_subnet.public.*.id
    type = "FARGATE"
  }
  service_role = aws_iam_role.aws_batch_service_role.arn
  type         = "MANAGED"
  depends_on = [
    aws_iam_role_policy_attachment.aws_batch_service_role
  ]
}

resource "aws_batch_job_queue" "batch" {
  name     = "${var.namespace}_batch_job_queue_${var.environment}"
  state    = "ENABLED"
  priority = "0"
  compute_environments = [
    aws_batch_compute_environment.batch.arn,
  ]
}

resource "aws_batch_job_definition" "batch" {
  name = "${var.namespace}_batch_job_definition_${var.environment}"

  type = "container"
  platform_capabilities = [
    "FARGATE",
  ]
  container_properties = jsonencode({
    command = ["echo", "test"]
    image = "${aws_ecr_repository.queue.repository_url}:latest"

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
        }
      ]
    )
    
    fargatePlatformConfiguration = {
      platformVersion = "LATEST"
    }

    networkConfiguration = {
      assignPublicIp = "ENABLED"
    }

    resourceRequirements = [
      {
        type  = "VCPU"
        value = "0.25"
      },
      {
        type  = "MEMORY"
        value = "512"
      }
    ]

    executionRoleArn = aws_iam_role.ecs_task_execution_role.arn
  })
}

