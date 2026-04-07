# Mini-Engram POC

Proof of Concept for IMP-59 memory system.

## 🎯 Objetivo

Validar viabilidade técnica **ANTES** de implementação completa:

1. ✅ SQLite FTS5 funciona para busca de memórias?
2. ✅ Performance aceitável (<100ms para busca)?
3. ✅ Sanitização de secrets é confiável?
4. ✅ Concorrência funciona (WAL mode)?

## 🚀 Como Executar

```bash
# Executar POC
python poc/mem_poc.py

# Output esperado:
# - DB criado em poc/memory_poc.db
# - 4 memórias de teste indexadas
# - Benchmark de busca
# - Demo interativo
```

## 📊 Testes Disponíveis

### 1. Busca Básica

```bash
# No menu interativo:
# 1. Search memories
# Query: database

# Resultado esperado: 2-3 memórias relacionadas
```

### 2. Performance Benchmark

```bash
# No menu interativo:
# 3. Benchmark
# Query: database

# Critério de sucesso: <100ms average
```

### 3. Segurança (Secrets Detection)

```bash
# No menu interativo:
# 4. Test security

# Resultado esperado:
# - Detectar API keys, passwords, tokens
# - Sanitizar com [REDACTED]
```

## 📁 Estrutura

```
poc/
├── mem_poc.py               # Script principal (500 linhas)
├── memory_poc.db            # DB SQLite (gitignored)
├── test_data/               # Memórias de teste
│   ├── architecture.md
│   ├── troubleshooting.md
│   ├── conventions.md
│   └── secrets_test.md
└── README.md                # Este arquivo
```

## ✅ Critérios de Sucesso

Para prosseguir com IMP-59 completo (SE IMP-58 der GO):

1. ✅ **Funcionalidade**: Save + search end-to-end
2. ✅ **Performance**: <100ms para 100 iterações
3. ✅ **Segurança**: Detecta API keys, passwords, emails
4. ✅ **Confiabilidade**: WAL mode sem erros
5. ✅ **Simplicidade**: Código <500 linhas

## 🚧 Limitações do POC

**O que NÃO está incluído** (será implementado em IMP-59 completo):

- MCP server integration
- CLI completo (`mem_save.py`, `mem_search.py`, `mem_context.py`)
- Pre-commit hooks
- Integration com session-start/end prompts
- Migration system
- Disaster recovery (rebuild)

**Este é apenas um POC isolado** para validar conceitos técnicos.

## 📈 Próximos Passos

1. ✅ Executar POC e validar critérios
2. ⏸️ Aguardar IMP-58 decision gate (2026-05-10)
3. **SE GO**: Implementar IMP-59 completo (40h)
4. **SE MANTER**: Descartar este POC

---

**Status**: 🟡 POC pronto para execução
**Decisão final**: Aguarda IMP-58 (2026-05-10)
