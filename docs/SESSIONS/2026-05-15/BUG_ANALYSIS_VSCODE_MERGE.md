# 🐛 Análise de Bugs — Sistema de Merge não Aplicado em .vscode

**Data**: 2026-05-15
**Sessão**: docs/SESSIONS/2026-05-15/
**Branch**: 017-bug-16-merge-strategy
**Origem**: Análise do log de scaffold `test-workspace-fix`

---

## 📊 Sumário Executivo

**Problema**: Sistema de merge (BUG-16) implementado e testado (178/178 tests passing), MAS não está sendo aplicado em arquivos `.vscode/*` durante upgrade/scaffold.

**Impacto**:
- ❌ `.vscode/settings.json` - Não recebe merge (JSONMerger disponível)
- ❌ `.vscode/mcp.json` - Não recebe merge (JSONMerger disponível)
- ❌ `.vscode/extensions.json` - Não recebe merge (JSONMerger disponível)
- ❌ `.vscode/tasks.json` - Não recebe merge (VSCodeConfigMerger disponível)
- ❌ `.vscode/launch.json` - Não recebe merge (VSCodeConfigMerger disponível)

**Resultado**: Usuários perdem atualizações do template em configs do VS Code mesmo tendo mergers implementados e testados.

---

## 🔍 Evidências do Log

### Log Original (test-workspace-fix)

```
[SKIPPED] file | .vscode/settings.json | já existe
[SKIPPED] file | .vscode/mcp.json | já existe
[SKIPPED] file | .vscode/extensions.json | já existe
[SKIPPED] file | .vscode/tasks.json | já existe
[SKIPPED] file | .vscode/launch.json | já existe
```

**Esperado**: Mensagens `[MERGED]` ou `[UPDATED]` usando JSONMerger e VSCodeConfigMerger

---

## 🐛 Bug #1: Skip Incondicional em vscode.py (P0 CRÍTICO)

### Arquivo
`scripts/lib/vscode.py`

### Funções Afetadas

#### 1. `generate_settings()` (linha 235)
```python
def generate_settings(config: ProjectConfig) -> CreatedItem:
    """Gera `.vscode/settings.json` personalizado..."""
    dest = config.project_path / ".vscode" / "settings.json"
    if dest.exists():
        return CreatedItem(path=dest, kind="file", status="skipped", message="já existe")  # ❌ BUG
    # ... resto da função
```

**Problema**: Skip incondicional - não usa `merge_or_skip()`
**Merger disponível**: ✅ `JSONMerger` (registrado e testado)

#### 2. `generate_mcp()` (linha 258)
```python
def generate_mcp(config: ProjectConfig) -> CreatedItem:
    """Gera `.vscode/mcp.json`..."""
    dest = config.project_path / ".vscode" / "mcp.json"
    if dest.exists():
        return CreatedItem(path=dest, kind="file", status="skipped", message="já existe")  # ❌ BUG
    # ... resto da função
```

**Problema**: Skip incondicional - não usa `merge_or_skip()`
**Merger disponível**: ✅ `JSONMerger` (registrado e testado)

#### 3. `generate_extensions()` (linha 283)
```python
def generate_extensions(config: ProjectConfig) -> CreatedItem:
    """Gera `.vscode/extensions.json`..."""
    dest = config.project_path / ".vscode" / "extensions.json"
    if dest.exists():
        return CreatedItem(path=dest, kind="file", status="skipped", message="já existe")  # ❌ BUG
    # ... resto da função
```

**Problema**: Skip incondicional - não usa `merge_or_skip()`
**Merger disponível**: ✅ `JSONMerger` (registrado e testado)

### Impacto

- **Severidade**: P0 CRÍTICO
- **Arquivos afetados**: 3 arquivos críticos (.vscode/settings.json, mcp.json, extensions.json)
- **Usuários impactados**: 100% dos projetos com .vscode pré-existente
- **Funcionalidade perdida**: Atualizações de configs do VS Code nunca são aplicadas

### Correção Necessária

Substituir skip incondicional por chamada a `merge_or_skip()`:

```python
def generate_settings(config: ProjectConfig) -> CreatedItem:
    """Gera `.vscode/settings.json` personalizado..."""
    dest = config.project_path / ".vscode" / "settings.json"
    
    # Gerar conteúdo do template
    settings: dict = {}
    settings.update(_SETTINGS_GLOBAL)
    settings.update(_SETTINGS_BY_DOMAIN.get(config.domain, {}))
    settings.update(_SETTINGS_BY_LANGUAGE.get(config.language, {}))
    
    if dest.exists():
        # ✅ FIX: Usar merge_or_skip ao invés de skip incondicional
        import json
        from . import file_merge
        template_content = json.dumps(settings, indent=2, ensure_ascii=False)
        return file_merge.merge_or_skip(dest, template_content, interactive=False)
    
    # Arquivo não existe - criar novo
    return _write_json(dest, settings)
```

---

## 🐛 Bug #2: Processamento Duplicado de copilot-instructions.md (P1 ALTA)

### Arquivo
`scripts/lib/flows/upgrade.py`

### Evidência do Log

```
[SKIPPED] file | .github/copilot-instructions.md | arquivo já existe
...
[CREATED] file | .github/copilot-instructions.md
```

**Problema**: Arquivo processado DUAS VEZES no mesmo scaffold

### Causa Raiz

Duas chamadas em `upgrade.py` processam o mesmo arquivo:

1. **Linha 201**: `generate_copilot_instructions(cfg)`
   - Função em `templates.py:455`
   - Faz skip incondicional se existe (linha 468)
   - Retorna status "skipped"

2. **Linha 260**: `copy_copilot_instructions(cfg)`
   - Função em `project.py:2334`
   - Chama `_copy_file()` que USA `merge_or_skip()` (correto!)
   - Cria/atualiza o arquivo

### Impacto

- **Severidade**: P1 ALTA
- **Problema**: Duplicação no log confunde análise de resultados
- **Funcionalidade**: Arquivo ESTÁ sendo processado corretamente na 2ª chamada (linha 260)
- **Efeito colateral**: Log mostra "SKIPPED" e "CREATED" para mesmo arquivo

### Correção Necessária

**Opção 1**: Remover chamada duplicada (linha 201)
```python
# L198-201 em upgrade.py
results.append(vscode.generate_settings(cfg))
results.append(vscode.generate_mcp(cfg))
results.append(vscode.generate_extensions(cfg))
# results.append(templates.generate_copilot_instructions(cfg))  # ❌ REMOVER - duplicado com L260
```

**Opção 2**: Consolidar em uma única chamada
- Manter apenas `copy_copilot_instructions(cfg)` (L260) que usa merge_or_skip
- Remover `generate_copilot_instructions(cfg)` (L201)

---

## 🐛 Bug #3: tasks.json e launch.json não usam VSCodeConfigMerger (P1 ALTA)

### Contexto

Sprint 4 implementou `VSCodeConfigMerger` especificamente para `.vscode/tasks.json` e `.vscode/launch.json` (linhas 430-438 em vscode_config_merge.py).

### Problema

Arquivos são criados em `create_structure()` via `FILES_TO_CREATE`, que:
1. ✅ Chama `merge_or_skip()` se arquivo existe (project.py:1918)
2. ✅ `VSCodeConfigMerger` está registrado
3. ❌ MAS `tasks.json` e `launch.json` NÃO estão em `FILES_TO_CREATE`

### Verificação

Precisamos confirmar se `tasks.json` e `launch.json` estão em `FILES_TO_CREATE` ou se são gerados por outra função.

```bash
grep -n "tasks.json\|launch.json" scripts/lib/project.py
```

### Impacto

- **Severidade**: P1 ALTA
- **Arquivos afetados**: .vscode/tasks.json, .vscode/launch.json
- **Funcionalidade perdida**: Deep merge de configurações e tasks

---

## ✅ Comportamentos Corretos Observados

### 1. `.github/agents/*.agent.md` - CORRETO ✅

```
[SKIPPED] file | .github/agents/context-architect.agent.md
[SKIPPED] file | .github/agents/debian-linux-expert.agent.md
...
[CREATED] file | .github/agents/session-manager.agent.md
[CREATED] file | .github/agents/speckit.analyze.agent.md
```

**Comportamento esperado**:
- Agents existentes → SKIPPED (ou MERGED se houver mudanças)
- Agents novos → CREATED
- `CopilotAgentMerger` registrado e funcionando

