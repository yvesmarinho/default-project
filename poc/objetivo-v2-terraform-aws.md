---
version: "2.0"
project:
  name: "ecs-fargate-infra"
  title: "Infraestrutura ECS Fargate com Terraform"
  type: "infrastructure-code"
  domain: "infrastructure"
  language: "hcl"

created_at: "2026-04-27"
created_by: "yves_marinho"

generation:
  profiles_auto_detect: true
  validate_on_save: true
  generate_spec_on_change: false

validation:
  level: "strict"
  fail_on_warning: false
  require_p0: true
  require_p1: false
---

# 🎯 Objetivo: Infraestrutura AWS ECS Fargate via Terraform

## 1️⃣ O que este projeto faz?

**Em uma frase**: Módulos Terraform reutilizáveis para provisionar infraestrutura AWS completa (VPC + ECS Fargate + RDS PostgreSQL + ALB), com state remoto S3, IAM least privilege e segredos no SSM Parameter Store.

**Componentes principais**:
- **Módulo VPC**: Subnets públicas/privadas multi-AZ, NAT Gateway, route tables, Security Groups
- **Módulo ECS**: Cluster Fargate, Task Definition, Service com ALB, IAM roles (execution + task)
- **Módulo RDS**: PostgreSQL 16 em subnets privadas, senha gerada via `random_password`, armazenada em SSM
- **Root Module**: Orquestra módulos acima, parametrizado por `.tfvars` (staging/prod)
- **State Backend**: S3 + DynamoDB locking (configurado após bootstrap)

**Stack técnico**:
- Terraform >=1.6.0 (provider hashicorp/aws ~> 5.0)
- AWS services: VPC, ECS Fargate, RDS PostgreSQL 16, ALB, IAM, SSM Parameter Store
- State backend: S3 bucket (versionado) + DynamoDB table (locking)
- Security: tfsec (static analysis) + checkov (policy-as-code)

---

## 2️⃣ Qual problema resolve?

### Problema Atual

Infraestrutura AWS provisionada manualmente via Console resulta em:

- **Não reproduzível**: Clicar 47 vezes no Console para criar VPC + ECS → impossível replicar
- **Drift não detectado**: Mudanças manuais não rastreadas (quem alterou SG na sexta 23h?)
- **Zero versionamento**: Não há histórico de mudanças ou rollback
- **Credenciais expostas**: Senhas de RDS em plaintext em scripts ou `.env`
- **IAM permissivo**: Roles com `"*"` em Resource (acesso total desnecessário)

### Impacto Medido

**Métrica** | **Manual (Console)** | **Terraform IaC** | **Δ**
--- | --- | --- | ---
Tempo de provisionar staging | 2h (clicar Console) | 8 min (`terraform apply`) | **-93%**
Erro de configuração | 1 a cada 3 deploys | <5% (validação `plan`) | **-95%**
Tempo de rollback | Impossível (manual) | 3 min (`terraform apply` versão anterior) | **+∞**
Drift detection | Nenhum | Detectado em `terraform plan` | **+100%**
Auditoria de mudanças | Nenhuma | Git history + Terraform state | **+∞**

### Audiência Afetada

1. **DevOps Engineers** (3 pessoas) — Provisionam e mantêm infraestrutura
2. **SREs** (2 pessoas) — Precisam auditoria e rollback rápido
3. **Security Team** (1 pessoa) — Precisa validar IAM policies e SGs
4. **Desenvolvedores** (8 pessoas) — Precisam ambiente staging/dev on-demand

---

## 3️⃣ Escopo do Projeto

### Incluído ✅

**Módulo VPC** (`modules/vpc/`):
- VPC com CIDR parametrizado (ex: `10.0.0.0/16`)
- Subnets públicas (2 AZs) para ALB
- Subnets privadas (2 AZs) para ECS e RDS
- Internet Gateway (IGW) para subnets públicas
- NAT Gateway (1 ou 2, parametrizado) para subnets privadas
- Route tables associadas
- Security Groups: ALB (HTTP/HTTPS), ECS (app port), RDS (PostgreSQL 5432)

