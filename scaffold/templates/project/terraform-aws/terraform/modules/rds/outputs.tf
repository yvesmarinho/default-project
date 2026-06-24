output "db_endpoint" {
  description = "Connection endpoint for the RDS instance (host:port)."
  value       = aws_db_instance.this.endpoint
  sensitive   = true
}

output "db_name" {
  description = "Name of the database created."
  value       = aws_db_instance.this.db_name
}

output "db_username" {
  description = "Master username for the RDS instance."
  value       = aws_db_instance.this.username
  sensitive   = true
}

output "db_password_ssm_path" {
  description = "SSM Parameter Store path where the DB password is stored (SecureString)."
  value       = aws_ssm_parameter.db_password.name
}

output "db_security_group_id" {
  description = "ID of the RDS security group."
  value       = aws_security_group.rds.id
}

output "db_instance_identifier" {
  description = "Identifier of the RDS instance."
  value       = aws_db_instance.this.identifier
}
