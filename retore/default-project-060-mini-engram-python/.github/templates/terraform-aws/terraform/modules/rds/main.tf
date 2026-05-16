# ============================================================
# modules/rds/main.tf — RDS PostgreSQL instance.
#
# Security defaults:
#   - publicly_accessible = false  (always — no exceptions)
#   - storage_encrypted = true
#   - Password via random_password + AWS SSM (never in tfvars)
#   - Ingress only from ECS security group
# ============================================================

resource "random_password" "db" {
  length           = 24
  special          = true
  override_special = "!#$%&*()-_=+[]{}:?"
}

# Store password in SSM Parameter Store (encrypted with KMS)
# Access via ECS task role with ssm:GetParameter on this ARN
resource "aws_ssm_parameter" "db_password" {
  name        = "/${var.project_name}/${var.env}/db/password"
  description = "Master password for ${var.project_name}-${var.env} RDS instance"
  type        = "SecureString"
  value       = random_password.db.result

  tags = {
    Name = "${var.project_name}-${var.env}-db-password"
  }
}

# ── Security Group ────────────────────────────────────────────────────────────

resource "aws_security_group" "rds" {
  name        = "${var.project_name}-${var.env}-rds-sg"
  description = "Allow PostgreSQL traffic only from ECS tasks security group"
  vpc_id      = var.vpc_id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = compact([var.ecs_security_group_id])
    description     = "PostgreSQL from ECS tasks only"
  }

  # No 0.0.0.0/0 egress for RDS — RDS initiates connections, not egress
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-${var.env}-rds-sg"
  }
}

# ── Subnet Group ─────────────────────────────────────────────────────────────

resource "aws_db_subnet_group" "this" {
  name        = "${var.project_name}-${var.env}-db-subnet-group"
  description = "Private subnets for ${var.project_name}-${var.env} RDS"
  subnet_ids  = var.private_subnet_ids

  tags = {
    Name = "${var.project_name}-${var.env}-db-subnet-group"
  }
}

# ── RDS Instance ──────────────────────────────────────────────────────────────

resource "aws_db_instance" "this" {
  identifier = "${var.project_name}-${var.env}"

  # Engine
  engine               = "postgres"
  engine_version       = var.postgres_version
  instance_class       = var.db_instance_class

  # Storage
  allocated_storage     = var.allocated_storage
  max_allocated_storage = var.allocated_storage * 3
  storage_type          = "gp3"
  storage_encrypted     = true  # Always encrypted

  # Credentials — password from SSM (never hardcoded)
  db_name  = var.db_name
  username = var.db_username
  password = random_password.db.result

  # Networking — never publicly accessible
  publicly_accessible    = false
  db_subnet_group_name   = aws_db_subnet_group.this.name
  vpc_security_group_ids = [aws_security_group.rds.id]

  # Backups and maintenance
  backup_retention_period  = var.backup_retention_days
  backup_window            = "02:00-03:00"
  maintenance_window       = "Mon:03:30-Mon:04:30"
  auto_minor_version_upgrade = true

  # Deletion protection — always true in prod
  deletion_protection = var.deletion_protection
  skip_final_snapshot = var.deletion_protection ? false : true
  final_snapshot_identifier = var.deletion_protection ? "${var.project_name}-${var.env}-final" : null

  apply_immediately = var.apply_immediately

  tags = {
    Name = "${var.project_name}-${var.env}-rds"
  }
}
