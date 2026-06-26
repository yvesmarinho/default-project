<!--
Criado em: 26/06/2026 11:30
Modificado em: 26/06/2026 11:30
-->

# ✅ BUG-24 RESOLVIDO: Agents Copilot Gerados em Projetos `ai_assistant=claude`

**Data**: 2026-06-26  
**Reportado por**: Yves Marinho  
**Resolvido por**: Claude Sonnet 4.6

---

## 🐛 Problema Relatado

Projeto criado com `ai_assistant=claude` estava recebendo 17 agents do GitHub Copilot em `.github/agents/`. Esses agents (`.github/agents/*.agent.md`) são assets exclusivos do Copilot e não devem existir em projetos configurados para Claude.

### Evidência

Análise de `tmp/test-runs/test-000-prog-py-claude/.scaffold-state.yaml`:
```yaml
ai_assistant: claude
```

Porém o projeto gerado continha em `.github/agents/`:
- `context-architect.agent.md`
- `debug.agent.md`
- `devops-expert.agent.md`
- `session-manager.agent.md`
- `speckit.analyze.agent.md`
- *(+ 12 outros)*

---

## 🔍 Causa Raiz

**Arquivo**: `scripts/lib/project.py` → função `copy_speckit()` (~linha 2181 antes da correção)

A função `copy_speckit()` copiava indiscriminadamente todos os assets do diretório `scaffold/templates/speckit/agents/` e `scaffold/templates/speckit/prompts/` para `.github/agents/` e `.github/prompts/`, **sem verificar `config.ai_assistant`**.

Adicionalmente, havia confusão arquitetural:
- Assets SpecKit gerenciados (`speckit.*`) devem vir do `specify init` (CLI oficial)
- Agents customizados do usuário (`session-manager`, `debug`, etc.) devem ser copiados separadamente
- Perfis de domínio (`.github/prompts/domain/`) devem ir para TODAS as IAs (Claude também os usa)

---

## ✅ Solução Implementada

### 1. Refatoração de `copy_speckit()`

**Antes**: copiava agents + prompts + perfis de domínio para todos, sem filtro de IA.

**Depois**: copia **apenas perfis de domínio** → `.github/prompts/domain/` para **todas as IAs**:

```python
def copy_speckit(config: ProjectConfig, force: bool = False) -> list[CreatedItem]:
    """
    Compõe perfis de domínio do scaffold para o projeto gerado.
    Agents, prompts e .specify/ são gerados exclusivamente por run_speckit_init().
    Perfis de domínio vão para .github/prompts/domain/ e são usados por TODAS as IAs:
      - Claude: session-start referencia .github/prompts/domain/ diretamente
      - Copilot: referenciados via .github/prompts/
    """
    results: list[CreatedItem] = []
    # Sem guard de ai_assistant — domain profiles são universais
    domain_profile = DOMAIN_DEFAULT_PROFILES.get(config.domain)
    if domain_profile:
        result = _copy_domain_profile(...)
    for profile_name in config.extra_profiles:
        ...
    for profile_name in SPECKIT_TRANSVERSAL_PROFILES:
        ...
    return results
```

### 2. Nova função `copy_custom_agents()`

Criada para separar a responsabilidade de agents customizados do usuário:

```python
def copy_custom_agents(config: ProjectConfig, force: bool = False) -> list[CreatedItem]:
    """
    Copia agents customizados do scaffold para o projeto gerado.
    - Agents speckit.* são gerenciados pelo specify init e NÃO são copiados aqui.
    - Agents customizados (session-manager, debug, etc.) foram criados pelo usuário
      e devem estar presentes em TODAS as IAs configuradas.
    Destinos:
      - "claude"/"both"  → .github/agents/
      - "copilot"/"both" → .github/agents/
      - "none"           → ignorado
    """
    if config.ai_assistant == "none":
        return results
    src_agents = _SPECKIT_TEMPLATES / "agents"
    for src_file in sorted(src_agents.glob("*.agent.md")):
        if src_file.name.startswith("speckit."):
            continue  # gerido pelo specify init
        dst_file = base / ".github" / "agents" / src_file.name
        ...
```

### 3. Atualização do flow `new_project.py`

```python
# 5. SpecKit: inicialização via specify CLI
results.extend(project.run_speckit_init(cfg))

# 5a. Perfis de domínio → .github/prompts/domain/ (TODAS as IAs)
results.extend(project.copy_speckit(cfg))

# 5aa. Agents customizados do scaffold — etapa independente
results.extend(project.copy_custom_agents(cfg))
```

---

## 📊 Separação Final de Responsabilidades

| Fonte | Função | Destino | IAs |
|-------|--------|---------|-----|
| `specify init --integration claude` | `run_speckit_init()` | `.claude/skills/speckit-*/` | claude, both |
| `specify init --integration copilot` | `run_speckit_init()` | `.github/agents/speckit.*` | copilot, both |
| `scaffold/profiles/*.yaml` | `copy_speckit()` | `.github/prompts/domain/` | TODAS |
| `scaffold/templates/speckit/agents/` (non-speckit.*) | `copy_custom_agents()` | `.github/agents/` | claude, copilot, both |
| `.claude/commands/` e `.claude/skills/` | `copy_claude_config()` via plugin | `.claude/` | claude, both |

---

## 🧪 Validação

Suite de testes: **251 passed, 5 failed (pré-existentes), 7 skipped** — sem regressões.

Teste relevante: `tests/test_smoke_imp17.py` → `test_copy_speckit_includes_issue_templates`

---

## 📝 Arquivos Modificados

1. ✅ `scripts/lib/project.py`
   - `copy_speckit()`: removida cópia de agents/prompts; mantida apenas cópia de domain profiles
   - `copy_custom_agents()`: nova função para agents customizados do usuário
   - `copy_github_templates()`: adicionada cópia de ISSUE_TEMPLATE `.md`

2. ✅ `scripts/lib/flows/new_project.py`
   - Adicionada chamada a `copy_custom_agents()` como etapa independente (linha 74)

3. ✅ `tests/test_smoke_imp17.py`
   - `test_copy_speckit_includes_issue_templates`: atualizado para chamar `copy_github_templates()`

---

## 🎯 Status Final

| Item | Status |
|------|--------|
| Problema identificado | ✅ |
| Causa raiz encontrada | ✅ |
| Solução implementada | ✅ |
| Testes passando | ✅ 251 passed |
| Documentação | ✅ |

---

**Assinado**: Claude Sonnet 4.6  
**Timestamp**: 2026-06-26T11:30:00-03:00
