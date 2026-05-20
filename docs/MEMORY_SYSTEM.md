# Sistema de Memória — Guia Completo

**Versão**: 1.1.0 (IMP-65 P1 Complete)
**Última atualização**: 2026-05-20
**Status**: ✅ Produção

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Estrutura de Diretórios](#estrutura-de-diretórios)
3. [Scopes de Memória](#scopes-de-memória)
4. [Boas Práticas](#boas-práticas)
5. [Nomenclatura de Arquivos](#nomenclatura-de-arquivos)
6. [YAML Frontmatter](#yaml-frontmatter)
7. [Comandos Úteis](#comandos-úteis)
8. [Troubleshooting](#troubleshooting)
9. [Referências](#referências)

---

## Visão Geral

O **Sistema de Memória** é uma infraestrutura de conhecimento persistente que suporta:

- ✅ **Contexto cross-workspace**: Memórias persistem entre projetos (user scope)
- ✅ **Contexto local**: Conhecimento específico do workspace (.memory/)
- ✅ **Contexto de sessão**: Notas temporárias da conversa atual
- ✅ **Busca semântica**: FTS5 full-text search integrado
- ✅ **Versionamento**: Memórias versionadas no Git
- ✅ **Qualidade**: Pre-commit hooks + scripts de validação

### Quando usar?

- 🟢 **Usar memórias**: Decisões arquiteturais, convenções do projeto, comandos frequentes, bugs recorrentes, lições aprendidas
- 🔴 **NÃO usar**: Dados temporários, logs de debug, testes automatizados, dados sensíveis

---

## Estrutura de Diretórios

O sistema possui **duas** estruturas de memória:

### 1. `/memories/` — Copilot Memory Tool (MCP)

```
/memories/
├── user-memory.md          # Memórias cross-workspace (carregadas automaticamente)
├── project-notes.md        # Notas específicas do usuário
└── session/                # Memórias da sessão atual (temporárias)
    └── planning-notes.md
```

**Características**:
- Gerenciado via **MCP memory tool** (memory create, memory view, memory delete)
- User scope (`/memories/*.md`): Persiste entre todos os workspaces
- Session scope (`/memories/session/*.md`): Apenas conversação atual
- **Primeiro 200 linhas** de user memory carregadas automaticamente no contexto

### 2. `.memory/` — Mini-Engram Local

```
.memory/
└── memories/
    ├── project/            # Conhecimento do projeto
    │   ├── 2026-05-18__architectural-decision-x.md
    │   └── 2026-05-18__security-audit-finding.md
    ├── team/               # Convenções da equipe
    │   └── 2026-05-10__code-review-checklist.md
    └── sessions/           # Histórico de sessões
        └── 2026-05-18__session-summary.md
```

**Características**:
- Gerenciado via **scripts Python** (scripts/mem_*.py)
- Versionado no Git (`.memory/` não está no .gitignore)
- Busca via FTS5: `python scripts/mem_search.py "query"`
- Específico do workspace (não compartilhado entre projetos)

---

## Scopes de Memória

### User Scope (`/memories/`)

**Localização**: `~/.copilot/memories/` (ou workspace-specific via MCP config)
**Acesso**: Todos os workspaces do usuário
**Duração**: Permanente (até deletar manualmente)

**Quando usar**:
- ✅ Preferências pessoais do desenvolvedor
- ✅ Padrões de desenvolvimento favoritos
- ✅ Comandos shell frequentes
- ✅ Atalhos e workflows pessoais

**Exemplo**:
```markdown
# user-preferences.md

## Python
- Preferência: type hints obrigatórios
- Linter: ruff (não flake8)
- Formatter: black, line-length 100

## Git
- Commits: Conventional Commits sempre
- Branches: feature/NNN-nome-da-feature
```

### Repository Scope (`/memories/repo/`)

**Localização**: `/memories/repo/` (dentro do MCP user scope, mas com path indicando workspace)
**Acesso**: Apenas workspace atual
**Duração**: Permanente (versionado no MCP, mas workspace-specific)

**Quando usar**:
- ✅ Convenções específicas do projeto
- ✅ Decisões arquiteturais do repositório
- ✅ Configurações de build e deploy
- ✅ Troubleshooting de problemas recorrentes

**Exemplo**:
```markdown
# /memories/repo/build-commands.md

## Build Commands

- Dev: `make dev`
- Prod: `make build`
- Tests: `make test-all`
- Docker: `make docker-up`
```

### Session Scope (`/memories/session/`)

**Localização**: `/memories/session/`
**Acesso**: Apenas conversação atual
**Duração**: Temporário (deletado ao fim da sessão)

**Quando usar**:
- ✅ Notas temporárias da tarefa atual
- ✅ Contexto de debugging em andamento
- ✅ Planos de implementação em progresso
- ✅ Decisões pendentes de aprovação

**Exemplo**:
```markdown
# /memories/session/bug-investigation.md

## BUG-20: MCP GitHub HTTP Merge Failure

### Hipóteses
1. Shallow merge não sobrescreve server config ✅ CONFIRMADA
2. Backup não criado antes do merge ✅ CONFIRMADA

### Próximos passos
- Implementar deep merge em file_merge.py
- Adicionar validação pós-merge
```

### Local Scope (`.memory/memories/`)

**Localização**: `.memory/memories/` (versionado no Git)
**Acesso**: Todos os desenvolvedores do workspace
**Duração**: Permanente (versionado)

**Quando usar**:
- ✅ Knowledge base compartilhado da equipe
- ✅ Histórico de decisões arquiteturais
- ✅ Padrões de código do projeto
- ✅ Lições aprendidas de incidents

**Exemplo**:
```markdown
---
category: project
tags: [architecture, database, performance]
date: 2026-05-18
---

# ADR-001: Migração PostgreSQL → MongoDB

## Contexto
Performance de queries agregadas degradando com 10M+ registros.

## Decisão
Migrar para MongoDB para queries de agregação complexas.

## Consequências
- ✅ 85% redução em tempo de query
- ✅ Suporte nativo a JSON
- ❌ Perda de ACID em alguns casos
```

---

## Boas Práticas

### ✅ DO: Faça isso

1. **Use scopes apropriados**
   - User: Preferências pessoais
   - Repo: Decisões do projeto
   - Session: Notas temporárias
   - Local: Knowledge base compartilhado

2. **Seja conciso**
   - User memory: Primeira 200 linhas carregadas automaticamente
   - Priorize bullet points sobre prosa
   - Uma memória = um tópico específico

3. **Use YAML frontmatter** (`.memory/` only)
   ```markdown
   ---
   category: project
   tags: [security, authentication]
   date: 2026-05-18
   ---
   ```

4. **Nomeie arquivos descritivamente**
   - Bom: `2026-05-18__mcp-github-http-migration.md`
   - Ruim: `notes.md`, `temp.md`

5. **Atualize regularmente**
   - Revise memórias mensalmente
   - Delete informações obsoletas
   - Mantenha decisões atuais no topo

6. **Versione memórias locais**
   - `.memory/` está versionado no Git
   - Commit mudanças em memórias importantes
   - Use mensagens de commit descritivas

### ❌ DON'T: Evite isso

1. **Não armazene dados sensíveis**
   - ❌ Senhas, tokens, API keys
   - ❌ Dados de produção
   - ❌ PII (Personally Identifiable Information)

2. **Não use memórias para testes**
   - ❌ Arquivos `test-*.md` em `.memory/`
   - ✅ Use test fixtures isolados (tests/conftest.py)

3. **Não crie memórias duplicadas**
   - ❌ Mesma informação em 3 scopes diferentes
   - ✅ Escolha o scope mais apropriado

4. **Não escreva romances**
   - ❌ Documentação de 10.000 palavras em user memory
   - ✅ Resumos curtos + link para docs/

5. **Não misture projetos**
   - ❌ Dados do projeto A em user memory com tag "project-a"
   - ✅ Use repo scope ou local scope

---

## Nomenclatura de Arquivos

### User/Session Scope (`/memories/`)

Formato livre, mas recomendado:

```
<topico-descritivo>.md

Exemplos:
- python-preferences.md
- git-workflow.md
- debugging-tips.md
```

### Local Scope (`.memory/memories/`)

Formato obrigatório:

```
YYYY-MM-DD__<titulo-descritivo>.md

Componentes:
- YYYY-MM-DD: Data de criação (ISO 8601)
- __: Separador duplo underscore
- titulo-descritivo: kebab-case, lowercase

Exemplos:
✅ 2026-05-18__architectural-decision-mongodb.md
✅ 2026-05-15__security-audit-findings.md
✅ 2026-05-10__team-code-review-checklist.md

❌ architectural-decision.md        (falta data)
❌ 2026-05-18_single-underscore.md  (underscore errado)
❌ 2026-05-18__Test File.md         (uppercase, espaços)
```

### Padrões de Teste (BLOQUEADOS)

Estes padrões são **bloqueados pelo pre-commit hook**:

```
❌ *__test-*.md                    # Arquivos de teste
❌ *__auto-generated-title.md      # Títulos auto-gerados
❌ *__search-test-*.md             # Testes de busca
```

---

## YAML Frontmatter

### Quando usar?

- **Obrigatório**: `.memory/memories/*.md` (recomendado)
- **Opcional**: `/memories/*.md` (user/session scope)

### Formato

```yaml
---
category: <categoria>
tags: [tag1, tag2, tag3]
date: YYYY-MM-DD
author: <nome> (opcional)
status: draft|active|archived (opcional)
---
```

### Categorias Válidas

| Categoria | Descrição | Exemplo |
|-----------|-----------|---------|
| `project` | Conhecimento específico do projeto | Arquitetura, decisões técnicas |
| `team` | Convenções da equipe | Code review, workflows |
| `decision` | ADR (Architectural Decision Record) | ADR-001: Escolha de DB |
| `pattern` | Padrões de código/design | Singleton, Factory |
| `incident` | Post-mortems, RCAs | Outage 2026-05-15 |
| `user` | Preferências pessoais | Atalhos, comandos |

### Exemplos

```markdown
---
category: decision
tags: [architecture, database, mongodb]
date: 2026-05-18
author: Equipe Backend
status: active
---

# ADR-001: Migração para MongoDB

...
```

```markdown
---
category: incident
tags: [security, mcp, github]
date: 2026-05-18
status: resolved
---

# Incident: MCP GitHub CLI Obsolete

...
```

### Validação

O **pre-commit hook** (IMP-65 P1, implementado 2026-05-20) valida automaticamente:

✅ Frontmatter bem-formado (---...---)
✅ Categorias válidas (project|team|decision|pattern|incident|user)
✅ Bloqueia test files (__test-*.md, __auto-generated-title.md, __search-test-*.md)
❌ Frontmatter malformado → commit bloqueado
❌ Categoria inválida → commit bloqueado
❌ Test files em .memory/ → commit bloqueado

**Implementação**: `scripts/git-hooks/pre-commit` (~240 linhas)
**Testes**: `tests/test_precommit_validate_memory.py` (10 testes, 100%)
**Instalação**: `make git-hooks-install`

---

## Comandos Úteis

### MCP Memory Tool (`/memories/`)

```bash
# Criar memória
memory create /memories/python-tips.md

# Visualizar memória
memory view /memories/python-tips.md

# Atualizar memória (str_replace)
memory str_replace /memories/python-tips.md \
  old_str="antigo" \
  new_str="novo"

# Deletar memória
memory delete /memories/python-tips.md

# Listar memórias
memory view /memories/
```

### Scripts Locais (`.memory/`)

```bash
# Salvar memória local
python scripts/mem_save.py \
  --category project \
  --title "Decisão Arquitetural" \
  --content "MongoDB para analytics..."

# Buscar memórias
python scripts/mem_search.py "mongodb migration"

# Ver contexto de memória
python scripts/mem_context.py project

# Limpeza automática
make memory-cleanup              # Dry-run (mostra o que seria removido)
make memory-cleanup-force        # Executar com backup automático
```

### Makefile Targets

```bash
# Validação
make config-validate             # Validar configs críticos
make git-hooks-install           # Instalar pre-commit hooks

# Limpeza
make memory-cleanup              # Dry-run de limpeza
make memory-cleanup-force        # Executar com backup
make clean                       # Limpeza geral do projeto
```

### Git Hooks

```bash
# Instalar hooks
make git-hooks-install

# Hooks instalados:
# - pre-commit: Valida memórias antes de commit
#   - Bloqueia test-*.md em .memory/
#   - Valida YAML frontmatter
# - commit-msg: Valida Conventional Commits

# Bypass (emergências apenas)
git commit --no-verify
```

---

## Troubleshooting

### Problema: Arquivos de teste em `.memory/`

**Sintoma**:
```
❌ Pre-commit validation failed
  ❌ .memory/memories/project/2026-05-18__test-feature.md
     Test files should not be committed to .memory/
```

**Causa**: Testes escrevendo em `.memory/` real ao invés de fixtures isolados

**Solução**:
```bash
# 1. Remover arquivos de teste
make memory-cleanup-force

# 2. Atualizar testes para usar fixtures
# Ver: tests/conftest.py → temp_memory_dir, isolated_memory

# 3. Verificar se resolvido
make memory-cleanup  # Deve mostrar "✅ No files to clean"
```

### Problema: YAML frontmatter inválido

**Sintoma**:
```
❌ Pre-commit validation failed
  ❌ .memory/memories/project/2026-05-18__decision.md
     Invalid category 'proj'. Valid: project, team, decision, pattern, incident, user
```

**Solução**:
```bash
# Editar arquivo e corrigir categoria
vim .memory/memories/project/2026-05-18__decision.md

# Categorias válidas:
# - project
# - team
# - decision
# - pattern
# - incident
# - user
```

### Problema: Memórias duplicadas

**Sintoma**:
```
.memory/memories/project/2026-04-20__test-basic-save.md
.memory/memories/project/2026-04-28__test-basic-save.md
.memory/memories/project/2026-05-11__test-basic-save.md
```

**Causa**: Mesmo arquivo copiado múltiplas vezes

**Solução**:
```bash
# Script detecta duplicados por SHA256 hash
python scripts/memory-cleanup.py --find-duplicates

# Executar limpeza (mantém arquivo mais antigo)
python scripts/memory-cleanup.py --execute --backup --find-duplicates
```

### Problema: User memory muito grande (>200 linhas)

**Sintoma**: Contexto do Copilot poluído, respostas lentas

**Solução**:
```markdown
<!-- /memories/user-preferences.md -->

## Regras Críticas (primeiras 50 linhas)
- Criar arquivos: create_file tool (nunca heredoc)
- Git commits: ./scripts/git-commit-with-file.sh
- Leitura: read_file tool (nunca cat)

## Detalhes completos
Ver: docs/COPILOT_RULES.md (link, não duplicar conteúdo)
```

### Problema: Configs obsoletos não detectados

**Sintoma**: MCP GitHub CLI ainda em uso após atualização

**Solução**:
```bash
# Validar todos os configs
make config-validate

# Saída esperada:
# ✅ MCP GitHub: HTTP configuration (correct)
# ✅ Critical dependencies properly configured
# ✅ .copilot-rules.md exists (7 sections)

# Se falhar:
# ❌ MCP GitHub: Using obsolete CLI configuration
#    Update to HTTP: npx -y @modelcontextprotocol/server-github
#    See: docs/guides/MCP-GITHUB-HTTP-UPDATE.md
```

### Problema: Dependências desatualizadas

**Sintoma**: Passo 4.5 session-start reporta pacotes outdated

**Solução**:
```bash
# Verificar quais pacotes
make deps-check

# Atualizar pacotes críticos (bandit, safety)
make update-deps-safe

# Atualizar todos (cuidado: breaking changes)
make update-deps  # Confirmação interativa
```

**Automação** (IMP-65 P1, implementado 2026-05-20):
- Workflow `.github/workflows/dependency-check.yml` executa semanalmente (segundas 9h UTC)
- `pip-audit` para CVE scanning automático
- `pip list --outdated` para dependency freshness
- Cria issues P0 automaticamente se vulnerabilidades detectadas
- Artifacts: `outdated.json`, `audit.json` (retention 30 dias)
- Testes: `tests/test_dependency_check_workflow.py` (17 testes, 100%)

---

## Referências

### Documentação Relacionada

- [.copilot-rules.md](../.copilot-rules.md): Regras de projeto (P0, P1, P2)
- [.github/copilot-instructions.md](../.github/copilot-instructions.md): Instruções do Copilot
- [docs/INDEX.md](INDEX.md): Índice completo da documentação
- [docs/TODO.md](TODO.md): Tarefas pendentes

### Implementações (IMP-65)

- [docs/debates/DEBATE-001-memory-cleanup-and-session-start-improvements.md](debates/DEBATE-001-memory-cleanup-and-session-start-improvements.md): Debate multi-agente (27K words)
- [docs/planning/ACTION_PLAN-memory-cleanup-and-session-start.md](planning/ACTION_PLAN-memory-cleanup-and-session-start.md): Plano de implementação (17 tasks)
- [docs/planning/EXECUTIVE_SUMMARY-debate-and-action-plan.md](planning/EXECUTIVE_SUMMARY-debate-and-action-plan.md): Sumário executivo

### Scripts

- [scripts/memory-cleanup.py](../scripts/memory-cleanup.py): Limpeza defensiva automática
- [scripts/validate-configs.py](../scripts/validate-configs.py): Validação de configs
- [scripts/git-hooks/pre-commit](../scripts/git-hooks/pre-commit): Hook de validação
- [scripts/mem_save.py](../scripts/mem_save.py): Salvar memória local
- [scripts/mem_search.py](../scripts/mem_search.py): Buscar memórias (FTS5)
- [scripts/mem_context.py](../scripts/mem_context.py): Visualizar contexto

### Workflows

- [.github/workflows/dependency-check.yml](../.github/workflows/dependency-check.yml): CI/CD semanal de dependências
- [.github/prompts/session-start.prompt.md](../.github/prompts/session-start.prompt.md): Ritual de início de sessão (8 passos)

---

**Versão**: 1.1.0
**Última revisão**: 2026-05-20
**Próxima revisão**: 2026-06-20
**Maintainer**: Equipe de Plataforma

---

## Histórico de Mudanças

### 2026-05-20 — v1.1.0 (IMP-65 P1 Complete)
- ✅ Atualizado com implementações IMP-65 P1 completas
- ✅ Seção "Validação" expandida (pre-commit hook details)
- ✅ Troubleshooting "Dependências" expandido (dependency-check workflow)
- ✅ Referências atualizadas (17 testes dependency-check, 10 testes pre-commit)
- ✅ Status: ✅ Estável → ✅ Produção

### 2026-05-18 — v1.0.0 (IMP-65 P1-3)
- ✅ Primeira versão completa da documentação
- ✅ 8 seções conforme ACTION_PLAN
- ✅ Exemplos práticos e troubleshooting
- ✅ Integração com P0/P1 tasks implementadas
