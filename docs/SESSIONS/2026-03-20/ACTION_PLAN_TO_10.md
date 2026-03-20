# 🎯 Plano de Ação: De 9.4 para 10/10

**Projeto**: enterprise-infra-docker
**Score Atual**: 9.4/10
**Score Alvo**: 10/10
**Data**: 2026-03-20
**Baseado em**: `PROJECT_VALIDATION_enterprise-infra-docker.md`

---

## 📊 Status por Categoria

| Categoria | Atual | Alvo | Gap | Prioridade |
|-----------|-------|------|-----|------------|
| 1. Estrutura | 10/10 | 10/10 | 0 | N/A |
| 2. VS Code | 10/10 | 10/10 | 0 | N/A |
| 3. Documentação | 9/10 | 10/10 | -1 | P1 |
| 4. Profile Compliance | 10/10 | 10/10 | 0 | N/A |
| 5. Código Python | 9/10 | 10/10 | -1 | P0 |
| 6. Ansible | 9/10 | 10/10 | -1 | P1 |
| 7. Docker Templates | 10/10 | 10/10 | 0 | N/A |
| 8. Segurança | 8/10 | 10/10 | -2 | P0 |
| 9. Melhorias de Estrutura | N/A | ⭐ Bônus | 0 | P2 |

**Total de Ações**: 27 ações distribuídas em 5 categorias (23 principais + 4 melhorias estruturais)

---

## 🔴 CATEGORIA 3: Documentação (9/10 → 10/10)

**Gap**: -1 ponto | **Prioridade**: P1 | **Esforço Estimado**: 4-6h

### Ações Necessárias

#### 3.1 Completar README.md (P1)
**Descrição**: Resolver 2 string replacements pendentes mencionados no TODO.md

**Tarefas**:
1. Abrir `/home/yves_marinho/VyaJobs/enterprise-infra-docker/README.md`
2. Identificar placeholders pendentes (ex: `{{PROJECT_NAME}}`, `{{DESCRIPTION}}`)
3. Substituir por valores corretos:
   - `{{PROJECT_NAME}}` → `enterprise-infra-docker`
   - `{{DESCRIPTION}}` → Descrição real do projeto
4. Validar com `grep -r "{{.*}}" README.md` (deve retornar vazio)

**Critério de Sucesso**: ✅ Nenhum placeholder não resolvido no README

**Tempo estimado**: 30 min

---

#### 3.2 Adicionar Troubleshooting Guide Completo (P1)
**Descrição**: Expandir documentação de troubleshooting com cenários comuns

**Tarefas**:
1. Criar `docs/TROUBLESHOOTING.md` com seções:
   ```markdown
   # Troubleshooting Guide

   ## SSH Connection Issues
   - Problema: "Permission denied (publickey)"
   - Solução: Verificar `.secrets/ssh/id_rsa` permissions (chmod 600)

   ## Docker Container Not Starting
   - Problema: Container reinicia constantemente
   - Solução: Verificar logs com `docker compose logs -f <service>`

   ## Ansible Playbook Failures
   - Problema: "Host unreachable"
   - Solução: Verificar inventory, testar com `ansible all -m ping`

   ## MySQL Connection Refused
   - Problema: "Can't connect to MySQL server"
   - Solução: Verificar container status, portas, credenciais em .env

   ## Portainer Not Accessible
   - Problema: 404 na interface web
   - Solução: Verificar se container está rodando, restart se necessário
   ```

2. Adicionar link no `docs/INDEX.md`:
   ```markdown
   - [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Guia de resolução de problemas comuns
   ```

3. Adicionar referência no `README.md`:
   ```markdown
   ## 🔧 Troubleshooting

   Para problemas comuns e soluções, consulte [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md).
   ```

**Critério de Sucesso**: ✅ Guia com pelo menos 5 cenários de troubleshooting documentados

**Tempo estimado**: 2h

---

#### 3.3 Validar e Corrigir Links Quebrados (P1)
**Descrição**: Escanear e corrigir todos os links internos na documentação

**Tarefas**:
1. Escanear links em todos os arquivos markdown:
   ```bash
   cd /home/yves_marinho/VyaJobs/enterprise-infra-docker
   find docs/ -name "*.md" -exec grep -H '\[.*\](.*)' {} \;
   ```

2. Validar cada link:
   - Links relativos: verificar se arquivo/seção existe
   - Links para código: verificar se caminho está correto
   - Links para templates: verificar se arquivo existe

3. Corrigir links quebrados encontrados

4. Opcionalmente, adicionar script de validação:
   ```bash
   # scripts/validate-docs-links.sh
   #!/usr/bin/env bash
   # Valida links em arquivos markdown
   find docs/ -name "*.md" | while read file; do
       # Extract and validate links
       grep -oP '\[.*?\]\(\K[^\)]+' "$file" | while read link; do
           if [[ ! -f "$link" ]]; then
               echo "❌ Broken link in $file: $link"
           fi
       done
   done
   ```

**Critério de Sucesso**: ✅ Nenhum link interno quebrado na documentação

**Tempo estimado**: 1h

---

#### 3.4 Adicionar Convenções Técnicas (P2)
**Descrição**: Documentar padrões e convenções do projeto

**Tarefas**:
1. Criar `docs/CONVENTIONS.md`:
   ```markdown
   # Convenções Técnicas

   ## Estrutura de Código
   - Python: PEP 8, line length 88 (black)
   - Ansible: YAML com 2 espaços de indentação
   - Shell: shellcheck compliance

   ## Nomenclatura
   - Arquivos Python: `snake_case.py`
   - Arquivos Ansible: `kebab-case.yml`
   - Variáveis de ambiente: `UPPER_SNAKE_CASE`
   - Playbooks: `verbo-objeto.yml` (ex: `deploy-docker-service.yml`)

   ## Git Commits
   - Formato: `tipo(escopo): descrição`
   - Tipos: feat, fix, docs, refactor, test, chore
   - Escopos: ansible, docker, python, docs, security

   ## Organização de Arquivos
   - Código Python: `src/`
   - Scripts de automação: `scripts/`
   - Playbooks Ansible: `ansible/playbooks/`
   - Templates Docker: `docker-compose-templates/`
   - Credenciais: `.secrets/` (NUNCA versionar)

   ## Type Hints (Python)
   - Todas as funções públicas devem ter type hints
   - Usar `typing` para tipos complexos
   - Return types sempre explícitos

   ## Logging
   - Usar logger do módulo `src.utils.logger`
   - Níveis: DEBUG (desenvolvimento), INFO (operações), WARNING (atenção), ERROR (falhas)

   ## Testes
   - Cobertura mínima: 80%
   - Testes unitários: `tests/unit/`
   - Testes de integração: `tests/integration/`
   - Pytest fixtures: usar `conftest.py`
   ```

2. Adicionar link no `docs/INDEX.md`

**Critério de Sucesso**: ✅ Convenções documentadas em todas as áreas principais

**Tempo estimado**: 1h

---

#### 3.5 Adicionar Changelog (P2)
**Descrição**: Criar CHANGELOG.md para rastrear mudanças

**Tarefas**:
1. Criar `CHANGELOG.md` na raiz:
   ```markdown
   # Changelog

   Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

   O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
   e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

   ## [Unreleased]

   ### Added
   - Estrutura inicial do projeto via scaffold.py
   - 5 templates Docker Compose (PostgreSQL, Portainer, Adminer, Dashy)
   - SSHClient com suporte a chaves SSH
   - CLIs para diagnóstico (docker-health, mysql-diag)
   - Playbooks Ansible (deploy, health-check, troubleshoot)
   - Documentação completa (README, TODO, INDEX, QUICK_GUIDE)

   ### Security
   - Configuração de `.secrets/` para credenciais
   - `.gitignore` protegendo arquivos sensíveis

   ## [0.1.0] - 2026-03-16

   ### Added
   - Projeto criado via `scaffold.py` v1.0.0
   - Profile: devops-infrastructure
   - Domínio: infrastructure
   ```

2. Adicionar link no README.md:
   ```markdown
   ## 📝 Changelog

   Veja [CHANGELOG.md](CHANGELOG.md) para histórico de mudanças.
   ```

**Critério de Sucesso**: ✅ CHANGELOG.md criado e vinculado na documentação

**Tempo estimado**: 30 min

---

### ✅ Checklist de Conclusão: Documentação

- [ ] README.md: 2 string replacements resolvidos
- [ ] TROUBLESHOOTING.md: criado com 5+ cenários
- [ ] Links validados: nenhum link quebrado
- [ ] CONVENTIONS.md: criado com padrões documentados
- [ ] CHANGELOG.md: criado na raiz
- [ ] docs/INDEX.md: atualizado com novos documentos

