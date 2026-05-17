# Rotação de Credenciais

## Visão Geral

A rotação de credenciais é uma prática essencial de segurança que reduz o risco de comprometimento ao limitar o tempo de validade de senhas, tokens e chaves. Este guia estabelece políticas e procedimentos para rotação sistemática de todos os tipos de credenciais no projeto.

--- ## Política de Rotação

### Frequência Recomendada

| Tipo de Credencial | Frequência | Prioridade | Justificativa |
|-------------------|------------|------------|---------------|
| **Vault Password (Ansible)** | 180 dias | 🔴 Crítica | Protege todas as credenciais encriptadas |
| **Senhas SSH** | 90 dias | 🟠 Alta | Acesso direto aos servidores |
| **Senhas de Banco de Dados** | 60 dias | 🟠 Alta | Acesso a dados críticos |
| **Tokens de API** | 30 dias | 🟡 Média | Acesso a serviços externos |
| **Chaves SSH** | 365 dias | 🟠 Alta | Autenticação de sistemas |
| **Senhas de Aplicação** | 90 dias | 🟡 Média | Acesso de usuários |
| **Secrets do GitHub** | 90 dias | 🟠 Alta | Acesso ao pipeline CI/CD |

### Gatilhos para Rotação Imediata

Além da rotação programada, as credenciais devem ser rotacionadas **imediatamente** nas seguintes situações:

- ⚠️ Suspeita de comprometimento
- ⚠️ Saída de colaborador com acesso
- ⚠️ Exposição acidental (commit, logs, chat)
- ⚠️ Incidente de segurança
- ⚠️ Após auditoria de segurança
- ⚠️ Mudança de ambiente (dev → prod)

---

## Procedimentos de Rotação

### 1. Rotação de Vault Password (Ansible)

**Criticidade**: 🔴 Crítica
**Frequência**: 180 dias
**Tempo estimado**: 15-20 minutos

#### Passo a Passo

```bash
#!/usr/bin/env bash
# rotate-vault-password.sh

set -euo pipefail

echo "🔐 Iniciando rotação de Vault Password..."

# 1. Gerar nova senha forte
echo "📝 Gerando nova senha..."
openssl rand -base64 32 > .secrets/.vault_pass.new
chmod 600 .secrets/.vault_pass.new

# 2. Fazer backup da senha atual
cp .secrets/.vault_pass .secrets/.vault_pass.backup.$(date +%Y%m%d)

# 3. Re-encriptar todos arquivos vault
echo "🔄 Re-encriptando arquivos vault..."
find ansible/inventory -name "vault.yml" | while read vault_file; do
    echo "  - Processando: $vault_file"
    ansible-vault rekey "${vault_file}" \
        --vault-password-file .secrets/.vault_pass \
        --new-vault-password-file .secrets/.vault_pass.new
done

# 4. Substituir arquivo de senha
mv .secrets/.vault_pass.new .secrets/.vault_pass
chmod 600 .secrets/.vault_pass

# 5. Testar nova senha
echo "✅ Testando nova senha..."
ansible-vault view ansible/inventory/dev/group_vars/all/vault.yml > /dev/null

echo "✅ Rotação de Vault Password concluída com sucesso!"
echo "📊 Próxima rotação: $(date -d '+180 days' +%Y-%m-%d)"

# 6. Registrar rotação
echo "$(date +%Y-%m-%d) - Vault Password rotacionado" >> .secrets/rotation_audit.log
```

#### Checklist Pós-Rotação

- [ ] Testar playbooks em ambiente DEV
- [ ] Atualizar senha no gerenciador de senhas da equipe
- [ ] Notificar equipe sobre mudança
- [ ] Atualizar CI/CD (GitHub Secrets, GitLab Variables)
- [ ] Documentar data no audit log
- [ ] Deletar backups após 30 dias

---

### 2. Rotação de Senhas SSH

**Criticidade**: 🟠 Alta
**Frequência**: 90 dias
**Tempo estimado**: 10-15 minutos por servidor

