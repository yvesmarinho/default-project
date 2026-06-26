<!--
Criado em: 26/06/2026 00:00
Modificado em: 26/06/2026 16:30
-->

# 📋 Daily Activities — 2026-06-26

**Branch**: master
**Objetivo da sessão**: Correção de bugs no scaffold — arquitetura SpecKit/Claude/Copilot.

---

### Correção BUG-scaffold-claude-agents + BUG-speckit-via-copy-not-init (P0)

**11:00 — ✅ Completo**

**Objetivo**: Corrigir geração incorreta de agents Copilot em projetos `ai_assistant=claude` e migrar assets SpecKit para geração exclusiva via `specify init`.

**Contexto**: Análise de `tmp/test-runs/test-000-prog-py-claude` revelou 17 agents Copilot gerados indevidamente; `copy_speckit()` copiava tudo sem filtrar por IA; `run_speckit_init()` falhava silenciosamente sem diagnóstico útil.

**Passos executados**:
1. Analisou `tmp/stdout.txt` e identificou que `specify init --integration claude` retornou code ≠ 0 com stderr vazio
2. Testou `specify init --here --force --integration claude` manualmente → funciona (exit 0)
3. Testou via `subprocess.run` com `capture_output=True` → funciona; raiz do hanging era stdin herdado do TTY
4. Testou `specify init --integration copilot` → confirma que só gera `speckit.*` em `.github/agents/`
5. Refatorou `copy_speckit()`: remove toda cópia de agents/prompts; copia apenas perfis de domínio para TODAS as IAs
6. Criou `copy_custom_agents()`: nova etapa independente, copia agents não-`speckit.*` para `claude`/`copilot`/`both`; ignora `none`
7. Corrigiu `run_speckit_init()`: adicionou `stdin=subprocess.DEVNULL` + log `stderr or stdout` no diagnóstico de erro
8. Moveu ISSUE_TEMPLATE para `copy_github_templates()` (onde pertence semanticamente)
9. Atualizou `tests/test_smoke_imp17.py` para chamar `copy_github_templates()` no teste de ISSUE_TEMPLATE

**Resultado**: 251 passed, 5 failed (pré-existentes em `test_github_best_practices_p2.py`), 7 skipped — sem regressões.

**Decisões técnicas**:
- Perfis de domínio copiados para TODAS as IAs (Claude também referencia `.github/prompts/domain/` em `session-start..md`)
- `copy_custom_agents()` pula arquivos `speckit.*` (gerenciados exclusivamente pelo `specify init`)
- `stdin=subprocess.DEVNULL` evita blocking quando scaffold executa dentro de TTY interativo

**Arquivos modificados/criados**:
- `scripts/lib/project.py` (~2125-2280): `run_speckit_init()`, `copy_speckit()`, `copy_custom_agents()`, `copy_github_templates()`
- `scripts/lib/flows/new_project.py` (linhas 64-74): adicionada chamada `copy_custom_agents()`
- `tests/test_smoke_imp17.py`: atualizado `test_copy_speckit_includes_issue_templates`
- `docs/planning/lembrete.md`: TaskList atualizada com `[x]` nos dois bugs

**Status**: ✅ Completo

---

### Implementação BUG-P0: Pre-commit com varredura de IPs e credenciais (Git Guardian rules)

**13:00 — ✅ Completo**

**Objetivo**: Adicionar varredura de conteúdo ao pre-commit hook — bloquear IPs internos e credenciais hardcoded antes do commit.

**Contexto**: O hook existente só verificava nomes de arquivos e `.secrets/`. Não havia varredura de conteúdo, expondo risco de commitar IPs privados, chaves PEM, tokens e senhas literais.

**Passos executados**:
1. Analisou hook existente (`_PRE_COMMIT_SECRETS_HOOK` em `scripts/lib/project.py`) — verificava apenas nomes de arquivo
2. Analisou DEV hook (`scripts/git-hooks/pre-commit`) — verificava apenas `.memory/`
3. Implementou varredura de conteúdo com Python inline no hook bash (template)
4. Implementou novo hook Python completo para o projeto DEV
5. Instalou hook em `.git/hooks/pre-commit`
6. Validou detecção com conteúdo de teste (IP + senha)

**Regras implementadas (Git Guardian)**:
- IPs RFC 1918: `10.x.x.x`, `172.16-31.x.x`, `192.168.x.x`
- IPs loopback (`127.x.x.x`) e link-local (`169.254.x.x`)
- Chaves privadas PEM (`-----BEGIN ... PRIVATE KEY-----`)
- AWS Access Key ID (`AKIA*`)
- GitHub tokens (`ghp_`, `gho_`, `ghs_`, `ghr_`)
- Credenciais em URL (`user:pass@host`)
- Senhas/tokens literais em variáveis
- Bearer tokens hardcoded
- Valores base64 em campos sensíveis