**Resultado Esperado**: 10/10 na categoria Documentação

---

## 🔴 CATEGORIA 5: Código Python (9/10 → 10/10)

**Gap**: -1 ponto | **Prioridade**: P0 | **Esforço Estimado**: 8-12h

### Ações Necessárias

#### 5.1 Implementar Testes Unitários (P0)
**Descrição**: Criar suite completa de testes unitários para todos os módulos Python

**Tarefas**:

##### 5.1.1 Configurar Ambiente de Testes
1. Adicionar dependências de teste no `pyproject.toml`:
   ```toml
   [project.optional-dependencies]
   test = [
       "pytest>=8.0.0",
       "pytest-cov>=4.1.0",
       "pytest-mock>=3.12.0",
       "pytest-asyncio>=0.23.0",
       "freezegun>=1.4.0",
   ]
   ```

2. Criar `pytest.ini` na raiz:
   ```ini
   [pytest]
   testpaths = tests
   python_files = test_*.py
   python_classes = Test*
   python_functions = test_*
   addopts =
       --verbose
       --cov=src
       --cov-report=html
       --cov-report=term-missing
       --cov-fail-under=80
   ```

3. Criar estrutura de testes:
   ```bash
   mkdir -p tests/{unit,integration,fixtures}
   touch tests/__init__.py
   touch tests/conftest.py
   ```

**Tempo estimado**: 1h

---

##### 5.1.2 Testes para `src/utils/ssh_client.py`
1. Criar `tests/unit/test_ssh_client.py`:
   ```python
   """Testes unitários para SSHClient."""
   import pytest
   from unittest.mock import Mock, patch, MagicMock
   from pathlib import Path
   from src.utils.ssh_client import SSHClient


   @pytest.fixture
   def mock_env_vars(monkeypatch):
       """Mock de variáveis de ambiente."""
       monkeypatch.setenv("SSH_HOST", "test.example.com")
       monkeypatch.setenv("SSH_PORT", "22")
       monkeypatch.setenv("SSH_USER", "testuser")
       monkeypatch.setenv("SSH_KEY_PATH", "/path/to/key")


   @pytest.fixture
   def ssh_client(mock_env_vars):
       """Fixture de SSHClient."""
       with patch("src.utils.ssh_client.paramiko.SSHClient"):
           return SSHClient()


   class TestSSHClientInit:
       """Testes de inicialização."""

       def test_init_loads_env_vars(self, mock_env_vars):
           """Testa carregamento de variáveis de ambiente."""
           with patch("src.utils.ssh_client.paramiko.SSHClient"):
               client = SSHClient()
               assert client.host == "test.example.com"
               assert client.port == 22
               assert client.username == "testuser"

       def test_init_missing_required_vars(self, monkeypatch):
           """Testa erro quando faltam variáveis obrigatórias."""
           monkeypatch.delenv("SSH_HOST", raising=False)
           with pytest.raises(ValueError, match="SSH_HOST"):
               SSHClient()


   class TestSSHClientConnect:
       """Testes de conexão SSH."""

       def test_connect_with_key(self, ssh_client):
           """Testa conexão usando chave SSH."""
           with patch.object(ssh_client.client, "connect") as mock_connect:
               ssh_client.connect()
               mock_connect.assert_called_once()
               assert "key_filename" in mock_connect.call_args[1]

       def test_connect_with_password(self, monkeypatch):
           """Testa conexão usando senha."""
           monkeypatch.setenv("SSH_PASSWORD", "testpass")
           with patch("src.utils.ssh_client.paramiko.SSHClient") as mock_ssh:
               client = SSHClient()
               client.connect()
               mock_ssh.return_value.connect.assert_called_once()

       def test_connect_timeout(self, ssh_client):
           """Testa timeout de conexão."""
           with patch.object(ssh_client.client, "connect", side_effect=TimeoutError):
               with pytest.raises(TimeoutError):
                   ssh_client.connect()


   class TestSSHClientExecuteCommand:
       """Testes de execução de comandos."""

       def test_execute_command_success(self, ssh_client):
           """Testa execução bem-sucedida de comando."""
           mock_stdout = Mock()
           mock_stdout.read.return_value = b"command output"
           mock_stderr = Mock()
           mock_stderr.read.return_value = b""

           with patch.object(ssh_client.client, "exec_command") as mock_exec:
               mock_exec.return_value = (None, mock_stdout, mock_stderr)

               result = ssh_client.execute_command("ls -la")

               assert result["stdout"] == "command output"
               assert result["stderr"] == ""
               assert result["exit_code"] == 0

       def test_execute_command_with_sudo(self, ssh_client):
           """Testa execução com sudo."""
           ssh_client.sudo_mode = "yes"

           with patch.object(ssh_client.client, "exec_command") as mock_exec:
               ssh_client.execute_command("apt update")

               called_command = mock_exec.call_args[0][0]
               assert "sudo" in called_command

       def test_execute_command_error(self, ssh_client):
           """Testa comando que retorna erro."""
           mock_stdout = Mock()
           mock_stdout.read.return_value = b""
           mock_stderr = Mock()
           mock_stderr.read.return_value = b"command not found"

           with patch.object(ssh_client.client, "exec_command") as mock_exec:
               mock_exec.return_value = (None, mock_stdout, mock_stderr)

               result = ssh_client.execute_command("invalid_command")

               assert result["exit_code"] != 0
               assert "command not found" in result["stderr"]


   class TestSSHClientClose:
       """Testes de fechamento de conexão."""

       def test_close_connection(self, ssh_client):
           """Testa fechamento de conexão."""
           with patch.object(ssh_client.client, "close") as mock_close:
               ssh_client.close()
               mock_close.assert_called_once()
   ```

2. Executar testes:
   ```bash
   pytest tests/unit/test_ssh_client.py -v --cov=src.utils.ssh_client
   ```

**Critério de Sucesso**: ✅ Cobertura ≥ 90% em ssh_client.py

**Tempo estimado**: 3h

---

##### 5.1.3 Testes para `src/diagnostics/container_health.py`
1. Criar `tests/unit/test_container_health.py`:
   ```python
   """Testes unitários para ContainerHealthChecker."""
   import pytest
   from unittest.mock import Mock, patch
   from src.diagnostics.container_health import ContainerHealthChecker


   @pytest.fixture
   def health_checker():
       """Fixture de ContainerHealthChecker."""
       with patch("src.diagnostics.container_health.docker.from_env"):
           return ContainerHealthChecker()


   class TestContainerHealthChecker:
       """Testes de health check de containers."""

       def test_check_all_containers_healthy(self, health_checker):
           """Testa quando todos containers estão saudáveis."""
           mock_container = Mock()
           mock_container.name = "test-container"
           mock_container.status = "running"
           mock_container.attrs = {"State": {"Health": {"Status": "healthy"}}}

           with patch.object(health_checker.client.containers, "list") as mock_list:
               mock_list.return_value = [mock_container]

               results = health_checker.check_all()

               assert len(results) == 1
               assert results[0]["status"] == "healthy"

       def test_check_unhealthy_container(self, health_checker):
           """Testa detecção de container não saudável."""
           mock_container = Mock()
           mock_container.name = "failing-container"
           mock_container.status = "running"
           mock_container.attrs = {"State": {"Health": {"Status": "unhealthy"}}}

           with patch.object(health_checker.client.containers, "list") as mock_list:
               mock_list.return_value = [mock_container]

               results = health_checker.check_all()

               assert results[0]["status"] == "unhealthy"

       def test_check_stopped_container(self, health_checker):
           """Testa container parado."""
           mock_container = Mock()
           mock_container.name = "stopped-container"
           mock_container.status = "exited"

           with patch.object(health_checker.client.containers, "list") as mock_list:
               mock_list.return_value = [mock_container]

               results = health_checker.check_all()

               assert results[0]["status"] == "stopped"
   ```

**Critério de Sucesso**: ✅ Cobertura ≥ 85% em container_health.py

**Tempo estimado**: 2h

---

