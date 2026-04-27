# BUG-07: Workspace File Missing MCP Configuration

**Status**: ✅ RESOLVIDO  
**Data**: 2026-04-27  
**Prioridade**: P0 (Critical)  
**Branch**: 060-mini-engram-python  

---

## 📋 Resumo

Projetos criados com scaffold.py não incluíam configurações MCP no arquivo `.code-workspace`, fazendo com que o VS Code carregasse MCP servers incorretos quando aberto via workspace file (ao invés de abrir a pasta diretamente).

---

## 🔍 Contexto

### Descoberta
User criou projeto test-reorganization, copiou para local externo, abriu pelo workspace file e descobriu que o MCP estava carregando perfil "enterprise-kubernetes" ao invés dos servers corretos do domínio "programming".

### Impacto
- **Severidade**: CRÍTICO - afeta todos projetos criados
- **Escopo**: Qualquer projeto aberto via `.code-workspace` file
- **Comportamento**: MCP servers incorretos → prompts/skills errados → sugestões inadequadas

---

## 🐛 Problema Técnico

### Root Cause
O arquivo `.code-workspace` era gerado a partir de template **FIXO** (`_CODE_WORKSPACE` em `scripts/lib/project.py` linha 1256), que não incluía seção `"mcp": { "servers": {...} }`.

### Arquitetura do Problema
```
VS Code Priority:
1. .code-workspace settings (FALTAVA MCP) ❌
2. .vscode/mcp.json (CORRETO) ✅ ← ignorado!

Resultado: MCP global/incorreto carregado
```

### Evidência
```json
// ANTES - .code-workspace (sem MCP)
{
  "folders": [{"path": "."}],
  "settings": { ... },
  "tasks": { ... },
  "launch": { ... }
  // ❌ SEM "mcp" section
}
```

---

## ✅ Solução Implementada

### Mudanças no Código

**1. Novo Generator: `scripts/lib/vscode.py`**
```python
def generate_workspace(config: ProjectConfig) -> CreatedItem:
    """
    Gera [project-name].code-workspace com MCP integrado.
    
    Inclui:
    - Folders, settings, tasks, launch
    - ⭐ MCP servers (por domínio) - FIX BUG-07
    """
    # Get MCP servers for domain
    server_names = _MCP_BY_DOMAIN.get(config.domain, [...])
    mcp_servers = {name: _ALL_MCP_SERVERS[name] for name in server_names}
    
    workspace_config = {
        "folders": [{"path": "."}],
        "settings": {...},
        "mcp": {  # ⭐ NOVO
            "servers": mcp_servers
        },
        "tasks": {...},
        "launch": {...}
    }
    
    return _write_json(dest, workspace_config)
```

**2. Modificação: `scripts/lib/project.py`**
```python
# ANTES (linha 1675-1683)
ws_path = base / f"{config.project_name}.code-workspace"
if ws_path.exists():
    results.append(CreatedItem(path=ws_path, kind="file", status="skipped"))
else:
    ws_path.write_text(_CODE_WORKSPACE, encoding="utf-8")  # ❌ template fixo
    results.append(CreatedItem(...))

# DEPOIS (linha 1675-1677)
from . import vscode

ws_result = vscode.generate_workspace(config)  # ✅ dinâmico com MCP
results.append(ws_result)
```

**3. Template Removido**
- Deletado `_CODE_WORKSPACE` (70 linhas) de `project.py` linha 1256
- Substituído por geração dinâmica

---

## 🧪 Validação

### Teste Manual
```bash
uv run scripts/scaffold.py --new --ci \
  --name test-workspace-fix \
  --domain programming \
  --language python \
  --target-dir poc/test-workspace-fix
```

### Resultado do Workspace File
```json
{
  "folders": [{"path": "."}],
  "settings": {
    "python.defaultInterpreterPath": ".venv/bin/python",
    ...
  },
  "mcp": {  // ✅ PRESENTE AGORA
    "servers": {
      "memory": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-memory"],
        "type": "stdio"
      },
      "sequential-thinking": { ... },
      "filesystem": { ... },
      "github": {
        "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": "${env:...}"}
      }
    }
  },
  "tasks": { ... },
  "launch": { ... }
}
```

