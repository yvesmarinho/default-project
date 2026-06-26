---
mode: agent
description: Ritual de início de sessão recorrente. Execute no começo de cada sessão de trabalho.
---

# 🚀 Session Start — Ritual de Início de Sessão

> Execute este ritual **no início de cada sessão** (não da primeira — para primeira sessão use `session-start-first.prompt.md`).

---

## 🎯 Modo de Execução

Antes de iniciar, pergunte ao usuário:

```
Modo de execução: [quick | completo]
```

**Modo QUICK** (IMP-65 P2 — ~5s de duração):
- ✅ Passos essenciais apenas (0, 1, 2, 3, 4, 4.5)
- ❌ Pula: git status, documentos de sessão, escopo
- **Quando usar**: Sessões rápidas de debugging, consultas pontuais, verificações rápidas

**Modo COMPLETO** (~15s de duração):
- ✅ Todos os passos (0-8, completo + robusto)
- **Quando usar**: Sessões de desenvolvimento, implementações, sessões longas

**Passos por modo**:

| Passo | Quick | Completo | Descrição |
|-------|-------|----------|-----------|
| 0. Time Tracker | ✅ | ✅ | session-time-tracker.py start (sempre) |
| 1. Verificar MCP | ✅ | ✅ | Configuração MCP servers |
| 2. Recuperar Contexto | ✅ | ✅ | TODO.md, INDEX.md, sessão anterior |
| 3. Carregar Regras | ✅ | ✅ | .copilot-rules.md enforcement |
| 4. Scan Segurança | ✅ | ✅ | Verificar credenciais expostas |
| 4.5. Dependências | ✅ | ✅ | Verificar vulnerabilidades |
| 5. Estado do Projeto | ❌ | ✅ | git status, log |
| 6. Docs de Sessão | ❌ | ✅ | SESSION_RECOVERY, DAILY_ACTIVITIES |
| 6.5. Session Index | ❌ | ✅ | Verificar session-index.db |
| 7. Escopo da Sessão | ❌ | ✅ | Domain profile, objetivo |
| 8. Atualizar Índice | ❌ | ✅ | TODO.md, índice de sessão |

---

## ▶️ Execução do Ritual

Execute os passos abaixo em ordem. Confirme cada etapa antes de avançar.

**Se modo QUICK**: Execute passos 0-4.5 e pule para "Checklist Final".
**Se modo COMPLETO**: Execute todos os passos 0-8.

---

### Passo 0 — Iniciar Rastreamento de Tempo (SEMPRE — QUICK e COMPLETO)

**Ação do agente**: Disparar `session-time-tracker.py start` imediatamente, antes de qualquer outro passo.

```python
python3 - << 'EOF'
import subprocess
from pathlib import Path

tracker = Path("scripts/session-time-tracker.py")
if not tracker.exists():
    print("⚠️  session-time-tracker.py não encontrado — pular")
else:
    result = subprocess.run(
        ["python3", str(tracker), "start"],
        capture_output=True, text=True,
    )
    if result.returncode == 0:
        print(result.stdout.strip() or "✅ Session time tracker: iniciado")
    else:
        # Sessão já ativa é aceitável — não bloquear o ritual
        print(f"⚠️  Time tracker: {result.stderr.strip() or result.stdout.strip()}")
EOF
```

**Resultado esperado**:
```
✅ Session time tracker: iniciado
Session ID: [auto-generated]
Start time: [YYYY-MM-DD HH:MM:SS]
```

> Se já existir uma sessão ativa (restart do prompt), o tracker irá reportar
> o aviso — **não bloquear o ritual**. O tempo continuará contando da sessão existente.

---

### Passo 1 — Verificar Configuração MCP

**Ação do agente**: ler `.vscode/mcp.json` e confirmar que os servidores abaixo estão configurados e **não comentados**:

| Servidor | Propósito |
|----------|-----------|
| `memory` | Memória persistente entre sessões |
| `sequential-thinking` | Raciocínio estruturado |

Resultado esperado:
```
✅ MCP Config OK — memory ✅ | sequential-thinking ✅
```

Se algum servidor estiver ausente ou comentado no arquivo → reportar e instruir o usuário a descomentar e executar `Command Palette → "MCP: Refresh Servers"`.