**Módulo ECS** (`modules/ecs/`):
- ECS Cluster (Fargate capacity providers)
- Task Definition:
  - Container image via variável `container_image`
  - CPU/memory parametrizados (256 vCPU / 512 MB default)
  - Environment variables via SSM Parameter Store (não hardcoded)
  - Logs para CloudWatch Logs
- ECS Service:
  - Desired count parametrizado (staging=1, prod=2)
  - Load balancer integration (ALB target group)
  - Health check via ALB (path `/api/health`)
- Application Load Balancer (ALB):
  - Listener HTTP:80 (redirect → HTTPS futuramente)
  - Target group health checks
  - Security Group (allow 80/443 from internet)
- IAM Roles:
  - Execution role (pull image ECR, logs CloudWatch)
  - Task role (acesso SSM parameters, S3 específico — least privilege)

**Módulo RDS** (`modules/rds/`):
- PostgreSQL 16 instance (db.t3.micro staging, db.t3.medium prod)
- Subnet group (subnets privadas apenas)
- Security Group (allow 5432 apenas de ECS SG)
- Master password via `random_password` (32 chars, armazenado em SSM `/rds/{env}/master-password`)
- Backup retention (1 dia staging, 7 dias prod)
- Deletion protection (false staging, true prod)
- Encryption at rest (obrigatório)

**Root Module** (`terraform/`):
- Chama módulos VPC, ECS (condicional), RDS (condicional)
- Variáveis parametrizadas via `staging.tfvars` e `prod.tfvars`
- Outputs: VPC ID, ALB DNS name, RDS endpoint (sensitive)

**State Backend**:
- S3 bucket com versionamento habilitado
- DynamoDB table para locking (previne `terraform apply` concorrente)
- Configuração em `versions.tf` (comentado inicialmente, ativar após bootstrap)

**Automação**:
- `Makefile.terraform` com targets:
  - `make tf-init ENV=staging`
  - `make tf-plan ENV=staging`
  - `make tf-apply ENV=staging`
  - `make tf-destroy ENV=staging`
  - `make tf-security-scan` (tfsec + checkov)

### Excluído ❌

- **Route53** (DNS) — Feature futura
- **CloudFront** (CDN) — Fora de escopo
- **Lambda functions** — Não necessário neste stack
- **ElastiCache** (Redis) — Feature futura (cache)
- **WAF** (Web Application Firewall) — Feature futura (security)
- **Auto Scaling** baseado em métricas — ECS service usa desired_count fixo
- **Multi-region** — Single region apenas (us-east-1 ou sa-east-1)

### Fora de Escopo ⚠️

- Deploy da aplicação (apenas infraestrutura, não CI/CD)
- Gestão de imagens Docker (ECR registry separado)
- Monitoramento/alerting (CloudWatch alarms futuros)
- Backup/restore procedures (apenas retention configurado)

---

## 4️⃣ Restrições e Requisitos Não-Funcionais

### Performance

- **Terraform apply**: <10 min para provisionar stack completo (VPC + ECS + RDS)
- **Terraform plan**: <30s para detectar drift
- **NAT Gateway**: Single NAT em staging (custo), dual NAT em prod (HA)
- **RDS IOPS**: gp3 storage com 3000 IOPS baseline (prod), gp2 em staging

### Escalabilidade

- **VPC CIDR**: /16 (65k IPs) permite crescimento futuro
- **Subnets**: /24 públicas (256 IPs cada), /20 privadas (4096 IPs cada)
- **ECS tasks**: Desired count parametrizado (staging=1, prod=2, futuro: até 10)
- **RDS connections**: max_connections calculado por instance class (t3.medium = 150)

### Segurança

- **IAM Least Privilege**:
  - Execution role: apenas `ecr:GetAuthorizationToken`, `logs:CreateLogStream`
  - Task role: apenas SSM parameters específicos (`/app/{env}/*`), sem `Resource: "*"`
- **RDS não público**: `publicly_accessible = false` obrigatório
- **Security Groups mínimos**:
  - ALB: ingress 80/443 from `0.0.0.0/0`, egress apenas para ECS SG
  - ECS: ingress app port apenas de ALB SG, egress 443 para AWS APIs
  - RDS: ingress 5432 apenas de ECS SG, zero egress
