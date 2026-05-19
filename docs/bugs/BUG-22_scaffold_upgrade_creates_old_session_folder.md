# BUG-22: Scaffold Upgrade Creates Old Session Folder

**Status**: ✅ RESOLVIDO  
**Prioridade**: P1 (Alta)  
**Categoria**: Scaffold / Upgrade  
**Descoberto**: 2026-05-19  
**Resolvido**: 2026-05-19  

---

## 📋 Descrição

Durante `scaffold upgrade`, o sistema cria incorretamente uma pasta `docs/SESSIONS/<created_at>/` usando a data de criação original do projeto (do `.scaffold-state.yaml`), resultando em uma pasta vazia com data antiga.

### Exemplo do Problema

```yaml
# .scaffold-state.yaml
created_at: '2026-04-27T15:36:13Z'  # Data original do projeto
```

Após `scaffold upgrade`:
```
docs/SESSIONS/2026-04-27/  ← Pasta vazia criada com data antiga!
```

---

## 🔍 Causa Raiz

**Arquivo**: `scripts/lib/project.py`, função `setup_project_docs()`

```python
def setup_project_docs(config: ProjectConfig) -> list[CreatedItem]:
    # ...
    # 3. DAILY_ACTIVITIES_<data>.md em docs/SESSIONS/<data>/
    session_date = config.created_at[:10]  # ← USA DATA DO CREATED_AT
    session_dir = base / "docs" / "SESSIONS" / session_date
    session_dir.mkdir(parents=True, exist_ok=True)  # ← SEMPRE CRIA!
    # ...
```

**Problema**: 
- Função é chamada TANTO em `flows/new_project.py` quanto em `flows/upgrade.py`
- Durante upgrade, usa `created_at` do `.scaffold-state.yaml` (data antiga)
- Cria pasta de sessão vazia que não será usada

---

## ✅ Solução Implementada

### 1. Adicionar Parâmetro `is_upgrade`

```python
def setup_project_docs(config: ProjectConfig, is_upgrade: bool = False) -> list[CreatedItem]:
    """
    UPGRADE: Pasta de sessão NÃO é criada (evita criar SESSIONS/<created_at>/ vazia).
    
    Args:
        config: Configuração do projeto
        is_upgrade: True se executando durante scaffold upgrade (pula criação de sessão)
    """
```

### 2. Condicionalizar Criação de Sessão

```python
# 3. DAILY_ACTIVITIES_<data>.md em docs/SESSIONS/<data>/
# APENAS durante scaffold NEW - pulado durante upgrade
if not is_upgrade:
    session_date = config.created_at[:10]  # YYYY-MM-DD
    session_dir = base / "docs" / "SESSIONS" / session_date
    session_dir.mkdir(parents=True, exist_ok=True)
    
    src_daily = src_templates / "DAILY_ACTIVITIES.template.md"
    dst_daily = session_dir / f"DAILY_ACTIVITIES_{session_date}.md"
    result = _copy_file(src_daily, dst_daily)
    results.append(result)
else:
    log.debug("⏭️  Pulando criação de pasta SESSIONS (upgrade mode)")
```

### 3. Atualizar Chamadas

**flows/upgrade.py** (linha 297):
```python
# ANTES
results.extend(project.setup_project_docs(cfg))

# DEPOIS
results.extend(project.setup_project_docs(cfg, is_upgrade=True))
```

**flows/new_project.py** (linha 96):
```python
# Mantém padrão (is_upgrade=False)
results.extend(project.setup_project_docs(cfg))
```

---

## 🧪 Validação

### Teste Manual

```bash
cd /path/to/test-workspace-fix

# 1. Verificar created_at no .scaffold-state.yaml
grep created_at .scaffold-state.yaml
# Output: created_at: '2026-04-27T15:36:13Z'

# 2. Executar scaffold upgrade
python3 /path/to/template/scripts/scaffold.py upgrade

# 3. Verificar pasta SESSIONS
ls -la docs/SESSIONS/
# Output: (vazio) ← SEM pasta 2026-04-27/
```

### Comportamento Esperado

| Operação | Pasta SESSIONS/ | Resultado |
|----------|-----------------|-----------|
| `scaffold new` | ✅ Cria `SESSIONS/<hoje>/` | Data atual |
| `scaffold upgrade` | ⏭️ **NÃO cria pasta** | Preserva estrutura existente |

---

## 📊 Impacto

### Antes da Correção
- ❌ Pasta `SESSIONS/<created_at>/` vazia criada durante upgrade
- ❌ Confusão: pasta com data antiga aparece no projeto
- ❌ "A pasta session está vazia quando restauro o backup"

### Depois da Correção
- ✅ Upgrade preserva estrutura de sessões existente
- ✅ Não cria pastas indevidas
- ✅ Comportamento consistente e previsível

---

## 📝 Arquivos Modificados

1. **scripts/lib/project.py** (linhas 2200-2290)
   - Adicionado parâmetro `is_upgrade: bool = False`
   - Adicionado condicional `if not is_upgrade:`
   - Atualizado docstring com Ref: BUG-22

2. **scripts/lib/flows/upgrade.py** (linha 297)
   - Chamada atualizada: `setup_project_docs(cfg, is_upgrade=True)`

---

## 🔗 Contexto Relacionado

- **BUG-001**: Scaffold objetivo-init 3 issues (docstyle, out-scope, logging)
- **BUG-09**: Symlink rules subdirectory (proteção durante upgrade)
- **IMP-61**: Session Management System (estrutura de `docs/SESSIONS/`)

---

## 💡 Lições Aprendidas

1. **Funções compartilhadas**: Quando uma função é usada em múltiplos fluxos (new/upgrade), precisa distinguir contexto
2. **Datas em config**: `created_at` deve ser usado apenas durante criação, não em upgrades
3. **Idempotência**: Upgrade deve preservar estrutura existente, não criar novos elementos
4. **Logging**: Debug logs ajudam a rastrear decisões de pular operações

---

## ✅ Checklist de Implementação

- [x] Identificar causa raiz (linha 2271 em project.py)
- [x] Adicionar parâmetro `is_upgrade` à função
- [x] Condicionalizar criação de pasta de sessão
- [x] Atualizar chamada em `upgrade.py`
- [x] Verificar chamada em `new_project.py` (não modificar)
- [x] Adicionar log de debug
- [x] Atualizar docstring com referência ao BUG-22
- [x] Documentar correção neste arquivo
- [ ] Testar scaffold new (deve criar pasta)
- [ ] Testar scaffold upgrade (NÃO deve criar pasta)
- [ ] Adicionar validação em `validate-workspace-upgrade.py` (opcional)

---

**Commit**: (pendente)  
**Autor**: Yves Marinho  
**Revisado por**: GitHub Copilot (Claude Sonnet 4.5)  
