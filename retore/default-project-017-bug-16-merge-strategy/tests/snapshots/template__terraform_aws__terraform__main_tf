# ============================================================
# main.tf — Root module. Composes vpc, ecs, and rds modules.
# Each module is fully parametrized — no hardcoded values.
# ============================================================

module "vpc" {
  source = "./modules/vpc"

  project_name       = var.project_name
  env                = var.env
  vpc_cidr           = var.vpc_cidr
  availability_zones = var.availability_zones
}

module "ecs" {
  count  = var.enable_ecs ? 1 : 0
  source = "./modules/ecs"

  project_name      = var.project_name
  env               = var.env
  aws_region        = var.aws_region
  aws_account_id    = var.aws_account_id
  vpc_id            = module.vpc.vpc_id
  public_subnet_ids = module.vpc.public_subnet_ids
  private_subnet_ids = module.vpc.private_subnet_ids
  container_image   = var.container_image
  container_port    = var.container_port
  cpu               = var.ecs_cpu
  memory            = var.ecs_memory
  desired_count     = var.ecs_desired_count
  health_check_path = var.health_check_path
}

module "rds" {
  count  = var.enable_rds ? 1 : 0
  source = "./modules/rds"

  project_name          = var.project_name
  env                   = var.env
  vpc_id                = module.vpc.vpc_id
  private_subnet_ids    = module.vpc.private_subnet_ids
  ecs_security_group_id = var.enable_ecs ? module.ecs[0].ecs_security_group_id : null
  db_instance_class     = var.db_instance_class
  db_name               = var.db_name
  db_username           = var.db_username
  allocated_storage     = var.db_allocated_storage
  backup_retention_days = var.db_backup_retention_days
  deletion_protection   = var.db_deletion_protection
}