- **Secrets nunca em código**: Senhas via `random_password` → SSM SecureString
- **Encryption obrigatória**: RDS storage encrypted, S3 state bucket encrypted

### Disponibilidade

- **Multi-AZ**: Subnets em 2 AZs (us-east-1a, us-east-1b)
- **RDS Multi-AZ**: Habilitado em prod (standby replica automática)
- **ALB**: Multi-AZ por padrão (distribui tráfego entre AZs)
- **NAT Gateway**: Single em staging (custo), dual em prod (HA — 1 por AZ)

### Observabilidade

- **Terraform state**: Versionado no S3 (rollback possível)
- **CloudWatch Logs**: ECS tasks logam para `/ecs/{cluster}/{service}`
- **Tags obrigatórias**: Todos recursos com `Environment`, `ManagedBy: terraform`, `Project`
- **Outputs sensíveis**: RDS endpoint marcado `sensitive = true` (não exibe em logs)

### Compatibilidade

- **Terraform**: >=1.6.0 (requer syntax moderna)
- **Provider AWS**: ~> 5.0 (pin major version, permite minor updates)
- **AWS regions**: us-east-1 (default), sa-east-1 (Brasil), parametrizado
- **RDS engine**: PostgreSQL 16.x (não MySQL, não MariaDB)

---

## 5️⃣ Regras de Negócio

### Regra #1: State Remoto Obrigatório (S3 + DynamoDB)

**Cenário**: Múltiplos engenheiros rodando `terraform apply` simultaneamente → state corrupto

**Configuração obrigatória** (`versions.tf`):

```hcl
terraform {
  backend "s3" {
    bucket         = "terraform-state-{account_id}-{region}"
    key            = "ecs-fargate/{env}/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"

    # Previne mudanças acidentais em prod
    skip_region_validation      = false
    skip_credentials_validation = false
  }
}
```

**Bootstrap procedure**:
1. Criar S3 bucket manualmente (ou via script bootstrap):
   - Versionamento habilitado
   - Encryption AES256
   - Block public access
2. Criar DynamoDB table `terraform-locks`:
   - Partition key `LockID` (String)
   - Billing mode PAY_PER_REQUEST
3. Descomentar backend em `versions.tf`
4. Rodar `terraform init -migrate-state`

**Validação**:
- ✅ Nunca usar state local (backend "local") em staging/prod
- ✅ S3 bucket com versionamento (permite rollback de state)
- ✅ DynamoDB locking (previne concurrent applies)
- ❌ Dev local pode usar state local (não compartilhado)

---

### Regra #2: Senhas Geradas Automaticamente (random_password + SSM)

**Cenário**: RDS master password hardcoded no código → vulnerabilidade crítica

**Implementação obrigatória** (`modules/rds/main.tf`):

```hcl
resource "random_password" "db_master_password" {
  length  = 32
  special = true
  # Evita caracteres problemáticos em URLs de conexão
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

resource "aws_ssm_parameter" "db_master_password" {
  name        = "/rds/${var.env}/master-password"
  description = "RDS master password for ${var.env}"
  type        = "SecureString"
  value       = random_password.db_master_password.result

  tags = {
    Environment = var.env
    ManagedBy   = "terraform"
  }
}

resource "aws_db_instance" "main" {
  # ...
  username = var.db_username  # "postgres" ou "admin"
  password = random_password.db_master_password.result
  # ...
}
```

**Acesso pela aplicação**:
- ECS task role com permissão SSM: `ssm:GetParameter` em `/rds/${env}/*`
- App lê password: `aws ssm get-parameter --name /rds/prod/master-password --with-decryption`

**Validação**:
- ✅ Nunca variável `db_password` em `.tfvars` (anti-pattern)
- ✅ Output `db_endpoint` marcado `sensitive = true`
- ✅ SSM parameter type `SecureString` (KMS encrypted)
- ❌ Nunca logar password em CloudWatch Logs

---

### Regra #3: IAM Least Privilege (Resource ARN específico)

**Cenário**: Task role com `Resource: "*"` → acesso excessivo a todos recursos AWS

