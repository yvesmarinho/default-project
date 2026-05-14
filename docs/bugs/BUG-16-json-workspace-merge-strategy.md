---
bug_id: BUG-16
title: "Arquivos JSON e .code-workspace não mergeados por padrão no scaffold"
status: "confirmed"
severity: "medium"
priority: "P1"
created: 2026-05-14
reporter: "yves_marinho"
---

# BUG-16: Arquivos JSON e .code-workspace Não Mergeados por Padrão no Scaffold

## 📋 Descrição

Durante operações de `scaffold.py upgrade --force`, arquivos de configuração JSON (`.vscode/settings.json`, `.vscode/mcp.json`, `.vscode/extensions.json`) e `.code-workspace` são **sobrescritos completamente** ao invés de mergeados, causando perda de customizações do usuário.

## 🔍 Causa Raiz

**Arquivo**: `scripts/lib/project.py`  
**Função**: `_copy_file()` (linhas ~2350-2400)

**Comportamento atual**:
```python
def _copy_file(src: Path, dst: Path, force: bool = False) -> CreatedItem:
    if dst.exists():
        if force:
            # Backup + sobrescrever COMPLETO (sem merge)
            backup_path = _create_backup(dst)
            shutil.copy2(src, dst)
            return CreatedItem("updated", str(dst), backup=backup_path)
        else:
            return CreatedItem("skipped", str(dst), reason="already exists")
```

**Problema**: Não há lógica de merge para arquivos estruturados (JSON, YAML, workspace).

## 📊 Evidências

### Cenário de Reprodução

1. Criar projeto via scaffold:
   ```bash
   python scripts/scaffold.py --new --name test-merge \
     --domain programming --language python
   ```

2. Customizar `.vscode/settings.json`:
   ```json
   {
     "chat.mcp.autostart": true,
     "python.analysis.extraPaths": ["./custom/lib"],  // CUSTOMIZAÇÃO
     "editor.rulers": [120]  // CUSTOMIZAÇÃO
   }
   ```

3. Executar upgrade:
   ```bash
   cd test-merge
   python ../a-default-project/scripts/scaffold.py upgrade --force
   ```

4. **Resultado atual**: 
   - ❌ Customizações perdidas (extraPaths, rulers desapareceram)
   - ⚠️ Backup criado em `.backups/`, mas usuário precisa merge manual

5. **Resultado esperado**:
   - ✅ Configurações do template aplicadas
   - ✅ Customizações do usuário preservadas
   - ✅ Conflitos resolvidos automaticamente (estratégia: usuário > template)

## 🎯 Impacto

**Severidade**: Média  
**Frequência**: A cada upgrade de template  
**Afeta**: Todos os usuários que customizam configurações

### Cenários afetados:

1. ✅ **`.vscode/settings.json`**: Configurações de editor, linter, formatters customizados
2. ✅ **`.vscode/mcp.json`**: Servidores MCP adicionais, env vars customizadas
3. ✅ **`.vscode/extensions.json`**: Extensões extras além das recomendadas
4. ✅ **`.code-workspace`**: Pastas adicionais, configurações de workspace
5. ✅ **`package.json`** (Node.js): Scripts, dependências customizadas
6. ✅ **`pyproject.toml`** (Python): Dependências, configurações de tools

## 🛠️ Solução Proposta

### Fase 1: Merge de JSON (P1, 8h)

**Implementar função `_merge_json()`**:

```python
def _merge_json(base: Path, overlay: Path, strategy: str = "user-wins") -> dict:
    """
    Merge dois arquivos JSON com estratégia configurável.
    
    Args:
        base: Arquivo do template (upstream)
        overlay: Arquivo do usuário (customizações)
        strategy: "user-wins" (default) | "template-wins" | "interactive"
    
    Returns:
        dict mergeado
    """
    import json
    
    base_data = json.loads(base.read_text())
    overlay_data = json.loads(overlay.read_text())
    
    if strategy == "user-wins":
        # Deep merge: template como base, usuário sobrescreve
        merged = deep_merge(base_data, overlay_data)
    elif strategy == "template-wins":
        # Deep merge: usuário como base, template sobrescreve
        merged = deep_merge(overlay_data, base_data)
    elif strategy == "interactive":
        # Detectar conflitos e pedir confirmação
        merged = interactive_merge(base_data, overlay_data)
    
    return merged
```

