resource "aws_db_subnet_group" "rds_postgres_subnet_group" {
  name = "openpdfai-db-subnet-group"
  subnet_ids = aws_subnet.private[*].id

  tags = {
    Name     = "${var.namespace}_rds_postgres_subnet_group_${var.environment}"

  }
}

resource "aws_db_instance" "openpdfai_db" {
  allocated_storage = 10
  db_name = var.env_vars["POSTGRES_DB"]
  storage_type = "gp2"
  engine = "postgres"
  instance_class = "db.t3.micro"
  identifier = "openpdfai-db"
  username = var.env_vars["POSTGRES_USER"]
  password = var.env_vars["POSTGRES_PASSWORD"]

  vpc_security_group_ids = [aws_security_group.rds_postgres.id]
  db_subnet_group_name = aws_db_subnet_group.rds_postgres_subnet_group.name

  skip_final_snapshot = true
}