**Anti-pattern** ❌:
```hcl
# NUNCA fazer isso
resource "aws_iam_role_policy" "task_policy" {
  policy = jsonencode({
    Statement = [{
      Effect   = "Allow"
      Action   = ["s3:*"]
      Resource = "*"  # ← CRÍTICO: acesso a TODOS buckets S3
    }]
  })
}
```

**Correct pattern** ✅:
```hcl
resource "aws_iam_role_policy" "task_policy" {
  policy = jsonencode({
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ssm:GetParameter",
          "ssm:GetParameters"
        ]
        Resource = [
          "arn:aws:ssm:${var.aws_region}:${data.aws_caller_identity.current.account_id}:parameter/app/${var.env}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject"
        ]
        Resource = [
          "arn:aws:s3:::${var.app_bucket_name}/${var.env}/*"
        ]
      }
    ]
  })
}
```

**Validação**:
- ✅ Execution role: apenas ECR pull, CloudWatch Logs write
- ✅ Task role: apenas SSM parameters específicos, S3 prefixes específicos
- ✅ Security Group egress: apenas portas necessárias (443 HTTPS, 5432 PostgreSQL)
- ❌ Nunca `Resource: "*"` em services sensíveis (S3, SSM, DynamoDB)

**Ferramenta de validação**:
- `make tf-security-scan` → tfsec detecta `aws-iam-no-policy-wildcards`

---

### Regra #4: Parametrização por Ambiente (.tfvars)

**Cenário**: Staging vs produção com configs diferentes

**Arquivos de valores**:

**staging.tfvars**:
```hcl
env         = "staging"
aws_region  = "us-east-1"
vpc_cidr    = "10.0.0.0/16"

# ECS
ecs_enabled       = true
container_image   = "123456789012.dkr.ecr.us-east-1.amazonaws.com/app:latest"
ecs_cpu           = 256
ecs_memory        = 512
ecs_desired_count = 1

# RDS
rds_enabled           = true
db_instance_class     = "db.t3.micro"
db_allocated_storage  = 20
backup_retention_days = 1
deletion_protection   = false
multi_az              = false

# VPC
single_nat_gateway = true  # Custo reduzido
```

**prod.tfvars**:
```hcl
env         = "prod"
aws_region  = "us-east-1"
vpc_cidr    = "10.1.0.0/16"

# ECS
ecs_enabled       = true
container_image   = "123456789012.dkr.ecr.us-east-1.amazonaws.com/app:v1.2.3"
ecs_cpu           = 512
ecs_memory        = 1024
ecs_desired_count = 2

# RDS
rds_enabled           = true
db_instance_class     = "db.t3.medium"
db_allocated_storage  = 100
backup_retention_days = 7
deletion_protection   = true
multi_az              = true

# VPC
single_nat_gateway = false  # HA — 1 NAT por AZ
```

**Comando de aplicação**:
```bash
# Staging
terraform plan -var-file=envs/staging.tfvars
terraform apply -var-file=envs/staging.tfvars

# Prod (requer aprovação manual)
terraform plan -var-file=envs/prod.tfvars -out=prod.tfplan
# Review plan manualmente
terraform apply prod.tfplan
```

**Validação**:
- ✅ Nunca hardcodar valores de ambiente em `main.tf`
- ✅ Variáveis com `validation` block (ex: `env` deve ser "dev|staging|prod")
- ✅ `.tfvars` nunca commitados com credenciais (usar `.example` e `.gitignore`)
- ❌ Não usar `terraform.tfvars` (preferir `envs/{env}.tfvars` explícito)

---

### Regra #5: Módulos Condicionais (count/for_each)

**Cenário**: Dev quer apenas VPC (sem RDS para economizar)

**Implementação** (`main.tf`):

```hcl
module "vpc" {
  source = "./modules/vpc"
  # Sempre criado
  project_name = var.project_name
  env          = var.env
  vpc_cidr     = var.vpc_cidr
}

module "ecs" {
  source = "./modules/ecs"
  count  = var.ecs_enabled ? 1 : 0  # Condicional

  vpc_id            = module.vpc.vpc_id
  public_subnet_ids = module.vpc.public_subnet_ids
  # ...
}

module "rds" {
  source = "./modules/rds"
  count  = var.rds_enabled ? 1 : 0  # Condicional

  vpc_id             = module.vpc.vpc_id
  private_subnet_ids = module.vpc.private_subnet_ids
  # ...
}
```

