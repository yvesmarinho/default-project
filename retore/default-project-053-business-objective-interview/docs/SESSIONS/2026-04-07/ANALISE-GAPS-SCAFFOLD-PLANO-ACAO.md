# 📋 ANÁLISE DE GAPS DO SCAFFOLD + PLANO DE AÇÃO

**Data**: 2026-04-07 16:50:00
**Contexto**: Análise de conformidade do projeto `yves-eti-br` vs especificação do template
**Trigger**: Debate técnico identificou 9 gaps no sistema de scaffold

---

## 🔍 ANÁLISE DETALHADA DOS GAPS

### ❌ GAP #1: Pasta `.secrets/` sem proteção completa

**Status**: ⚠️ PARCIALMENTE IMPLEMENTADO

**O que existe**:
- ✅ `.secrets/` em `DIRS_TO_CREATE` (scripts/lib/project.py:427)
- ✅ `.secrets/README.md` criado com documentação (projeto.py:212)
- ✅ `.secrets/` no `.gitignore` (projeto.py:181)

**O que falta**:
- ❌ Arquivo `.secrets/.env.example` (template de variáveis)
- ❌ Validação de permissões (`chmod 700 .secrets/`)
- ❌ Pre-commit hook para prevenir commit acidental
- ❌ Script de setup: `scripts/setup-secrets.sh`
- ❌ Documentação em `docs/SECURITY.md` sobre gestão de secrets

**Impacto**: 🟡 MÉDIO
- Risco de commit acidental de credenciais
- Documentação incompleta sobre uso de secrets

**Prioridade**: P1 (Alta)
**Estimativa**: 4h

---

### ❌ GAP #2: Sub-pastas padrão de `docs/` faltando

**Status**: ❌ NÃO IMPLEMENTADO

**O que existe**:
- ✅ `docs/` criado (projeto.py:421)
- ✅ `docs/SESSIONS/` criado (projeto.py:422)
- ✅ `docs/copilot/` criado (projeto.py:423)

**O que falta**:
```
docs/
├── debates/          ❌ FALTANDO (debates técnicos entre agentes)
├── decisions/        ❌ FALTANDO (ADRs - Architecture Decision Records)
├── templates/        ❌ FALTANDO (templates de documentos)
├── guides/           ❌ FALTANDO (guias práticos)
├── retrospectives/   ❌ FALTANDO (retrospectivas de sprint/sessão)
└── architecture/     ❌ FALTANDO (diagramas, C4 models)
```

**Arquivos template faltantes**:
- `docs/templates/CHAT-YYYYMMDD-HHMMSS.md` (captura de conversas)
- `docs/templates/ADR-NNN-titulo.md` (Architecture Decision Record)
- `docs/templates/DEBATE-TEMA.md` (estrutura de debate)
- `docs/templates/RETROSPECTIVE-YYYY-MM-DD.md` (retro de sessão)

**Impacto**: 🟡 MÉDIO
- Documentação desorganizada
- Sem estrutura para ADRs (gap identificado no debate anterior)
- Sem captura sistemática de conversas (IMP-55)

**Prioridade**: P1 (Alta)
**Estimativa**: 3h

---

### ❌ GAP #3: Templates do `.specify/` não copiados

**Status**: ⚠️ PARCIALMENTE IMPLEMENTADO

**O que existe**:
- ✅ Função `copy_speckit()` existe (projeto.py:535)
- ✅ Copia `.specify/templates/` (projeto.py:572-582)
- ✅ Copia agents e prompts (projeto.py:554-567)

**O que aconteceu no `yves-eti-br`**:
- ❓ Templates foram copiados? (verificar se há logs)
- ❓ Destino correto: `{project}/.specify/templates/`

**Verificação necessária**:
```bash
ls -la /home/yves_marinho/DevOps/Projetos/yves-eti-br/.specify/templates/
```

**Se confirmado que falta**:
- ❌ `.specify/templates/spec-template.md`
- ❌ `.specify/templates/plan-template.md`
- ❌ `.specify/templates/tasks-template.md`
- ❌ `.specify/templates/checklist-template.md`
- ❌ `.specify/templates/constitution-template.md`

**Impacto**: 🔴 ALTO
- SpecKit não funciona sem templates
- `/speckit.specify`, `/speckit.plan`, `/speckit.tasks` quebrados

**Prioridade**: P0 (Crítica)
**Estimativa**: 2h (investigação + correção)

---

### ❌ GAP #4: Falta "Resumo completo da criação do projeto"

