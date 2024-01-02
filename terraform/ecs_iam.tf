data "aws_iam_policy_document" "task_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_role_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role" "ecs_task_execution_role" {
  name               = "${var.namespace}_ecs_execution_role_${var.environment}"
  assume_role_policy = data.aws_iam_policy_document.task_assume_role_policy.json
}

resource "aws_iam_role" "ecs_task_iam_role" {
  name               = "${var.namespace}_ecs_task_iam_role_${var.environment}"
  assume_role_policy = data.aws_iam_policy_document.task_assume_role_policy.json
}

############

data "aws_iam_policy_document" "batch_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["batch.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "aws_batch_service_role" {
  name = "${var.namespace}_batch_service_role_${var.environment}"
  assume_role_policy = data.aws_iam_policy_document.batch_assume_role_policy.json
}

resource "aws_iam_role_policy_attachment" "aws_batch_service_role" {
  role       = aws_iam_role.aws_batch_service_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSBatchServiceRole"
}