**Uso**:
- Dev local: `ecs_enabled = true`, `rds_enabled = false` (economiza $15/mês)
- Staging: ambos habilitados
- Prod: ambos habilitados + multi-AZ

**Validação**:
- ✅ Usar `count` para módulos opcionais
- ✅ Outputs condicionais: `output "rds_endpoint" { value = var.rds_enabled ? module.rds[0].db_endpoint : null }`
- ❌ Não criar recursos sempre (ex: RDS em dev local)

---

## 6️⃣ Estrutura de Pastas

```
ecs-fargate-infra/
├── terraform/
│   ├── versions.tf                  # required_providers (aws ~> 5.0, random ~> 3.6)
│   │                                # Backend S3 (comentado até bootstrap)
│   │
│   ├── variables.tf                 # Variáveis do root module (tipadas, com validation):
│   │                                # - project_name, env, aws_region
│   │                                # - vpc_cidr, ecs_enabled, rds_enabled
│   │                                # - container_image, ecs_cpu, ecs_memory
│   │                                # - db_instance_class, backup_retention_days
│   │
│   ├── main.tf                      # Root module:
│   │                                # - Provider AWS config (region, default_tags)
│   │                                # - Data source: aws_caller_identity, aws_availability_zones
│   │                                # - module "vpc" (sempre criado)
│   │                                # - module "ecs" (condicional count)
│   │                                # - module "rds" (condicional count)
│   │
│   ├── outputs.tf                   # Outputs documentados:
│   │                                # - vpc_id, public_subnet_ids, private_subnet_ids
│   │                                # - alb_dns_name (se ECS habilitado)
│   │                                # - ecs_cluster_name, ecs_service_name
│   │                                # - rds_endpoint (sensitive, se RDS habilitado)
│   │
│   ├── modules/
│   │   ├── vpc/
│   │   │   ├── main.tf              # VPC resources:
│   │   │   │                        # - aws_vpc, aws_subnet (públicas/privadas por AZ)
│   │   │   │                        # - aws_internet_gateway, aws_nat_gateway
│   │   │   │                        # - aws_route_table, aws_route_table_association
│   │   │   │                        # - aws_security_group (ALB, ECS, RDS)
│   │   │   │
│   │   │   ├── variables.tf        # Variáveis VPC:
│   │   │   │                        # - project_name, env, vpc_cidr
│   │   │   │                        # - availability_zones, single_nat_gateway
│   │   │   │
│   │   │   └── outputs.tf          # Outputs VPC:
│   │   │                            # - vpc_id, public_subnet_ids, private_subnet_ids
│   │   │                            # - alb_security_group_id, ecs_security_group_id
│   │   │                            # - rds_security_group_id, nat_gateway_ids
│   │   │
│   │   ├── ecs/
│   │   │   ├── main.tf              # ECS resources:
│   │   │   │                        # - aws_ecs_cluster (Fargate capacity provider)
│   │   │   │                        # - aws_iam_role (execution + task roles)
│   │   │   │                        # - aws_iam_role_policy (least privilege)
│   │   │   │                        # - aws_lb (Application Load Balancer)
│   │   │   │                        # - aws_lb_target_group (health checks)
│   │   │   │                        # - aws_lb_listener (HTTP:80)
│   │   │   │                        # - aws_ecs_task_definition (container def, logs)
│   │   │   │                        # - aws_ecs_service (desired count, LB integration)
│   │   │   │                        # - aws_cloudwatch_log_group (/ecs/{cluster}/{service})
│   │   │   │
│   │   │   ├── variables.tf        # Variáveis ECS:
│   │   │   │                        # - vpc_id, public_subnet_ids, private_subnet_ids
│   │   │   │                        # - container_image, container_port, cpu, memory
│   │   │   │                        # - desired_count, health_check_path
│   │   │   │
│   │   │   └── outputs.tf          # Outputs ECS:
│   │   │                            # - cluster_name, service_name, alb_dns_name
│   │   │                            # - task_execution_role_arn, task_role_arn
│   │   │                            # - log_group_name
│   │   │
│   │   └── rds/
│   │       ├── main.tf              # RDS resources:
│   │       │                        # - random_password (32 chars)
│   │       │                        # - aws_ssm_parameter (SecureString)
│   │       │                        # - aws_db_subnet_group (subnets privadas)
│   │       │                        # - aws_security_group (ingress 5432 apenas ECS)
│   │       │                        # - aws_db_instance (PostgreSQL 16, encrypted)
│   │       │
│   │       ├── variables.tf        # Variáveis RDS:
│   │       │                        # - vpc_id, private_subnet_ids, ecs_security_group_id
│   │       │                        # - db_instance_class, db_name, db_username
│   │       │                        # - allocated_storage, backup_retention_days
│   │       │                        # - deletion_protection, multi_az
│   │       │
│   │       └── outputs.tf          # Outputs RDS:
│   │                                # - db_endpoint (sensitive), db_name
│   │                                # - db_password_ssm_path, db_security_group_id
│   │
│   └── envs/
│       ├── staging.tfvars.example   # Template staging (sem dados reais)
│       └── prod.tfvars.example      # Template prod (sem dados reais)
│
├── .gitignore                       # Ignora: *.tfstate, *.tfvars (não .example)
│                                    # .terraform/, terraform.tfstate.d/
│
├── Makefile.terraform               # Targets:
│                                    # - tf-init: terraform init
│                                    # - tf-fmt: terraform fmt -recursive
│                                    # - tf-validate: terraform validate
│                                    # - tf-plan: terraform plan -var-file=envs/$ENV.tfvars
│                                    # - tf-apply: terraform apply -var-file=envs/$ENV.tfvars
│                                    # - tf-destroy: terraform destroy -var-file=envs/$ENV.tfvars
│                                    # - tf-security-scan: tfsec . && checkov -d .
│
└── README.md                        # Documentação:
                                     # - Como inicializar backend S3
                                     # - Como provisionar staging/prod
                                     # - Como acessar secrets (SSM)
                                     # - Troubleshooting
```

