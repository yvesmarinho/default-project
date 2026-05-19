# BUG-001: scaffold objetivo-init — 3 Issues de Comportamento

**Data**: 2026-05-18
**Prioridade**: 🟡 P1 (Funcionalidade com workarounds)
**Tipo**: Bug Report
**Componente**: `scripts/scaffold.py` — comando `objetivo-init`
**Impacto**: Baixo/Médio (não bloqueia uso, mas gera inconsistências)
**Status**: ✅ **RESOLVED** (2026-05-19, commit `ec46cfe`)

---

## 🎯 Resolução

**Commit**: `ec46cfe` — `fix(scaffold): resolve BUG-001 objetivo-init 3 issues`
**Data**: 2026-05-19
**Testes**: 8 passed (tests/test_bug001_objetivo_init.py)

### Correções Implementadas

1. **Issue #1**: Adicionada constante `DEFAULT_DOCSTYLE` em `objetivo_wizard.py`
2. **Issue #2**: Regex para remover linha `out-scope` quando vazio
3. **Issue #3**: Função `_log_objetivo_init()` integrada em `flows/objetivo_init.py`

**Arquivos modificados**:
- `scripts/lib/objetivo_wizard.py` (+20 linhas)
- `scripts/lib/flows/objetivo_init.py` (+54 linhas)
- `tests/test_bug001_objetivo_init.py` (novo, 411 linhas)

---

## 📋 Resumo

O comando `scaffold objetivo-init` apresenta 3 comportamentos incorretos:
1. Não define valor padrão para campo `docstyle` quando omitido
2. Inclui campo `out-scope` vazio quando não informado (deveria omitir)
3. Não gera logs de execução (dificulta debugging)

---

## 🐛 Bug #1: Campo `docstyle` sem valor padrão

### Comportamento Esperado
Quando o campo `docstyle` não é informado no `objetivo.yaml`, o scaffold deve usar o padrão:

```yaml
docstyle: "Google Style Docstrings com type hints completos, Sphinx para geração de docs, ADRs para decisões arquiteturais, OpenAPI/Swagger para documentação de API"
```

### Comportamento Atual
Campo fica vazio ou não é processado corretamente.

### Impacto
- ⚠️ Projetos sem padrão de documentação definido
- ⚠️ Inconsistência entre projetos gerados

### Reprodução
```bash
# Criar objetivo.yaml sem campo docstyle
cat > objetivo-test.yaml << 'EOF'
project:
  name: "test-project"
  # docstyle NÃO INFORMADO
EOF

# Executar scaffold
uv run scripts/scaffold.py objetivo-test.yaml
```

---

## 🐛 Bug #2: Campo `out-scope` incluído quando vazio

### Comportamento Esperado
Quando o campo `out-scope` não é informado, **não deve ser incluído** no arquivo gerado.

### Comportamento Atual
Campo `out-scope: ""` ou `out-scope: []` é incluído no arquivo, poluindo o YAML.

### Impacto
- ⚠️ Arquivos gerados com campos vazios desnecessários
- ⚠️ Ruído visual no `objetivo.yaml` final

### Reprodução
```bash
# Criar objetivo.yaml sem out-scope
cat > objetivo-test.yaml << 'EOF'
project:
  name: "test-project"
  # out-scope NÃO INFORMADO
EOF

# Executar scaffold
uv run scripts/scaffold.py objetivo-test.yaml

# Verificar arquivo gerado (esperado: sem out-scope)
grep -A2 "out-scope" objetivo-generated.yaml
```

---

## 🐛 Bug #3: Ausência de logs de execução

### Comportamento Esperado
O comando `scaffold objetivo-init` deve gerar logs em `logs/scaffolds.yaml` ou similar, incluindo:
- Timestamp de execução
- Arquivo de entrada (`objetivo.yaml`)
- Perfis aplicados
- Arquivos gerados
- Erros/warnings

### Comportamento Atual
Nenhum log é gerado. Dificulta:
- Debugging de problemas
- Auditoria de scaffolds executados
- Rastreabilidade de mudanças

### Impacto
- ⚠️ Sem histórico de scaffolds executados
- ⚠️ Debugging mais difícil em caso de erros

### Reprodução
```bash
# Executar scaffold
uv run scripts/scaffold.py objetivo-test.yaml

# Verificar logs (esperado: registro criado)
cat logs/scaffolds.yaml  # Deveria existir, mas não existe
```

---

## 🔍 Análise Técnica

### Localização Provável do Bug

**Arquivo**: `scripts/scaffold.py`

**Funções afetadas**:
1. Bug #1: Função que processa campo `docstyle` (provavelmente em `parse_objetivo()` ou similar)
2. Bug #2: Função que gera YAML de saída (provavelmente em `write_objetivo()` ou similar)
3. Bug #3: Ausência de chamada para `scaffold_logger.py` ou logger não configurado

### Código Suspeito (Hipótese)

```python
# Bug #1 - Falta default para docstyle
docstyle = objetivo_data.get('docstyle')  # ❌ Deveria ter default
# Correção:
docstyle = objetivo_data.get('docstyle', DEFAULT_DOCSTYLE)

# Bug #2 - Sempre inclui out-scope
out_scope = objetivo_data.get('out-scope', [])  # ❌ Deveria ser None
# Correção:
out_scope = objetivo_data.get('out-scope')
if out_scope:  # Só incluir se não for None/vazio
    yaml_output['out-scope'] = out_scope

# Bug #3 - Logger não invocado
# ❌ Falta:
from scaffold_logger import log_scaffold_execution
log_scaffold_execution(objetivo_file, profiles, generated_files)
```

