resource "aws_db_subnet_group" "rds_postgres_subnet_group" {
  name = "openpdfai-db-subnet-group"
  subnet_ids = aws_subnet.private[*].id

  tags = {
    Name     = "${var.namespace}_rds_postgres_subnet_group_${var.environment}"
  }
}

resource "aws_db_instance" "openpdfai_db" {
  allocated_storage = 10
  db_name = var.POSTGRES_DB
  storage_type = "gp2"
  engine = "postgres"
  instance_class = "db.t3.micro"
  identifier = "openpdfai-db"
  username = var.POSTGRES_USER
  password = var.POSTGRES_PASSWORD

  publicly_accessible = true

  vpc_security_group_ids = [aws_security_group.rds_postgres.id]
  db_subnet_group_name = aws_db_subnet_group.rds_postgres_subnet_group.name

  backup_retention_period = 7 # Number of days to retain automated backups
  backup_window = "03:00-04:00" # Preferred UTC backup window (hh24:mi-hh24:mi format)
  maintenance_window = "mon:04:00-mon:04:30" # Preferred UTC maintenance window

  # enable backup
  skip_final_snapshot = false
  final_snapshot_identifier = "db-snap"
}