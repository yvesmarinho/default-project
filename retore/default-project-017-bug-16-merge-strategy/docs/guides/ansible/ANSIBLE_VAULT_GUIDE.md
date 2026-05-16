# Guia de Uso: Ansible Vault

## O que é Ansible Vault?

Ansible Vault é uma ferramenta de encriptação integrada ao Ansible para proteger dados sensíveis em playbooks, inventários e variáveis. Ele usa criptografia AES256 para garantir que credenciais, tokens e outras informações confidenciais nunca sejam armazenadas em texto plano.

## Por que usar Ansible Vault?

✅ **Segurança**: Credenciais encriptadas com AES256
✅ **Versionamento seguro**: Commit de arquivos encriptados no Git
✅ **Controle de acesso**: Apenas quem tem a senha pode desencriptar
✅ **Auditoria**: Histórico de mudanças mantido no Git
✅ **Compliance**: Atende requisitos de segurança (SOC2, ISO27001, LGPD)

---

## Configuração Inicial

### 1. Criar Senha do Vault

A senha do vault deve ser armazenada em `.secrets/.vault_pass` (nunca versionada):

```bash
# Gerar senha forte (32 bytes em base64)
openssl rand -base64 32 > .secrets/.vault_pass

# Proteger arquivo (permissões apenas para o dono)
chmod 600 .secrets/.vault_pass
```

### 2. Configurar ansible.cfg

Adicionar configuração para usar o arquivo de senha automaticamente:

```ini
[defaults]
vault_password_file = .secrets/.vault_pass
```

### 3. Validar Configuração

```bash
# Verificar se senha está configurada
cat .secrets/.vault_pass

# Verificar se arquivo está protegido
ls -l .secrets/.vault_pass
# Deve mostrar: -rw------- (600)
```

---

## Estrutura Recomendada

### Organização de Variáveis por Ambiente

```
ansible/
├── inventory/
│   ├── dev/
│   │   └── group_vars/
│   │       └── all/
│   │           ├── vars.yml          # Variáveis públicas
│   │           └── vault.yml         # Variáveis encriptadas
│   ├── staging/
│   │   └── group_vars/
│   │       └── all/
│   │           ├── vars.yml
│   │           └── vault.yml
│   └── prod/
│       └── group_vars/
│           └── all/
│               ├── vars.yml
│               └── vault.yml
└── ansible.cfg
```

### Padrão de Nomenclatura

**vault.yml** (encriptado):
```yaml
---
# Sempre usar prefixo vault_
vault_mysql_root_password: "SuperSecretPassword123!"
vault_mysql_user_password: "AnotherSecretPass456!"
vault_ssh_private_key_passphrase: "MySSHKeyPassphrase789!"
vault_api_token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
vault_portainer_admin_password: "PortainerAdminPass000!"
```

**vars.yml** (não encriptado):
```yaml
---
# Variáveis públicas que referenciam vault
mysql_root_password: "{{ vault_mysql_root_password }}"
mysql_user_password: "{{ vault_mysql_user_password }}"
ssh_key_passphrase: "{{ vault_ssh_private_key_passphrase }}"
api_token: "{{ vault_api_token }}"
portainer_admin_password: "{{ vault_portainer_admin_password }}"

# Configurações não sensíveis
mysql_host: "localhost"
mysql_port: 3306
mysql_database: "myapp"
```

---

## Comandos Essenciais

### Criar Arquivo Vault

```bash
# Criar novo arquivo encriptado
ansible-vault create ansible/inventory/dev/group_vars/all/vault.yml
```

Isso abrirá seu editor padrão para inserir o conteúdo. Ao salvar, o arquivo será automaticamente encriptado.

### Editar Arquivo Vault

```bash
# Editar arquivo encriptado existente
ansible-vault edit ansible/inventory/dev/group_vars/all/vault.yml
```

### Ver Conteúdo (sem editar)

```bash
# Visualizar conteúdo desencriptado
ansible-vault view ansible/inventory/dev/group_vars/all/vault.yml
```

### Encriptar Arquivo Existente

```bash
# Encriptar arquivo que está em texto plano
ansible-vault encrypt ansible/inventory/dev/group_vars/all/secrets.yml
```

### Desencriptar Arquivo

```bash
# Desencriptar arquivo (use com cuidado!)
ansible-vault decrypt ansible/inventory/dev/group_vars/all/vault.yml
```

⚠️ **ATENÇÃO**: Depois de desencriptar, o arquivo fica em texto plano. Sempre re-encriptar antes de commitar!

### Re-encriptar com Nova Senha

```bash
# Mudar senha do vault (rotação de credenciais)
ansible-vault rekey ansible/inventory/dev/group_vars/all/vault.yml
```

### Encriptar String Individual

