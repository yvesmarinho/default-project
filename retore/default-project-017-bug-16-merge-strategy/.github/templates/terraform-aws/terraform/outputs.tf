# ============================================================
# outputs.tf — Root module outputs.
# All outputs have descriptions — they serve as documentation.
# ============================================================

output "vpc_id" {
  description = "ID of the VPC created by the vpc module."
  value       = module.vpc.vpc_id
}

output "public_subnet_ids" {
  description = "IDs of the public subnets (ALB, NAT Gateway)."
  value       = module.vpc.public_subnet_ids
}

output "private_subnet_ids" {
  description = "IDs of the private subnets (ECS tasks, RDS)."
  value       = module.vpc.private_subnet_ids
}

output "alb_dns_name" {
  description = "DNS name of the Application Load Balancer (null when ECS disabled)."
  value       = var.enable_ecs ? module.ecs[0].alb_dns_name : null
}

output "ecs_cluster_name" {
  description = "Name of the ECS cluster (null when ECS disabled)."
  value       = var.enable_ecs ? module.ecs[0].cluster_name : null
}

output "ecs_service_name" {
  description = "Name of the ECS service (null when ECS disabled)."
  value       = var.enable_ecs ? module.ecs[0].service_name : null
}

output "rds_endpoint" {
  description = "Connection endpoint for the RDS instance (null when RDS disabled)."
  value       = var.enable_rds ? module.rds[0].db_endpoint : null
  sensitive   = true
}

output "rds_db_name" {
  description = "Name of the database created in RDS (null when RDS disabled)."
  value       = var.enable_rds ? module.rds[0].db_name : null
}