**Arquivos modificados/criados**:
- `scripts/lib/project.py` (~linha 402): `_PRE_COMMIT_SECRETS_HOOK` reescrito
- `scripts/git-hooks/pre-commit`: hook do DEV reescrito em Python
- `.git/hooks/pre-commit`: instalado (não versionado)

**Status**: ✅ Completo

---

### Criação de `objetivo-init-minimal.yaml` e atualização de template no worktree

**15:30 — ✅ Completo**

**Objetivo**: Criar template enriquecido `objetivo-init-minimal.yaml` incorporando seções avançadas do arquivo de referência externo, e sincronizar o template do worktree.

**Contexto**: Os templates existentes (`objetivo-init-template.yaml`) eram esqueléticos — apenas 9 campos com placeholders simples. O arquivo de referência em `ai-local-setup` continha seções adicionais relevantes para qualquer projeto: `ai_safety_instructions`, `regras_projeto`/`regras_gerais` padronizadas, `infrastructure` com hardware spec, `profile` detalhado com expertise por domínio, `expected_outcome` com success_criteria e quality_gates.

**Passos executados**:
1. Leu arquivo de referência externo (`/home/.../ai-local-setup/objetivo-init-minimal.yaml`) — 378 linhas com estrutura rica
2. Leu templates existentes no scaffold (`objetivo-init-template.yaml`, `objetivo-init_template.yaml`) para não duplicar
3. Criou `scaffold/templates/objetivo/objetivo-init-minimal.yaml` com seções novas incorporadas via placeholders
4. Copiou template enriquecido para `.claude/worktrees/agent-a11d9f5d8c2bbb800/template-bases/objetivo-init-template.yaml`
5. Atualizou `lembrete.md` marcando as duas tasks como `[x]`

**Decisões técnicas**:
- Template usa sintaxe `{{PLACEHOLDER}}` (consistente com `objetivo-init-template.yaml` existente)
- `ai_safety_instructions` sem placeholders — são regras universais que se aplicam a todos os projetos
- `regras_gerais` tem regras fixas (boas práticas invariantes) + placeholder `{{FOLDER_STRUCTURE_CUSTOM}}`
- `pending_tasks` organizado em fases (prerequisites → core implementation → quality validation)

**Arquivos modificados/criados**:
- `scaffold/templates/objetivo/objetivo-init-minimal.yaml` (criado, ~200 linhas)
- `.claude/worktrees/agent-a11d9f5d8c2bbb800/template-bases/objetivo-init-template.yaml` (atualizado)
- `docs/planning/lembrete.md` (2 tasks marcadas `[x]`)

**Status**: ✅ Completo

---

### SESSION_DOCS_STYLE_GUIDE.md ausente em projetos novos + correções session-start-first.prompt.md

**16:30 — ✅ Completo**

**Objetivo**: Garantir que `SESSION_DOCS_STYLE_GUIDE.md` seja copiado para projetos novos pelo scaffold e corrigir 4 problemas no `session-start-first.prompt.md`.

**Contexto**: Projetos recém-criados não recebiam o `SESSION_DOCS_STYLE_GUIDE.md` (referenciado pelo `session-start.prompt.md`). Adicionalmente, o template `session-start-first.prompt.md` tinha: sequência `uv` incorreta, dois pipes bloqueados por regra P0, e sem instrução sobre curl → Python.

**Passos executados**:
1. Corrigiu `session-start-first.prompt.md`: `uv venv` → `uv init` + `uv venv`
2. Substituiu `uv pip list | head -20` por `subprocess.run` + slice Python
3. Substituiu `grep -q ".venv" .gitignore && echo...` por `pathlib.Path` Python
4. Adicionou callout `⚠️ Regra de Segurança — Requisições HTTP`: curl só para bootstrap do `uv`
5. Corrigiu 2 referências em `session-start.prompt.md`: `docs/SESSION_DOCS_STYLE_GUIDE.md` → `docs/guides/SESSION_DOCS_STYLE_GUIDE.md`
6. Adicionou passo 2b em `setup_project_docs()`: copia `SESSION_DOCS_STYLE_GUIDE.md` para `docs/guides/` em projetos novos

**Arquivos modificados**:
- `scaffold/templates/speckit/prompts/session-start-first.prompt.md` (4 correções)
- `scaffold/templates/speckit/prompts/session-start.prompt.md` (2 paths corrigidos)
- `scripts/lib/project.py` (`setup_project_docs()`: passo 2b + docstring)

**Validação**: 31 passed (test_smoke_imp17.py), sem regressões

**Status**: ✅ Completo

---