```bash
# Encriptar apenas uma string (útil para inline vars)
ansible-vault encrypt_string 'SuperSecretPassword' --name 'mysql_password'
```

Saída:
```yaml
mysql_password: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          66386439653632336337313...
```

---

## Uso em Playbooks

### Executar Playbook com Vault

#### Usando Arquivo de Senha (Recomendado)

Se `vault_password_file` está configurado em `ansible.cfg`:

```bash
# Execução normal, senha lida automaticamente
ansible-playbook ansible/playbooks/deploy.yml -i ansible/inventory/prod/hosts.yml
```

#### Pedindo Senha Manualmente

```bash
# Pedir senha interativamente
ansible-playbook ansible/playbooks/deploy.yml --ask-vault-pass
```

#### Especificando Arquivo de Senha

```bash
# Especificar arquivo de senha explicitamente
ansible-playbook ansible/playbooks/deploy.yml --vault-password-file .secrets/.vault_pass
```

### Exemplo de Playbook Usando Variáveis Vault

```yaml
---
- name: Deploy Application with Encrypted Credentials
  hosts: app_servers
  gather_facts: true
  become: true

  tasks:
    - name: Create .env file from template
      template:
        src: templates/app.env.j2
        dest: "/opt/myapp/.env"
        mode: '0600'
        owner: app
        group: app
      vars:
        db_password: "{{ mysql_root_password }}"  # Vem de vault
        api_secret: "{{ api_token }}"              # Vem de vault

    - name: Deploy Docker Compose service
      community.docker.docker_compose:
        project_src: "/opt/myapp"
        state: present
      environment:
        MYSQL_ROOT_PASSWORD: "{{ mysql_root_password }}"
```

### Template Jinja2 com Variáveis Vault

**templates/app.env.j2**:
```jinja2
# Application Environment Variables
# Generated by Ansible - DO NOT EDIT MANUALLY

# Database Configuration
DB_HOST={{ mysql_host }}
DB_PORT={{ mysql_port }}
DB_NAME={{ mysql_database }}
DB_USER=root
DB_PASSWORD={{ mysql_root_password }}

# API Configuration
API_TOKEN={{ api_token }}

# Admin Credentials
ADMIN_PASSWORD={{ portainer_admin_password }}
```

---

## Boas Práticas

### ✅ DO (Faça)

1. **Sempre use prefixo `vault_`** em variáveis encriptadas:
   ```yaml
   vault_api_key: "secret123"
   ```

2. **Separe variáveis públicas de privadas**:
   - `vars.yml` → configurações públicas
   - `vault.yml` → credenciais encriptadas

3. **Um vault por ambiente**:
   ```
   inventory/dev/group_vars/all/vault.yml
   inventory/staging/group_vars/all/vault.yml
   inventory/prod/group_vars/all/vault.yml
   ```

4. **Proteja arquivo de senha**:
   ```bash
   chmod 600 .secrets/.vault_pass
   ```

5. **Versione arquivos encriptados**:
   ```bash
   git add ansible/inventory/*/group_vars/all/vault.yml
   git commit -m "feat(vault): add encrypted credentials"
   ```

6. **Rotacione senhas periodicamente**:
   - Vault password: 180 dias
   - Credenciais: 60-90 dias

### ❌ DON'T (Não Faça)

1. ❌ **Nunca commite arquivos desencriptados**:
   ```bash
   # Verificar se arquivo está encriptado antes de commit
   head -1 ansible/inventory/dev/group_vars/all/vault.yml
   # Deve começar com: $ANSIBLE_VAULT;1.1;AES256
   ```

2. ❌ **Nunca versione `.vault_pass`**:
   ```gitignore
   # .gitignore
   .secrets/
   *.vault_pass
   ```

3. ❌ **Nunca use mesma senha em todos ambientes**:
   - Dev, Staging e Prod devem ter vaults separados

4. ❌ **Nunca coloque credenciais em `vars.yml`**:
   - Use `vault.yml` e referencie com `{{ vault_* }}`

5. ❌ **Nunca compartilhe senha do vault por email/chat**:
   - Use gerenciador de senhas (1Password, LastPass)
   - Ou compartilhe pessoalmente

---

## Troubleshooting

### Erro: "Vault password file not found"

**Causa**: Arquivo `.secrets/.vault_pass` não existe

**Solução**:
```bash
openssl rand -base64 32 > .secrets/.vault_pass
chmod 600 .secrets/.vault_pass
```

### Erro: "Decryption failed"

**Causa**: Senha incorreta no arquivo `.vault_pass`

**Solução**:
1. Verificar conteúdo do arquivo de senha
2. Confirmar que é a senha correta para este vault
3. Se esqueceu a senha, é necessário recriar o vault do zero

### Erro: "ERROR! Attempting to decrypt but no vault secrets found"

