# SpecKit Constitution — Knowledge Harvester Library (KHL)

**Data**: 2026-04-28  
**Owner**: `yvesmarinho`  
**Projeto**: **KHL — Knowledge Harvester Library**  
**Propósito**: Compilar (agregar) conhecimento operacional (agents, prompts, skills, rules e docs) a partir de uma **pasta local** que contém repositórios (forks) selecionados, produzindo um **output em JSON** seguro, determinístico e fácil de reutilizar em outros projetos (incluindo integração com o template `default-project`).

---

## 1. Princípios (Constituição)

### 1.1. Determinismo e rastreabilidade
1. Todo documento agregado **MUST** conter metadados de rastreio (mínimo):
   - `repo_path` (caminho local do repo)
   - `repo_name`
   - `commit_sha`
   - `rel_path` (caminho relativo do arquivo no repo)
   - `content_hash` (hash do conteúdo normalizado)
   - `collected_at` (ISO8601)
2. O pipeline **MUST** ser reexecutável: mesmo input (repo+sha+arquivo) → mesmo output (bytes JSON), exceto campos explicitamente variáveis (`collected_at`).

### 1.2. Segurança por padrão
1. O sistema **MUST** aplicar sanitização de segredos antes de persistir output.
2. O sistema **MUST** suportar uma política explícita de redaction:
   - `mask` (padrão): substitui por `"[REDACTED]"`
   - `drop`: remove linhas/trechos
   - `fail`: aborta a coleta daquele documento
3. O sistema **MUST** registrar eventos de segurança (audit log) sem vazar o segredo.

### 1.3. Escopo: pasta local com forks selecionados
1. A descoberta de repositórios parte de um diretório raiz local (`--repos-root`).
2. Não indexar GitHub diretamente (sem API), por decisão explícita.
3. O sistema **MUST** lidar com repositórios Git (com `.git/`) e ignorar diretórios que não sejam repos.

### 1.4. Output: JSON como contrato principal
1. O **contrato de saída principal** é JSON (ou JSONL), independente de driver.
2. O sistema **SHOULD** gerar artefatos adicionais opcionais (ex: `SUMMARY.md`), mas o “source of truth” é JSON.

### 1.5. UX Linux/CLI
1. Operação primária via CLI, para execução local e agendamento via `cron`.
2. Saída deve suportar:
   - texto (humano)
   - `--json` (máquina)
3. Compatível com pipelines (`| jq`, `| less`).

---

## 2. Definições

- **Repo Root**: diretório local contendo vários repositórios Git (forks).
- **Documento**: arquivo textual (Markdown, JSON, YAML etc.) considerado “conhecimento”.
- **Knowledge Artifact**: JSON/JSONL gerado contendo conteúdo + metadados + classificação.
- **Sanitização**: detecção e mascaramento/remoção de segredos.

---

## 3. Requisitos funcionais (RF)

### RF-01 — Descoberta de repositórios
- Entrada: `repos_root: Path`.
- Saída: lista de repositórios válidos.
- Critério: diretório contém `.git/`.

### RF-02 — Seleção de arquivos “conhecimento”
- Deve selecionar por regras configuráveis:
  - paths: `.github/prompts/`, `agents/`, `skills/`, `prompts/`, `docs/`, `README*`, `.copilot-*.md`, `.copilot-rules.md`.
  - extensões: `.md`, `.rst`, `.txt`, `.json`, `.yml`, `.yaml`, `.toml`.
- Deve excluir por padrão:
  - binários e assets (`.png`, `.pdf`, `.zip`, etc.)
  - pastas: `.venv/`, `node_modules/`, `dist/`, `build/`, `.git/`.

### RF-03 — Coleta e normalização
- Ler arquivo com detecção robusta de encoding (fallback UTF-8 com substituição controlada).
- Normalizar:
  - `\r\n` → `\n`
  - remover `\x00`
  - trimming opcional configurável.

### RF-04 — Classificação (tipo do documento)
- Classificar em categorias:
  - `agent`, `skill`, `prompt`, `rule`, `doc`, `workflow`, `config`, `unknown`.
- Regras baseadas em path e/ou heurísticas (ex: frontmatter, headings).

### RF-05 — Sanitização de segredos
- Detectar padrões típicos (não exaustivo):
  - tokens (`ghp_`, `github_pat_`)
  - AWS keys
  - JWT
  - `password=`, `token=`, `secret=`, `api_key=`
  - chaves PEM (`-----BEGIN`)
- Aplicar política `mask|drop|fail`.

### RF-06 — Geração do output JSON
- Gerar:
  - `library/documents.jsonl` (um documento por linha)
  - `library/index.json` (metadados agregados: repos, contagens, hashes)
- Documentos devem conter:
  - `id` estável (hash)
  - metadados de rastreio
  - `type`
  - `title` (quando possível)
  - `tags` (opcional)
  - `text` (sanitizado)

### RF-07 — Incremental / cache
- Evitar reprocessar se `commit_sha` do repo não mudou.
- Manter `state.json` com:
  - repo → sha → timestamp

---

## 4. Requisitos não funcionais (RNF)

### RNF-01 — Confiabilidade
- Em erro de leitura/parse/sanitização: registrar erro e **continuar** o processamento (best-effort), exceto se modo `--strict`.

### RNF-02 — Performance
- Alvo atual: <5 repos, mas deve escalar para dezenas.
- Clone/pull não faz parte (repos já existem); apenas leitura local.

### RNF-03 — Observabilidade
- Logs:
  - `INFO`: progresso
  - `WARNING`: arquivo ignorado por regra
  - `ERROR`: falha processando doc
- Opcional: `--log-json`.

### RNF-04 — Portabilidade
- Python 3.11+.
- Sem dependências pesadas por padrão.

---

## 5. Interface (CLI) — contrato

### Comandos mínimos
1. `khl scan --repos-root <path>`
2. `khl build --repos-root <path> --out <path>`
3. `khl query --out <path> "termo"` (fase 2; opcional, textual simples sobre JSON)

### Flags
- `--include-ext md,json,yaml,yml,rst,txt,toml`
- `--exclude-dirs .git,.venv,node_modules,dist,build`
- `--secrets-policy mask|drop|fail`
- `--strict`

---

## 6. Integração com template `default-project`

1. O output deve ser copiável para projetos gerados pelo scaffold.
2. Estrutura recomendada no projeto destino:
   - `docs/knowledge/library/` (ou `docs/library/`)
   - `prompts/library/` (se houver exportação por tipo)
3. Futuro: o scaffold pode oferecer opção `--with-knowledge <path_to_library>`.

---

## 7. Critérios de aceitação

1. Dado um `repos_root` com 2 repos e 20 arquivos, o comando `khl build` gera:
   - `documents.jsonl` não-vazio
   - `index.json` válido
2. Segredos conhecidos (ex: `ghp_...`) não aparecem no output.
3. Reexecução sem alteração em repos não reprocessa (usa `state.json`).

---

## 8. Decisões (ADR-lite)

- **JSON/JSONL** é o formato canônico de exportação (decisão do usuário).
- Execução local via cron (decisão do usuário).
- Fonte é pasta local com forks separados (decisão do usuário).
- Segurança é mandatória: sanitização sempre habilitada (decisão do usuário).