### Validação
- ✅ Seção `"mcp"` presente no workspace file
- ✅ Servers corretos por domínio (programming → memory, sequential-thinking, filesystem, github)
- ✅ Estrutura JSON válida
- ✅ Mantém settings/tasks/launch como antes

---

## 📊 Arquivos Modificados

| Arquivo | Tipo | Mudança |
|---------|------|---------|
| `scripts/lib/vscode.py` | Adição | Nova função `generate_workspace()` (+100 linhas) |
| `scripts/lib/project.py` | Modificação | Usa `vscode.generate_workspace()` ao invés de template fixo (-80 linhas) |
| `scripts/lib/project.py` | Remoção | Template `_CODE_WORKSPACE` deletado (-70 linhas) |

**Net change**: +100 -150 = -50 linhas (código mais enxuto e dinâmico)

---

## 🔗 Relação com Outros Bugs

- **BUG-06**: Corrigiu profile loading (nomes de arquivos) - RESOLVIDO
- **ISSUE-T1/T2/T3**: Corrigiu placeholders e hatchling - RESOLVIDO
- **BUG-07** (este): Corrigiu MCP no workspace file - RESOLVIDO

Todos relacionados ao sistema de profiles e templates.

---

## 📝 Lições Aprendidas

### Arquitetura
1. **VS Code workspace files têm prioridade sobre .vscode/**: Sempre incluir configs críticas no workspace file
2. **Templates fixos são frágeis**: Preferir geração dinâmica
3. **MCP deve estar em 2 lugares**: `.vscode/mcp.json` E `.code-workspace` file

### Processo
1. **Testar em local externo**: POC projects dentro do repo podem esconder bugs de configuração
2. **Validar via workspace file**: Não apenas via "Open Folder"
3. **Documentar prioridades do VS Code**: Workspace > Folder > User

### Código
1. **Reutilizar lógica existente**: `_MCP_BY_DOMAIN` e `_ALL_MCP_SERVERS` já existiam
2. **Manter consistência**: Mesmo padrão de `generate_mcp()`, `generate_settings()`, etc
3. **Menos é mais**: Remover template fixo reduziu linhas e bugs

---

## ✅ Checklist de Resolução

- [x] Root cause identificado (template fixo sem MCP)
- [x] Solução implementada (generate_workspace())
- [x] Template fixo removido (project.py)
- [x] Import adicionado (from . import vscode)
- [x] Teste manual (poc/test-workspace-fix)
- [x] Validação do workspace file (JSON correto)
- [x] Documentação criada (este arquivo)
- [ ] Commit + push
- [ ] Atualizar INDEX.md
- [ ] Marcar TODO.md completo

---

## 🎯 Próximos Passos

1. Testar em projeto externo (copiar poc/test-workspace-fix para ~/DevOps/Projetos/)
2. Abrir via workspace file e verificar MCP servers corretos
3. Validar que prompts/skills do domínio programming são carregados
4. Aplicar fix no projeto test-reorganization original do user
5. Fechar sessão e documentar

---

**Commit message sugerida**:
```
fix(workspace): add dynamic MCP server configuration (BUG-07)

PROBLEM:
- Workspace files used static template without MCP servers
- VS Code prioritizes workspace settings over .vscode/mcp.json
- Result: Wrong MCP profile loaded when opening via workspace file

SOLUTION:
- Add generate_workspace() function to vscode.py
- Generate workspace file dynamically with domain-specific MCP servers
- Remove static _CODE_WORKSPACE template

IMPACT:
- All new projects get correct MCP configuration in workspace file
- Existing projects need manual workspace file regeneration

Files:
- scripts/lib/vscode.py: +100 lines (new generate_workspace function)
- scripts/lib/project.py: -150 lines (use dynamic generation, remove template)

Fixes: BUG-07
Related: BUG-06, ISSUE-T1, ISSUE-T2, ISSUE-T3
```