**Status**: ❌ NÃO IMPLEMENTADO

**O que existe**:
- ✅ Função `print_final_summary()` (lib/ui.py)
- ✅ Lista de `CreatedItem` em memória durante scaffold
- ❌ **NÃO é persistido em arquivo**

**O que falta**:
- Arquivo: `docs/PROJECT_CREATION_SUMMARY.md`
- Conteúdo:
  ```markdown
  # Resumo da Criação do Projeto

  **Data**: YYYY-MM-DD HH:MM:SS
  **Scaffold version**: v1.0.0
  **Comando**: python scripts/scaffold.py new --name ...

  ## Arquivos Criados
  - ✅ README.md
  - ✅ docs/INDEX.md
  - ...

  ## Perfis Aplicados
  - devops-programming
  - typescript-next

  ## Configuração
  - Domínio: programming
  - Linguagem: typescript
  - Repositório: https://github.com/...

  ## Próximos Passos
  1. Configurar secrets: .secrets/.env
  2. Instalar dependências: make install-deps
  3. Inicializar git: git init
  ```

**Impacto**: 🟡 MÉDIO
- Dificulta troubleshooting
- Sem rastro do que foi gerado

**Prioridade**: P2 (Média)
**Estimativa**: 3h

---

### ❌ GAP #5: Pasta `.vscode/` e arquivos MCP incompletos

**Status**: ⚠️ PARCIALMENTE IMPLEMENTADO

**O que existe**:
- ✅ `.vscode/` em `DIRS_TO_CREATE` (projeto.py:428)
- ✅ `.vscode/mcp.json` criado (projeto.py:437)
- ✅ `.vscode/settings.json` criado (projeto.py:438)
- ✅ Funções `vscode.generate_*()` em lib/vscode.py

**O que falta**:
- ❌ `.vscode/extensions.json` - não verificado se é criado
- ❌ `.vscode/tasks.json` - não verificado se é criado
- ❌ `.vscode/launch.json` - não verificado se é criado
- ❌ Configuração de MCP servers específicos do domínio
  - Ex: devops → `@modelcontextprotocol/server-postgres`
  - Ex: security → `@modelcontextprotocol/server-aws`

**Verificação necessária**:
```bash
ls -la /home/yves_marinho/DevOps/Projetos/yves-eti-br/.vscode/
```

**Se confirmado que falta extensions.json**:
```json
{
  "recommendations": [
    "github.copilot",
    "github.copilot-chat",
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode"
  ]
}
```

**Impacto**: 🟡 MÉDIO
- VS Code setup incompleto
- MCP servers genéricos (não otimizados por domínio)

**Prioridade**: P2 (Média)
**Estimativa**: 3h

---

### ❌ GAP #6: Agentes não criados no projeto destino