#### Método 1: Via Ansible (Recomendado)

```bash
#!/usr/bin/env bash
# rotate-ssh-passwords.sh

set -euo pipefail

ENVIRONMENT=${1:-dev}

echo "🔐 Rotacionando senhas SSH - Ambiente: $ENVIRONMENT"

# 1. Gerar novas senhas para cada servidor
echo "📝 Gerando novas senhas..."
declare -A NEW_PASSWORDS

for host in $(ansible -i "ansible/inventory/${ENVIRONMENT}/hosts.yml" all --list-hosts | tail -n +2); do
    NEW_PASSWORDS[$host]=$(openssl rand -base64 24)
done

# 2. Atualizar senhas nos servidores
for host in "${!NEW_PASSWORDS[@]}"; do
    echo "  - Atualizando: $host"

    ansible -i "ansible/inventory/${ENVIRONMENT}/hosts.yml" "$host" \
        -m user \
        -a "name=ansible password={{ '${NEW_PASSWORDS[$host]}' | password_hash('sha512') }}" \
        --become
done

# 3. Atualizar vault
echo "🔄 Atualizando vault..."
ansible-vault edit "ansible/inventory/${ENVIRONMENT}/group_vars/all/vault.yml"
# Manualmente atualizar vault_ssh_passwords para cada host

# 4. Testar novas credenciais
echo "✅ Testando conexão..."
ansible -i "ansible/inventory/${ENVIRONMENT}/hosts.yml" all -m ping

echo "✅ Rotação de senhas SSH concluída!"
```

#### Método 2: Manual

```bash
# 1. No servidor remoto
ssh user@server
sudo passwd ansible  # Inserir nova senha

# 2. Atualizar vault local
ansible-vault edit ansible/inventory/prod/group_vars/all/vault.yml
# Alterar: vault_ssh_password

# 3. Testar
ansible -i ansible/inventory/prod/hosts.yml all -m ping
```

---

### 3. Rotação de Senhas de Banco de Dados

**Criticidade**: 🟠 Alta
**Frequência**: 60 dias
**Tempo estimado**: 20-30 minutos

#### MySQL/PostgreSQL

```bash
#!/usr/bin/env bash
# rotate-db-passwords.sh

set -euo pipefail

DB_TYPE=${1:-mysql}  # mysql ou postgresql
ENVIRONMENT=${2:-dev}

echo "🔐 Rotacionando senhas de banco de dados - ${DB_TYPE} - ${ENVIRONMENT}"

# 1. Gerar nova senha
NEW_PASSWORD=$(openssl rand -base64 32)

# 2. Conectar ao banco e alterar senha
case $DB_TYPE in
    mysql)
        docker exec -it mysql mysql -u root -p -e \
            "ALTER USER 'root'@'%' IDENTIFIED BY '${NEW_PASSWORD}';"
        ;;
    postgresql)
        docker exec -it postgres psql -U postgres -c \
            "ALTER USER postgres WITH PASSWORD '${NEW_PASSWORD}';"
        ;;
esac

# 3. Atualizar vault
echo "🔄 Atualizando vault..."
ansible-vault edit "ansible/inventory/${ENVIRONMENT}/group_vars/all/vault.yml"
# Alterar: vault_mysql_root_password ou vault_postgres_password

# 4. Re-deploy aplicações que dependem do banco
echo "🚀 Re-deploy de aplicações..."
ansible-playbook \
    -i "ansible/inventory/${ENVIRONMENT}/hosts.yml" \
    ansible/playbooks/deploy-docker-service.yml \
    --tags database

# 5. Testar conexão
echo "✅ Testando conexão ao banco..."
case $DB_TYPE in
    mysql)
        docker exec -it mysql mysql -u root -p"${NEW_PASSWORD}" -e "SELECT 1;"
        ;;
    postgresql)
        docker exec -it postgres psql -U postgres -c "SELECT 1;"
        ;;
esac

echo "✅ Rotação de senha ${DB_TYPE} concluída!"
```