##### 5.1.4 Testes para `src/diagnostics/mysql_diagnostics.py`
1. Criar `tests/unit/test_mysql_diagnostics.py`:
   ```python
   """Testes unitários para MySQLDiagnostics."""
   import pytest
   from unittest.mock import Mock, patch, MagicMock
   from src.diagnostics.mysql_diagnostics import MySQLDiagnostics


   @pytest.fixture
   def mysql_diag(monkeypatch):
       """Fixture de MySQLDiagnostics."""
       monkeypatch.setenv("MYSQL_HOST", "localhost")
       monkeypatch.setenv("MYSQL_PORT", "3306")
       monkeypatch.setenv("MYSQL_USER", "root")
       monkeypatch.setenv("MYSQL_PASSWORD", "testpass")

       with patch("src.diagnostics.mysql_diagnostics.SSHClient"):
           return MySQLDiagnostics()


   class TestMySQLDiagnostics:
       """Testes de diagnóstico MySQL."""

       def test_check_connection_success(self, mysql_diag):
           """Testa conexão bem-sucedida ao MySQL."""
           mock_result = {"stdout": "mysql: [Warning] Using a password", "exit_code": 0}

           with patch.object(mysql_diag.ssh, "execute_command") as mock_exec:
               mock_exec.return_value = mock_result

               result = mysql_diag.check_connection()

               assert result["status"] == "connected"

       def test_check_connection_failure(self, mysql_diag):
           """Testa falha de conexão ao MySQL."""
           mock_result = {"stderr": "Access denied", "exit_code": 1}

           with patch.object(mysql_diag.ssh, "execute_command") as mock_exec:
               mock_exec.return_value = mock_result

               result = mysql_diag.check_connection()

               assert result["status"] == "failed"

       def test_get_status_variables(self, mysql_diag):
           """Testa leitura de variáveis de status."""
           mock_result = {
               "stdout": "Uptime\t3600\nThreads_connected\t10",
               "exit_code": 0
           }

           with patch.object(mysql_diag.ssh, "execute_command") as mock_exec:
               mock_exec.return_value = mock_result

               status = mysql_diag.get_status_variables()

               assert "Uptime" in status
               assert status["Threads_connected"] == "10"
   ```

**Critério de Sucesso**: ✅ Cobertura ≥ 85% em mysql_diagnostics.py

**Tempo estimado**: 2h

---

##### 5.1.5 Testes para CLIs
1. Criar `tests/unit/test_cli_docker_health.py` e `tests/unit/test_cli_mysql_diag.py`
2. Testar argumentos, saídas, erros
3. Mock de chamadas ao Docker/SSH

**Tempo estimado**: 2h

---

#### 5.2 Adicionar Docstrings Completas (P1)
**Descrição**: Adicionar docstrings em todos os módulos, classes e funções

**Tarefas**:

1. Usar formato Google Style Docstrings:
   ```python
   def execute_command(self, command: str, use_sudo: bool = False) -> dict:
       """Execute um comando SSH no servidor remoto.

       Args:
           command: O comando a ser executado.
           use_sudo: Se True, executa o comando com sudo.

       Returns:
           Dicionário contendo:
               - stdout: Saída padrão do comando
               - stderr: Saída de erro do comando
               - exit_code: Código de saída do comando

       Raises:
           ConnectionError: Se não houver conexão ativa.
           TimeoutError: Se o comando exceder o timeout.

       Examples:
           >>> ssh = SSHClient()
           >>> ssh.connect()
           >>> result = ssh.execute_command("ls -la")
           >>> print(result["stdout"])
       """
   ```

2. Adicionar docstrings em todos os arquivos:
   - `src/utils/ssh_client.py`
   - `src/utils/config.py`
   - `src/utils/logger.py`
   - `src/diagnostics/container_health.py`
   - `src/diagnostics/mysql_diagnostics.py`
   - `src/cli/docker_health.py`
   - `src/cli/mysql_diag.py`

3. Validar com:
   ```bash
   # Verificar docstrings ausentes
   pylint src/ --disable=all --enable=missing-docstring
   ```

**Critério de Sucesso**: ✅ Todas as classes e funções públicas têm docstrings completas

**Tempo estimado**: 3h

---

#### 5.3 Melhorar Type Hints (P2)
**Descrição**: Adicionar type hints em todos os lugares e validar com mypy

**Tarefas**:

1. Adicionar `mypy` ao ambiente de desenvolvimento:
   ```toml
   [project.optional-dependencies]
   dev = [
       "mypy>=1.8.0",
       "types-paramiko>=3.4.0",
       "types-PyYAML>=6.0.0",
   ]
   ```

2. Criar `mypy.ini`:
   ```ini
   [mypy]
   python_version = 3.12
   warn_return_any = True
   warn_unused_configs = True
   disallow_untyped_defs = True
   disallow_incomplete_defs = True
   check_untyped_defs = True
   no_implicit_optional = True
   warn_redundant_casts = True
   warn_unused_ignores = True
   warn_no_return = True
   warn_unreachable = True
   strict_equality = True

   [mypy-docker.*]
   ignore_missing_imports = True

   [mypy-paramiko.*]
   ignore_missing_imports = True
   ```

3. Adicionar type hints onde ausentes:
   ```python
   from typing import Optional, Dict, List, Any

   def get_container_stats(self, container_id: str) -> Dict[str, Any]:
       """..."""

   def list_all_containers(self, include_stopped: bool = False) -> List[Dict[str, str]]:
       """..."""
   ```

4. Executar validação:
   ```bash
   mypy src/
   ```

**Critério de Sucesso**: ✅ `mypy src/` retorna 0 erros

**Tempo estimado**: 2h

---

### ✅ Checklist de Conclusão: Código Python

- [ ] pytest.ini configurado
- [ ] Testes para ssh_client.py (cobertura ≥ 90%)
- [ ] Testes para container_health.py (cobertura ≥ 85%)
- [ ] Testes para mysql_diagnostics.py (cobertura ≥ 85%)
- [ ] Testes para CLIs
- [ ] Cobertura total ≥ 80%
- [ ] Docstrings completas em todos os módulos
- [ ] mypy.ini configurado
- [ ] Type hints completos (mypy passa sem erros)

**Resultado Esperado**: 10/10 na categoria Código Python

---

## 🔴 CATEGORIA 6: Ansible (9/10 → 10/10)

**Gap**: -1 ponto | **Prioridade**: P1 | **Esforço Estimado**: 6-8h

### Ações Necessárias

#### 6.1 Adicionar Playbooks Adicionais (P1)
**Descrição**: Criar playbooks para operações comuns não cobertas

**Tarefas**:

##### 6.1.1 Playbook de Restart de Serviços
1. Criar `ansible/playbooks/restart-docker-service.yml`:
   ```yaml
   ---
   - name: Restart Docker Services
     hosts: docker_hosts
     gather_facts: true
     become: true

     vars_prompt:
       - name: service_name
         prompt: "Nome do serviço Docker Compose"
         private: false
       - name: compose_file_path
         prompt: "Caminho do docker-compose.yml"
         default: "/opt/docker"
         private: false

     tasks:
       - name: Verificar se docker-compose.yml existe
         stat:
           path: "{{ compose_file_path }}/docker-compose.yml"
         register: compose_file

       - name: Falhar se docker-compose.yml não existir
         fail:
           msg: "docker-compose.yml não encontrado em {{ compose_file_path }}"
         when: not compose_file.stat.exists

       - name: Parar serviço Docker Compose
         community.docker.docker_compose:
           project_src: "{{ compose_file_path }}"
           state: absent
         register: stop_result

       - name: Aguardar 5 segundos
         pause:
           seconds: 5

       - name: Iniciar serviço Docker Compose
         community.docker.docker_compose:
           project_src: "{{ compose_file_path }}"
           state: present
           pull: true
         register: start_result

       - name: Exibir resultado
         debug:
           msg: "Serviço {{ service_name }} reiniciado com sucesso"
   ```

**Tempo estimado**: 1h

---

##### 6.1.2 Playbook de Cleanup
1. Criar `ansible/playbooks/docker-cleanup.yml`:
   ```yaml
   ---
   - name: Docker Cleanup and Optimization
     hosts: docker_hosts
     gather_facts: true
     become: true

     vars:
       remove_unused_images: true
       remove_unused_volumes: false  # Cuidado com volumes!
       remove_unused_networks: true

     tasks:
       - name: Parar containers órfãos
         shell: docker ps -aq -f status=exited | xargs -r docker rm
         register: removed_containers
         ignore_errors: true

       - name: Remover imagens sem uso
         shell: docker image prune -af
         when: remove_unused_images
         register: removed_images

       - name: Remover networks sem uso
         shell: docker network prune -f
         when: remove_unused_networks
         register: removed_networks

       - name: Remover volumes sem uso (CUIDADO!)
         shell: docker volume prune -f
         when: remove_unused_volumes
         register: removed_volumes

       - name: Exibir estatísticas de limpeza
         debug:
           msg:
             - "Containers removidos: {{ removed_containers.stdout_lines | length }}"
             - "Imagens limpas: {{ removed_images.stdout if removed_images is defined else 'N/A' }}"
             - "Networks removidas: {{ removed_networks.stdout if removed_networks is defined else 'N/A' }}"
             - "Volumes removidos: {{ removed_volumes.stdout if removed_volumes is defined else 'N/A' }}"

       - name: Exibir uso de disco após cleanup
         shell: df -h /var/lib/docker
         register: disk_usage

       - name: Mostrar uso de disco
         debug:
           var: disk_usage.stdout_lines
   ```

