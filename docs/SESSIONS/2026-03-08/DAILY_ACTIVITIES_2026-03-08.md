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

