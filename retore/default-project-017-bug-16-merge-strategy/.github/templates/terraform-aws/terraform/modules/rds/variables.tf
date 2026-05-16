variable "project_name" {
  type        = string
  description = "Name of the project — used in resource naming."
}

variable "env" {
  type        = string
  description = "Deployment environment: dev, staging, or prod."
}

variable "vpc_id" {
  type        = string
  description = "ID of the VPC where RDS will be deployed."
}

variable "private_subnet_ids" {
  type        = list(string)
  description = "IDs of private subnets for the DB subnet group (≥ 2 AZs required by AWS)."
}

variable "ecs_security_group_id" {
  type        = string
  description = "Security group ID of the ECS tasks that need DB access. Null if no ECS module."
  default     = null
}

variable "db_instance_class" {
  type        = string
  description = "RDS DB instance type (e.g. db.t3.micro for staging, db.t3.medium for prod)."
  default     = "db.t3.micro"
}

variable "db_name" {
  type        = string
  description = "Name of the PostgreSQL database to create."
  default     = "appdb"
}

variable "db_username" {
  type        = string
  description = "Master DB username. Password is managed by random_password + SSM."
  default     = "appuser"
}

variable "postgres_version" {
  type        = string
  description = "PostgreSQL engine version."
  default     = "16"
}

variable "allocated_storage" {
  type        = number
  description = "Allocated storage in GiB. Auto-scaling up to 3x this value."
  default     = 20
}

variable "backup_retention_days" {
  type        = number
  description = "Days to retain automated RDS backups (min 7 for production)."
  default     = 7
}

variable "deletion_protection" {
  type        = bool
  description = "Prevent accidental instance deletion. Always true in prod."
  default     = false
}

variable "apply_immediately" {
  type        = bool
  description = "Apply changes immediately (true for dev, false for prod — waits for maintenance window)."
  default     = false
}