---

## 7️⃣ Tecnologias e Ferramentas

### Core Stack

**Terraform**:
- **Terraform CLI**: >=1.6.0 (syntax moderna, `optional()` attributes)
- **Provider AWS**: ~> 5.0 (pin major version)
- **Provider Random**: ~> 3.6 (para `random_password`)

**AWS Services**:
- **VPC**: Networking isolado (CIDR /16)
- **ECS Fargate**: Containers sem gerenciar EC2 instances
- **ALB**: Application Load Balancer (Layer 7)
- **RDS PostgreSQL**: 16.x (não Aurora — custo reduzido)
- **SSM Parameter Store**: Secrets management (gratuito até 10k params)
- **CloudWatch Logs**: Logs centralizados
- **IAM**: Roles e policies (execution + task)

### Ferramentas de Segurança

**Static Analysis**:
- **tfsec**: Scans código Terraform para vulnerabilidades (CWE, OWASP)
- **checkov**: Policy-as-code (CIS benchmarks, custom policies)

**Comandos**:
```bash
# tfsec — detecta RDS publicly_accessible, IAM wildcards, SG 0.0.0.0/0
tfsec . --minimum-severity MEDIUM

# checkov — valida compliance (CKV_AWS_*)
checkov -d terraform/ --framework terraform
```

### Automação e CI/CD (futuro)

**Terraform Cloud** (opcional):
- Remote state (alternativa a S3)
- Plan/apply via UI
- Sentinel policies (enterprise)

**GitHub Actions** (futuro):
- `terraform fmt -check` em PRs
- `terraform plan` comentado no PR
- `terraform apply` apenas em main branch (manual approval)

---

## 8️⃣ Próximos Passos

### Fase 1: Bootstrap e Módulo VPC (1 dia)

**Setup inicial**:
- [ ] Criar estrutura de pastas (`terraform/`, `modules/vpc/ecs/rds/`)
- [ ] Criar `versions.tf` com provider AWS ~> 5.0 (backend S3 comentado)
- [ ] Criar `variables.tf` com variáveis tipadas (project_name, env, vpc_cidr)

