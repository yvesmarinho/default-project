# BUG-23: Template Configuration Issues — 3 Missing/Incorrect Settings

**Data**: 2026-05-20
**Prioridade**: 🟡 P1 (Configuração incorreta/incompleta)
**Tipo**: Bug Report
**Componente**: Template configuration files
**Impacto**: Médio (não bloqueia uso, mas gera inconsistências)
**Status**: 🔴 **OPEN** — Aguardando correção

---

## 📋 Resumo

O template possui 3 problemas de configuração:
1. `.vscode/mcp.json` falta servidores Pylance e Markitdown
2. `.gitignore` do template não tem a pasta `./tmp` na lista
3. `scaffold objetivo-validate --file objetivo-init.yaml` apresenta erro de parsing

---

## 🐛 Bug #1: MCP Servers Missing — Pylance e Markitdown

### Comportamento Esperado
O arquivo `.vscode/mcp.json` deve incluir todos os servidores MCP necessários:
- `memory` ✅ (presente)
- `sequential-thinking` ✅ (presente)
- `filesystem` ✅ (presente)
- `github` ✅ (presente)
- `pylance` ❌ (ausente)
- `markitdown` ❌ (ausente)

### Comportamento Atual
Servidores Pylance e Markitdown não estão configurados no template.

### Impacto
- ⚠️ Projetos criados não têm acesso ao servidor Pylance MCP
- ⚠️ Funcionalidades de conversão de documentos (Markitdown) não disponíveis
- ⚠️ Usuários precisam adicionar manualmente após criar projeto

### Localização
- Arquivo: `.vscode/mcp.json` (raiz do template)
- Também: `template-bases/.vscode/mcp.json` (template base)

### Configuração Esperada
```json
{
  "mcpServers": {
    "memory": { ... },
    "sequential-thinking": { ... },
    "filesystem": { ... },
    "github": { ... },
    "pylance": {
      "command": "code",
      "args": ["--ms-python.python", "mcp", "start"]
    },
    "markitdown": {
      "command": "uvx",
      "args": ["markitdown-mcp"]
    }
  }
}
```

### Ação Necessária
- [ ] Adicionar servidor Pylance em `.vscode/mcp.json`
- [ ] Adicionar servidor Markitdown em `.vscode/mcp.json`
- [ ] Atualizar template-bases/.vscode/mcp.json (se aplicável)
- [ ] Documentar em MEMORY_SYSTEM.md ou MCP guide

---

## 🐛 Bug #2: .gitignore Template Missing `./tmp` Directory

### Comportamento Esperado
O arquivo `.gitignore` do template deve incluir a pasta `tmp/` para evitar versionamento de arquivos temporários:

```gitignore
# Temporary files
tmp/*
!tmp/README.md
```

### Comportamento Atual
A pasta `tmp/` não está listada no `.gitignore` do template.

### Impacto
- ⚠️ Arquivos temporários podem ser commitados acidentalmente
- ⚠️ Inconsistência: projeto template tem `tmp/` funcional, mas novos projetos não têm proteção
- ⚠️ Violação de convenção documentada em README.md (seção "Temporary Files Management")

### Localização
- Arquivo: `.gitignore` (raiz do template)
- Também: `template-bases/.gitignore` (se existir)

### Contexto
O projeto template possui:
- ✅ Pasta `tmp/` com `tmp/README.md` documentado
- ✅ Script `scripts/cleanup-tmp.sh` para limpeza
- ✅ Documentação em README.md sobre uso de `tmp/`
- ❌ `.gitignore` do template **não** protege `tmp/`

### Reprodução
1. Criar novo projeto: `./scripts/scaffold.py new --ci --name test-tmp-bug`
2. Verificar `.gitignore` gerado: `grep -n "tmp" test-tmp-bug/.gitignore`
3. Resultado: Nenhuma entrada para `tmp/` encontrada

