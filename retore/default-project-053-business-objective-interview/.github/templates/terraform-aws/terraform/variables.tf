# ============================================================
# variables.tf — Root module variables.
# All variables are typed with descriptions.
# Sensitive values (DB passwords, secrets) are NOT defined here
# — use AWS Secrets Manager or SSM Parameter Store.
# ============================================================

variable "project_name" {
  type        = string
  description = "Name of the project — used in resource naming and tagging."
}

variable "env" {
  type        = string
  description = "Deployment environment: dev, staging, or prod."
  validation {
    condition     = contains(["dev", "staging", "prod"], var.env)
    error_message = "env must be one of: dev, staging, prod."
  }
}

variable "aws_region" {
  type        = string
  description = "AWS region to deploy resources in (e.g. us-east-1, sa-east-1)."
  default     = "us-east-1"
}

variable "aws_account_id" {
  type        = string
  description = "AWS account ID — used to scope IAM policy resource ARNs."
}

# ── VPC ──────────────────────────────────────────────────────────────────────

variable "vpc_cidr" {
  type        = string
  description = "CIDR block for the VPC (e.g. 10.0.0.0/16)."
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  type        = list(string)
  description = "List of AZs to use (≥ 2 for high availability in prod)."
  default     = ["us-east-1a", "us-east-1b"]
}

# ── ECS ──────────────────────────────────────────────────────────────────────

variable "enable_ecs" {
  type        = bool
  description = "Whether to deploy the ECS Fargate module."
  default     = true
}

variable "container_image" {
  type        = string
  description = "Full container image URI including tag (e.g. 123456789.dkr.ecr.us-east-1.amazonaws.com/my-app:1.0.0)."
  default     = "nginx:stable-alpine"
}

variable "container_port" {
  type        = number
  description = "Port the container listens on (e.g. 8000 for FastAPI, 3000 for Next.js)."
  default     = 8000
}

variable "ecs_cpu" {
  type        = number
  description = "ECS task CPU units (256 = 0.25 vCPU, 512 = 0.5 vCPU, 1024 = 1 vCPU)."
  default     = 256
}

variable "ecs_memory" {
  type        = number
  description = "ECS task memory in MiB."
  default     = 512
}

variable "ecs_desired_count" {
  type        = number
  description = "Desired number of ECS tasks running."
  default     = 1
}

variable "health_check_path" {
  type        = string
  description = "HTTP path for ALB health check (e.g. /api/health, /healthz)."
  default     = "/api/health"
}

# ── RDS ──────────────────────────────────────────────────────────────────────

variable "enable_rds" {
  type        = bool
  description = "Whether to deploy the RDS PostgreSQL module."
  default     = false
}

variable "db_instance_class" {
  type        = string
  description = "RDS instance type (e.g. db.t3.micro for staging, db.t3.medium for prod)."
  default     = "db.t3.micro"
}

variable "db_name" {
  type        = string
  description = "Name of the PostgreSQL database to create."
  default     = "appdb"
}

variable "db_username" {
  type        = string
  description = "Master DB username — password is managed by AWS Secrets Manager."
  default     = "appuser"
}

variable "db_allocated_storage" {
  type        = number
  description = "Allocated storage for RDS in GiB."
  default     = 20
}

variable "db_backup_retention_days" {
  type        = number
  description = "Number of days to retain RDS automated backups (min 7 for prod)."
  default     = 7
}

variable "db_deletion_protection" {
  type        = bool
  description = "Prevent accidental DB deletion — always true in prod."
  default     = false
}
