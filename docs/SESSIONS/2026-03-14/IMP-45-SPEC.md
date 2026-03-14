# 📐 IMP-45 — Especificação Técnica: Engram MCP — Memória Persistente por Projeto

**Data**: 2026-03-14
**Versão**: 1.0.0
**Status**: 🔵 Backlog — pré-requisito externo ausente (binário `engram`)
**Origem**: Análise de impacto da doc `docs/GitHub Copilot - Engram how to.md`
**Prioridade**: P3 — Evolução de Developer Experience (não bloqueia nenhum IMP ativo)

---

## 1. Visão Geral

Integrar o [Gentleman-Programming/engram](https://github.com/Gentleman-Programming/engram) como MCP server
de memória persistente por projeto. O Engram é um servidor Go com SQLite + FTS5 exposto via MCP (stdio),
permitindo que o Copilot Agent salve e recupere contexto entre sessões sem depender exclusivamente dos
arquivos de sessão em `docs/SESSIONS/`.

### 1.1 Problema a Resolver

- Hoje o histórico de sessões vive em `docs/SESSIONS/YYYY-MM-DD/*.md` — ótimo para humanos, mas não
  há busca por relevância: para recuperar "qual foi a decisão sobre subcomandos CLI?", o agente precisa
  navegar manualmente pelos arquivos.
- O mecanismo `/memories/repo/` do Copilot existe, mas não tem busca FTS e não persiste cross-máquina
  via repositório.
- A integração com Engram adiciona uma camada de busca full-text rápida e auditável, complementar ao
  histórico textual já existente.

### 1.2 Fora de Escopo

- Substituto do padrão `docs/SESSIONS/` (continua existindo em paralelo)
- Sincronização automática Git (`.engram/index/engram.db` permanece no `.gitignore`)
- Perfis Layer 2/3 exportando configuração do Engram (nenhum perfil depende disso)
- Qualquer modificação em `scripts/scaffold.py` ou `scripts/lib/`

---

## 2. Pré-requisitos e Bloqueadores

| Item | Status | Ação necessária |
|------|--------|-----------------|
| Binário `engram` instalado | ❌ Ausente | Instalar via release do repo upstream |
| `engram --help` validado | ❌ Pendente | Verificar subcomandos `mem`, `import`, `mcp` |
| `engram mcp --help` validado | ❌ Pendente | Verificar env vars aceitas pelo MCP server |
| `engram import` (ou equivalente) | ❌ Desconhecido | Verificar se suporta import de diretório |
| Code 1.110.1 MCP suporte estável | ✅ Confirmado | `mcp.json` já presente e funcional |

> **Bloqueador P0**: Esta IMP NÃO deve ser iniciada sem que o binário `engram` esteja instalado
> e os três `--help` acima tenham sido validados e documentados aqui.

---

## 3. Arquitetura Proposta

### 3.1 Estrutura de Arquivos

```
.engram/
├── AGENT_MEMORY_POLICY.md      ← commitável — política de uso para o agente
├── memory/                     ← commitável — fonte de verdade em texto
│   └── TEMPLATE.md             ← template de memória com campos padronizados
├── scripts/
│   ├── engram_mcp.sh           ← wrapper (seta env vars, garante cwd por-projeto)
│   └── engram_rebuild_index.sh ← reconstrói engram.db a partir de memory/
└── index/                      ← ← NÃO COMMITÁVEL (.gitignore)
    └── engram.db               ← SQLite + FTS5 — cache local, reconstruível
```

### 3.2 Chave de Design: Event Sourcing

- **Fonte de verdade**: `.engram/memory/*.md` (texto commitável, versionado)
- **Índice**: `.engram/index/engram.db` (binário, ignorado; reconstruível via `make engram-rebuild`)
- Ao clonar o repo em nova máquina: `make engram-rebuild` reconstrói o índice

### 3.3 Wrapper Script (`.engram/scripts/engram_mcp.sh`)

```bash
#!/usr/bin/env bash
set -euo pipefail

ENGRAM_DB="${ENGRAM_DB:-${PWD}/.engram/index/engram.db}"
ENGRAM_MEMORY_DIR="${ENGRAM_MEMORY_DIR:-${PWD}/.engram/memory}"

mkdir -p "$(dirname "$ENGRAM_DB")" "$ENGRAM_MEMORY_DIR"

exec engram mcp
```

> **Nota**: as env vars exatas que o Engram aceita devem ser validadas via `engram mcp --help`
> antes de finalizar este script.

### 3.4 Configuração MCP (adição ao `.vscode/mcp.json`)

```json
"engram": {
    "command": "bash",
    "args": ["${workspaceFolder}/.engram/scripts/engram_mcp.sh"]
}
```

---

## 4. Formato de Memória (`.engram/memory/`)

Convenção de nome: `YYYY-MM-DD__<categoria>__<slug>.md`

Categorias padronizadas:

| Categoria | Uso |
|-----------|-----|
| `arquitetura` | Decisões de design, ADRs, escolhas tecnológicas |
| `build` | Comandos de build, dependências, configurações |
| `ci` | Pipelines, jobs, variáveis de ambiente |
| `deploy` | Procedures de deploy, rollback, checklist |
| `debug` | Pegadinhas, erros resolvidos, workarounds |
| `refactor` | Mudanças estruturais significativas, IMP executadas |
| `segurança` | Controles, ferramentas, decisões de AppSec |
| `convenções` | Padrões de nomenclatura, estrutura de arquivos |

Template (`TEMPLATE.md`):
```markdown
# Título: <curto e direto>
Data: YYYY-MM-DD
Tags: #<categoria> #<tecnologia> #<imp-xx>

## Contexto
<quando e por que isso se aplica>

## O que foi feito / decidido
<descrição objetiva>

## Arquivos impactados
- `caminho/do/arquivo.py` — breve descrição

## Aprendizados / Pegadinhas
<opcional — somente se relevante para o futuro>

## Reproduzir
<comandos exatos para reproduzir / verificar, se aplicável>
```

---

## 5. Política de Memória do Agente (`.engram/AGENT_MEMORY_POLICY.md`)

```markdown
## Antes de iniciar tarefas
1. `mem_search` com 3-5 queries: termos do IMP, tecnologia, arquivos a editar
2. Ler memórias retornadas antes de editar qualquer código

## Ao concluir tarefas relevantes
1. Salvar memória com: IMP concluída, arquivos impactados, decisões, comandos
2. Tags obrigatórias: #<categoria> #imp-XX
3. Proibido salvar: tokens, passwords, paths absolutos com username, credenciais

## Critério de relevância
Salvar memória quando: nova IMP concluída, decisão arquitetural tomada,
bug difícil resolvido, convenção adotada, comando não-óbvio descoberto.
NÃO salvar: cada edição de arquivo, outputs de pytest, conteúdo de sessões
(esse já está em docs/SESSIONS/).
```

---

## 6. Integração com Makefile

```makefile
.PHONY: engram-rebuild engram-check

engram-rebuild: ## Reconstrói índice FTS do Engram a partir de .engram/memory/
    @bash .engram/scripts/engram_rebuild_index.sh

engram-check: ## Verifica se o binário engram está instalado e funcional
    @command -v engram >/dev/null 2>&1 \
        || (echo "❌ engram não encontrado. Instale via: https://github.com/Gentleman-Programming/engram" && exit 1)
    @echo "✅ engram: $$(engram version 2>/dev/null || engram --version 2>/dev/null || echo 'versão desconhecida')"
```

---

## 7. Alterações no `.gitignore`

```gitignore
# Engram: índice local (reconstruível via make engram-rebuild)
.engram/index/
```

---

## 8. Deliverables

| Artefato | Tipo | Commitável |
|----------|------|------------|
| `.engram/AGENT_MEMORY_POLICY.md` | Novo | ✅ |
| `.engram/memory/TEMPLATE.md` | Novo | ✅ |
| `.engram/scripts/engram_mcp.sh` | Novo | ✅ |
| `.engram/scripts/engram_rebuild_index.sh` | Novo | ✅ (finalizar após validar `engram import`) |
| `.vscode/mcp.json` — entrada `engram` | Editar | ✅ |
| `Makefile` — targets `engram-rebuild` e `engram-check` | Editar | ✅ |
| `.gitignore` — entrada `.engram/index/` | Editar | ✅ |
| `.engram/index/` (pasta) | Gerado localmente | ❌ |

---

## 9. Testes

Não há testes automatizados para esta IMP (MCP server externo, binário Go).

Checklist de validação manual:

- [ ] `make engram-check` retorna ✅
- [ ] `engram mcp` inicia sem erro via wrapper
- [ ] VS Code reconhece o servidor em "MCP: List Servers"
- [ ] `mem_save` salva arquivo em `.engram/memory/`
- [ ] `mem_search "scaffold subcomandos"` retorna resultado relevante
- [ ] `make engram-rebuild` reconstrói índice a partir do zero
- [ ] Clone limpo + `make engram-rebuild` funciona sem dados pré-existentes

---

## 10. Decisões de Design Pendentes

| Decisão | Opções | Recomendação |
|---------|--------|--------------|
| Este setup entra no template base ou fica como opt-in? | (a) template base — todo projeto herdado; (b) opt-in — só ativa se `engram` instalado | **(b) opt-in** — evita dependência de binário Go em projetos que não precisam |
| Sincronização Git de `.engram/memory/`? | (a) commitado no projeto; (b) só local | **(a) commitado** — garante não perder após problemas, sem segredos |
| Reconstrução do índice: automática no `make init`? | (a) sim, se `engram` disponível; (b) manual | **(b) manual** — `make engram-rebuild` explícito, sem efeitos colaterais no `make init` |