#### Checklist Pós-Rotação

- [ ] Testar conexão da aplicação ao banco
- [ ] Verificar logs de erro
- [ ] Atualizar backups (se necessário)
- [ ] Atualizar ferramentas de monitoramento
- [ ] Documentar mudança

---

### 4. Rotação de Tokens de API

**Criticidade**: 🟡 Média
**Frequência**: 30 dias
**Tempo estimado**: 5-10 minutos por token

#### Procedimento Geral

```bash
# 1. Gerar novo token no provedor (GitHub, AWS, etc.)
# Interface web do provedor → Generate new token

# 2. Atualizar vault
ansible-vault edit ansible/inventory/prod/group_vars/all/vault.yml
# Alterar: vault_api_token_github, vault_api_token_aws, etc.

# 3. Re-deploy serviços que usam o token
ansible-playbook \
    -i ansible/inventory/prod/hosts.yml \
    ansible/playbooks/deploy-docker-service.yml

# 4. Revogar token antigo no provedor
# Interface web do provedor → Revoke old token

# 5. Testar funcionalidade
curl -H "Authorization: Bearer ${NEW_TOKEN}" https://api.example.com/test
```

#### Tokens Específicos

**GitHub Personal Access Token**:
```bash
# 1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
# 2. Generate new token → Copiar token
# 3. Atualizar vault_github_token
# 4. Atualizar GitHub Secrets do repositório (se usado em CI/CD)
# 5. Revogar token antigo
```

**AWS Access Keys**:
```bash
# 1. AWS Console → IAM → Users → Security credentials
# 2. Create access key → Copiar Access Key ID e Secret Access Key
# 3. Atualizar vault_aws_access_key_id e vault_aws_secret_access_key
# 4. Atualizar ~/.aws/credentials (se necessário)
# 5. Inativar chave antiga
# 6. Aguardar 24h e deletar chave antiga
```

---

### 5. Rotação de Chaves SSH

**Criticidade**: 🟠 Alta
**Frequência**: 365 dias
**Tempo estimado**: 30-40 minutos

```bash
#!/usr/bin/env bash
# rotate-ssh-keys.sh

set -euo pipefail

ENVIRONMENT=${1:-dev}
KEY_TYPE=${2:-ed25519}  # rsa, ed25519, ecdsa

echo "🔐 Rotacionando chaves SSH - ${ENVIRONMENT} - ${KEY_TYPE}"

# 1. Gerar novo par de chaves
echo "📝 Gerando novo par de chaves ${KEY_TYPE}..."
ssh-keygen -t "$KEY_TYPE" -C "ansible@$(hostname)" \
    -f ".secrets/ssh/id_${KEY_TYPE}.new" -N ""

# 2. Distribuir chave pública para servidores
echo "📤 Distribuindo chave pública..."
ansible -i "ansible/inventory/${ENVIRONMENT}/hosts.yml" all \
    -m authorized_key \
    -a "user=ansible key={{ lookup('file', '.secrets/ssh/id_${KEY_TYPE}.new.pub') }}" \
    --become

# 3. Testar nova chave
echo "✅ Testando nova chave..."
ssh -i ".secrets/ssh/id_${KEY_TYPE}.new" \
    -o StrictHostKeyChecking=no \
    ansible@$(ansible -i "ansible/inventory/${ENVIRONMENT}/hosts.yml" all --list-hosts | tail -1) \
    "echo 'SSH key test successful'"

# 4. Remover chave antiga dos servidores
echo "🗑️  Removendo chave antiga..."
ansible -i "ansible/inventory/${ENVIRONMENT}/hosts.yml" all \
    -m authorized_key \
    -a "user=ansible key={{ lookup('file', '.secrets/ssh/id_${KEY_TYPE}.pub') }} state=absent" \
    --become

# 5. Substituir chaves localmente
mv ".secrets/ssh/id_${KEY_TYPE}" ".secrets/ssh/id_${KEY_TYPE}.old.$(date +%Y%m%d)"
mv ".secrets/ssh/id_${KEY_TYPE}.pub" ".secrets/ssh/id_${KEY_TYPE}.pub.old.$(date +%Y%m%d)"
mv ".secrets/ssh/id_${KEY_TYPE}.new" ".secrets/ssh/id_${KEY_TYPE}"
mv ".secrets/ssh/id_${KEY_TYPE}.new.pub" ".secrets/ssh/id_${KEY_TYPE}.pub"
chmod 600 ".secrets/ssh/id_${KEY_TYPE}"

# 6. Atualizar ansible.cfg (se necessário)
sed -i "s/id_[^=]*\.old/id_${KEY_TYPE}/g" ansible/ansible.cfg

echo "✅ Rotação de chaves SSH concluída!"
echo "🗑️  Chaves antigas salvas em: .secrets/ssh/*.old.$(date +%Y%m%d)"
echo "⚠️  Deletar chaves antigas após 30 dias"
```

