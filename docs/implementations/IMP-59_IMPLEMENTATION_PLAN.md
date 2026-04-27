# IMP-59 — Implementation Plan: Mini-Engram Python

**Status**: 🟢 GO — Approved for implementation (2026-04-20)
**Decision**: Early termination of IMP-58 survey collection based on single high-need response
**Estimativa original**: 40h
**Implementação**: Incremental, 6 fases

---

## 🎯 Decision Rationale

**IMP-58 Survey Results**:
- Responses collected: 1/N (Yves Marinho)
- Score: 25/40 (62.5%) — **Necessidade Alta**
- Key pain points:
  - Memória de curta duração (<5 min em contextos complexos)
  - Instruções `.copilot-rules*` ignoradas frequentemente
  - Perda de contexto → código duplicado
  - Workflow: 100% IA-assisted coding

**Decision**: Único respondente demonstra **necessidade crítica e caso de uso claro** para memória ativa. Prosseguir com implementação sem aguardar mais respostas.

---

## 📋 Implementation Phases

### **Fase 1: Estrutura Base** (4-6h)

**Objetivo**: Criar estrutura de diretórios, schema SQLite, core library

**Deliverables**:
- [ ] Estrutura `.memory/` completa:
  ```
  .memory/
  ├── memories/
  │   ├── project/
  │   ├── team/
  │   ├── sessions/
  │   └── .templates/
  ├── index/
  │   ├── memory.db
  │   └── .gitignore
  ├── MEMORY_POLICY.md
  └── README.md
  ```
- [ ] `scripts/lib/memory.py` (~400 linhas):
  - Classes: `MemoryStore`, `Memory`, `SearchResult`
  - Métodos: `save()`, `search()`, `index()`, `rebuild()`
  - SQLite schema com FTS5 + triggers
- [ ] `.gitignore` atualizado: `.memory/index/`, `*.db`
- [ ] Smoke test: criar memória, buscar, verificar

**POC Reference**: `poc/mem_poc.py` (linhas 1-200)

---

### **Fase 2: CLI Tools** (6-8h)

**Objetivo**: Implementar CLIs para salvar e buscar memórias

**Deliverables**:
- [ ] `scripts/mem_save.py` (~200 linhas):
  - Flags: `--category`, `--tags`, `--file`, `--append`, `--auto`
  - Validação de entrada
  - Output formatado (✅ Memory saved)
- [ ] `scripts/mem_search.py` (~250 linhas):
  - Busca FTS5 com ranking BM25
  - Filtros: `--category`, `--tags`, `--after`, `--limit`
  - Output: resultados com snippets e relevância
  - Flag `--json` para integração
- [ ] Tests:
  - `test_memory_save.py` (5 tests)
  - `test_memory_search.py` (5 tests)

**POC Reference**: `poc/mem_poc.py` (linhas 100-300)

---

### **Fase 3: Segurança — Sanitização** (3-4h)

**Objetivo**: Detectar e redactar PII/secrets antes de salvar

**Deliverables**:
- [ ] `scripts/lib/sanitize.py` (~200 linhas):
  - Patterns: api_key, token, password, email, aws_key, github_token, IP
  - Funções: `detect_secrets()`, `sanitize()`, `validate_safe()`
  - Modo: `--redact` (replace) vs `--remove` (delete)
- [ ] Integração em `mem_save.py`:
  - Scan automático antes de salvar
  - Warning se secrets detectados
  - Flag `--allow-unsafe` para override (logs)
- [ ] `.gitleaks-memory.toml`:
  - Configuração para `.memory/memories/`
  - Patterns adicionais específicos do projeto
- [ ] Tests: `test_memory_security.py` (5 tests)

**POC Reference**: `poc/mem_poc.py` (linhas 20-80)

---

### **Fase 4: Contexto Proativo** (8-10h)

**Objetivo**: Sugerir memórias relevantes automaticamente

**Deliverables**:
- [ ] `scripts/mem_context.py` (~300 linhas):
  - Análise de contexto: branch, commits recentes, arquivos abertos
  - Algoritmo de relevância: keywords + data + category
  - Modo `--auto`: detecção automática
  - Modo `--query`: manual
  - Output: top 3-5 memórias com % relevância