**Tempo estimado**: 1h

---

##### 6.1.3 Playbook de Backup
1. Criar `ansible/playbooks/backup-docker-volumes.yml`:
   ```yaml
   ---
   - name: Backup Docker Volumes and Configs
     hosts: docker_hosts
     gather_facts: true
     become: true

     vars:
       backup_dir: "/opt/backups/docker"
       backup_timestamp: "{{ ansible_date_time.iso8601_basic_short }}"
       volumes_to_backup:
         - postgresql_data
         - portainer_data
         - adminer_config

     tasks:
       - name: Criar diretório de backup
         file:
           path: "{{ backup_dir }}/{{ backup_timestamp }}"
           state: directory
           mode: '0755'

       - name: Parar containers antes do backup
         community.docker.docker_compose:
           project_src: "/opt/docker"
           state: stopped

       - name: Fazer backup de volumes Docker
         shell: >
           docker run --rm
           -v {{ item }}:/source:ro
           -v {{ backup_dir }}/{{ backup_timestamp }}:/backup
           alpine tar czf /backup/{{ item }}.tar.gz -C /source .
         loop: "{{ volumes_to_backup }}"

       - name: Backup de arquivos de configuração
         archive:
           path: "/opt/docker"
           dest: "{{ backup_dir }}/{{ backup_timestamp }}/docker-configs.tar.gz"

       - name: Reiniciar containers
         community.docker.docker_compose:
           project_src: "/opt/docker"
           state: present

       - name: Remover backups antigos (> 7 dias)
         find:
           paths: "{{ backup_dir }}"
           age: 7d
           recurse: false
           file_type: directory
         register: old_backups

       - name: Deletar backups antigos
         file:
           path: "{{ item.path }}"
           state: absent
         loop: "{{ old_backups.files }}"

       - name: Exibir resultado
         debug:
           msg: "Backup concluído em {{ backup_dir }}/{{ backup_timestamp }}"
   ```

**Tempo estimado**: 2h

---

#### 6.2 Validar Playbooks Existentes (P1)
**Descrição**: Executar testes end-to-end dos playbooks já criados

**Tarefas**:

1. Configurar ambiente de teste (Vagrant ou Docker):
   ```ruby
   # Vagrantfile (opcional)
   Vagrant.configure("2") do |config|
     config.vm.box = "ubuntu/jammy64"
     config.vm.network "private_network", ip: "192.168.56.10"
     config.vm.provision "ansible" do |ansible|
       ansible.playbook = "ansible/playbooks/docker-health-check.yml"
     end
   end
   ```

2. Criar script de validação:
   ```bash
   # scripts/validate-ansible-playbooks.sh
   #!/usr/bin/env bash
   set -euo pipefail

   PLAYBOOKS=(
       "docker-health-check.yml"
       "docker-troubleshoot.yml"
       "mysql-troubleshoot.yml"
       "deploy-docker-service.yml"
   )

   echo "🔍 Validando playbooks Ansible..."

   for playbook in "${PLAYBOOKS[@]}"; do
       echo "Validando: $playbook"
       ansible-playbook \
           --syntax-check \
           "ansible/playbooks/$playbook"

       ansible-lint "ansible/playbooks/$playbook" || true
   done

   echo "✅ Validação concluída"
   ```

3. Executar validação:
   ```bash
   bash scripts/validate-ansible-playbooks.sh
   ```

4. Testar playbooks em ambiente DEV:
   ```bash
   ansible-playbook -i ansible/inventory/dev/hosts.yml \
       ansible/playbooks/docker-health-check.yml \
       --check  # Dry-run primeiro

   ansible-playbook -i ansible/inventory/dev/hosts.yml \
       ansible/playbooks/docker-health-check.yml
   ```

**Critério de Sucesso**: ✅ Todos playbooks passam em syntax-check e ansible-lint

**Tempo estimado**: 2h

---

#### 6.3 Criar Roles Reutilizáveis (P2)
**Descrição**: Refatorar playbooks em roles para melhor reutilização

**Tarefas**:

1. Criar role de docker:
   ```bash
   cd ansible/roles
   ansible-galaxy init docker_management
   ```

2. Estruturar role:
   ```
   roles/docker_management/
   ├── tasks/
   │   ├── main.yml             # Entry point
   │   ├── health_check.yml     # Health checks
   │   ├── cleanup.yml          # Cleanup tasks
   │   └── backup.yml           # Backup tasks
   ├── handlers/
   │   └── main.yml             # Restart handlers
   ├── templates/
   │   └── docker-compose.yml.j2
   ├── defaults/
   │   └── main.yml             # Default variables
   └── README.md
   ```

3. Refatorar playbooks para usar roles:
   ```yaml
   ---
   - name: Docker Health Check with Role
     hosts: docker_hosts
     roles:
       - role: docker_management
         vars:
           docker_action: health_check
   ```

**Critério de Sucesso**: ✅ Pelo menos 1 role criada e utilizada

**Tempo estimado**: 2h

---

#### 6.4 Adicionar Testes Molecule (P2)
**Descrição**: Implementar testes automatizados de roles com Molecule

**Tarefas**:

1. Instalar Molecule:
   ```bash
   pip install molecule molecule-docker ansible-lint
   ```

2. Inicializar Molecule no role:
   ```bash
   cd ansible/roles/docker_management
   molecule init scenario -d docker
   ```

3. Criar testes em `molecule/default/tests/test_default.py`:
   ```python
   """Testes Molecule para docker_management role."""
   import os
   import testinfra.utils.ansible_runner

   testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
       os.environ['MOLECULE_INVENTORY_FILE']
   ).get_hosts('all')


   def test_docker_installed(host):
       """Verifica se Docker está instalado."""
       docker = host.package("docker-ce")
       assert docker.is_installed


   def test_docker_service_running(host):
       """Verifica se serviço Docker está rodando."""
       docker_service = host.service("docker")
       assert docker_service.is_running
       assert docker_service.is_enabled


   def test_docker_compose_installed(host):
       """Verifica se Docker Compose está instalado."""
       cmd = host.run("docker compose version")
       assert cmd.rc == 0
   ```

4. Executar testes:
   ```bash
   molecule test
   ```

**Critério de Sucesso**: ✅ Testes Molecule executam sem erros

**Tempo estimado**: 2h

---

### ✅ Checklist de Conclusão: Ansible

- [ ] Playbook restart-docker-service.yml criado
- [ ] Playbook docker-cleanup.yml criado
- [ ] Playbook backup-docker-volumes.yml criado
- [ ] Script de validação de playbooks criado
- [ ] Todos playbooks existentes validados (syntax-check + ansible-lint)
- [ ] Pelo menos 1 role criada (docker_management)
- [ ] Testes Molecule implementados (opcional, P2)
- [ ] Documentação atualizada no README

**Resultado Esperado**: 10/10 na categoria Ansible

---

## 🔴 CATEGORIA 8: Segurança (8/10 → 10/10)

**Gap**: -2 pontos | **Prioridade**: P0 | **Esforço Estimado**: 6-8h

### Ações Necessárias

#### 8.1 Implementar Scan de Secrets (P0)
**Descrição**: Adicionar scan automático de secrets para prevenir vazamento de credenciais

**Tarefas**:

##### 8.1.1 Instalar e Configurar Gitleaks
1. Instalar gitleaks:
   ```bash
   # Via Homebrew (macOS/Linux)
   brew install gitleaks

   # Via apt (Ubuntu/Debian)
   wget https://github.com/gitleaks/gitleaks/releases/download/v8.18.1/gitleaks_8.18.1_linux_x64.tar.gz
   tar -xzf gitleaks_8.18.1_linux_x64.tar.gz
   sudo mv gitleaks /usr/local/bin/
   ```

