# KHL — Knowledge Harvester Library

Agregador local de conhecimento (agents, prompts, skills, rules e docs) a partir de uma pasta contendo **repositórios Git (forks)** selecionados. Gera uma **biblioteca em JSON/JSONL** sanitizada (sem segredos) e pronta para ser incorporada em outros projetos (incluindo integração com `default-project`).

> **Status**: Especificação definida (2026-04-28). Implementação planejada em fases.

---

## Objetivo

- Consolidar conhecimento espalhado em múltiplos repositórios (ex.: `awesome-copilot`, `agent-skills`, `claude-skills` etc.) em um **artefato local único**.
- Tornar o conhecimento reutilizável e auditável.
- Operar localmente (Linux) e executar via `cron`.

---

## Escopo (definido pelo questionário)

- **Fonte**: uma pasta local (`repos_root`) contendo apenas repositórios que você fez fork e separou para este projeto.
- **Não** inclui repositórios privados via GitHub API (sem GitHub API).
- **Modo**: execução local.
- **Output principal**: **JSON** (preferência por independência de driver e legibilidade).
- **Busca**: fase inicial apenas agregação/compilação (opção A do questionário).

---

## O que será indexado

### Diretórios/arquivos tipicamente relevantes
Prioridade alta (padrão):
- `.github/prompts/**`
- `agents/**`
- `skills/**`
- `prompts/**`
- `docs/**`
- `README*`
- `.copilot-rules.md`, `.copilot-*.md`

Extensões padrão:
- `.md`, `.rst`, `.txt`, `.json`, `.yml`, `.yaml`, `.toml`

### Exclusões padrão
- `.git/`, `.venv/`, `node_modules/`, `dist/`, `build/`
- arquivos binários: `.png`, `.pdf`, `.zip`, etc.

---

## Artefatos gerados

Diretório de saída (ex.: `library/`):
- `documents.jsonl` — 1 documento por linha (conteúdo + metadados)
- `index.json` — visão agregada (repos, contagens, hashes)
- `state.json` — cache incremental (repo → commit sha)
- `security_report.json` — eventos de sanitização (sem expor segredo)

---

## Modelo de documento (draft)

Cada linha do `documents.jsonl` (um JSON por linha) contém, no mínimo:

- `id` (hash estável)
- `repo_path`
- `repo_name`
- `commit_sha`
- `rel_path`
- `type` (`agent|skill|prompt|rule|doc|workflow|config|unknown`)
- `title` (inferido quando possível)
- `collected_at` (ISO8601)
- `content_hash`
- `text` (sanitizado)

---

## Segurança (mandatório)

- Sanitização sempre ligada.
- Políticas:
  - `mask` (padrão): substitui por `[REDACTED]`
  - `drop`: remove trecho/linha
  - `fail`: rejeita documento

---

## Execução via cron (exemplo)

```cron
# Atualiza biblioteca todos os dias às 02:15
15 2 * * * /usr/bin/env bash -lc 'cd ~/khl && .venv/bin/python -m khl build --repos-root ~/forks-khl --out ~/khl-library > ~/khl/logs/cron.log 2>&1'
```

---

## Próximos passos (recomendado)

1. Implementar MVP:
   - scan repos
   - selecionar arquivos
   - sanitizar
   - exportar JSONL
2. Adicionar incremental (`state.json`).
3. Adicionar exportação por tipo (opcional): `export/agents/`, `export/prompts/`.

---

## Documentos do projeto

- Constituição do SpecKit: `docs/spec/CONSTITUTION-SPECKIT-KHL.md`
