# Debate Técnico: Bug de Duplicação no Sistema de Merge JSON

**Data**: 17 de maio de 2026  
**Projeto**: a-default-project (Enterprise Default Project Template)  
**Branch**: 061-recovery-017-correction  
**Bug ID**: Duplicação de arrays em `.vscode/extensions.json`  
**Participantes**: Software Engineer Agent, Principal Software Engineer, DevOps Expert, Python MCP Server Expert

---

## 📋 Executive Summary

### Problema Identificado
Sistema de merge JSON está duplicando arrays em `.vscode/extensions.json`, causando taxa de duplicação de 100% (20/20 extensões duplicadas).

### Root Cause
Arquivo `extensions.json` está usando `JSONMerger` genérico (que faz union de arrays via `deepmerge.always_merger.merge()`) ao invés de `VSCodeJSONMerger` (user-wins sem union).

### Impacto nos Arquivos
- ✅ `mcp.json`: OK (corrigido em commit `9595ac9`)
- ✅ `settings.json`: OK (usa `VSCodeJSONMerger`)
- ❌ `extensions.json`: **FALHA** (usando `JSONMerger` errado)
- ❓ Outros arquivos `.vscode/*.json`: Status desconhecido (launch.json, tasks.json)

### Evidências
- **Log de duplicação**: `tmp/evidencia/json_diif_20260517_1116.log`
- **Arquivo afetado**: `tmp/evidencia/extensions.json` (41 itens = 21 únicos)
- **Taxa de duplicação**: 100% (todos os 20 arrays afetados)
- **Padrão**: Primeira metade limpa, segunda metade duplicada exatamente

---

## 🔬 Análise Técnica por Agente

### 1️⃣ Software Engineer Agent — Análise do Bug

#### Código Problemático Identificado

**Localização**: `scripts/lib/json_merge.py` (linhas 376-382)

```python
class VSCodeJSONMerger:
    def can_merge(self, file_path: Path) -> bool:
        """Verifica se é mcp.json ou settings.json em .vscode/."""
        return (
            file_path.name in ["mcp.json", "settings.json"] and  # ❌ Lista incompleta!
            ".vscode" in file_path.parts
        )
```

#### Por que `extensions.json` Não Foi Incluído?

1. **Lista whitelist incompleta**: Apenas 2 de 3+ arquivos VSCode na lista
2. **Sem documentação**: Não há guia sobre quais arquivos requerem qual merger
3. **Falta de testes**: Nenhum teste validando cobertura de arquivos `.vscode/`

#### Fluxo de Execução que Causa o Bug

```
Scaffold encontra .vscode/extensions.json existente
  ↓
Chain of Responsibility percorre mergers:
  VSCodeJSONMerger.can_merge() → False (não está na lista)
  WorkspaceMerger.can_merge() → False (não é .code-workspace)
  JSONMerger.can_merge() → True ✅ (qualquer .json)
  ↓
JSONMerger.merge() é chamado
  ↓
Usa deep_merge_json() com always_merger.merge()
  ↓
always_merger faz UNION de arrays
  ↓
💥 DUPLICAÇÃO
  Template: ["ext1", "ext2"]
  User:     ["ext1", "ext2"]
  Result:   ["ext1", "ext2", "ext1", "ext2"]  ❌
```

#### Code Smells Identificados

| Smell | Localização | Severidade | Impacto |
|-------|-------------|------------|---------|
| **Magic Strings** | Lista hardcoded em `can_merge()` | HIGH | Frágil, não escalável |
| **Implicit Assumptions** | Sem doc sobre merge strategies | MEDIUM | Dificulta manutenção |
| **Missing Tests** | Sem cobertura `.vscode/*` | HIGH | Bugs não detectados |
| **Chain of Responsibility Abuse** | Ordem de mergers crítica mas implícita | MEDIUM | Bugs sutis possíveis |

#### Proposta de Correção

**P0 — Solução Mínima (Deploy Imediato)**:
```python
class VSCodeJSONMerger:
    def can_merge(self, file_path: Path) -> bool:
        """Verifica se é arquivo .json em .vscode/ que requer user-wins."""
        return (
            file_path.name in ["mcp.json", "settings.json", "extensions.json"] and  # ✅ FIX
            ".vscode" in file_path.parts
        )
```