**Status**: ⚠️ INCOMPLETO (depende de GAP #3)

**O que existe**:
- ✅ Função `copy_speckit()` copia agents (projeto.py:554-567)
- ✅ Glob pattern: `.github/agents/*.agent.md`

**O que deveria ser copiado** (do template → projeto):
```
.github/agents/
├── session-manager.agent.md       ✅ Copiado (verificar)
├── speckit.specify.agent.md       ✅ Copiado (verificar)
├── speckit.clarify.agent.md       ✅ Copiado (verificar)
├── speckit.plan.agent.md          ✅ Copiado (verificar)
├── speckit.tasks.agent.md         ✅ Copiado (verificar)
├── speckit.implement.agent.md     ✅ Copiado (verificar)
├── speckit.analyze.agent.md       ✅ Copiado (verificar)
├── speckit.checklist.agent.md     ✅ Copiado (verificar)
├── speckit.constitution.agent.md  ✅ Copiado (verificar)
├── speckit.taskstoissues.agent.md ✅ Copiado (verificar)
└── template-architect.agent.md    ✅ Copiado (verificar)
```

**O que falta** (se não foram copiados):
- ❌ Agentes customizados do domínio (ex: `security-audit.agent.md`)
- ❌ Agentes de CI/CD (ex: `deployment-manager.agent.md`)

**Verificação necessária**:
```bash
ls -la /home/yves_marinho/DevOps/Projetos/yves-eti-br/.github/agents/
```

**Impacto**: 🔴 ALTO
- Copilot sem agentes = sem workflows SpecKit
- Perda total de produtividade

**Prioridade**: P0 (Crítica)
**Estimativa**: 1h (verificação) + 2h (correção se necessário)

---

### ❌ GAP #7: Arquivo `.code-workspace` não criado

**Status**: ❌ FALSO POSITIVO (É CRIADO!)

**O que existe**:
- ✅ Código cria `{project_name}.code-workspace` (projeto.py:519-529)
- ✅ Template `_CODE_WORKSPACE` definido (projeto.py:346-409)

**Verificação**:
```bash
ls -la /home/yves_marinho/DevOps/Projetos/yves-eti-br/*.code-workspace
```

**Resultado esperado**: `yves-eti-br.code-workspace` deve existir

**Se confirmado que existe**: ✅ **FECHAR ESTE ITEM** (não é bug)

**Se confirmado que NÃO existe**:
- 🔴 Bug crítico na função `create_structure()`
- Investigar: exceção silenciosa?

**Impacto**: 🔴 ALTO (se confirmado bug)
- VS Code não reconhece workspace
- Settings, tasks, launch não aplicados

**Prioridade**: P0 (Crítica se bug) | N/A (se não é bug)
**Estimativa**: 1h (investigação)

---

### ❌ GAP #8: Arquivos de segurança do GitHub faltando

**Status**: ❌ NÃO IMPLEMENTADO

**O que existe**:
- ✅ `.github/` criado (projeto.py:424)
- ❌ **NÃO copia arquivos de segurança**

**O que falta**:
```
.github/
├── SECURITY.md               ❌ FALTANDO (security policy)
├── CODEOWNERS                ❌ FALTANDO (code review assignments)
├── dependabot.yml            ❌ FALTANDO (auto-updates)
├── workflows/
│   ├── security-scan.yml     ❌ FALTANDO (CodeQL, Trivy, etc.)
│   └── dependency-review.yml ❌ FALTANDO (review de PRs)
└── ISSUE_TEMPLATE/
    └── security-report.md    ❌ FALTANDO (template de report)
```

**Hardening não aplicado**:
- ❌ Branch protection rules (documentação ausente)
- ❌ Secret scanning configurado
- ❌ Dependabot configurado
- ❌ Code scanning (CodeQL) configurado
- ❌ Security advisories habilitado

**Impacto**: 🔴 ALTO
- Projeto vulnerável a dependências desatualizadas
- Sem proteção de branches
- Violação do Principle IV (Zero-Trust on Secrets) do constitution

**Prioridade**: P0 (Crítica)
**Estimativa**: 6h

---

### ❌ GAP #9: Estrutura Git não inicializada

**Status**: ⚠️ PARCIALMENTE IMPLEMENTADO

**O que existe**:
- ✅ Função `git.init_repository()` chamada (new_project.py:68)
- ✅ Implementação em `lib/git.py`

**O que aconteceu no `yves-eti-br`**:
```bash
# Repositório informado no comando:
--repo https://github.com/yvesmarinho/yves-eti-br
```

**Verificação necessária**:
```bash
cd /home/yves_marinho/DevOps/Projetos/yves-eti-br
git status  # Se der erro, git não foi inicializado
```

**Se confirmado que NÃO foi inicializado**:
- 🔴 Bug na função `git.init_repository()`
- Investigar: exceção capturada e silenciada?

**O que deveria ter sido feito**:
1. ✅ `git init`
2. ⚠️ `git remote add origin <repo>`
3. ⚠️ `git branch -M main`
4. ❌ Commit inicial: `chore: initial commit from scaffold`
5. ❌ Tags de scaffold: `git tag scaffold-v1.0.0`

**Impacto**: 🟡 MÉDIO
- Git não configurado = sem versionamento
- Sem remote = sem push automático

**Prioridade**: P1 (Alta)
**Estimativa**: 3h

---

## 📊 SCORECARD DE GAPS

| GAP # | Item | Status | Impacto | Prioridade | Estimativa |
|-------|------|--------|---------|------------|------------|
| 1 | `.secrets/` proteção | ⚠️ Parcial | 🟡 Médio | P1 | 4h |
| 2 | Sub-pastas `docs/` | ❌ Ausente | 🟡 Médio | P1 | 3h |
| 3 | Templates `.specify/` | ⚠️ Verificar | 🔴 Alto | P0 | 2h |
| 4 | Resumo de criação | ❌ Ausente | 🟡 Médio | P2 | 3h |
| 5 | `.vscode/` completo | ⚠️ Verificar | 🟡 Médio | P2 | 3h |
| 6 | Agentes copiados | ⚠️ Verificar | 🔴 Alto | P0 | 3h |
| 7 | `.code-workspace` | ⚠️ Verificar | 🔴 Alto | P0 | 1h |
| 8 | Segurança GitHub | ❌ Ausente | 🔴 Alto | P0 | 6h |
| 9 | Git inicializado | ⚠️ Verificar | 🟡 Médio | P1 | 3h |

**Total estimado**: **28 horas** (3.5 dias de trabalho)

---

## 🎯 PLANO DE AÇÃO

### 🔴 **FASE 1: VERIFICAÇÃO URGENTE** (P0 - 6h)

**Objetivo**: Confirmar se bugs existem ou são falsos positivos

**Tarefas**:
1. **[VERIFY-01]** Verificar se `.specify/templates/` foi copiado
   ```bash
   ls -la /home/yves_marinho/DevOps/Projetos/yves-eti-br/.specify/templates/
   ```
   - Se VAZIO → BUG confirmado ⚠️
   - Se CHEIO → Fechar GAP #3 ✅

2. **[VERIFY-02]** Verificar se agentes foram copiados
   ```bash
   ls -la /home/yves_marinho/DevOps/Projetos/yves-eti-br/.github/agents/
   ```
   - Se VAZIO → BUG confirmado ⚠️
   - Se CHEIO → Fechar GAP #6 ✅

3. **[VERIFY-03]** Verificar se `.code-workspace` existe
   ```bash
   ls -la /home/yves_marinho/DevOps/Projetos/yves-eti-br/*.code-workspace
   ```
   - Se NÃO EXISTE → BUG confirmado ⚠️
   - Se EXISTE → Fechar GAP #7 ✅

4. **[VERIFY-04]** Verificar se `.vscode/` completo
   ```bash
   ls -la /home/yves_marinho/DevOps/Projetos/yves-eti-br/.vscode/
   ```
   - Verificar: `extensions.json`, `tasks.json`, `launch.json`

5. **[VERIFY-05]** Verificar se git foi inicializado
   ```bash
   cd /home/yves_marinho/DevOps/Projetos/yves-eti-br && git status
   ```
   - Se erro → BUG confirmado ⚠️
   - Se OK → Verificar se remote configurado

**Deliverable**: Relatório de bugs confirmados vs falsos positivos

---

### 🔴 **FASE 2: CORREÇÕES CRÍTICAS** (P0 - 8h)

**Objetivo**: Corrigir bugs críticos que impedem uso do SpecKit

**Tarefas**:

1. **[BUG-04]** Corrigir cópia de templates `.specify/`
   - **Se confirmado bug**: Investigar `copy_speckit()` (projeto.py:535)
   - Provável causa: path relativo incorreto
   - Teste: Criar projeto novo e verificar templates
   - **Estimativa**: 2h

2. **[BUG-05]** Corrigir cópia de agentes `.github/agents/`
   - **Se confirmado bug**: Mesmo código de GAP #3
   - **Estimativa**: 1h (já corrigido junto com GAP #3)

3. **[BUG-06]** Implementar arquivos de segurança GitHub
   - Criar templates:
     - `.github/SECURITY.md`
     - `.github/CODEOWNERS`
     - `.github/dependabot.yml`
     - `.github/workflows/security-scan.yml`
   - Adicionar em `FILES_TO_CREATE`
   - **Estimativa**: 6h

**Deliverable**: Scaffold gera projeto completo com SpecKit funcional

---

### 🟡 **FASE 3: MELHORIAS IMPORTANTES** (P1 - 10h)

**Objetivo**: Completar estrutura padrão do projeto

**Tarefas**:

1. **[IMP-60]** Completar proteção de `.secrets/`
   - Adicionar `.secrets/.env.example`
   - Script `scripts/setup-secrets.sh` com `chmod 700`
   - Pre-commit hook para secrets scanning
   - Documentação em `docs/SECURITY.md`
   - **Estimativa**: 4h

2. **[IMP-61]** Criar sub-pastas padrão de `docs/`
   - Adicionar em `DIRS_TO_CREATE`:
     ```python
     "docs/debates",
     "docs/decisions",
     "docs/templates",
     "docs/guides",
     "docs/retrospectives",
     "docs/architecture",
     ```
   - Criar templates em `docs/templates/`:
     - `ADR-template.md`
     - `DEBATE-template.md`
     - `CHAT-template.md`
     - `RETROSPECTIVE-template.md`
   - **Estimativa**: 3h

3. **[IMP-62]** Melhorar inicialização Git
   - Commit inicial automático
   - Tag de scaffold: `git tag scaffold-v1.0.0`
   - Documentar branches sugeridas (main, develop, feature/*)
   - **Estimativa**: 3h

**Deliverable**: Projeto com estrutura completa e boas práticas

---

### 🟢 **FASE 4: FEATURES ADICIONAIS** (P2 - 6h)

**Objetivo**: Documentação e rastreabilidade

**Tarefas**:

1. **[IMP-63]** Gerar resumo de criação do projeto
   - Função: `project.generate_creation_summary()`
   - Arquivo: `docs/PROJECT_CREATION_SUMMARY.md`
   - Conteúdo:
     - Data/hora de criação
     - Comando usado
     - Arquivos criados (lista de `CreatedItem`)
     - Perfis aplicados
     - Configuração (domain, language, repo)
     - Próximos passos sugeridos
   - **Estimativa**: 3h

2. **[IMP-64]** Completar setup `.vscode/`
   - Criar `extensions.json` por domínio
   - MCP servers específicos por domínio:
     - `devops-*` → postgres, aws, kubernetes
     - `python-*` → pylance, jupyter
     - `typescript-*` → eslint, prettier
   - **Estimativa**: 3h

**Deliverable**: Experiência completa de onboarding

---

## 📝 ISSUES A CRIAR

### Verificações (P0 - URGENTE)
- [ ] **[VERIFY-01]** Verificar cópia de `.specify/templates/` no yves-eti-br
- [ ] **[VERIFY-02]** Verificar cópia de agentes no yves-eti-br
- [ ] **[VERIFY-03]** Verificar existência de `.code-workspace`
- [ ] **[VERIFY-04]** Verificar arquivos `.vscode/`
- [ ] **[VERIFY-05]** Verificar inicialização Git

### Bugs Críticos (P0)
- [ ] **[BUG-04]** Scaffold não copia templates `.specify/` (se confirmado)
- [ ] **[BUG-05]** Scaffold não copia agentes `.github/agents/` (se confirmado)
- [ ] **[BUG-06]** Faltam arquivos de segurança GitHub (hardening)
- [ ] **[BUG-07]** Git não inicializado corretamente (se confirmado)
- [ ] **[BUG-08]** `.code-workspace` não criado (se confirmado)

### Improvements (P1)
- [ ] **[IMP-60]** Completar proteção de `.secrets/` (chmod, pre-commit, docs)
- [ ] **[IMP-61]** Criar sub-pastas padrão de `docs/` (debates, decisions, etc.)
- [ ] **[IMP-62]** Melhorar inicialização Git (commit inicial, tags, remotes)

### Features (P2)
- [ ] **[IMP-63]** Gerar `docs/PROJECT_CREATION_SUMMARY.md` ao final do scaffold
- [ ] **[IMP-64]** Completar setup `.vscode/` (extensions, MCP por domínio)

---

## 🔄 ATUALIZAÇÃO DO WORKFLOW SPECKIT

### **Workflow Atual** (ANTES das correções):

```
1. /speckit.specify    → Cria spec.md
2. /speckit.clarify    → Clarifica underspec
3. /speckit.plan       → Gera plan.md
4. /speckit.tasks      → Gera tasks.md
5. /speckit.implement  → Executa tasks
6. /speckit.analyze    → Valida consistência
```

### **Workflow Proposto** (DEPOIS das correções):

```
0. 🆕 /scaffold.verify  → Verifica se projeto foi gerado corretamente
1. /speckit.specify    → Cria spec.md
2. /speckit.clarify    → Clarifica underspec
3. /speckit.plan       → Gera plan.md
   ├─ 3a. 🆕 ADR check → Valida ADRs em plan.md
   └─ 3b. 🆕 Security  → Valida security headers, HSTS, CSP
4. /speckit.tasks      → Gera tasks.md
5. /speckit.implement  → Executa tasks
6. /speckit.analyze    → Valida consistência
   ├─ 6a. ✅ Spec vs Code
   ├─ 6b. ✅ Plan vs Tasks
   ├─ 6c. 🆕 Security hardening check
   └─ 6d. 🆕 Docs structure check
7. 🆕 /speckit.document → Gera docs/PROJECT_SUMMARY.md
```

### **Novos Agentes Necessários**:

1. **`scaffold-verifier.agent.md`** (P0)
   - Verifica se projeto foi scaffolded corretamente
   - Checa: templates, agentes, .vscode/, git, .secrets/
   - Gera relatório de conformidade

2. **`security-auditor.agent.md`** (P0)
   - Valida configurações de segurança
   - Checa: headers HTTP, hardening GitHub, secrets
   - Integrado no `/speckit.analyze`

3. **`docs-structure-validator.agent.md`** (P1)
   - Valida estrutura de docs/
   - Checa: sub-pastas, templates, índices
   - Sugere criação de docs faltantes

4. **`adr-reviewer.agent.md`** (P2)
   - Revisa ADRs no plan.md
   - Valida: contexto, decisão, consequências
   - Sugere melhorias

---

## ⚡ QUICK WINS (podem ser feitos hoje)

### 1. **Verificar bugs no yves-eti-br** (30 min)
```bash
cd /home/yves_marinho/DevOps/Projetos/yves-eti-br

# Verificação 1: Templates
ls -la .specify/templates/

# Verificação 2: Agentes
ls -la .github/agents/

# Verificação 3: Workspace
ls -la *.code-workspace

# Verificação 4: VS Code
ls -la .vscode/

# Verificação 5: Git
git status
git remote -v
```

### 2. **Adicionar sub-pastas docs/** (15 min)
```python
# Em scripts/lib/project.py, adicionar:
DIRS_TO_CREATE = [
    # ... existentes ...
    "docs/debates",
    "docs/decisions",
    "docs/templates",
    "docs/guides",
    "docs/retrospectives",
    "docs/architecture",
]
```

### 3. **Criar template de ADR** (20 min)
```markdown
# ADR-NNN: [Título da Decisão]

**Data**: YYYY-MM-DD
**Status**: Proposto | Aceito | Rejeitado | Deprecated
**Contexto**: [Feature/Issue]

## Contexto

[Descrever o problema, requisitos, constraints]

## Decisão

[Qual decisão foi tomada e por quê]

## Consequências

### Positivas
- [Benefício 1]
- [Benefício 2]

### Negativas
- [Custo 1]
- [Risco 1]

### Mitigações
- [Como mitigar riscos]
```

---

## 📈 MÉTRICAS DE SUCESSO

### **Pré-correção** (yves-eti-br atual):
- ⚠️ Templates copiados: ? (verificar)
- ⚠️ Agentes copiados: ? (verificar)
- ❌ Arquivos segurança: 0/5
- ❌ Sub-pastas docs: 0/6
- ⚠️ Git configurado: Parcial
- ❌ Resumo criação: Não existe

**Score**: **~40%** (assumindo bugs confirmados)

### **Pós-correção** (objetivo):
- ✅ Templates copiados: 100%
- ✅ Agentes copiados: 100%
- ✅ Arquivos segurança: 5/5
- ✅ Sub-pastas docs: 6/6
- ✅ Git configurado: 100%
- ✅ Resumo criação: Gerado

**Score**: **100%**

---

## 🎯 PRIORIZAÇÃO FINAL

### **Semana 1** (P0 - Crítico):
- [ ] Dia 1: Verificações (VERIFY-01 a 05)
- [ ] Dia 2-3: Correções de bugs (BUG-04 a 08)
- [ ] Dia 4: Arquivos de segurança (BUG-06)
- [ ] Dia 5: Testes e validação

### **Semana 2** (P1 - Importante):
- [ ] Dia 1-2: Proteção `.secrets/` (IMP-60)
- [ ] Dia 3: Sub-pastas `docs/` (IMP-61)
- [ ] Dia 4: Git melhorado (IMP-62)
- [ ] Dia 5: Testes e documentação

### **Semana 3** (P2 - Desejável):
- [ ] Dia 1-2: Resumo de criação (IMP-63)
- [ ] Dia 3: VS Code completo (IMP-64)
- [ ] Dia 4-5: Novos agentes (scaffold-verifier, security-auditor)

---

## 📚 REFERÊNCIAS

1. **Debate Técnico**: `docs/SESSIONS/2026-04-07/DEBATE-TECHNICAL-REVIEW-yves-eti-br.md`
2. **Chat Anterior**: `docs/SESSIONS/2026-04-07/CHAT-20260407-155500.md`
3. **Lembrete Original**: `docs/lembrete.md`
4. **Código Scaffold**: `scripts/lib/project.py`, `scripts/lib/flows/new_project.py`
5. **SpecKit Agents**: `.github/agents/speckit.*.agent.md`

---

**Documento criado**: 2026-04-07 16:50:00
**Próxima ação**: Executar FASE 1 (Verificações) no projeto yves-eti-br
**Responsável**: @template-architect + @session-manager + @devops_lima

---

**EOF**