2. Criar `.gitleaks.toml`:
   ```toml
   title = "Gitleaks Configuration for enterprise-infra-docker"

   [extend]
   useDefault = true

   [allowlist]
   description = "Allowlist for false positives"
   paths = [
       '''.env.example''',
       '''docs/''',
       '''README.md''',
   ]

   regexes = [
       '''(example|sample|test)_?(key|token|password)''',
   ]

   [[rules]]
   id = "ansible-vault-password"
   description = "Ansible Vault Password File"
   regex = '''\.vault_pass'''
   path = '''\.secrets/'''

   [[rules]]
   id = "ssh-private-key"
   description = "SSH Private Key"
   regex = '''-----BEGIN (RSA|OPENSSH|DSA|EC|PGP) PRIVATE KEY-----'''
   path = '''\.secrets/ssh/'''

   [[rules]]
   id = "env-credentials"
   description = "Credentials in .env files"
   regex = '''(PASSWORD|TOKEN|SECRET|KEY)=.+'''
   path = '''\.secrets/\.env'''
   ```

3. Executar scan:
   ```bash
   gitleaks detect --config .gitleaks.toml --verbose
   ```

**Tempo estimado**: 1h

---

##### 8.1.2 Configurar Pre-commit Hook
1. Instalar pre-commit:
   ```bash
   pip install pre-commit
   ```

2. Criar `.pre-commit-config.yaml`:
   ```yaml
   repos:
     - repo: https://github.com/gitleaks/gitleaks
       rev: v8.18.1
       hooks:
         - id: gitleaks
           name: Gitleaks Secret Scanner
           entry: gitleaks protect --staged --verbose
           language: system
           pass_filenames: false

     - repo: https://github.com/pre-commit/pre-commit-hooks
       rev: v4.5.0
       hooks:
         - id: check-yaml
           name: Check YAML Syntax
         - id: check-json
           name: Check JSON Syntax
         - id: check-added-large-files
           name: Check Large Files
           args: ['--maxkb=1000']
         - id: detect-private-key
           name: Detect Private Keys
         - id: trailing-whitespace
           name: Trim Trailing Whitespace
         - id: end-of-file-fixer
           name: Fix End of Files

     - repo: https://github.com/ansible/ansible-lint
       rev: v6.22.1
       hooks:
         - id: ansible-lint
           name: Ansible Lint
           files: \.(yaml|yml)$
           exclude: ^\.github/
   ```

3. Instalar hooks:
   ```bash
   pre-commit install
   ```

4. Testar hooks:
   ```bash
   pre-commit run --all-files
   ```

**Critério de Sucesso**: ✅ Pre-commit hooks instalados e funcionando

**Tempo estimado**: 1h

---

##### 8.1.3 Configurar GitHub Action para Scan
1. Criar `.github/workflows/security-scan.yml`:
   ```yaml
   name: Security Scan

   on:
     push:
       branches: [main, master, develop]
     pull_request:
       branches: [main, master, develop]
     schedule:
       - cron: '0 2 * * 1'  # Toda segunda-feira às 2h

   jobs:
     gitleaks:
       name: Gitleaks Secret Scanner
       runs-on: ubuntu-latest
       steps:
         - name: Checkout code
           uses: actions/checkout@v4
           with:
             fetch-depth: 0

         - name: Run Gitleaks
           uses: gitleaks/gitleaks-action@v2
           env:
             GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
             GITLEAKS_LICENSE: ${{ secrets.GITLEAKS_LICENSE }}  # Opcional

     trufflehog:
       name: TruffleHog Secret Scanner
       runs-on: ubuntu-latest
       steps:
         - name: Checkout code
           uses: actions/checkout@v4
           with:
             fetch-depth: 0

         - name: Run TruffleHog
           uses: trufflesecurity/trufflehog@main
           with:
             path: ./
             base: main
             head: HEAD

     ansible-lint:
       name: Ansible Lint
       runs-on: ubuntu-latest
       steps:
         - name: Checkout code
           uses: actions/checkout@v4

         - name: Setup Python
           uses: actions/setup-python@v5
           with:
             python-version: '3.12'

         - name: Install ansible-lint
           run: pip install ansible-lint

         - name: Run ansible-lint
           run: ansible-lint ansible/playbooks/*.yml

     docker-security:
       name: Docker Security Scan (Trivy)
       runs-on: ubuntu-latest
       steps:
         - name: Checkout code
           uses: actions/checkout@v4

         - name: Run Trivy on Docker Compose Templates
           uses: aquasecurity/trivy-action@master
           with:
             scan-type: 'config'
             scan-ref: 'docker-compose-templates/'
             format: 'sarif'
             output: 'trivy-results.sarif'

         - name: Upload Trivy results to GitHub Security
           uses: github/codeql-action/upload-sarif@v3
           if: always()
           with:
             sarif_file: 'trivy-results.sarif'
   ```

**Critério de Sucesso**: ✅ GitHub Action configurada e executando

**Tempo estimado**: 1h

---

#### 8.2 Implementar Ansible Vault (P0)
**Descrição**: Adicionar exemplos e documentação de uso de Ansible Vault para variáveis sensíveis

**Tarefas**:

##### 8.2.1 Configurar Ansible Vault
1. Criar senha do vault (já existe em `.secrets/.vault_pass`):
   ```bash
   # Se não existir, criar:
   openssl rand -base64 32 > .secrets/.vault_pass
   chmod 600 .secrets/.vault_pass
   ```

2. Adicionar ao `.gitignore` (já deve estar):
   ```gitignore
   .secrets/
   ```

3. Configurar `ansible.cfg` para usar vault password file (verificar se já existe):
   ```ini
   [defaults]
   vault_password_file = .secrets/.vault_pass
   ```

**Tempo estimado**: 30min

---

##### 8.2.2 Criar Variáveis Encriptadas
1. Criar `ansible/inventory/dev/group_vars/all/vault.yml`:
   ```bash
   ansible-vault create ansible/inventory/dev/group_vars/all/vault.yml
   ```

2. Adicionar variáveis sensíveis:
   ```yaml
   ---
   # Credenciais MySQL
   vault_mysql_root_password: "SuperSecretPassword123!"
   vault_mysql_user_password: "AnotherSecretPass456!"

   # Credenciais SSH
   vault_ssh_private_key_passphrase: "MySSHKeyPassphrase789!"

   # Credenciais de API
   vault_api_token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

   # Credenciais Portainer
   vault_portainer_admin_password: "PortainerAdminPass000!"
   ```

3. Criar `ansible/inventory/dev/group_vars/all/vars.yml` (não encriptado):
   ```yaml
   ---
   # Variáveis públicas que referenciam vault
   mysql_root_password: "{{ vault_mysql_root_password }}"
   mysql_user_password: "{{ vault_mysql_user_password }}"
   ssh_key_passphrase: "{{ vault_ssh_private_key_passphrase }}"
   api_token: "{{ vault_api_token }}"
   portainer_admin_password: "{{ vault_portainer_admin_password }}"
   ```

4. Replicar estrutura para staging e prod:
   ```bash
   mkdir -p ansible/inventory/{staging,prod}/group_vars/all

   # Criar vault files separados para cada ambiente
   ansible-vault create ansible/inventory/staging/group_vars/all/vault.yml
   ansible-vault create ansible/inventory/prod/group_vars/all/vault.yml
   ```

**Tempo estimado**: 1h

---

##### 8.2.3 Atualizar Playbooks para Usar Vault
1. Exemplo em `ansible/playbooks/deploy-docker-service.yml`:
   ```yaml
   ---
   - name: Deploy Docker Service with Encrypted Variables
     hosts: docker_hosts
     gather_facts: true
     become: true

     tasks:
       - name: Create .env file from template
         template:
           src: templates/docker-compose.env.j2
           dest: "/opt/docker/.env"
           mode: '0600'
         vars:
           mysql_password: "{{ mysql_root_password }}"
           api_token: "{{ api_token }}"

       - name: Deploy service
         community.docker.docker_compose:
           project_src: "/opt/docker"
           state: present
   ```

2. Criar template `ansible/templates/docker-compose.env.j2`:
   ```jinja2
   # Docker Compose Environment Variables
   # Generated by Ansible - DO NOT EDIT MANUALLY

   MYSQL_ROOT_PASSWORD={{ mysql_root_password }}
   MYSQL_USER_PASSWORD={{ mysql_user_password }}
   API_TOKEN={{ api_token }}
   PORTAINER_ADMIN_PASSWORD={{ portainer_admin_password }}
   ```

**Tempo estimado**: 1h

---