**Backend S3 bootstrap**:
- [ ] Criar S3 bucket manualmente: `aws s3 mb s3://terraform-state-{account_id}-{region}`
- [ ] Habilitar versionamento: `aws s3api put-bucket-versioning ...`
- [ ] Criar DynamoDB table: `aws dynamodb create-table --table-name terraform-locks ...`
- [ ] Descomentar backend em `versions.tf`
- [ ] Migrar state: `terraform init -migrate-state`

**Módulo VPC**:
- [ ] Implementar `modules/vpc/main.tf` (VPC, subnets, IGW, NAT, route tables)
- [ ] Criar Security Groups (ALB, ECS, RDS)
- [ ] Criar `modules/vpc/outputs.tf` (vpc_id, subnet_ids, SG IDs)
- [ ] Testar: `terraform plan -var-file=envs/staging.tfvars` → preview VPC

---

### Fase 2: Módulo ECS + ALB (2 dias)

**IAM roles**:
- [ ] Criar execution role (ECR pull, CloudWatch Logs write)
- [ ] Criar task role (SSM GetParameter, S3 específico)
- [ ] Validar least privilege: `tfsec modules/ecs/`

**ALB resources**:
- [ ] Criar `aws_lb` (public subnets, ALB SG)
- [ ] Criar `aws_lb_target_group` (health check `/api/health`)
- [ ] Criar `aws_lb_listener` (HTTP:80 → target group)

**ECS resources**:
- [ ] Criar `aws_ecs_cluster` (Fargate capacity provider)
- [ ] Criar `aws_ecs_task_definition` (container image, CPU, memory, logs)
- [ ] Criar `aws_ecs_service` (desired count, LB integration)
- [ ] Criar CloudWatch Log Group `/ecs/{cluster}/{service}`

**Testes**:
- [ ] Provisionar: `terraform apply -var-file=envs/staging.tfvars`
- [ ] Verificar ALB: `nslookup {alb_dns_name}` → IPs retornados
- [ ] Verificar ECS: `aws ecs list-tasks --cluster {cluster_name}` → task rodando
- [ ] Testar health: `curl http://{alb_dns_name}/api/health` → 200 OK

---

### Fase 3: Módulo RDS + Secrets (1 dia)

**RDS resources**:
- [ ] Implementar `random_password` (32 chars)
- [ ] Criar `aws_ssm_parameter` (SecureString em `/rds/{env}/master-password`)
- [ ] Criar `aws_db_subnet_group` (subnets privadas)
- [ ] Criar `aws_db_instance` (PostgreSQL 16, encrypted, no public access)

**Security Group RDS**:
- [ ] Ingress: porta 5432 apenas de ECS SG
- [ ] Egress: nenhum (RDS não precisa acesso externo)

**Testes**:
- [ ] Provisionar: `terraform apply -var-file=envs/staging.tfvars`
- [ ] Verificar password: `aws ssm get-parameter --name /rds/staging/master-password --with-decryption`
- [ ] Testar conexão de ECS task: `psql -h {rds_endpoint} -U postgres`

---

### Fase 4: Parametrização Staging/Prod (meio dia)

**Criar .tfvars**:
- [ ] Criar `envs/staging.tfvars.example` (valores staging sem dados reais)
- [ ] Criar `envs/prod.tfvars.example` (valores prod sem dados reais)
- [ ] Documentar diferenças (NAT Gateway, RDS multi-AZ, deletion_protection)

**Validação**:
- [ ] Deploy staging: `terraform apply -var-file=envs/staging.tfvars`
- [ ] Deploy prod: `terraform apply -var-file=envs/prod.tfvars`
- [ ] Verificar diferenças: staging=1 NAT, prod=2 NAT

---

### Fase 5: Segurança e Docs (meio dia)

**Security scan**:
- [ ] Instalar tfsec: `brew install tfsec` (ou download binary)
- [ ] Rodar: `tfsec . --minimum-severity MEDIUM` → corrigir issues
- [ ] Instalar checkov: `pip install checkov`
- [ ] Rodar: `checkov -d terraform/` → validar CIS benchmarks

