variable "project_name" {
  type        = string
  description = "Name of the project — used in resource naming."
}

variable "env" {
  type        = string
  description = "Deployment environment: dev, staging, or prod."
}

variable "vpc_cidr" {
  type        = string
  description = "CIDR block for the VPC."
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  type        = list(string)
  description = "List of AZs to deploy subnets in (≥ 2 for high availability)."
}

variable "single_nat_gateway" {
  type        = bool
  description = "Use a single NAT Gateway for all private subnets (cheaper but less HA). Recommended for non-prod."
  default     = true
}
