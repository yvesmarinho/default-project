variable "project_name" {
  type        = string
  description = "Name of the project — used in resource naming."
}

variable "env" {
  type        = string
  description = "Deployment environment: dev, staging, or prod."
}

variable "aws_region" {
  type        = string
  description = "AWS region where resources are deployed."
}

variable "aws_account_id" {
  type        = string
  description = "AWS account ID — used to scope IAM policy resource ARNs."
}

variable "vpc_id" {
  type        = string
  description = "ID of the VPC where ECS resources will be deployed."
}

variable "public_subnet_ids" {
  type        = list(string)
  description = "IDs of public subnets for the Application Load Balancer."
}

variable "private_subnet_ids" {
  type        = list(string)
  description = "IDs of private subnets for ECS Fargate tasks."
}

variable "container_image" {
  type        = string
  description = "Full container image URI including tag."
}

variable "container_port" {
  type        = number
  description = "Port the application container listens on."
  default     = 8000
}

variable "cpu" {
  type        = number
  description = "ECS task CPU units (256, 512, 1024, 2048, 4096)."
  default     = 256
}

variable "memory" {
  type        = number
  description = "ECS task memory in MiB."
  default     = 512
}

variable "desired_count" {
  type        = number
  description = "Desired number of ECS task instances."
  default     = 1
}

variable "health_check_path" {
  type        = string
  description = "HTTP path for ALB health check."
  default     = "/api/health"
}

variable "log_retention_days" {
  type        = number
  description = "Number of days to retain CloudWatch logs."
  default     = 30
}