> **Nota**: verificar se os servidores estão *em execução* no VS Code requer ação manual do usuário: `Command Palette → "MCP: List Servers"`. O agente verifica apenas a configuração em arquivo.

---

### Passo 2 — Recuperar Contexto da Sessão Anterior

Leia os seguintes arquivos na ordem indicada:

1. `docs/TODO.md` — estado atual de todas as tarefas
2. `docs/INDEX.md` — mapa de arquivos importantes
3. `docs/SESSIONS/[YYYY-MM-DD mais recente]/FINAL_STATUS_*.md` — estado final da última sessão
4. `docs/SESSIONS/[YYYY-MM-DD mais recente]/DAILY_ACTIVITIES_*.md` — atividades detalhadas
5. `.copilot-rules.md` — regras ativas (Camada 1, sempre prevalecem)

**Ao final deste passo, declare:**
```
✅ Contexto recuperado. Última sessão: [data].
Itens pendentes de alta prioridade: [lista dos P0/P1 do TODO.md].
Regras ativas carregadas: .copilot-rules.md [N] linhas, [N] seções.
```

---

### Passo 3 — Carregar Regras Copilot

**ENFORCEMENT TÉCNICO** — Executar read_file nos arquivos críticos:

1. **Regras completas**: `.copilot-rules.md` (7 seções, ~400 linhas)
   ```
   read_file(.copilot-rules.md, startLine=1, endLine=50)
   ```
   - P0: Criar/editar arquivos NUNCA via terminal → `create_file`, `replace_string_in_file`
   - P0: Ler/buscar/listar NUNCA via terminal → `read_file`, `grep_search`, `file_search`, `list_dir`
   - P0: Mover/copiar/excluir → Python stdlib (shutil, pathlib, logging)
   - P0: Git commits ≥6 linhas → `./scripts/git-commit-with-file.sh`

2. **Instruções customizadas**: `.github/copilot-instructions.md` (~100 linhas)
   ```
   read_file(.github/copilot-instructions.md, startLine=1, endLine=100)
   ```
   - Resumo das regras P0/P1
   - Estrutura do projeto
   - Rituais de sessão

**Checklist de confirmação**:

| Regra | Verificado |
|-------|-----------|
| `.copilot-rules.md` lido e carregado | ✅ |
| `.github/copilot-instructions.md` lido e carregado | ✅ |
| P0: Nunca heredoc/echo para criar arquivos | ✅ |
| P0: Nunca cat/grep/find/ls via terminal | ✅ |
| P0: Mover/copiar/excluir → Python stdlib | ✅ |

Se existir `.copilot-rules-[projeto].md` específico, ler também (Camada 3).

---

### Passo 4 — Scan de Segurança

Verificar ausência de credenciais ou arquivos sensíveis fora de `.secrets/`:

Padrões a verificar (excluindo `.git/` e `.secrets/`):
```
*.env, .env*, *.key, *.pem, *.crt, *.p12
*secret*, *password*, *token*, *credentials*, *.log
```

**Resultado esperado**: `🟢 LIMPO — nenhum arquivo sensível fora de .secrets/`

Se encontrar algo: **PARAR e reportar antes de continuar.**

Verificar também:
- `.secrets/` está no `.gitignore` ✅
- Nenhum valor real em `.env.example` (apenas placeholders)

---

### Passo 4.5 — Verificação de Dependências

**Ação do agente**: Verificar pacotes desatualizados e vulnerabilidades de segurança.

**Comando**:
```bash
pip list --outdated --format=json | python -c "
import sys, json
data = json.load(sys.stdin) if sys.stdin.isatty() == False else []

# Pacotes críticos de segurança
critical_packages = ['bandit', 'safety', 'pytest']
critical = [p for p in data if p['name'] in critical_packages]

# Pacotes desatualizados gerais
if critical:
    print('🚨 PACOTES CRÍTICOS DESATUALIZADOS!')
    for p in critical:
        print(f\"  - {p['name']}: {p['version']} → {p['latest_version']}\")
    print('\n⚠️  Execute: make update-deps-safe')
    sys.exit(1)  # Bloqueia sessão (força atualização)

elif len(data) > 0:
    print(f'⚠️  {len(data)} pacote(s) desatualizado(s) (não-críticos)')
    print('💡 Sugestão: Execute \"make update-deps\" quando tiver tempo')
else:
    print('✅ Todas dependências atualizadas')
"
```