### Ação Necessária
- [ ] Adicionar `tmp/*` ao `.gitignore` do template
- [ ] Adicionar exceção `!tmp/README.md`
- [ ] Validar que `tmp/README.md` é criado durante scaffold new
- [ ] Testar que arquivos em `tmp/` são ignorados pelo git

---

## 🐛 Bug #3: scaffold objetivo-validate Parsing Error

### Comportamento Esperado
O comando `scaffold objetivo-validate --file objetivo-init.yaml` deve validar o arquivo sem erros.

### Comportamento Atual
Comando retorna erro de parsing de frontmatter:

```
❌ Erro de validação: Failed to parse frontmatter in objetivo-init.yaml:
Missing or malformed YAML frontmatter. Expected format:
---
version: "2.0"
...
---
```

### Impacto
- ⚠️ Validação de `objetivo-init.yaml` não funciona
- ⚠️ Impossível detectar erros em arquivos objetivo-init antes de uso
- ⚠️ Workflow de desenvolvimento interrompido

### Contexto
- Arquivo: `objetivo-init.yaml` (raiz do projeto ou template)
- Comando: `scaffold objetivo-validate --file objetivo-init.yaml`
- Parser esperado: YAML frontmatter v2.0

### Possíveis Causas
1. **Arquivo malformado**: `objetivo-init.yaml` não tem frontmatter correto
2. **Parser incorreto**: Comando espera formato v2.0 mas arquivo está em v1.0
3. **Path incorreto**: Comando procura arquivo em localização errada
4. **Formato híbrido**: Arquivo usa Markdown Híbrido mas parser não suporta

### Reprodução
```bash
# Tentar validar objetivo-init.yaml
./scripts/scaffold.py objetivo-validate --file objetivo-init.yaml

# Resultado esperado: ✅ Validação bem-sucedida
# Resultado atual: ❌ Erro de parsing frontmatter
```

### Debug Necessário
- [ ] Verificar formato atual de `objetivo-init.yaml`
- [ ] Comparar com `template-bases/objetivo-init_template.yaml` (se existir)
- [ ] Verificar se `objetivo-validate` suporta formato v2.0
- [ ] Testar com arquivo objetivo.yaml v2.0 válido conhecido

### Ação Necessária
1. Determinar se erro está no arquivo ou no parser
2. Se arquivo: corrigir frontmatter em `objetivo-init.yaml`
3. Se parser: atualizar comando `objetivo-validate` para suportar v2.0
4. Adicionar teste: `pytest tests/test_objetivo_validator.py -k "validate_file"`

---

## 📊 Impacto Geral

| Bug | Prioridade | Componente | Bloqueante? |
|-----|-----------|------------|-------------|
| #1 Pylance/Markitdown | P1 | .vscode/mcp.json | Não |
| #2 tmp/ gitignore | P1 | .gitignore | Não |
| #3 objetivo-validate | P1 | scaffold.py | Sim (para workflow de validação) |

**Estimativa de Correção**: ~2-3h
- Bug #1: 30min (adicionar 2 servidores MCP)
- Bug #2: 20min (adicionar 2 linhas no .gitignore)
- Bug #3: 1-2h (debugging + correção de parser ou arquivo)

---

## 🔗 Referências

- [MEMORY_SYSTEM.md](../MEMORY_SYSTEM.md) — Documentação MCP servers
- [README.md](../../README.md) — Seção "Temporary Files Management"
- [scaffold.py](../../scripts/scaffold.py) — Comando objetivo-validate
- Sprint 5 CHANGELOG: tmp/ directory structure creation

---

## 📝 Histórico

| Data | Evento | Autor |
|------|--------|-------|
| 2026-05-20 | Bug reportado | Session 2026-05-20 |
| 2026-05-20 | Bug report criado (BUG-23) | GitHub Copilot |

---

**Status**: 🔴 OPEN — Aguardando investigação e correção
**Next Steps**: Analisar cada bug individualmente e implementar correções
