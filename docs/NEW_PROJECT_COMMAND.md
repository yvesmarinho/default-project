# 🚀 new-project — Comando Global

Script conveniente instalado em `~/.local/bin/new-project` para criar projetos usando o Enterprise Default Project Template de qualquer lugar.

## Instalação

✅ **Já instalado!** O script está em:
- Localização: `~/.local/bin/new-project`
- Executável: ✅
- No PATH: ✅

## Uso Básico

```bash
# Modo interativo (recomendado para iniciantes)
new-project

# Quick start com nome
new-project my-api

# Com perfil específico
new-project my-api --compose python-fastapi

# Frontend Next.js
new-project my-frontend --compose typescript-next

# Infraestrutura
new-project infra-aws --domain infrastructure --compose terraform-aws
```

## Comandos Úteis

```bash
# Ver ajuda completa
new-project --help

# Listar todos os perfis disponíveis
new-project --list-profiles

# Validar perfis do template
new-project --validate
```

## Exemplos Práticos

### Backend Python FastAPI

```bash
new-project my-api --compose python-fastapi
cd my-api
make install-deps
make dev
```

### Frontend TypeScript Next.js

```bash
new-project my-frontend --compose typescript-next
cd my-frontend
npm install
npm run dev
```

### Fullstack Monorepo

```bash
# Backend
new-project my-app-backend --compose python-fastapi --target-dir ~/workspace/my-app

# Frontend
new-project my-app-frontend --compose typescript-next --target-dir ~/workspace/my-app
```

### Infraestrutura Terraform

```bash
new-project infra-prod --domain infrastructure --compose terraform-aws
cd infra-prod
terraform init
```

## Opções Avançadas

```bash
--domain DOMAIN       # programming | infrastructure | analysis
--language LANG       # python | typescript | go | other
--compose PROFILE     # python-fastapi, python-flask, typescript-next, etc.
--target-dir DIR      # Diretório pai onde criar o projeto
```

## Validação de Nome

O script valida automaticamente o nome do projeto:
- ✅ Formato: `kebab-case` (letras minúsculas, números, hífens)
- ✅ Exemplos válidos: `my-api`, `api-v2`, `backend-service`
- ❌ Inválidos: `My_API`, `api v2`, `API-Service`

## Detecção de Conflitos

O script **previne automaticamente** a criação de estruturas duplicadas (BUG-01 resolvido):

```bash
# ❌ Antes (buggy)
cd my-project/
new-project my-project  # criava my-project/my-project/

# ✅ Agora (corrigido)
cd my-project/
new-project my-project  # ❌ Erro com mensagem clara
```

## Localização do Template

O script aponta para:
```bash
~/Documentos/DevOps/Vya-Jobs/a-default-project
```

Se você moveu o template, edite a variável `TEMPLATE_DIR` no início do script:

```bash
nano ~/.local/bin/new-project
# Ajuste a linha:
# TEMPLATE_DIR="${HOME}/Seu/Caminho/a-default-project"
```

## Troubleshooting

### Comando não encontrado

```bash
# Verificar se está no PATH
echo $PATH | grep -q "$HOME/.local/bin" && echo "✅ OK" || echo "❌ Adicionar ao PATH"

# Adicionar ao ~/.zshrc (se necessário)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Permissão negada

```bash
chmod +x ~/.local/bin/new-project
```

### Template não encontrado

```bash
# Verificar localização
ls ~/Documentos/DevOps/Vya-Jobs/a-default-project/scripts/scaffold.py

# Ajustar caminho no script se necessário
nano ~/.local/bin/new-project
```

## Ver Também

- Template principal: `~/Documentos/DevOps/Vya-Jobs/a-default-project`
- Quick Start: `~/Documentos/DevOps/Vya-Jobs/a-default-project/QUICKSTART.md`
- Regras Copilot: `~/Documentos/DevOps/Vya-Jobs/a-default-project/.copilot-rules.md`
- Perfis disponíveis: `new-project --list-profiles`