**Resultado esperado**:

**Cenário 1 — Tudo atualizado** (mais comum):
```
✅ Todas dependências atualizadas
```

**Cenário 2 — Deps não-críticos desatualizados**:
```
⚠️  5 pacote(s) desatualizado(s) (não-críticos)
💡 Sugestão: Execute "make update-deps" quando tiver tempo
```

**Cenário 3 — Deps críticos desatualizados** (bloqueia sessão):
```
🚨 PACOTES CRÍTICOS DESATUALIZADOS!
  - bandit: 1.7.5 → 1.7.8
  - safety: 3.0.0 → 3.1.0

⚠️  Execute: make update-deps-safe

❌ SESSÃO BLOQUEADA — Corrija vulnerabilidades antes de continuar
```

**Duração esperada**: 3-5 segundos

---

### Passo 5 — Verificar Estado do Projeto

> **🚀 Modo QUICK**: ⏭️ **PULAR este passo** (ir para Passo 6 ou Checklist Final)

```bash
git status          # arquivos modificados não commitados
git log --oneline -5   # últimos 5 commits
```

**Interpretar:**
- Arquivos inesperadamente modificados → investigar antes de continuar
- Branch ativa diferente do esperado → confirmar com usuário
- Muitos commits não pushados → sugerir `git push` antes de iniciar

---

<!--
### Passo 5.5 — Verificar Memórias Relevantes (OPCIONAL — IMP-59)

**ATENÇÃO**: Este passo é opcional e requer que o Mini-Engram Memory System (IMP-59) esteja instalado.

**Verificar disponibilidade**:
```bash
test -f scripts/mem_context.py && echo "✅ Mini-Engram disponível" || echo "⚠ Mini-Engram não instalado"
```

**Se disponível**, executar análise de contexto:
```bash
make memory-context
# OU
python scripts/mem_context.py --auto
```

**Resultado esperado**:
```
💡 Suggested Context for Current Session

Based on: Branch: 060-mini-engram-python, Recent commits: ...

[1] Memory Title (95% relevance)
    Category: project | Updated: 2026-04-20
    Why: Title matches; Tags match; Branch context
    File: .memory/memories/project/2026-04-20__memory.md
```

**Ações**:
1. Revisar as memórias sugeridas (top 3-5)
2. Abrir arquivos relevantes em `.memory/memories/` se necessário
3. Incorporar insights ao planejamento da sessão

Se não houver memórias relevantes (score < 40%): continuar normalmente.

**Resultado**: `✅ Memórias verificadas: [N] relevantes encontradas` ou `⚠ Mini-Engram não disponível (pular)`

-->

---

### Passo 6 — Criar Documentos de Sessão e Carregar Protocolo

> **🚀 Modo QUICK**: ⏭️ **PULAR este passo** (ir para Passo 7 ou Checklist Final)

Criar os arquivos de sessão do dia (se ainda não existirem):

**Caminho**: `docs/SESSIONS/[YYYY-MM-DD]/`

Arquivos a criar:
1. `SESSION_RECOVERY_[YYYY-MM-DD].md` — resumo do contexto recuperado
2. `DAILY_ACTIVITIES_[YYYY-MM-DD].md` — log de atividades (será preenchido durante a sessão)

**Template SESSION_RECOVERY**:
```markdown
# 🔄 Session Recovery — [YYYY-MM-DD]

**Sessão anterior**: [data]
**Branch**: [branch ativa]
**Status dos IMPs**: [lista resumida]

## Contexto Recuperado
[resumo do que foi feito anteriormente]

## Itens P0 para Esta Sessão
[lista do TODO.md]
```

**Protocolo de Documentação Incremental**:

Durante a sessão, o agente deve **atualizar incrementalmente** `DAILY_ACTIVITIES_[YYYY-MM-DD].md` seguindo o formato estruturado definido em [`docs/guides/SESSION_DOCS_STYLE_GUIDE.md`](../../docs/guides/SESSION_DOCS_STYLE_GUIDE.md).

**Regras de documentação durante a sessão**:

1. **Quando documentar**: Após completar atividades significativas (>= 10 linhas de código, decisões técnicas, criação/modificação de documentação estrutural)

2. **Formato obrigatório**: Usar template canônico com separador `---` e campos estruturados:
   ```markdown
   ---

   ### [Título da Atividade] ([TODO-ID])

   **HH:MM — [STATUS]**

   **Objetivo**: [O que foi feito]
   **Contexto**: [Por que foi necessário]
   **Passos executados**:
   1. [Passo 1 com ferramenta usada]
   2. [Passo 2 com comando executado]

   **Resultado**: [Outcome — sucesso/bloqueio/aprendizado]
   **Arquivos modificados/criados**:
   - path/to/file.py (+N/-N)

   **Commits**:
   - `abc1234` — tipo(escopo): descrição

   **Status**: [✅ Completo | 🔵 Em progresso | ❌ Bloqueado | ⏸️ On hold]

   ---
   ```

3. **Atualização**: Usar `replace_string_in_file` em modo **append** (adicionar blocos ao final do arquivo)

4. **Não documentar**: Typos (< 5 linhas), chores, mudanças cosméticas

5. **Segurança**: NUNCA incluir credenciais, tokens, senhas, ou dados sensíveis nos blocos

**Carregar style guide**:
- Ler [`docs/guides/SESSION_DOCS_STYLE_GUIDE.md`](../../docs/guides/SESSION_DOCS_STYLE_GUIDE.md) após criar os arquivos de sessão
- Confirmar compreensão dos campos obrigatórios vs opcionais
- Confirmar compreensão dos anti-padrões (DO/DON'T)

**Resultado esperado**:
```
✅ Documentos de sessão criados
✅ SESSION_DOCS_STYLE_GUIDE.md carregado — protocolo ativo
```

---

### Passo 6.5 — Verificar Session Index

> **🚀 Modo QUICK**: ⏭️ **PULAR este passo** (ir para Passo 7 ou Checklist Final)

> **Nota**: O Session Time Tracker já foi iniciado no Passo 0 (automático). Este passo
> verifica apenas o session-index (base de busca em sessões anteriores).

**Ação do agente**: Garantir que session-index está operacional.

```python
python3 - << 'EOF'
from pathlib import Path
import subprocess

index_db = Path(".session-index/index.db")
if not index_db.exists():
    print("⚠️  Session index não encontrado. Reconstruindo...")
    result = subprocess.run(
        ["python3", "scripts/session-index.py", "--rebuild"],
        capture_output=True, text=True,
    )
    print(result.stdout.strip() or "✅ Session index reconstruído")
else:
    size_kb = index_db.stat().st_size // 1024
    print(f"✅ Session index OK ({size_kb}KB)")
EOF
```

**Resultado esperado**:
```
✅ Session index OK (~50KB ou mais)
```

**Resultado geral do passo**:
```
✅ Session index: operacional
✅ Session time tracker: ativo desde Passo 0
```

---

### Passo 7 — Definir Escopo da Sessão

> **🚀 Modo QUICK**: ⏭️ **PULAR este passo** (ir para Passo 8 ou Checklist Final)

Pergunte ao usuário sobre o escopo desta sessão:

```
📋 Escopo da Sessão

Você deseja:
[1] Continuar tarefas pendentes da sessão anterior
[2] Iniciar novas tarefas

Escolha [1 ou 2]:
```

**Se escolher [1] — Continuar tarefas anteriores**:

1. Extrair do `docs/TODO.md` todos os itens pendentes (não marcados como `[x]`)
2. Listar por prioridade (P0 > P1 > P2 > P3)
3. Perguntar qual tarefa priorizar ou se trabalhar em sequência
4. Identificar o Domain Profile pelo tipo de tarefa:
   - Feature/Bug/Test → PROGRAMMING
   - CI/CD/Deploy/Infrastructure → INFRASTRUCTURE
   - Debugging/Performance/Analysis → ANALYSIS
5. Carregar Domain Profile correspondente

**Se escolher [2] — Novas tarefas**:

Pergunte:
```
Modo: [PROGRAMMING | INFRASTRUCTURE | ANALYSIS]
Objetivo: [1 frase descrevendo o foco da sessão]
```

Com base na resposta, carregar o Domain Profile correspondente:
- `PROGRAMMING` → `.github/prompts/domain/devops-programming.prompt.md`
- `INFRASTRUCTURE` → `.github/prompts/domain/devops-infrastructure.prompt.md`
- `ANALYSIS` → `.github/prompts/domain/devops-analysis.prompt.md`

**Resultado esperado**:
```
✅ Escopo definido: [Continuar | Novas tarefas]
✅ Domain Profile carregado: [PROGRAMMING | INFRASTRUCTURE | ANALYSIS]
✅ Objetivo: [descrição da tarefa]
```

---

### Passo 8 — Atualizar Índice e TODO

> **🚀 Modo QUICK**: ⏭️ **PULAR este passo** (ir para Checklist Final)

Atualizar `docs/TODO.md`:
- Verificar se há itens "in-progress" da sessão anterior sem conclusão registrada
- Adicionar itens novos identificados durante a recuperação de contexto

---

## ✅ Checklist Final de Início de Sessão

### Modo QUICK

Antes de começar o trabalho efetivo, confirmar:

- [ ] **Session time tracker iniciado** (Passo 0 — automático)
- [ ] MCP configurado em `.vscode/mcp.json` (memory ✅ + sequential-thinking ✅)
- [ ] Contexto da sessão anterior recuperado e declarado
- [ ] `.copilot-rules.md` lido e regras P0 ativas
- [ ] Scan de segurança: 🟢 LIMPO
- [ ] Dependências verificadas (sem vulnerabilidades críticas)

**Duração esperada**: ~5s
**Resultado**: `✅ Session started (QUICK mode) — ready to work`

---

### Modo COMPLETO

Antes de começar o trabalho efetivo, confirmar:

- [ ] **Session time tracker iniciado** (Passo 0 — automático)
- [ ] MCP configurado em `.vscode/mcp.json` (memory ✅ + sequential-thinking ✅)
- [ ] Contexto da sessão anterior recuperado e declarado
- [ ] `.copilot-rules.md` lido e regras P0 ativas
- [ ] Scan de segurança: 🟢 LIMPO
- [ ] Dependências verificadas (sem vulnerabilidades críticas)
- [ ] `git status` verificado — sem surpresas
- [ ] `SESSION_RECOVERY_[data].md` criado
- [ ] `DAILY_ACTIVITIES_[data].md` criado
- [ ] Session index operacional
- [ ] Domínio declarado + Domain Profile carregado
- [ ] Objetivo da sessão declarado em 1 frase

**Duração esperada**: ~15s
**Resultado**: `✅ Session started (COMPLETO mode) — ready to work`

---

## ⚠️ Anti-Patterns de Início de Sessão

| ❌ Proibido | ✅ Correto |
|------------|-----------|
| Começar a escrever código sem recuperar contexto | Sempre ler TODO.md primeiro |
| Supor qual era o estado do projeto | Ler FINAL_STATUS da última sessão |
| Pular o scan de segurança | Scan obrigatório a cada sessão (ambos modos) |
| Trabalhar sem declarar o domínio (modo completo) | Declarar modo antes do primeiro commit |
| Criar arquivos sem verificar se já existem | Checar com file_search antes de criar |
| Usar modo QUICK para sessões longas de desenvolvimento | Usar modo COMPLETO para implementações |
| Usar modo COMPLETO para consultas rápidas | Usar modo QUICK para debugging pontual |

---

## 💡 Quando Usar Cada Modo

### Use Modo QUICK quando:
- ✅ Debugging pontual (< 30 minutos)
- ✅ Consultas rápidas de código
- ✅ Verificações de configuração
- ✅ Sessões de leitura (sem commits)
- ✅ Hotfix urgente (já sabe exatamente o que fazer)

### Use Modo COMPLETO quando:
- ✅ Implementações de features (IMP-*)
- ✅ Correção de bugs documentados (BUG-*)
- ✅ Sessões longas (> 1 hora)
- ✅ Trabalho que requer documentação (DAILY_ACTIVITIES)
- ✅ Trabalho colaborativo (precisa rastrear tempo/atividades)

---

*Session Start Prompt v2.0 | IMP-65 P2 | 2026-05-20*
