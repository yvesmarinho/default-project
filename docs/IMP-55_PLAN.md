# IMP-55: Sistema de Captura CHAT-*.md

**Status**: 🔵 EM PROGRESSO
**Prioridade**: P2 (Média)
**Data Início**: 2026-04-14
**Estimativa**: 1 semana (40h)

---

## Executive Summary

Implementar sistema de captura e estruturação de conversas do GitHub Copilot em arquivos `CHAT-YYYY-MM-DD-HHmm.md`, integrando com Session Search (IMP-51/57) para memória passiva aprimorada. Sistema permitirá busca full-text em conversas históricas, rastreabilidade de decisões, e contextualização de trabalho anterior.

---

## Contexto

### Problema

Atualmente, conversas do GitHub Copilot são perdidas após sessão terminar. Conhecimento valioso (decisões de design, debugging insights, alternativas consideradas) não fica registrado de forma estruturada e pesquisável.

**Pain points**:
- Sem histórico de conversas anteriores
- Impossível buscar "como resolvemos problema X na sessão passada?"
- Decisões importantes perdidas (não documentadas em ADRs)
- Retrabalho: re-debater questões já resolvidas
- Falta de contexto para onboarding de novos membros

### Origem

- **Debate**: `DEBATE_SPEC_DRIVEN_DEVELOPMENT_2026-04-05.md`
- **Mencionado em**: IMP-53/54 implementation (Layer 1: Business context)
- **Dependências**: IMP-51 (Session Search), IMP-57 (Multi-scope indexing)

---

## Objetivos

### Objetivo Principal

Criar sistema automatizado de captura de conversas GitHub Copilot em formato estruturado `CHAT-*.md`, com indexação FTS5 para busca e integração com memória passiva.

### Objetivos Específicos

1. **Captura automática**: Interceptar conversas do Copilot e salvar em `CHAT-YYYY-MM-DD-HHmm.md`
2. **Estruturação**: Formato markdown canônico (timestamps, roles, context blocks)
3. **Indexação**: Integrar com Session Search (scripts/lib/search.py)
4. **Busca**: `session-search.py --scope chats "query here"`
5. **Rastreabilidade**: Linkar CHAT → DAILY_ACTIVITIES → specs

---

## Arquitetura Proposta

### 1. Formato Arquivo CHAT-*.md

```markdown
---
type: chat
session_date: 2026-04-14
session_id: abc123def456
start_time: 14:30:00
end_time: 15:45:00
participants:
  - user: yves_marinho
  - agent: github-copilot
topics:
  - IMP-55 Sistema CHAT
  - Session Search Integration
  - FTS5 Indexing
related_sessions:
  - DAILY_ACTIVITIES_2026-04-14.md
  - SESSION_REPORT_2026-04-14.md
related_specs:
  - .specify/specs/IMP-55/spec.md
template_version: 1.0.0
---

# CHAT — 2026-04-14 14:30 — IMP-55 Sistema CHAT

**Session ID**: abc123def456
**Duration**: 1h 15min
**Context**: Implementação do sistema de captura de conversas

---

## 14:30:05 — USER

Vamos implementar o IMP-55 (Sistema CHAT-*.md)

---

## 14:30:12 — ASSISTANT

Entendi! Vou criar o plano de implementação para o sistema de captura de conversas...

[resto da conversa...]

---

## Summary

**Topics covered**:
- Definição de formato CHAT-*.md
- Arquitetura de captura
- Integração com Session Search

**Decisions made**:
- ADR-001: Usar transcripts API do VS Code
- ADR-002: Estrutura YAML frontmatter

**Next steps**:
- Implementar chat_capture.py
- Adicionar --scope chats ao session-search.py
```

### 2. Componentes do Sistema

#### A. Captura (`scripts/lib/chat_capture.py`)

```python
class ChatCapture:
    """Captura conversas do GitHub Copilot"""

    def __init__(self, session_dir: Path):
        self.session_dir = session_dir
        self.chat_dir = session_dir / "CHATS"

    def capture_from_transcript(self, transcript_path: Path) -> Path:
        """
        Lê transcript do VS Code, converte para CHAT-*.md

        Transcript path:
        ~/.config/Code - Insiders/User/workspaceStorage/.../GitHub.copilot-chat/transcripts/*.jsonl
        """
        pass

    def format_chat_message(self, msg: dict) -> str:
        """Formata mensagem em markdown canônico"""
        pass

    def extract_metadata(self, transcript: list) -> dict:
        """Extrai metadata: topics, participants, duration"""
        pass
```

#### B. Integração Search (`scripts/lib/search.py` - enhancement)

```python
class SessionSearcher:
    def search(self, query: str, scope: str = "all") -> List[SearchResult]:
        """
        scope: "sessions" | "docs" | "specs" | "chats" | "all"

        NEW: "chats" scope
        """
        if scope == "chats":
            return self._search_chats(query)
        # existing code...

    def _search_chats(self, query: str) -> List[SearchResult]:
        """Busca em CHAT-*.md files"""
        pass
```

#### C. CLI (`scripts/session-chat.py` - NEW)

```bash
# Capturar última conversa
./scripts/session-chat.py capture --latest

# Capturar conversa específica
./scripts/session-chat.py capture --transcript-id abc123def456

# Listar conversas
./scripts/session-chat.py list --date 2026-04-14

# Buscar em conversas
./scripts/session-chat.py search "IMP-55 implementation"

# Exportar conversa para spec.md context
./scripts/session-chat.py export --chat-id CHAT-2026-04-14-1430 --output context.md
```