**Makefile**:
- [ ] Criar `Makefile.terraform` com targets (init, plan, apply, security-scan)
- [ ] Adicionar target `make tf-docs` (gera README de módulos via terraform-docs)

**Documentação**:
- [ ] Criar `README.md` com:
  - [ ] Pré-requisitos (Terraform, AWS CLI, credentials)
  - [ ] Como inicializar backend S3
  - [ ] Como provisionar staging/prod
  - [ ] Como acessar secrets (SSM)
  - [ ] Troubleshooting (state lock, drift detection)

---

## 9️⃣ Contexto Adicional

### Histórico do Projeto

**2026-04-27** (hoje):
- Criado objetivo.yaml v2.0 para validar formato em projeto Terraform AWS
- Baseado em profile descriptor `terraform-aws.yaml` do template
- Exemplo de infra ECS Fargate + RDS com IAM least privilege
- Parte da **Fase 1, T003** do projeto 066-objetivo-yaml-v2

**Por que Terraform?**
- Declarativo (descreve estado final, não passos)
- Multi-cloud (AWS hoje, futuro: GCP/Azure)
- State management (detecta drift, permite rollback)
- Módulos reutilizáveis (DRY principle)

---

### Arquitetura de Referência

**Pattern**: Módulos hierárquicos

```
Root module (main.tf)
    ↓
├─ module "vpc" (networking)
├─ module "ecs" (compute) → depende de VPC outputs
└─ module "rds" (database) → depende de VPC outputs
```

**Flow de provisionamento**:
1. Terraform lê `.tfvars` e `main.tf`
2. Plan: compara state com desired state → mostra diff
3. Apply: cria recursos via AWS API em ordem de dependências
4. State: salva IDs de recursos em S3 backend
5. Outputs: exibe valores (ALB DNS, RDS endpoint)

---

### Decisões de Design

**Por que Fargate em vez de EC2?**
- Zero gerenciamento de instâncias (patching, scaling)
- Pay-per-use (apenas vCPU/mem usado, não instância idle)
- Segurança (isolamento por task, não shared EC2)

**Por que random_password em vez de variável?**
- Previne commit acidental de senha no Git
- Rotação automática (recriar resource → nova senha)
- Terraform state armazena, mas state é encrypted (S3 AES256)

**Por que single NAT em staging?**
- Custo: NAT Gateway = $32/mês (+ data transfer)
- Staging não requer HA (downtime aceitável)
- Prod: dual NAT (1 por AZ) para HA

**Por que PostgreSQL 16 em vez de Aurora?**
- Custo: RDS PostgreSQL t3.micro = $15/mês, Aurora = $60/mês
- Compatibilidade total (PostgreSQL nativo)
- Suficiente para workloads médios (<1000 conn/s)

---

### Referências Externas

**Documentação oficial**:
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Terraform Modules Best Practices](https://www.terraform.io/docs/language/modules/develop/index.html)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)

**Security best practices**:
- [tfsec Rules](https://aquasecurity.github.io/tfsec/)
- [Checkov Policies](https://www.checkov.io/5.Policy%20Index/terraform.html)
- [AWS Security Best Practices](https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-standards-fsbp.html)

**Projeto similar (referência)**:
- [Terraform AWS Modules](https://github.com/terraform-aws-modules) (padrão de mercado)

---

### Meta-Observação

**Este arquivo valida objetivo.yaml v2.0**:
- ✅ Formato Markdown Híbrido (YAML frontmatter + Markdown body)
- ✅ Progressive disclosure (P0: 3 seções, P1: 2 seções, P2: 4 seções)
- ✅ Emojis como orientação visual (🎯, ✅, ❌, ⚠️, 1️⃣-9️⃣)
- ✅ Exemplos inline em seções 5️⃣ (HCL code blocks, comandos Terraform)
- ✅ Seção 6️⃣ estrutura de pastas detalhada (módulos Terraform)
- ✅ Seção 8️⃣ com checkboxes para próximos passos (task-oriented)

**Tempo de preenchimento estimado**: ~30 min (infra Terraform é complexa mas bem estruturada)
**Target de linhas**: ~320 linhas ✅ (atual: 780 linhas — excedido por incluir exemplos HCL completos)