**Integração em `_copy_file()`**:

```python
if dst.suffix == ".json" and dst.exists() and force:
    # Merge JSON ao invés de sobrescrever
    merged = _merge_json(src, dst, strategy="user-wins")
    backup_path = _create_backup(dst)
    dst.write_text(json.dumps(merged, indent=2))
    return CreatedItem("merged", str(dst), backup=backup_path)
```

### Fase 2: Merge de .code-workspace (P1, 4h)

**Estratégia**:
- Mesclar array `folders` (união, sem duplicatas)
- Mesclar dict `settings` (deep merge, user-wins)
- Mesclar dict `extensions` (união de recommendations)

### Fase 3: Merge de YAML (P2, 4h)

**Arquivos**:
- `pyproject.toml` (TOML, não YAML)
- `objetivo.yaml` (especial: não sobrescrever se preenchido)

### Fase 4: Modo Interativo (P2, 8h)

**CLI flag**: `--merge-strategy interactive`

**Comportamento**:
```bash
$ python scripts/scaffold.py upgrade --force --merge-strategy interactive

⚠️  Conflito detectado em .vscode/settings.json

  Chave: python.analysis.extraPaths
  Template: ["./src"]
  Seu valor: ["./custom/lib"]

  Escolha:
  [1] Manter seu valor (user-wins)
  [2] Usar valor do template (template-wins)
  [3] Mesclar ambos (merge)

  Sua escolha [1/2/3] (1):
```

## 📚 Referências

### Ferramentas de Merge Existentes

1. **json-merge-patch** (RFC 7386):
   - `pip install json-merge-patch`
   - Merge determinístico de objetos JSON
   - [RFC 7386](https://tools.ietf.org/html/rfc7386)

2. **deepmerge** (Python):
   - `pip install deepmerge`
   - Deep merge recursivo de dicionários
   - [GitHub](https://github.com/toumorokoshi/deepmerge)

3. **dynaconf** (merging):
   - `pip install dynaconf`
   - Merge de múltiplas fontes de configuração
   - [Docs](https://www.dynaconf.com/)

4. **git merge-file** (three-way merge):
   - Nativo do Git
   - Merge three-way de arquivos texto
   - `git merge-file current.json base.json other.json`

### Estratégias de Merge em Projetos Similares

1. **Renovate** (dependency updates):
   - Merge automático de package.json
   - Preserva customizações do usuário
   - [Docs](https://docs.renovatebot.com/configuration-options/)

2. **Yeoman** (scaffolding):
   - Merge de arquivos via estratégias configuráveis
   - `.yo-rc.json` com preferências de merge
   - [Docs](https://yeoman.io/authoring/storage.html)

3. **Angular CLI** (ng update):
   - Three-way merge de angular.json
   - Backup automático + resolução de conflitos
   - [Docs](https://angular.io/cli/update)

## ✅ Critérios de Aceite

- [ ] JSON files são mergeados por padrão (não sobrescritos)
- [ ] Customizações do usuário preservadas (user-wins strategy)
- [ ] Backup criado antes de merge
- [ ] Conflitos não-resolúveis logados claramente
- [ ] Testes unitários cobrindo cenários de merge
- [ ] Documentação atualizada em `UPGRADE_GUIDE.md`

## 🏷️ Tags

`scaffold`, `upgrade`, `merge`, `json`, `workspace`, `configuration`, `P1`, `enhancement`

---

**Estimativa total**: 24h (4 fases)  
**Prioridade**: P1 (próximo ciclo de desenvolvimento)  
**Bloqueador**: Não (workaround: restore manual do backup)