---

## Fases de Implementação

### Fase 1: Estrutura Base (8h)

**Deliverables**:
- ✅ Formato canônico `CHAT-*.md` definido
- ✅ `scripts/lib/chat_capture.py` (classe base)
- ✅ `tests/test_chat_capture.py` (parsing, metadata extraction)
- ✅ Template `.specify/templates/chat-template.md`

**Tasks**:
1. Definir YAML frontmatter schema
2. Implementar `ChatMessage` dataclass
3. Implementar `format_chat_message()`
4. Criar testes para parsing

### Fase 2: Captura de Transcripts (12h)

**Deliverables**:
- ✅ `capture_from_transcript()` implementation
- ✅ Detecção automática de transcript path
- ✅ Conversão JSONL → CHAT.md
- ✅ Metadata extraction (topics via NLP)

**Tasks**:
1. Estudar formato transcript JSONL (VS Code Copilot)
2. Implementar parser JSONL → ChatMessage[]
3. Extrair topics via keyword extraction (TF-IDF simples)
4. Linking automático: detectar IMP-XXX, file paths, session dates

### Fase 3: Integração Search (8h)

**Deliverables**:
- ✅ `SessionSearcher._search_chats()` implementation
- ✅ Indexação de CHAT-*.md em FTS5
- ✅ `--scope chats` no session-search.py
- ✅ Tests para busca em chats

**Tasks**:
1. Estender `SessionIndexer.index_session()` para CHATS/
2. Adicionar `document_type = 'chat'` na tabela FTS5
3. Implementar `_search_chats()` com ranking BM25
4. Adicionar filtro `--scope chats` no CLI

### Fase 4: CLI e Workflow (8h)

**Deliverables**:
- ✅ `scripts/session-chat.py` (CLI completo)
- ✅ Makefile targets: `chat-capture`, `chat-list`, `chat-search`
- ✅ Integração com session-start.prompt / session-end.prompt
- ✅ Documentação: `SESSION_CHAT_GUIDE.md`

**Tasks**:
1. Implementar `session-chat.py capture` com --latest / --transcript-id
2. Implementar `session-chat.py list` com filtros de data
3. Implementar `session-chat.py export` para context blocks
4. Atualizar prompts para sugerir captura de conversas

### Fase 5: Testing e Docs (4h)

**Deliverables**:
- ✅ Test suite completo (>= 20 tests, 100% passing)
- ✅ `docs/SESSION_CHAT_GUIDE.md` (~500 linhas)
- ✅ Examples: 3 CHAT-*.md de exemplo
- ✅ TODO.md / INDEX.md updates

**Tasks**:
1. Testes end-to-end: capture → index → search
2. Testes de edge cases: conversas longas (>10k lines), Unicode, code blocks
3. Documentação completa com diagramas
4. Exemplos práticos: debugging session, design discussion, code review

---

## Critérios de Sucesso

| Métrica | Target | Medição |
|---------|--------|---------|
| Captura automática | 100% das conversas | Verificar CHATS/ após cada sessão |
| Busca performance | <0.1s per query | Benchmark com 50+ chats |
| Test coverage | >=90% | pytest --cov |
| Formato compliance | 100% YAML frontmatter válido | yamllint + JSON Schema |
| Integration | Zero breaking changes | Existing session-search.py unchanged |

---

## Riscos e Mitigações

### Risco 1: Transcript API instável

**Probabilidade**: Média
**Impacto**: Alto (bloqueia captura automática)
**Mitigação**:
- Fallback: manual capture via copy-paste
- Monitorar VS Code API changes
- Feature flag: `CHAT_CAPTURE_ENABLED=true`

### Risco 2: Conversas muito longas (>100k chars)

**Probabilidade**: Baixa
**Impacto**: Médio (performance search)
**Mitigação**:
- Split em múltiplos arquivos: `CHAT-YYYY-MM-DD-HHmm-part1.md`
- Limit FTS5 snippet length
- Pagination na busca

### Risco 3: Privacidade (credenciais em conversas)

**Probabilidade**: Alta
**Impacto**: Crítico (leak de secrets)
**Mitigação**:
- Scan com `.gitleaks-session-docs.toml` (já existente)
- Warning se detectar patterns de credencial
- `.gitignore` para CHATS/ (opcional por projeto)

---

## Dependências

- ✅ **IMP-51**: Session Search System (base FTS5)
- ✅ **IMP-57**: Multi-scope indexing (sessions + docs + specs)
- ⏸️ **IMP-58**: Avaliação de necessidade (pode influenciar formato)
- ⏳ **VS Code Copilot API**: Transcript access (pesquisar disponibilidade)

---

## Breaking Changes

**NENHUM**: Sistema é additive, não modifica existing workflows.

- ✅ Session Search continua funcionando sem --scope chats
- ✅ DAILY_ACTIVITIES.md não afetado
- ✅ Existing scripts não quebram

---

## Next Steps (Immediate)

1. **Investigar Transcript API** (30min)
   - Verificar se VS Code expõe transcripts via file system
   - Path: `~/.config/Code - Insiders/User/workspaceStorage/.../GitHub.copilot-chat/transcripts/`
   - Formato: JSONL ou JSON?

2. **Criar objetivo.yaml para IMP-55** (30min)
   - Run: `/speckit.clarify` Mode 1
   - Define business problem, success metrics, personas

3. **Implementar Fase 1** (8h)
   - Criar estrutura base + testes

---

**Fim do plano IMP-55**
**Próximo**: Investigar Transcript API e criar objetivo.yaml