- [ ] Integração experimental (opcional):
  - Hook em `session-start.prompt.md` (comentado)
  - Auto-sugestão ao iniciar sessão
- [ ] Tests: parte de `test_memory_integration.py`

**Complexidade**: Alta (requer heurísticas de relevância)

---

### **Fase 5: Testes Completos** (4-6h)

**Objetivo**: Cobertura 100% das funcionalidades

**Deliverables**:
- [ ] `test_memory_integration.py` (5 tests):
  - Workflow completo: save → search → context
  - Concurrency (múltiplas sessões)
  - Performance benchmarks (<100ms search)
  - Edge cases (memória vazia, DB corrompido)
- [ ] Smoke tests end-to-end:
  - Criar 10 memórias de diferentes categorias
  - Buscar com filtros
  - Validar resultados
- [ ] Performance targets:
  - Save: <50ms
  - Search: <100ms
  - Index rebuild: <1s para 100 memórias

**Total tests**: 20 (5 save + 5 search + 5 security + 5 integration)

---

### **Fase 6: Documentação e Integração** (6-8h)

**Objetivo**: Documentar, integrar com workflows existentes

**Deliverables**:
- [ ] `.memory/README.md` (~300 linhas):
  - Quick start (5 min)
  - Examples de uso comum
  - Troubleshooting
- [ ] `.memory/MEMORY_POLICY.md` (~200 linhas):
  - Secrets management
  - Data privacy guidelines
  - Usage best practices
  - Commit policy (o que versionar)
- [ ] `docs/IMP-59_IMPLEMENTATION.md` (~500 linhas):
  - Relatório completo da implementação
  - Decisões arquiteturais
  - Performance metrics
  - Lessons learned
- [ ] Makefile targets:
  - `make memory-save TEXT="..." CATEGORY=project`
  - `make memory-search QUERY="..."`
  - `make memory-context`
  - `make memory-rebuild`
- [ ] Atualizar `session-start.prompt.md`:
  - Adicionar passo (comentado): "Buscar contexto relevante com mem_context.py"
- [ ] Atualizar `session-end.prompt.md`:
  - Adicionar passo (comentado): "Salvar insights importantes com mem_save.py"

---

## 📊 Success Criteria

### Critérios Técnicos:
- ✅ 20/20 testes passando (100%)
- ✅ Search performance <100ms para queries simples
- ✅ Zero dependências externas (Python stdlib + SQLite)
- ✅ Security: 100% secrets detectados (padrões conhecidos)

### Critérios de Uso:
- ✅ Workflow funcional: save → search → context
- ✅ CLI intuitivo (documentado)
- ✅ Integração com session-start/end (opcional/comentado)

### Critérios de Qualidade:
- ✅ Documentação completa (README, POLICY, Implementation Report)
- ✅ Smoke tests end-to-end validados
- ✅ `.gitignore` configurado (não commitar DB)

---

## ⏱️ Timeline Estimado

| Fase | Estimativa | Dependências |
|------|------------|--------------|
| 1. Estrutura Base | 4-6h | POC existente |
| 2. CLI Tools | 6-8h | Fase 1 |
| 3. Segurança | 3-4h | POC existente |
| 4. Contexto Proativo | 8-10h | Fases 1, 2 |
| 5. Testes | 4-6h | Todas anteriores |
| 6. Docs + Integração | 6-8h | Todas anteriores |
| **TOTAL** | **31-42h** | — |

**Estimativa original**: 40h
**Estimativa revisada**: 31-42h (compatível)

---

## 🚀 Start Implementation

**Próxima ação**: Iniciar Fase 1 (Estrutura Base)

```bash
# Criar estrutura de diretórios
mkdir -p .memory/{memories/{project,team,sessions,.templates},index}

# Criar .gitignore para cache
echo "*.db" > .memory/index/.gitignore

# Iniciar implementação de scripts/lib/memory.py
# (baseado em poc/mem_poc.py)
```

**Comando para tracking**:
```bash
git checkout -b 060-mini-engram-python
```
