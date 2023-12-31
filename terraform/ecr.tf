resource "aws_ecr_repository" "ecr" {
  name  = "${lower(var.namespace)}/${var.service_name}"
  force_delete = var.ecr_force_delete

  image_scanning_configuration {
    scan_on_push = true
  }
}

output "ecr_repository_url" {
  value = aws_ecr_repository.ecr.repository_url
}

resource "aws_ecr_repository" "queue" {
  name  = "${lower(var.namespace)}/queue"
  force_delete = var.ecr_force_delete

  image_scanning_configuration {
    scan_on_push = true
  }
}

output "queue_repository_url" {
  value = aws_ecr_repository.queue.repository_url
}