### 2. `.github/prompts/*.prompt.md` - CORRETO ✅

```
[SKIPPED] file | .github/prompts/speckit.*.prompt.md (vários)
[CREATED] file | .github/prompts/session-end.prompt.md
[CREATED] file | .github/prompts/session-start.prompt.md
```

**Comportamento esperado**:
- Prompts existentes → SKIPPED (ou MERGED se houver mudanças)
- Prompts novos → CREATED
- `CopilotPromptMerger` registrado e funcionando

### 3. `.copilot-rules.md` - CORRETO ✅

```
[MERGED] file | .copilot-rules.md | Consolidação automática de múltiplos .copilot-rules*.md
```

**Comportamento esperado**:
- Consolidação de múltiplos arquivos .copilot-rules
- `CopilotRulesMerger` funcionando perfeitamente

### 4. `.github/ISSUE_TEMPLATE/*.md` - CORRETO ✅

```
[MERGED] file | .github/ISSUE_TEMPLATE/bug_report.md | Merged (body updated)
[MERGED] file | .github/ISSUE_TEMPLATE/feature_request.md | Merged (body updated)
[MERGED] file | .github/ISSUE_TEMPLATE/improvement.md | Merged (body updated)
```

**Comportamento esperado**:
- Templates mergeados com similaridade >70%
- `IssueTemplateMerger` (Sprint 4) funcionando perfeitamente

---

## 📋 Ações Recomendadas

### Prioridade P0 (Imediato)

1. **Corrigir vscode.py**
   - [ ] `generate_settings()` - usar `merge_or_skip()`
   - [ ] `generate_mcp()` - usar `merge_or_skip()`
   - [ ] `generate_extensions()` - usar `merge_or_skip()`
   - [ ] Criar testes para validar merge

2. **Corrigir templates.py**
   - [ ] `generate_copilot_instructions()` - usar `merge_or_skip()` ou remover função

3. **Remover duplicação em upgrade.py**
   - [ ] Linha 201 - remover `generate_copilot_instructions(cfg)` duplicado

### Prioridade P1 (Próxima sessão)

4. **Validar tasks.json e launch.json**
   - [ ] Confirmar se estão usando `VSCodeConfigMerger`
   - [ ] Se não, adicionar à lista de arquivos processados

5. **Documentar padrão**
   - [ ] Criar guideline: "NUNCA usar skip incondicional - sempre usar merge_or_skip()"
   - [ ] Adicionar lint rule ou test para detectar padrão antigo

### Prioridade P2 (Futuro)

6. **Teste E2E completo**
   - [ ] Criar projeto de teste
   - [ ] Customizar todos os arquivos .vscode
   - [ ] Executar upgrade
   - [ ] Validar que todas as customizações foram preservadas E novas configs foram adicionadas

---

## 📊 Impacto Geral

| Categoria | Arquivos | Status Atual | Status Esperado |
|-----------|----------|--------------|-----------------|
| **.vscode configs** | 3 | ❌ Skip incondicional | ✅ JSONMerger |
| **.vscode tasks/launch** | 2 | ⚠️ Investigar | ✅ VSCodeConfigMerger |
| **.github/agents** | 32+ | ✅ Funcionando | ✅ CopilotAgentMerger |
| **.github/prompts** | 26+ | ✅ Funcionando | ✅ CopilotPromptMerger |
| **.copilot-rules** | 1 | ✅ Funcionando | ✅ CopilotRulesMerger |
| **.github/ISSUE_TEMPLATE** | 3+ | ✅ Funcionando | ✅ IssueTemplateMerger |
| **copilot-instructions** | 1 | ⚠️ Duplicado | ✅ Sem duplicação |

**Cobertura atual**: ~85% (com os bugs)
**Cobertura esperada**: ~95% (após correções)

---

## 🔗 Referências

- **BUG-16**: Sistema de merge ausente (COMPLETO)
- **Sprint 4**: P2 Merge System Expansion (COMPLETO - 178/178 tests)
- **Log analisado**: `test-workspace-fix/logs/scaffold_2026-05-15_14-56-43.log`
- **Arquivos com bugs**:
  - `scripts/lib/vscode.py` (3 funções)
  - `scripts/lib/templates.py` (1 função)
  - `scripts/lib/flows/upgrade.py` (1 duplicação)
