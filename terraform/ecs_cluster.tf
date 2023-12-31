resource "aws_ecs_cluster" "default" {
  name = "${var.namespace}_ecs_cluster_${var.environment}"

  tags = {
    Name     = "${var.namespace}_ecs_cluster_${var.environment}"
  }
}