---

### 6. Rotação de Secrets do GitHub (CI/CD)

**Criticidade**: 🟠 Alta
**Frequência**: 90 dias
**Tempo estimado**: 15-20 minutos

#### Via GitHub CLI

```bash
#!/usr/bin/env bash
# rotate-github-secrets.sh

set -euo pipefail

REPO="organization/repository"

echo "🔐 Rotacionando GitHub Secrets - ${REPO}"

# 1. Gerar novos valores
NEW_ANSIBLE_VAULT_PASS=$(openssl rand -base64 32)
NEW_SSH_PRIVATE_KEY=$(cat .secrets/ssh/id_ed25519)

# 2. Atualizar secrets via GitHub CLI
gh secret set ANSIBLE_VAULT_PASSWORD \
    --repo "$REPO" \
    --body "$NEW_ANSIBLE_VAULT_PASS"

gh secret set SSH_PRIVATE_KEY \
    --repo "$REPO" \
    --body "$NEW_SSH_PRIVATE_KEY"

# 3. Listar secrets atualizados
echo "✅ Secrets atualizados:"
gh secret list --repo "$REPO"

echo "✅ Rotação de GitHub Secrets concluída!"
```

#### Via Interface Web

1. GitHub → Repositório → Settings → Secrets and variables → Actions
2. Clicar em cada secret e atualizar valor
3. Confirmar atualização
4. Testar pipeline CI/CD

---

## Auditoria e Rastreamento

### Log de Rotações

Manter registro de todas as rotações em `.secrets/rotation_audit.log`:

```
# Format: YYYY-MM-DD | Tipo | Ambiente | Responsável | Próxima Rotação
2026-03-20 | Vault Password | ALL | João Silva | 2026-09-16
2026-03-20 | SSH Keys | Production | João Silva | 2027-03-20
2026-03-15 | MySQL Password | Production | Maria Santos | 2026-05-14
2026-03-10 | GitHub Token | CI/CD | Pedro Costa | 2026-04-09
```

### Script de Auditoria

```bash
#!/usr/bin/env bash
# audit-credentials.sh

set -euo pipefail

echo "📊 Auditoria de Credenciais"
echo "==========================="
echo ""

# Verificar quando cada credencial precisa ser rotacionada
AUDIT_LOG=".secrets/rotation_audit.log"

if [ ! -f "$AUDIT_LOG" ]; then
    echo "⚠️  Arquivo de auditoria não encontrado: $AUDIT_LOG"
    exit 1
fi

TODAY=$(date +%Y-%m-%d)

while IFS='|' read -r date type env user next_rotation; do
    # Calcular dias até próxima rotação
    next_rotation_clean=$(echo "$next_rotation" | tr -d ' ')
    days_until=$(( ($(date -d "$next_rotation_clean" +%s) - $(date -d "$TODAY" +%s)) / 86400 ))

    status="✅ OK"
    if [ $days_until -le 0 ]; then
        status="🔴 VENCIDO"
    elif [ $days_until -le 7 ]; then
        status="🟠 URGENTE"
    elif [ $days_until -le 30 ]; then
        status="🟡 ATENÇÃO"
    fi

    echo "$status | Tipo: $type | Env: $env | Próxima: $next_rotation_clean (${days_until}d)"
done < "$AUDIT_LOG"

echo ""
echo "==========================="
echo "Legenda:"
echo "  🔴 VENCIDO: Rotacionar IMEDIATAMENTE"
echo "  🟠 URGENTE: Rotacionar nos próximos 7 dias"
echo "  🟡 ATENÇÃO: Rotacionar nos próximos 30 dias"
echo "  ✅ OK: Dentro do prazo"
```

