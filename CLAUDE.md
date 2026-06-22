# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Escopo do Repositório

Este repositório é **exclusivamente** para manutenção de dashboards Grafana. A configuração do stack Prometheus (docker-compose, prometheus.yaml, alertmanager.yml) está no repositório separado `enterprise-observability`. Mudanças no stack devem ser solicitadas via Issue naquele repositório.

## Comandos Frequentes

```bash
# Configuração inicial
make setup

# Validar templates JSON (obrigatório antes de commit)
python3 -m json.tool src/dashboards/models/<arquivo>.json.template

# Validar todos os templates
cd src/dashboards && make validate

# Gerar dashboards a partir de template
python3 scripts/generate-project.py \
  --server <servidor> \
  --hostname <hostname>.vya.digital \
  --template <tipo-dashboard> \
  --output /tmp/<arquivo>.json

# Converter dashboard existente em template
python3 src/dashboards/scripts/convert_to_template.py \
  src/dashboards/custom/<dashboard>.json \
  src/dashboards/models/<nome>.json.template \
  --template-name <nome>

# Importar dashboard no Grafana via API
./src/dashboards/scripts/import-dashboards.sh <grafana-url> <api-token> /tmp/

# Deploy do Prometheus stack para servidor remoto
bash deploy/prometheus-stack/scripts/deploy-rsync.sh <user>@<host> /opt/docker_user/prometheus-stack

# Validar configuração Prometheus antes de deploy
promtool check config deploy/prometheus-stack/config/prometheus/prometheus.yml
promtool check rules deploy/prometheus-stack/rules/infra-alerts.yml

# Gerar pacote deploy wfdb01
make build-wfdb01-public-deploy

# Encerramento de sessão (valida integridade do projeto)
make session-end

# Gerar configuração MCP
make mcp

# Limpeza
make clean
```

## Ambiente Python

O projeto usa `uv` e requer Python 3.12+. Dependência principal: `psycopg2-binary`. Ambiente virtual em `.venv/`.

## Arquitetura

### Sistema de Templates (`src/dashboards/`)

O núcleo do projeto é o sistema de templates JSON com variáveis dinâmicas. O fluxo é:

1. **Template** (`models/*.json.template`) — JSON com placeholders como `{{HOSTNAME}}`, `{{JOB_NAME}}`
2. **Geração** — `generate-project.py` substitui variáveis e gera JSON concreto
3. **Import** — `import-dashboards.sh` publica no Grafana via API

**Variáveis de template disponíveis:**
- `{{HOSTNAME}}` / `{{HOSTNAME_SLUG}}` — identificador do servidor
- `{{JOB_NAME}}` — job do Node Exporter no Prometheus
- `{{MYSQL_JOB}}`, `{{POSTGRES_JOB}}` — jobs dos exporters de banco
- `{{DOCKER_JOB}}`, `{{CADVISOR_JOB}}` — jobs de containers
- `{{MOUNTPOINT}}` — ponto de montagem do disco

**Tipos de template disponíveis** em `src/dashboards/models/`:
- `host-dashboard` — Node Exporter (CPU, RAM, disco, rede)
- `docker-dashboard` / `docker-v2-dashboard` — cAdvisor + Docker daemon
- `mysql-dashboard` — MySQL via mysqld_exporter
- `postgres-dashboard` — PostgreSQL via postgres_exporter
- `alertmanager_dashboard_template` — AlertManager

Dashboards customizados (específicos por servidor) ficam em `src/dashboards/custom/`, organizados em subpastas por servidor (wf001, wf008, wfdb01, wfdb02).

### Deploy (`deploy/`)

- `deploy/prometheus-stack/` — pacote autônomo do stack Prometheus para deploy via rsync ou git clone no servidor remoto
- `deploy/wfdb01-public/` — pacote de deploy específico para wfdb01 (construído por `make build-wfdb01-public-deploy`)

### Scripts de Automação (`scripts/`)

Scripts Python para automação diversa. Os principais:
- `generate-project.py` — gera dashboards a partir de templates
- `publish_dashboards.py` / `publish-dashboards.sh` — publica dashboards no Grafana
- `fix_wfdb02_datasources.py` — corrige datasources em dashboards existentes
- `victoria_metrics_collector.py` — coleta métricas do VictoriaMetrics

### Credenciais e API

Credenciais ficam em `.secrets/` (nunca versionado). Scripts de API usam Python + `requests` lendo credenciais de `.secrets/api_config.json` — **nunca usar curl com tokens na linha de comando**.

## Infraestrutura de Produção

- **Grafana**: grafana.vya.digital (v11.6+)
- **Prometheus**: prometheus.vya.digital (29+ jobs)
- **Servidores monitorados**: wfdb01, wfdb02, wf001, wf008 (todos sob `.vya.digital`)
- **Exporters ativos**: `mysqld_exporter`, `postgres_exporter`, `node_exporter`, `cAdvisor`

## Regras de Desenvolvimento

- Validar JSON de todos os templates antes de commit: `python3 -m json.tool <arquivo>`
- Variáveis não substituídas em dashboards gerados indicam erro: `grep -r "{{" /tmp/dashboards-generated/`
- Ao criar novo template, seguir o padrão de variáveis dos templates existentes em `models/`
- Configuração do stack Prometheus em `deploy/prometheus-stack/` deve ser validada com `promtool` antes de deploy

<!-- SPECKIT START -->
For additional context about technologies to be used, project structure,
shell commands, and other important information, read the current plan
<!-- SPECKIT END -->