**P1 — Solução Robusta (Próxima Semana)**:
```python
# scripts/lib/constants.py (NOVO)
VSCODE_USER_WINS_FILES = {
    "mcp.json",           # MCP server configs
    "settings.json",      # Workspace settings
    "extensions.json",    # Extension recommendations
    "launch.json",        # Debug configurations
    "tasks.json",         # Task definitions
}

class VSCodeJSONMerger:
    def can_merge(self, file_path: Path) -> bool:
        """Verifica se arquivo VSCode requer user-wins sem array union."""
        return (
            file_path.name in VSCODE_USER_WINS_FILES and
            ".vscode" in file_path.parts
        )
```

---

### 2️⃣ Principal Software Engineer — Visão Arquitetural

#### Falha no Design Pattern Atual

**Pattern utilizado**: Chain of Responsibility modificado

```
Request → Handler1.can_merge() → Handler2.can_merge() → Handler3.can_merge()
            ↓ True                  ↓ False                ↓ True
         Handler1.merge()                              Handler3.merge()
```

**Problemas arquiteturais identificados**:

1. **Implicit Priority Order**: Ordem de registro é crítica mas não documentada
2. **Negative Matching**: `JSONMerger` aceita "qualquer .json" (catch-all perigoso)
3. **Insufficient Granularity**: Falta nível intermediário "arquivos VSCode genéricos"
4. **Configuration Drift**: Cada merger tem própria lista de arquivos (DRY violation)

#### Estratégia de Mitigação em 3 Camadas

**Layer 1: Immediate Fix (P0 — Hoje)**
- ✅ Adicionar `extensions.json` na whitelist
- ✅ Script de detecção de duplicações
- ✅ Testes unitários mínimos

**Layer 2: Architecture Hardening (P1 — Esta Semana)**
- 📋 Centralizar configuração em `constants.py`
- 📋 Docstrings detalhados em cada merger
- 📋 Matriz de decisão (arquivo → merger → estratégia)
- 📋 Validação de duplicação pós-merge

**Layer 3: Future-Proofing (P2 — Próximo Sprint)**
- 🔮 Migrar para Strategy Pattern com registry explícito
- 🔮 Pre-commit hook para detectar duplicações
- 🔮 DSL declarativo para merge rules

#### Recomendações de Longo Prazo

| Princípio | Implementação | Benefício |
|-----------|---------------|-----------|
| **Explicit over Implicit** | Registry pattern com prioridades documentadas | Comportamento previsível |
| **Fail-Fast** | Lançar exceção se múltiplos mergers aplicáveis | Detecta ambiguidades |
| **Configuration as Code** | YAML/JSON com merge rules | Extensível sem código |
| **Defense in Depth** | Validação pré + pós-merge | Catch erros cedo |

---

### 3️⃣ DevOps Expert — Impacto Operacional

#### Superfície de Ataque do Bug

**Arquivos potencialmente afetados**:

```bash
.vscode/
├── extensions.json     ❌ CONFIRMADO: 20 extensões duplicadas
├── mcp.json            ✅ OK (usa VSCodeJSONMerger)
├── settings.json       ✅ OK (usa VSCodeJSONMerger)
├── launch.json         ❓ DESCONHECIDO (pode estar afetado)
├── tasks.json          ❓ DESCONHECIDO (pode estar afetado)
└── *.json              ❓ Outros arquivos VSCode
```

**Estimativa de impacto**:
- ✅ Arquivos protegidos: 2 (mcp.json, settings.json)
- ❌ Arquivos afetados: 1 confirmado (extensions.json)
- ❓ Arquivos em risco: 2-5 (launch.json, tasks.json, outros)

#### Estratégia de Remediação em 3 Fases

**Fase 1: Detecção (15min)**

Criar script `scripts/detect-json-duplications.py`:
- Escanear todos `.vscode/*.json`
- Detectar duplicações em arrays recursivamente
- Gerar relatório formatado + JSON para CI/CD
- Output: console + `duplications-report.json`

