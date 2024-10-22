# service variables
variable "namespace" {
  description = "Namespace for resource names"
  default     = "openpdfai"
  type        = string
}

variable "domain_name" {
  description = "Api domain name"
  default = "api.openpdfai.com"
  type        = string
}

variable "service_name" {
  description = "A Docker image-compatible name for the service"
  type        = string
}

variable "environment" {
  description = "Environment for deployment (like dev or staging)"
  default     = "production"
  type        = string
}

variable "cpu_units" {
  description = "Amount of CPU units for a single ECS task"
  default     = 512
  type        = number
}

variable "memory" {
  description = "Amount of memory in MB for a single ECS task"
  default     = 2048 
  type        = number
}

# aws credentials
variable "aws_access_key_id" {
  description = "AWS console access key"
  type        = string
}

variable "aws_secret_access_key" {
  description = "AWS console secret access key"
  type        = string
}

variable "region" {
  description = "AWS region"
  default     = "eu-central-1"
  type        = string
}

# network variables
variable "tld_zone_id" {
  description = "Top level domain hosted zone ID"
  type        = string
}

variable "vpc_cidr_block" {
  description = "CIDR block for the VPC network"
  default     = "10.1.0.0/16"
  type        = string
}

variable "az_count" {
  description = "Describes how many availability zones are used"
  default     = 2
  type        = number
}

# ecs variables
variable "ecs_task_desired_count" {
  description = "How many ECS tasks should run in parallel"
  default     = 1
  type        = number
}

variable "ecs_task_min_count" {
  description = "How many ECS tasks should minimally run in parallel"
  default     = 1
  type        = number
}

variable "ecs_task_max_count" {
  description = "How many ECS tasks should maximally run in parallel"
  default     = 3
  type        = number
}

variable "ecs_task_deployment_minimum_healthy_percent" {
  description = "How many percent of a service must be running to still execute a safe deployment"
  default     = 50
  type        = number
}

variable "ecs_task_deployment_maximum_percent" {
  description = "How many additional tasks are allowed to run (in percent) while a deployment is executed"
  default     = 100
  type        = number
}

variable "container_port" {
  description = "Port of the container"
  type        = number
  default     = 8000
}

# ecr
variable "ecr_force_delete" {
  description = "Forces deletion of Docker images before resource is destroyed"
  default     = true
  type        = bool
}

variable "hash" {
  description = "Task hash that simulates a unique version for every new deployment of the ECS Task"
  type        = string
}

# alb
variable "healthcheck_endpoint" {
  description = "Endpoint for ALB healthcheck"
  type        = string
  default     = "/api/v1/users/sanity"
}

variable "healthcheck_matcher" {
  description = "HTTP status code matcher for healthcheck"
  type        = string
  default     = "200"
}

# cloudfront
variable "retention_in_days" {
  description = "Retention period for Cloudwatch logs"
  default     = 7
  type        = number
}

# service level
# backend
variable "ENVIRONMENT" {}
variable "PROJECT_NAME" {}
variable "SERVER_HOST" {}
variable "DOMAIN" {}
variable "BACKEND_CORS_ORIGINS" {}
variable "FIRST_SUPERUSER" {}
variable "FIRST_SUPERUSER_PASSWORD" {}
variable "EMAILS_FROM_EMAIL" {}
variable "USERS_OPEN_REGISTRATION" {}
variable "SECRET_KEY" {}

# postgres
variable "POSTGRES_DB" {}
variable "POSTGRES_PASSWORD" {}
variable "POSTGRES_USER" {}

# google
variable "GOOGLE_CLIENT_ID" {}

# aws
variable "ACCESS_KEY_ID" {}
variable "SECRET_ACCESS_KEY" {}
variable "AWS_BUCKET_NAME" {}
variable "AWS_REGION" {}

# openai
variable "OPENAI_API_KEY" {}
variable "OPENAI_ORGANIZATION" {}

# qdrant
variable "COLLECTION_NAME" {}
variable "COLLECTION_SIZE" {}
variable "QDRANT_API_KEY" {}
variable "QDRANT_HOST" {}
variable "QDRANT_PORT" {}
variable "QDRANT_URL" {}

# smtp
variable "MAILTRAP_API_KEY" {}
variable "SMTP_HOST" {}
variable "SMTP_PASSWORD" {}
variable "SMTP_PORT" {}
variable "SMTP_TLS" {}
variable "SMTP_USER" {}

# stripe
variable "STRIPE_ENDPOINT_SECRET" {}
variable "STRIPE_PUBLISHABLE_KEY" {}
variable "STRIPE_SECRET_KEY" {}

# cron-job
variable "CRON_JOB_SECRET_KEY" {}
variable "DOCUMENT_PORECESSOR_SECRETE_KEY" {}