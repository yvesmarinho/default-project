# BUG CORRIGIDO — scaffold upgrade --force não respeitava flag

**Data**: 2026-05-13  
**Commit**: PENDENTE  
**Afetados**: BUG-11, BUG-12, BUG-13

---

## ❌ PROBLEMA IDENTIFICADO

Ao executar `scaffold upgrade --force`, o usuário reportou **saída inconsistente**:

```
✅ Prosseguindo com --force em 3 segundos...

[... atualiza 18 arquivos com drift ...]

📦 backup: session-manager.agent.md → session-manager.agent.md.backup
✅ atualizado: session-manager.agent.md

[... copia scripts de sessão e memory ...]

INFO ✅ copiado: session-index.py
INFO ✅ copiado: mem_context.py

[... mas NO FINAL ...]

📊 DRIFT DETECTADO: 2 arquivo(s) diferem do template upstream

Arquivos com drift:
  • .github/copilot-instructions.md
  • .copilot-rules.md

Nota: Arquivos com drift NÃO foram modificados (use --force ou merge manual)
```

**Inconsistência**: Flag `--force` foi usado, mas os arquivos de Copilot **NÃO foram atualizados**.

---

## 🔍 CAUSA RAIZ

### Código Original (BUGADO)

```python
# scripts/lib/project.py
def copy_copilot_instructions(config: ProjectConfig) -> list[CreatedItem]:
    # ...
    result = _copy_file(src_instructions, dst_instructions)  # ❌ SEM force
    result = _copy_file(src_rules, dst_rules)               # ❌ SEM force

def copy_session_scripts(config: ProjectConfig) -> list[CreatedItem]:
    # ...
    result = _copy_file(src_script, dst_script)             # ❌ SEM force

def copy_memory_scripts(config: ProjectConfig) -> list[CreatedItem]:
    # ...
    result = _copy_file(src_script, dst_script)             # ❌ SEM force
```

```python
# scripts/lib/flows/upgrade.py (linha 251, 256, 261)
results.extend(project.copy_copilot_instructions(cfg))      # ❌ Sem force
results.extend(project.copy_session_scripts(cfg))           # ❌ Sem force
results.extend(project.copy_memory_scripts(cfg))            # ❌ Sem force
```

**Problema**:
1. `_copy_file()` já aceita `force=False` como parâmetro
2. Mas as funções `copy_*()` **não aceitavam** `force`
3. Sempre chamavam `_copy_file()` sem `force` → comportamento idempotente
4. `scaffold upgrade --force` passava `force=True` para `copy_speckit()` mas NÃO para BUG-11/12/13

**Resultado**:
- Arquivos de SpecKit (.agent.md, .prompt.md, templates) → ✅ atualizados (tinham `force`)
- Scripts de sessão/memory → ✅ copiados (não existiam antes, primeira vez)
- **Copilot instructions** → ❌ **drift** (existiam, tinham diferença, SEM force)

---

## ✅ SOLUÇÃO IMPLEMENTADA

### 1. Modificar Assinaturas das Funções

```python
# scripts/lib/project.py

# BUG-13
def copy_copilot_instructions(config: ProjectConfig, force: bool = False) -> list[CreatedItem]:
    # ...
    result = _copy_file(src_instructions, dst_instructions, force=force)  # ✅ COM force
    result = _copy_file(src_rules, dst_rules, force=force)               # ✅ COM force

# BUG-11
def copy_session_scripts(config: ProjectConfig, force: bool = False) -> list[CreatedItem]:
    # ...
    result = _copy_file(src_script, dst_script, force=force)             # ✅ COM force

# BUG-12
def copy_memory_scripts(config: ProjectConfig, force: bool = False) -> list[CreatedItem]:
    # ...
    result = _copy_file(src_script, dst_script, force=force)             # ✅ COM force
```

### 2. Passar force em upgrade.py

```python
# scripts/lib/flows/upgrade.py (linhas 251, 256, 261)

results.extend(project.copy_copilot_instructions(cfg, force=force))  # ✅
results.extend(project.copy_session_scripts(cfg, force=force))       # ✅
results.extend(project.copy_memory_scripts(cfg, force=force))        # ✅
```

### 3. Proteção Contra Sobrescrever Symlinks

```python
# scripts/lib/project.py (linha ~2260)

def _copy_file(src: Path, dst: Path, force: bool = False) -> CreatedItem:
    # ...
    # PROTEÇÃO: Nunca sobrescrever symlinks
    if dst.is_symlink():
        log.info("🔗 skipped (symlink): %s → %s", dst.name, dst.resolve())
        return CreatedItem(
            path=dst,
            kind="symlink",
            status="skipped",
            message=f"Preservado symlink → {dst.resolve()}"
        )
    # ...
```

**Por quê?**
- Em `test-workspace-fix`, `.copilot-rules.md` é um **symlink**:
  ```
  .copilot-rules.md → ../../.copilot-shared/rules/.copilot-rules.md
  ```
- Sem proteção, `force=True` sobrescreveria o symlink com um arquivo real
- Nova lógica: **detecta symlink e preserva** (não sobrescreve)

---

## 🧪 COMPORTAMENTO ESPERADO

### Próxima Execução: `scaffold upgrade --force`

**Para `.github/copilot-instructions.md`** (arquivo regular com drift):
```
📦 backup: copilot-instructions.md → copilot-instructions.md.backup
✅ atualizado: copilot-instructions.md
```

**Para `.copilot-rules.md`** (symlink):
```
🔗 skipped (symlink): .copilot-rules.md → /caminho/completo/.copilot-rules.md
```

**Para scripts de sessão/memory** (se drift futuro):
```
📦 backup: session-index.py → session-index.py.backup
✅ atualizado: session-index.py
```

---

## 📋 CHECKLIST DE VALIDAÇÃO

Após commit e próximo upgrade:

- [ ] `copilot-instructions.md` → atualizado (backup criado)
- [ ] `.copilot-rules.md` → **skipped (symlink preservado)**
- [ ] Scripts de sessão → atualizados se drift (5 arquivos)
- [ ] Scripts de memory → atualizados se drift (5 arquivos)
- [ ] Nenhuma mensagem de drift no final do upgrade
- [ ] Flag `--force` respeitado em TODOS os `copy_*()` calls

---

## 🚀 PRÓXIMOS PASSOS

1. **Commit** das mudanças em `project.py` e `upgrade.py`
2. **Testar** upgrade no test-workspace-fix:
   ```bash
   cd /home/yves_marinho/DevOps/Projetos/test-workspace-fix
   scaffold upgrade --force
   # Responder "1" para atualizar path
   # Verificar saída: copilot-instructions.md deve mostrar "✅ atualizado"
   # Verificar: .copilot-rules.md deve mostrar "🔗 skipped (symlink)"
   ```
3. **Validar** que não há drift ao final
4. **Documentar** em lembrete.md como RESOLVIDO

---

**Arquivos Modificados**:
- `scripts/lib/project.py` (+3 assinaturas, +proteção symlink)
- `scripts/lib/flows/upgrade.py` (+3 parâmetros force)

**Impacto**: BUG-11, BUG-12, BUG-13 agora respeitam `--force` corretamente ✅