---

## 🛠️ Solução Proposta

### Correção #1: Adicionar constante DEFAULT_DOCSTYLE

```python
# scripts/scaffold.py (topo do arquivo)
DEFAULT_DOCSTYLE = (
    "Google Style Docstrings com type hints completos, "
    "Sphinx para geração de docs, "
    "ADRs para decisões arquiteturais, "
    "OpenAPI/Swagger para documentação de API"
)

# Na função de parsing:
docstyle = objetivo_data.get('docstyle', DEFAULT_DOCSTYLE)
```

### Correção #2: Condicional para out-scope

```python
# Ao gerar YAML de saída:
out_scope = objetivo_data.get('out-scope')
if out_scope and len(out_scope) > 0:  # Só incluir se tiver conteúdo
    yaml_output['out-scope'] = out_scope
# Caso contrário, omitir campo completamente
```

### Correção #3: Integrar scaffold_logger.py

```python
# scripts/scaffold.py (imports)
from scripts.scaffold_logger import log_scaffold_execution

# Ao final da execução do scaffold:
log_scaffold_execution(
    objetivo_file=objetivo_path,
    profiles=applied_profiles,
    generated_files=generated_file_list,
    errors=errors_list if errors_list else None
)
```

---

## ✅ Testes de Validação

### Teste #1: docstyle padrão aplicado
```bash
# 1. Criar objetivo.yaml sem docstyle
cat > test-docstyle.yaml << 'EOF'
project:
  name: "test-docstyle"
EOF

# 2. Executar scaffold
uv run scripts/scaffold.py test-docstyle.yaml

# 3. Validar que docstyle foi preenchido com padrão
grep "Google Style Docstrings" <arquivo-gerado>  # Deve retornar match
```

### Teste #2: out-scope omitido quando vazio
```bash
# 1. Criar objetivo.yaml sem out-scope
cat > test-outscope.yaml << 'EOF'
project:
  name: "test-outscope"
EOF

# 2. Executar scaffold
uv run scripts/scaffold.py test-outscope.yaml

# 3. Validar que out-scope NÃO está no arquivo
grep "out-scope" <arquivo-gerado>  # Não deve retornar nada
echo $?  # Deve ser 1 (grep não encontrou)
```

### Teste #3: Log gerado
```bash
# 1. Limpar logs anteriores
rm -f logs/scaffolds.yaml

# 2. Executar scaffold
uv run scripts/scaffold.py objetivo-test.yaml

# 3. Validar log criado
test -f logs/scaffolds.yaml && echo "✅ Log criado" || echo "❌ Log não criado"

# 4. Validar conteúdo do log
grep "objetivo-test.yaml" logs/scaffolds.yaml
```

---

## 📊 Priorização

| Bug | Severidade | Prioridade | Esforço | Risco |
|-----|------------|------------|---------|-------|
| #1 (docstyle) | 🟡 Médio | P1 | 🟢 Baixo (1h) | 🟢 Baixo |
| #2 (out-scope) | 🟢 Baixo | P2 | 🟢 Baixo (30min) | 🟢 Baixo |
| #3 (logs) | 🟡 Médio | P1 | 🟡 Médio (2h) | 🟡 Médio |

**Estimativa Total**: 3.5 horas
**Recomendação**: Fixar todos em uma única sessão

---

## 🔗 Referências

- Arquivo fonte: `scripts/scaffold.py`
- Logger existente: `scripts/scaffold_logger.py`
- Configuração: `.scaffold-config.json`
- Documentação: [docs/planning/lembrete.md](lembrete.md) (linhas 19-25)

---

## 👤 Reporter

**Usuário**: yves_marinho
**Sessão**: 2026-05-18
**Origem**: Seleção manual em `docs/planning/lembrete.md`

---

## 🏷️ Labels

- `bug`
- `scaffold`
- `P1`
- `good-first-issue` (para contribuidores)
- `documentation` (Bug #1 afeta docs)
- `logging` (Bug #3)

---

## ✅ Critérios de Aceitação

- [ ] Bug #1: Campo `docstyle` tem valor padrão quando omitido
- [ ] Bug #2: Campo `out-scope` não aparece no YAML quando vazio
- [ ] Bug #3: Logs são gerados em `logs/scaffolds.yaml` para cada execução
- [ ] Testes de validação passam (3/3)
- [ ] Documentação atualizada com comportamento correto
- [ ] Sem regressões em outros campos do `objetivo.yaml`

---

## 🚀 Próximos Passos

1. **Criar issue no GitHub** (se projeto usar GitHub Issues)
2. **Implementar correções** seguindo soluções propostas
3. **Executar testes de validação**
4. **Atualizar documentação** (README, guias de uso)
5. **Commit**: `fix(scaffold): Corrigir 3 bugs em objetivo-init (docstyle, out-scope, logs)`
6. **Fechar bug report** após validação em produção

---

**Status**: 🟡 Aberto
**Assignee**: (a definir)
**Milestone**: v1.7.0 ou próximo patch release