##### 8.2.4 Documentar Uso de Vault
1. Criar `docs/ANSIBLE_VAULT_GUIDE.md`:
   ```markdown
   # Guia de Uso: Ansible Vault

   ## O que é Ansible Vault?

   Ansible Vault é uma ferramenta de encriptação para proteger dados sensíveis em playbooks e inventários.

   ## Configuração

   ### Senha do Vault

   A senha está armazenada em `.secrets/.vault_pass` (nunca versionada).

   ```bash
   # Criar nova senha (apenas primeira vez)
   openssl rand -base64 32 > .secrets/.vault_pass
   chmod 600 .secrets/.vault_pass
   ```

   ### Variáveis Encriptadas

   Variáveis sensíveis estão em `ansible/inventory/{env}/group_vars/all/vault.yml`.

   ## Comandos Úteis

   ### Criar arquivo vault

   ```bash
   ansible-vault create ansible/inventory/dev/group_vars/all/vault.yml
   ```

   ### Editar arquivo vault

   ```bash
   ansible-vault edit ansible/inventory/dev/group_vars/all/vault.yml
   ```

   ### Ver conteúdo (sem editar)

   ```bash
   ansible-vault view ansible/inventory/dev/group_vars/all/vault.yml
   ```

   ### Encriptar arquivo existente

   ```bash
   ansible-vault encrypt ansible/inventory/dev/group_vars/all/secrets.yml
   ```

   ### Desencriptar arquivo

   ```bash
   ansible-vault decrypt ansible/inventory/dev/group_vars/all/vault.yml
   ```

   ### Re-encriptar com nova senha

   ```bash
   ansible-vault rekey ansible/inventory/dev/group_vars/all/vault.yml
   ```

   ## Uso em Playbooks

   ### Executar playbook com vault

   ```bash
   # Usando vault password file (configurado em ansible.cfg)
   ansible-playbook ansible/playbooks/deploy.yml

   # Ou, pedindo senha manualmente:
   ansible-playbook ansible/playbooks/deploy.yml --ask-vault-pass
   ```

   ### Estrutura recomendada

   ```
   group_vars/all/
   ├── vault.yml       # Variáveis encriptadas (vault_*)
   └── vars.yml        # Variáveis públicas que referenciam vault
   ```

   Exemplo:

   **vault.yml** (encriptado):
   ```yaml
   vault_mysql_password: "SuperSecret123"
   ```

   **vars.yml** (não encriptado):
   ```yaml
   mysql_password: "{{ vault_mysql_password }}"
   ```

   ## Boas Práticas

   1. ✅ **Sempre encriptar**: senhas, tokens, chaves API
   2. ✅ **Prefixo `vault_`**: usar em todas variáveis encriptadas
   3. ✅ **Vault separado por ambiente**: dev/staging/prod têm credenciais diferentes
   4. ✅ **Vault password file**: manter em `.secrets/` e nunca versionar
   5. ✅ **Rotação de senhas**: alterar vault periodicamente
   6. ❌ **Nunca commitar desencriptado**: sempre commit files encriptados

   ## Troubleshooting

   ### Erro: "Vault password file not found"

   Criar `.secrets/.vault_pass` com a senha do vault.

   ### Erro: "Decryption failed"

   Senha incorreta. Verificar `.secrets/.vault_pass`.

   ### Ver se arquivo está encriptado

   ```bash
   head -1 ansible/inventory/dev/group_vars/all/vault.yml
   # Deve começar com: $ANSIBLE_VAULT;1.1;AES256
   ```
   ```

2. Adicionar link no `docs/INDEX.md`:
   ```markdown
   - [ANSIBLE_VAULT_GUIDE.md](ANSIBLE_VAULT_GUIDE.md) - Guia de uso do Ansible Vault
   ```

**Critério de Sucesso**: ✅ Documentação completa de Ansible Vault criada

**Tempo estimado**: 1h

---

#### 8.3 Adicionar Rotação de Credenciais (P1)
**Descrição**: Documentar processo de rotação de credenciais e secrets

**Tarefas**:

1. Criar `docs/CREDENTIAL_ROTATION.md`:
   ```markdown
   # Rotação de Credenciais

   ## Frequência Recomendada

   | Tipo de Credencial | Frequência | Prioridade |
   |-------------------|------------|------------|
   | Senhas SSH | 90 dias | Alta |
   | Senhas MySQL | 60 dias | Alta |
   | Tokens API | 30 dias | Média |
   | Vault Password | 180 dias | Crítica |
   | Chaves SSH | 1 ano | Alta |

   ## Processo de Rotação

   ### 1. Senhas SSH

   ```bash
   # 1. Gerar nova senha
   NEW_PASS=$(openssl rand -base64 24)

   # 2. Atualizar no servidor remoto
   ansible -i inventory/prod/hosts.yml all -m user \
       -a "name=ansible password={{ NEW_PASS | password_hash('sha512') }}" \
       --become

   # 3. Atualizar vault
   ansible-vault edit inventory/prod/group_vars/all/vault.yml
   # Alterar vault_ssh_password para nova senha

   # 4. Testar conexão
   ansible -i inventory/prod/hosts.yml all -m ping
   ```

   ### 2. Senhas MySQL

   ```bash
   # 1. Gerar nova senha
   NEW_MYSQL_PASS=$(openssl rand -base64 24)

   # 2. Atualizar no MySQL
   docker exec -it postgresql mysql -u root -p -e \
       "ALTER USER 'root'@'%' IDENTIFIED BY '${NEW_MYSQL_PASS}';"

   # 3. Atualizar vault
   ansible-vault edit inventory/prod/group_vars/all/vault.yml
   # Alterar vault_mysql_root_password

   # 4. Atualizar .env e reiniciar containers
   ansible-playbook playbooks/deploy-docker-service.yml
   ```

   ### 3. Vault Password

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
   ansible-vault view inventory/dev/group_vars/all/vault.yml
   ```

   ### 4. Chaves SSH

   ```bash
   # 1. Gerar novo par de chaves
   ssh-keygen -t ed25519 -C "ansible@enterprise-infra" \
       -f .secrets/ssh/id_ed25519.new

   # 2. Distribuir chave pública para servidores
   ansible -i inventory/prod/hosts.yml all -m authorized_key \
       -a "user=ansible key={{ lookup('file', '.secrets/ssh/id_ed25519.new.pub') }}" \
       --become

   # 3. Testar nova chave
   ssh -i .secrets/ssh/id_ed25519.new user@server

   # 4. Remover chave antiga dos servidores
   ansible -i inventory/prod/hosts.yml all -m authorized_key \
       -a "user=ansible key={{ lookup('file', '.secrets/ssh/id_ed25519.pub') }} state=absent" \
       --become

   # 5. Substituir chave
   mv .secrets/ssh/id_ed25519.new .secrets/ssh/id_ed25519
   mv .secrets/ssh/id_ed25519.new.pub .secrets/ssh/id_ed25519.pub
   chmod 600 .secrets/ssh/id_ed25519
   ```

   ## Checklist de Rotação

   - [ ] Backup de vault files antes de alterar
   - [ ] Testar novas credenciais em DEV antes de PROD
   - [ ] Documentar data de rotação no TODO.md
   - [ ] Notificar equipe sobre mudança de credenciais
   - [ ] Verificar logs após rotação
   - [ ] Atualizar documentos de runbook

   ## Auditoria de Credenciais

   Manter registro de quando cada credencial foi alterada:

   ```bash
   # docs/CREDENTIAL_AUDIT.md
   | Credencial | Última Rotação | Próxima Rotação | Status |
   |-----------|----------------|----------------|--------|
   | SSH (prod) | 2026-02-01 | 2026-05-01 | ✅ OK |
   | MySQL (prod) | 2026-01-15 | 2026-03-15 | ⚠️ Vencendo |
   | Vault Pass | 2025-12-01 | 2026-06-01 | ✅ OK |
   ```
   ```

**Critério de Sucesso**: ✅ Processo de rotação documentado para todas credenciais

**Tempo estimado**: 1h

---

#### 8.4 Adicionar SAST e Dependency Scanning (P2)
**Descrição**: Integrar ferramentas de análise estática de segurança

**Tarefas**:

1. Adicionar Bandit para Python no `.github/workflows/security-scan.yml`:
   ```yaml
     bandit:
       name: Bandit SAST (Python)
       runs-on: ubuntu-latest
       steps:
         - name: Checkout code
           uses: actions/checkout@v4

         - name: Setup Python
           uses: actions/setup-python@v5
           with:
             python-version: '3.12'

         - name: Install Bandit
           run: pip install bandit[toml]

         - name: Run Bandit
           run: bandit -r src/ -f json -o bandit-report.json

         - name: Upload Bandit results
           uses: actions/upload-artifact@v4
           if: always()
           with:
             name: bandit-report
             path: bandit-report.json
   ```

2. Adicionar Safety para dependências Python:
   ```yaml
     safety:
       name: Safety Dependency Check
       runs-on: ubuntu-latest
       steps:
         - name: Checkout code
           uses: actions/checkout@v4

         - name: Setup Python
           uses: actions/setup-python@v5
           with:
             python-version: '3.12'

         - name: Install Safety
           run: pip install safety

         - name: Check dependencies
           run: safety check --json
   ```

3. Adicionar checkov para IaC:
   ```yaml
     checkov:
       name: Checkov IaC Scanner
       runs-on: ubuntu-latest
       steps:
         - name: Checkout code
           uses: actions/checkout@v4

         - name: Run Checkov
           uses: bridgecrewio/checkov-action@master
           with:
             directory: docker-compose-templates/
             framework: docker_compose
             output_format: sarif
             output_file_path: checkov-results.sarif

         - name: Upload Checkov results
           uses: github/codeql-action/upload-sarif@v3
           if: always()
           with:
             sarif_file: checkov-results.sarif
   ```

**Critério de Sucesso**: ✅ SAST e dependency scanning configurados e executando

**Tempo estimado**: 2h

---

### ✅ Checklist de Conclusão: Segurança

- [ ] Gitleaks instalado e configurado (.gitleaks.toml criado)
- [ ] Pre-commit hooks instalados e funcionando
- [ ] GitHub Action de security scan criada e ativa
- [ ] Ansible Vault configurado com vault password file
- [ ] Variáveis vault criadas para dev/staging/prod
- [ ] Playbooks atualizados para usar variáveis vault
- [ ] Documentação ANSIBLE_VAULT_GUIDE.md criada
- [ ] Documentação CREDENTIAL_ROTATION.md criada
- [ ] SAST (Bandit) integrado
- [ ] Dependency scanning (Safety) integrado
- [ ] IaC scanning (Checkov/Trivy) integrado

**Resultado Esperado**: 10/10 na categoria Segurança

---

## 🟢 CATEGORIA 9: Melhorias de Estrutura (P2)

**Prioridade**: P2 (Média) | **Esforço Estimado**: 1-2h

### Contexto

Atualmente, scripts e processos utilizam `/tmp/` do sistema Linux, o que pode gerar:
- ❌ Necessidade de permissões de sistema
- ❌ Conflitos com outros processos
- ❌ Arquivos temporários não organizados
- ❌ Dificuldade de limpeza e auditoria

**Solução**: Criar pasta `tmp/` local no projeto.

---

### Ações Necessárias

#### 9.1 Criar Estrutura de tmp/ Local (P2)
**Descrição**: Implementar pasta tmp/ no projeto para arquivos temporários

**Tarefas**:

1. Criar estrutura de diretórios:
   ```bash
   mkdir -p tmp/{logs,cache,downloads,commits}
   touch tmp/.gitkeep
   ```

2. Atualizar `.gitignore`:
   ```gitignore
   # Temporary files (local)
   tmp/*
   !tmp/.gitkeep
   ```

3. Criar `tmp/README.md`:
   ```markdown
   # Diretório de Arquivos Temporários
   
   Este diretório é usado para armazenar arquivos temporários do projeto.
   
   ## Estrutura
   
   - `logs/` - Logs temporários de execução
   - `cache/` - Cache de operações
   - `downloads/` - Downloads temporários
   - `commits/` - Mensagens de commit temporárias
   
   ## Limpeza
   
   Arquivos neste diretório são **automaticamente limpos** ao final de cada sessão.
   
   ## Uso
   
   Em scripts Python:
   ```python
   from pathlib import Path
   
   TMP_DIR = Path(__file__).parent / "tmp"
   TMP_DIR.mkdir(exist_ok=True)
   
   # Usar tmp/ local em vez de /tmp/
   temp_file = TMP_DIR / "commits" / "commit_message.txt"
   temp_file.write_text("feat: nova feature")
   ```
   
   Em scripts Bash:
   ```bash
   PROJECT_ROOT=$(git rev-parse --show-toplevel)
   TMP_DIR="${PROJECT_ROOT}/tmp"
   
   # Usar tmp/ local em vez de /tmp/
   echo "feat: nova feature" > "${TMP_DIR}/commits/commit_message.txt"
   ```
   ```

**Critério de Sucesso**: ✅ Estrutura tmp/ criada e documentada

**Tempo estimado**: 15 min

---

#### 9.2 Implementar Script de Limpeza Automática (P2)
**Descrição**: Criar script para limpar tmp/ no encerramento de sessão

**Tarefas**:

1. Criar `scripts/cleanup-tmp.sh`:
   ```bash
   #!/usr/bin/env bash
   # cleanup-tmp.sh - Limpa arquivos temporários do projeto
   
   set -euo pipefail
   
   PROJECT_ROOT=$(git rev-parse --show-toplevel)
   TMP_DIR="${PROJECT_ROOT}/tmp"
   
   echo "🧹 Limpando diretório tmp/..."
   
   if [[ ! -d "$TMP_DIR" ]]; then
       echo "⚠️  Diretório tmp/ não existe, criando..."
       mkdir -p "${TMP_DIR}"/{logs,cache,downloads,commits}
       touch "${TMP_DIR}/.gitkeep"
       exit 0
   fi
   
   # Contar arquivos antes
   FILES_BEFORE=$(find "$TMP_DIR" -type f ! -name '.gitkeep' | wc -l)
   
   # Limpar todos arquivos exceto .gitkeep
   find "$TMP_DIR" -type f ! -name '.gitkeep' -delete
   
   # Limpar diretórios vazios
   find "$TMP_DIR" -type d -empty -not -path "$TMP_DIR" -delete
   
   # Recriar estrutura
   mkdir -p "${TMP_DIR}"/{logs,cache,downloads,commits}
   
   # Contar arquivos depois
   FILES_AFTER=$(find "$TMP_DIR" -type f ! -name '.gitkeep' | wc -l)
   FILES_REMOVED=$((FILES_BEFORE - FILES_AFTER))
   
   echo "✅ Limpeza concluída: ${FILES_REMOVED} arquivos removidos"
   echo "📊 Total de arquivos temporários: ${FILES_AFTER}"
   ```

2. Tornar executável:
   ```bash
   chmod +x scripts/cleanup-tmp.sh
   ```

3. Adicionar ao Session Manager Agent (`.github/agents/session-manager.agent.md`):
   ```markdown
   **Step 7: Cleanup Temporary Files**
   - Execute: `./scripts/cleanup-tmp.sh`
   - Verify: `tmp/` directory is clean
   - Log: Files removed count
   ```

**Critério de Sucesso**: ✅ Script de limpeza funcional e integrado ao Session Manager

**Tempo estimado**: 30 min

---

#### 9.3 Atualizar Scripts Existentes (P2)
**Descrição**: Migrar scripts que usam `/tmp/` para usar `./tmp/`

**Tarefas**:

1. Identificar scripts que usam `/tmp/`:
   ```bash
   grep -r "/tmp/" scripts/ ansible/ --include="*.sh" --include="*.py"
   ```

2. Atualizar cada script encontrado:
   
   **Antes**:
   ```bash
   echo "feat: nova feature" > /tmp/commit.txt
   git commit -F /tmp/commit.txt
   ```
   
   **Depois**:
   ```bash
   PROJECT_ROOT=$(git rev-parse --show-toplevel)
   TMP_DIR="${PROJECT_ROOT}/tmp"
   echo "feat: nova feature" > "${TMP_DIR}/commits/commit.txt"
   git commit -F "${TMP_DIR}/commits/commit.txt"
   ```

3. Atualizar `scripts/lib/` (se houver funções auxiliares):
   ```python
   # scripts/lib/paths.py
   from pathlib import Path
   
   PROJECT_ROOT = Path(__file__).parent.parent.parent
   TMP_DIR = PROJECT_ROOT / "tmp"
   
   def get_tmp_file(subdir: str, filename: str) -> Path:
       """Retorna caminho para arquivo temporário."""
       tmp_path = TMP_DIR / subdir
       tmp_path.mkdir(parents=True, exist_ok=True)
       return tmp_path / filename
   ```

4. Atualizar documentação:
   - Adicionar seção em `docs/CONVENTIONS.md`:
     ```markdown
     ## Arquivos Temporários
     
     **SEMPRE** usar `./tmp/` em vez de `/tmp/`:
     - ✅ `./tmp/commits/message.txt`
     - ❌ `/tmp/commit.txt`
     
     **Motivos**:
     - Sem necessidade de permissões de sistema
     - Organização por propósito (logs, cache, downloads)
     - Limpeza automática no encerramento de sessão
     - Auditoria facilitada
     ```

**Critério de Sucesso**: ✅ Todos scripts migrados para usar `./tmp/`

**Tempo estimado**: 30 min

---

#### 9.4 Adicionar Validação de tmp/ (P2)
**Descrição**: Garantir que tmp/ está sempre disponível e limpo

**Tarefas**:

1. Criar `scripts/validate-tmp.sh`:
   ```bash
   #!/usr/bin/env bash
   # validate-tmp.sh - Valida estrutura de tmp/
   
   set -euo pipefail
   
   PROJECT_ROOT=$(git rev-parse --show-toplevel)
   TMP_DIR="${PROJECT_ROOT}/tmp"
   
   echo "🔍 Validando estrutura tmp/..."
   
   # Verificar se existe
   if [[ ! -d "$TMP_DIR" ]]; then
       echo "❌ Diretório tmp/ não existe"
       exit 1
   fi
   
   # Verificar subdiretorios
   REQUIRED_DIRS=("logs" "cache" "downloads" "commits")
   
   for dir in "${REQUIRED_DIRS[@]}"; do
       if [[ ! -d "${TMP_DIR}/${dir}" ]]; then
           echo "⚠️  Faltando: tmp/${dir}"
           mkdir -p "${TMP_DIR}/${dir}"
           echo "✅ Criado: tmp/${dir}"
       fi
   done
   
   # Verificar .gitkeep
   if [[ ! -f "${TMP_DIR}/.gitkeep" ]]; then
       echo "⚠️  Faltando: tmp/.gitkeep"
       touch "${TMP_DIR}/.gitkeep"
       echo "✅ Criado: tmp/.gitkeep"
   fi
   
   # Contar arquivos
   FILE_COUNT=$(find "$TMP_DIR" -type f ! -name '.gitkeep' | wc -l)
   
   echo "✅ Estrutura tmp/ válida"
   echo "📊 Total de arquivos temporários: ${FILE_COUNT}"
   ```

2. Adicionar validação ao Session Manager Agent (step de inicialização):
   ```markdown
   **Step 2: Validate Project Structure**
   - Execute: `./scripts/validate-tmp.sh`
   - Ensure: tmp/ structure is valid
   ```

**Critério de Sucesso**: ✅ Validação automática de tmp/ no início de cada sessão

**Tempo estimado**: 15 min

---

### ✅ Checklist de Conclusão: Melhorias de Estrutura

- [ ] Estrutura tmp/ criada (logs, cache, downloads, commits)
- [ ] tmp/ adicionado ao .gitignore (exceto .gitkeep)
- [ ] tmp/README.md criado com documentação
- [ ] Script cleanup-tmp.sh implementado
- [ ] Script validate-tmp.sh implementado
- [ ] Scripts migrados de /tmp/ para ./tmp/
- [ ] docs/CONVENTIONS.md atualizado com regras de tmp/
- [ ] Session Manager Agent atualizado (cleanup + validation)
- [ ] Testes de limpeza automática executados

**Resultado Esperado**: Estrutura mais organizada, segura e sem dependência de permissões de sistema

---

## 🎯 Resumo Executivo

### Priorização de Ações

| Prioridade | Ações | Esforço | Impacto |
|-----------|-------|---------|---------|
| **P0 (Crítico)** | Testes Python + Segurança | 14-20h | +2 pontos |
| **P1 (Alta)** | Documentação + Ansible | 10-14h | +2 pontos |
| **P2 (Média)** | Melhorias opcionais + Estrutura | 9-13h | Qualidade geral |

### Roadmap Sugerido

#### Sprint 1: Segurança (P0)
**Duração**: 3-4 dias
- 8.1 Scan de Secrets (Gitleaks + pre-commit + GitHub Action)
- 8.2 Ansible Vault (configuração + exemplos + documentação)
- 8.3 Rotação de Credenciais (documentação)

**Resultado**: Segurança 8/10 → 10/10 ✅

---

#### Sprint 2: Testes Python (P0)
**Duração**: 4-5 dias
- 5.1 Testes Unitários completos
- 5.2 Docstrings em todos módulos
- 5.3 Type hints + mypy

**Resultado**: Python 9/10 → 10/10 ✅

---

#### Sprint 3: Documentação (P1)
**Duração**: 2-3 dias
- 3.1 Completar README.md
- 3.2 TROUBLESHOOTING.md
- 3.3 Validar links
- 3.4 CONVENTIONS.md
- 3.5 CHANGELOG.md

**Resultado**: Documentação 9/10 → 10/10 ✅

---

#### Sprint 4: Ansible (P1)
**Duração**: 3-4 dias
- 6.1 Playbooks adicionais (restart, cleanup, backup)
- 6.2 Validação de playbooks existentes
- 6.3 Roles reutilizáveis
- 6.4 Testes Molecule (opcional)

**Resultado**: Ansible 9/10 → 10/10 ✅

---

#### Sprint 5: Melhorias de Estrutura (P2)
**Duração**: 1-2 dias
- 9.1 Configurar pasta `tmp/` no projeto
- 9.2 Adicionar limpeza automática no encerramento de sessão
- 9.3 Atualizar scripts para usar `./tmp/` em vez de `/tmp/`

**Resultado**: Estrutura mais segura e sem necessidade de permissões de sistema ✅

---

### Estimativa Total

| Categoria | Esforço | Dependências |
|-----------|---------|-------------|
| Segurança | 6-8h | Nenhuma |
| Python | 8-12h | Nenhuma |
| Documentação | 4-6h | Nenhuma |
| Ansible | 6-8h | Nenhuma |
| Estrutura (Melhorias) | 1-2h | Nenhuma |
| **TOTAL** | **25-36h** | Ações independentes |

**Tempo médio**: ~31 horas (~4 semanas em part-time, ~1 semana full-time)

---

### Resultado Esperado Final

| Categoria | Antes | Depois | Delta |
|-----------|-------|--------|-------|
| Estrutura | 10/10 | 10/10 | 0 |
| VS Code | 10/10 | 10/10 | 0 |
| Documentação | 9/10 | 10/10 | +1 |
| Profile Compliance | 10/10 | 10/10 | 0 |
| Python | 9/10 | 10/10 | +1 |
| Ansible | 9/10 | 10/10 | +1 |
| Docker | 10/10 | 10/10 | 0 |
| Segurança | 8/10 | 10/10 | +2 |
| **TOTAL** | **9.4/10** | **10/10** | **+0.6** |

---

## 📋 Checklist Geral de Progresso

### Segurança (8/10 → 10/10)
- [ ] Gitleaks configurado
- [ ] Pre-commit hooks instalados
- [ ] GitHub Action de security scan
- [ ] Ansible Vault implementado
- [ ] Rotação de credenciais documentada
- [ ] SAST integrado (Bandit/Safety/Checkov)

### Código Python (9/10 → 10/10)
- [ ] pytest.ini configurado
- [ ] Testes ssh_client.py (≥90%)
- [ ] Testes container_health.py (≥85%)
- [ ] Testes mysql_diagnostics.py (≥85%)
- [ ] Testes CLIs
- [ ] Docstrings completas
- [ ] mypy configurado e passando

### Documentação (9/10 → 10/10)
- [ ] README.md completo
- [ ] TROUBLESHOOTING.md criado
- [ ] Links validados
- [ ] CONVENTIONS.md criado
- [ ] CHANGELOG.md criado

### Ansible (9/10 → 10/10)
- [ ] Playbook restart-docker-service.yml
- [ ] Playbook docker-cleanup.yml
- [ ] Playbook backup-docker-volumes.yml
- [ ] Validação de playbooks existentes
- [ ] Role docker_management criada
- [ ] Testes Molecule (opcional)

### Melhorias de Estrutura (P2)
- [ ] Pasta tmp/ criada no projeto
- [ ] Script de limpeza automática implementado
- [ ] Scripts atualizados para usar ./tmp/
- [ ] Documentação sobre uso de tmp/ local
- [ ] .gitignore atualizado para incluir tmp/

---

## 🚀 Próximos Passos

1. **Revisar este documento** com a equipe
2. **Priorizar sprints** de acordo com necessidades do projeto
3. **Criar issues no GitHub** para cada ação (opcional)
4. **Executar Sprint 1** (Segurança - P0)
5. **Validar resultados** após cada sprint
6. **Atualizar score** no PROJECT_VALIDATION ao final

---

**Documento criado em**: 2026-03-20
**Válido para**: enterprise-infra-docker
**Baseado em**: PROJECT_VALIDATION_enterprise-infra-docker.md
**Autor**: GitHub Copilot + Session Manager Agent
