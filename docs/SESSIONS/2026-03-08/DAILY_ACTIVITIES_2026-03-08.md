# 📅 Daily Activities — 2026-03-08

**Branch**: master
**Sessão iniciada**: 2026-03-08
**Modo de trabalho**: A definir

---

## Log de Atividades

---

### IMP-29 — Documentação gerada por perfil ativo

**Status**: ✅ Concluído

**O que foi feito:**
- `scripts/lib/templates.py` — `generate_profile_guide()`, `_compute_combo_slug()`, helpers de camada
- `scripts/scaffold.py` — integrado em `flow_compose_profiles()` e `flow_upgrade()`
- `tests/test_smoke_imp29.py` — 33 testes
- `docs/TODO.md` — IMP-29 marcado como concluído

**Resultado**: 307 testes passando

---

### IMP-30 — scaffold.py --publish (tarball de release)

**O que foi feito:**
- `scripts/lib/publish.py` — novo módulo:
  - `_INCLUDE_PATTERNS` — 15 padrões glob para coleta de arquivos
  - `_collect_files(project_root)` — coleta deduplica, sem `__pycache__`/`.venv`/`.git`/`.secrets`/`dist`/`*.pyc`
  - `publish_template(output_dir, project_root)` — gera `enterprise-template-v{version}-{date}.tar.gz` + `release-manifest-v*.json`
  - `PublishResult` dataclass com `tarball_path`, `manifest_path`, `file_count`, `size_bytes`, `version`, `created_at`, `included_files`
- `scripts/scaffold.py` — `flow_publish()` + flags `--publish` e `--output-dir`
- `tests/test_smoke_imp30.py` — 35 testes (3 classes: TestCollectFiles, TestPublishTemplate, TestPublishCLI)
- `docs/TODO.md`, `CHANGELOG.md`, `docs/INDEX.md` — atualizados

**Resultado**: 342 testes passando (307 anteriores + 35 novos)

---

### IMP-31 — CI/CD do template (GitHub Actions)

**O que foi feito:**
- `.github/workflows/ci-template.yml` — workflow completo com 3 jobs:
  - **test** — matrix Python 3.10 / 3.11 / 3.12; `pip install pyyaml rich pytest`; `pytest tests/ --tb=short -q`
  - **cli-smoke** — `needs: test`; executa `--list-profiles --json`, `--dry-run`, `--publish --json` contra código real
  - **lint** — `py_compile` em `scripts/lib/*.py` + `yaml.safe_load` em `profile-descriptors/*.yaml`
- Disparo: `pull_request` + `push` com filtro `paths: ["scripts/**", "tests/**", "profile-descriptors/**", ".github/workflows/**"]`
- `concurrency: cancel-in-progress: true` para evitar runs duplicadas em PRs
- `tests/test_smoke_imp31.py` — 26 testes (5 classes: TestWorkflowExists, TestWorkflowTriggers, TestJobTest, TestJobCliSmoke, TestJobLint)
- `docs/TODO.md`, `CHANGELOG.md`, `docs/INDEX.md` — atualizados

**Resultado**: 368 testes passando (342 anteriores + 26 novos)

---

### IMP-32 — scaffold.py --validate (validação de profile-descriptors)

**O que foi feito:**
- `scripts/lib/validate.py` — novo módulo:
  - `ValidationIssue(field, severity, message)` — issue individual
  - `ProfileResult` — resultado por descriptor (status: ok/warning/error; filtra .errors e .warnings)
  - `ValidationReport` — agregado: valid, profiles_checked, total_errors, total_warnings
  - `_validate_descriptor(data, path)` — 6 regras: name, description, version (semver), last_tested, layer, YAML parse
  - `_cross_validate(results, all_data)` — nomes duplicados + combines_with/excludes_with com refs inválidas
  - `validate_descriptors(dir)` — entrada pública; carrega todos `*.yaml` via yaml.safe_load
  - Aceita schema antigo (VERSION/LAST_TESTED_DATE) e novo (version/last_tested)
  - combines_with: lista de strings OU lista de objetos {name, notes}
- `scripts/scaffold.py` — `flow_validate()` + flag `--validate` + `--validate --json`
- `tests/test_smoke_imp32.py` — 42 testes (7 classes: TestValidationIssue, TestProfileResult, TestValidationReport, TestValidateDescriptor, TestCrossValidate, TestValidateDescriptorsIntegration, TestValidateCLI)
- `docs/TODO.md`, `CHANGELOG.md`, `docs/INDEX.md` — atualizados

**Resultado**: 410 testes passando (368 anteriores + 42 novos)

---

### Homologação do template — Debate por 6 perspectivas profissionais

**O que foi feito:**
- Revisão completa do projeto por 6 papéis: Template Architect, DevEx/CLI Engineer, SRE/Infra, AppSec, Tech Docs, Release Maintainer
- Matriz de homologação gerada com scores por dimensão (estrutura, CLI, segurança, testes, docs, CI/CD)
- Criado `docs/SESSIONS/2026-03-08/HOMOLOGATION-DEBATE-2026-03-08.md` com debate completo e alertas levantados
- Debate commitado em `9b563e7`

**Alertas identificados (por perspectiva):**
- Template Architect: `devops-security.yaml` ausente (warnings em `--validate`), TEMPLATE-VERSIONS.md desatualizado
- DevEx/CLI: `--export-json` ausente, `--info <perfil>` ausente, shell-completion não implementado
- SRE/Infra: `docker-compose.yml` de dev não existe, integração com secrets managers (Vault/AWS SM) ausente
- AppSec: `SECURITY.md` ausente, SBOM não gerado no publish, scan SAST/DAST não configurado
- Tech Docs: `docs/ARCHITECTURE.md` ausente, `CONTRIBUTING.md` ausente, ADRs não existem
- Release Maintainer: `CHANGELOG.md` manual (sem conventional commits), `docs/COMPATIBILITY-MATRIX.md` desatualizado

**Resultado**: Debate documentado, roadmap criado — 12 novos itens no backlog

---

### Plano de Ação Pós-Homologação (IMP-33 a IMP-44)

**O que foi feito:**
- Criados 12 novos IMPs em `docs/TODO.md`, seção "Plano de Ação Pós-Homologação"
- Distribuídos em 4 prioridades (P0 a P3):
  - **P0** (crítico): IMP-33 (`devops-security.yaml`, atualização TEMPLATE-VERSIONS), IMP-34 (`SECURITY.md`, SBOM no publish)
  - **P1** (alta): IMP-35 (`--info <perfil>` CLI), IMP-36 (`docker-compose.yml` de dev), IMP-37 (SAST básico no CI)
  - **P2** (média): IMP-38 (`ARCHITECTURE.md`), IMP-39 (`CONTRIBUTING.md`), IMP-40 (ADRs), IMP-41 (`--export-json`)
  - **P3** (baixa): IMP-42 (shell-completion), IMP-43 (integração secrets managers), IMP-44 (conventional commits + changelog automation)
- Commitado em `9b563e7`

**Resultado**: Roadmap completo para as próximas sessões