**Fase 2: Correção Automática (10min)**

Criar script `scripts/fix-json-duplications.py`:
- Remove duplicações preservando ordem
- Cria backup antes de modificar
- Valida JSON após correção
- Log detalhado de ações

**Fase 3: Prevenção (CI/CD Integration)**

- **Pre-commit hook**: Bloqueia commits com duplicações
- **GitHub Actions**: Valida PRs antes de merge
- **Monitoring**: Alerta se duplicações aparecerem

#### Automação de Monitoramento

**Pre-commit hook** (`.git/hooks/pre-commit`):
```bash
#!/bin/bash
for file in $(git diff --cached --name-only | grep '\.json$'); do
    python scripts/detect-json-duplications.py "$file" || exit 1
done
```

**GitHub Actions** (`.github/workflows/validate-json.yml`):
```yaml
on: [push, pull_request]
jobs:
  check-duplications:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Scan JSON duplications
        run: python scripts/detect-json-duplications.py
```

---

### 4️⃣ Python MCP Server Expert — Análise de Código Python

#### Problemas no Pattern `can_merge()`

**Anti-pattern identificado**: Brittle String Matching

```python
# ❌ FRÁGIL
def can_merge(self, file_path: Path) -> bool:
    return (
        file_path.name in ["mcp.json", "settings.json"] and  # Lista hardcoded
        ".vscode" in file_path.parts  # String matching frágil
    )
```

**Problemas**:
1. **Magic Strings**: Sem constantes, fácil esquecer ao adicionar arquivos
2. **No Type Validation**: Aceita qualquer `Path`, sem validação
3. **Implicit Contract**: Sem interface explícita, comportamento não verificável
4. **Poor Testability**: Difícil testar todos os casos

#### Solução com Type Hints e Validação

**Proposta P1 — Type-Safe Config**:
```python
from dataclasses import dataclass
from enum import Enum
from typing import Protocol

class MergeStrategy(Enum):
    """Estratégias de merge disponíveis."""
    USER_WINS_NO_UNION = "user_wins_no_union"  # VSCode files
    DEEP_MERGE = "deep_merge"                   # Generic JSON
    WORKSPACE_SPECIALIZED = "workspace"         # .code-workspace

@dataclass(frozen=True)
class MergeConfig:
    """Configuração imutável de merge para um arquivo."""
    file_pattern: str
    strategy: MergeStrategy
    description: str
    examples: list[str]

MERGE_CONFIGS: dict[str, MergeConfig] = {
    "vscode_extensions": MergeConfig(
        file_pattern=".vscode/extensions.json",
        strategy=MergeStrategy.USER_WINS_NO_UNION,
        description="Extension recommendations - user list, no duplication",
        examples=["recommendations"]
    ),
    # ... outros configs
}

class Merger(Protocol):
    """Interface explícita para mergers."""
    def can_merge(self, file_path: Path) -> bool: ...
    def merge(self, existing: Path, template: str, interactive: bool = True) -> CreatedItem: ...
    @property
    def strategy(self) -> MergeStrategy: ...
```

#### Testing Strategy Proposta

**Cobertura mínima obrigatória**:

```python
# tests/test_json_merge_extensions.py

class TestExtensionsJsonMerge:
    def test_can_merge_extensions_json(self):
        """VSCodeJSONMerger reconhece extensions.json."""
        merger = VSCodeJSONMerger()
        assert merger.can_merge(Path(".vscode/extensions.json")) is True
    
    def test_no_array_union_in_recommendations(self, tmp_path):
        """Merge NÃO faz union de arrays."""
        # Template: ["ext1", "ext2"]
        # User: ["ext2", "ext3"]
        # Expected: ["ext2", "ext3"] (user wins, no union)
        ...
    
    def test_current_extensions_json_is_clean(self):
        """Arquivo atual não tem duplicações."""
        data = json.loads(Path(".vscode/extensions.json").read_text())
        counts = Counter(data["recommendations"])
        duplicates = [ext for ext, count in counts.items() if count > 1]
        assert len(duplicates) == 0
```