**Causa**: Arquivo não está encriptado ou corrompido

**Solução**:
```bash
# Verificar se arquivo está encriptado
head -1 ansible/inventory/dev/group_vars/all/vault.yml

# Se não estiver encriptado, encriptar agora
ansible-vault encrypt ansible/inventory/dev/group_vars/all/vault.yml
```

### Ver se Arquivo Está Encriptado

```bash
# Ver primeira linha do arquivo
head -1 ansible/inventory/dev/group_vars/all/vault.yml

# Se encriptado, mostrará:
# $ANSIBLE_VAULT;1.1;AES256

# Se não encriptado, mostrará o conteúdo em texto plano
```

### Recuperar de Arquivo Corrompido

Se o arquivo vault estiver corrompido:

1. **Se tiver backup**:
   ```bash
   cp backup/vault.yml ansible/inventory/dev/group_vars/all/vault.yml
   ```

2. **Se não tiver backup**:
   - Recriar arquivo vault do zero
   - Inserir credenciais novamente
   - Atualizar senhas nos servidores se necessário

---

## Rotação de Credenciais

### Quando Rotacionar

| Tipo de Credencial | Frequência | Criticidade |
|-------------------|------------|-------------|
| Vault Password | 180 dias | Crítica |
| Senhas SSH | 90 dias | Alta |
| Senhas MySQL | 60 dias | Alta |
| Tokens API | 30 dias | Média |
| Chaves SSH | 1 ano | Alta |

### Como Rotacionar Vault Password

```bash
# 1. Gerar nova senha
openssl rand -base64 32 > .secrets/.vault_pass.new

# 2. Re-encriptar todos arquivos vault
find ansible/inventory -name "vault.yml" | while read vault_file; do
    ansible-vault rekey "${vault_file}" \
        --vault-password-file .secrets/.vault_pass \
        --new-vault-password-file .secrets/.vault_pass.new
done

# 3. Substituir arquivo de senha
mv .secrets/.vault_pass.new .secrets/.vault_pass
chmod 600 .secrets/.vault_pass

# 4. Testar
ansible-vault view ansible/inventory/dev/group_vars/all/vault.yml
```

### Como Rotacionar Credenciais

```bash
# 1. Gerar nova senha
NEW_PASS=$(openssl rand -base64 24)

# 2. Atualizar no servidor remoto
# (exemplo para senha MySQL)
docker exec -it mysql mysql -u root -p -e \
    "ALTER USER 'root'@'%' IDENTIFIED BY '${NEW_PASS}';"

# 3. Atualizar vault
ansible-vault edit ansible/inventory/prod/group_vars/all/vault.yml
# Alterar vault_mysql_root_password para nova senha

# 4. Re-deploy da aplicação
ansible-playbook ansible/playbooks/deploy.yml -i ansible/inventory/prod/hosts.yml
```

---

## Integração com CI/CD

### GitHub Actions

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Ansible Vault Password
        run: |
          echo "${{ secrets.ANSIBLE_VAULT_PASSWORD }}" > .secrets/.vault_pass
          chmod 600 .secrets/.vault_pass

      - name: Run Ansible Playbook
        run: |
          ansible-playbook ansible/playbooks/deploy.yml \
            -i ansible/inventory/prod/hosts.yml
```

**⚠️ Importante**: Adicionar `ANSIBLE_VAULT_PASSWORD` nos Secrets do GitHub.

### GitLab CI

```yaml
deploy:
  stage: deploy
  script:
    - echo "$ANSIBLE_VAULT_PASSWORD" > .secrets/.vault_pass
    - chmod 600 .secrets/.vault_pass
    - ansible-playbook ansible/playbooks/deploy.yml -i ansible/inventory/prod/hosts.yml
  only:
    - main
```

---

## Checklist de Segurança

Antes de commitar código com Ansible Vault:

- [ ] Arquivo `.secrets/.vault_pass` está no `.gitignore`
- [ ] Arquivos vault estão encriptados (`head -1` mostra `$ANSIBLE_VAULT`)
- [ ] Permissões do `.vault_pass` são 600 (`ls -l`)
- [ ] Variáveis sensíveis usam prefixo `vault_`
- [ ] `vars.yml` não contém credenciais em texto plano
- [ ] Cada ambiente (dev/staging/prod) tem vault separado
- [ ] Senha do vault está armazenada em gerenciador de senhas
- [ ] Documentação de rotação está atualizada

---

## Referências

- [Ansible Vault Documentation](https://docs.ansible.com/ansible/latest/vault_guide/index.html)
- [Ansible Best Practices](https://docs.ansible.com/ansible/latest/tips_tricks/ansible_tips_tricks.html)
- [AES256 Encryption](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)

---

**Última atualização**: 2026-03-20
**Versão do guia**: 1.0.0