---

## Checklist Geral de Rotação

### Antes da Rotação

- [ ] Notificar equipe (com antecedência de 48h para prod)
- [ ] Verificar janela de manutenção
- [ ] Fazer backup completo
- [ ] Preparar rollback plan
- [ ] Revisar documentação e procedimentos

### Durante a Rotação

- [ ] Seguir procedimento específico da credencial
- [ ] Registrar todos os passos executados
- [ ] Manter comunicação com a equipe
- [ ] Monitorar logs e alertas

### Após a Rotação

- [ ] Testar funcionalidades críticas
- [ ] Verificar logs de erro
- [ ] Atualizar documentação
- [ ] Registrar rotação no audit log
- [ ] Atualizar gerenciador de senhas
- [ ] Deletar credenciais antigas após período de retenção
- [ ] Enviar relatório de rotação

---

## Troubleshooting

### Problema: "Ansible playbook falhou após rotação"

**Causa**: Nova credencial não foi atualizada corretamente

**Solução**:
1. Reverter para credencial antiga (se ainda válida)
2. Verificar vault: `ansible-vault view ansible/inventory/*/group_vars/all/vault.yml`
3. Corrigir credencial e tentar novamente

### Problema: "Aplicação não conecta ao banco após rotação"

**Causa**: Containers não foram reiniciados com nova senha

**Solução**:
```bash
# Re-deploy da aplicação
ansible-playbook ansible/playbooks/deploy-docker-service.yml --tags database

# Ou reiniciar containers manualmente
docker compose down && docker compose up -d
```

### Problema: "CI/CD pipeline falhou após rotação de secrets"

**Causa**: Secrets do GitHub/GitLab não foram atualizados

**Solução**:
1. Verificar secrets: `gh secret list`
2. Atualizar secrets faltantes
3. Re-executar pipeline

---

## Ferramentas Recomendadas

### Gerenciadores de Senhas

- **1Password Teams**: Compartilhamento seguro entre equipe
- **LastPass Business**: Auditoria de acessos
- **Bitwarden**: Open-source, self-hosted

### Automação

- **HashiCorp Vault**: Rotação automática de credenciais
- **AWS Secrets Manager**: Rotação gerenciada para AWS
- **Azure Key Vault**: Rotação gerenciada para Azure

### Auditoria

- **Teleport**: Auditoria de acessos SSH
- **Boundary** (HashiCorp): Controle de acesso zero-trust
- **StrongDM**: Auditoria e gravação de sessões

---

## Compliance e Regulamentações

### SOC 2

✅ Rotação periódica demonstra controles de acesso
✅ Audit log atende requisitos de rastreabilidade

### ISO 27001

✅ Política de rotação atende A.9.4.3 (Password management system)
✅ Procedimentos documentados atendem A.5.1.1

### LGPD

✅ Rotação de credenciais fortalece Art. 46 (Segurança)
✅ Audit log atende Art. 37 (Relatório de impacto)

---

## Referências

- [NIST Password Guidelines](https://pages.nist.gov/800-63-3/sp800-63b.html)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [CIS Controls](https://www.cisecurity.org/controls/)

---

**Última atualização**: 2026-03-20
**Versão do guia**: 1.0.0
**Próxima revisão**: 2026-06-20