**Meta-teste para garantir sincronização**:
```python
def test_all_vscode_files_have_tests(self):
    """Garante que VSCODE_USER_WINS_FILES está completo."""
    tested_files = {"mcp.json", "settings.json", "extensions.json", ...}
    assert VSCODE_USER_WINS_FILES == tested_files
```

---

## 📝 Análise Consolidada — Consenso dos 4 Agentes

### Root Causes Identificados

| Causa | Categoria | Severidade | Consenso |
|-------|-----------|------------|----------|
| Lista hardcoded incompleta em `can_merge()` | Code Smell | **CRITICAL** | 4/4 ✅ |
| Falta de testes para arquivos VSCode | Testing Gap | **HIGH** | 4/4 ✅ |
| Ausência de documentação sobre strategies | Documentation | **MEDIUM** | 3/4 ✅ |
| Pattern Chain of Responsibility frágil | Architecture | **MEDIUM** | 2/4 ⚠️ |

### Consenso: Solução Mínima P0

**Todos os 4 agentes concordam** com correção imediata:

1. ✅ Adicionar `extensions.json` à whitelist de `VSCodeJSONMerger`
2. ✅ Criar script de detecção de duplicações
3. ✅ Adicionar 3 testes unitários mínimos
4. ✅ Limpar duplicações existentes em extensions.json

### Divergências (Pontos de Debate)

| Questão | Software Eng | Principal Eng | DevOps | Python MCP |
|---------|--------------|---------------|---------|------------|
| Refatorar para Registry pattern? | 👍 P2 (futuro) | 👍 P1 (semana) | 🤷 Opcional | 👍 P1 (type-safe) |
| Adicionar launch.json/tasks.json? | 👍 Sim, agora | 👍 Sim + testes | ⚠️ Investigar | 👍 Sim + testes |
| CI/CD validation? | 🤷 Nice to have | 👍 Essencial | 👍 **CRÍTICO** | 👍 Pre-commit |

---

## 🎯 Conclusões e Recomendações

### Conclusão Principal

O bug é resultado de **lista incompleta** em VSCodeJSONMerger combinado com **falta de testes** e **documentação insuficiente** sobre o sistema de merge. O fix mínimo é simples (adicionar uma string), mas a arquitetura precisa de hardening para prevenir regressões.

### Recomendações Priorizadas

#### P0 — Crítico (Deploy Hoje — 30min)
1. ✅ Adicionar `"extensions.json"` na lista de `VSCodeJSONMerger.can_merge()`
2. ✅ Limpar duplicações existentes em `.vscode/extensions.json`
3. ✅ Criar 3 testes unitários mínimos
4. ✅ Commit com evidências e testes

#### P1 — Importante (Esta Semana — 2-3h)
1. 📋 Centralizar configuração em `scripts/lib/constants.py`
2. 📋 Script `detect-json-duplications.py`
3. 📋 Script `fix-json-duplications.py`
4. 📋 Validação pós-merge em `save_json_formatted()`
5. 📋 Documentação em `docs/guides/json-merge-system.md`

#### P2 — Desejável (Próximo Sprint — 3-4h)
1. 🔮 Pre-commit hook para validação
2. 🔮 GitHub Actions workflow
3. 🔮 Refatoração para Strategy Pattern (opcional, se consenso)
4. 🔮 Type-safe configuration com Protocols/dataclasses

### Próximos Passos Imediatos

1. **Executar plano P0** (ver arquivo `docs/planning/2026-05-17-json-merge-fix-action-plan.md`)
2. **Validar testes** passam após correção
3. **Commit com evidências** preservadas
4. **Planejar P1** para próxima sessão

---

## 📚 Referências

- **Commit relacionado**: `9595ac9` — fix(json-merge): Corrigir duplicação em mcp.json
- **Evidências**: `tmp/evidencia/json_diif_20260517_1116.log`
- **Código afetado**: `scripts/lib/json_merge.py` (classe VSCodeJSONMerger)
- **Sistema de merge**: Chain of Responsibility pattern em `scripts/lib/file_merge.py`
- **Biblioteca de merge**: `deepmerge.always_merger` (causa union de arrays)

---

**Fim do Debate Técnico**
