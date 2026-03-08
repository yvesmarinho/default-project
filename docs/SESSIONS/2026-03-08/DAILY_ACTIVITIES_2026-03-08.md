# 📅 Daily Activities — 2026-03-08

**Branch**: master
**Sessão iniciada**: 2026-03-08
**Modo de trabalho**: A definir

---

## Log de Atividades

---

### 🚀 IMP-29 — Documentação gerada por perfil ativo

**Horário**: início de sessão
**Status**: ✅ Concluído

**O que foi feito:**
- `scripts/lib/templates.py` — adicionados:
  - `_LAYER_SORT_ORDER`, `_LAYER_DISPLAY`, `_TAG_REFERENCES` — constantes de mapeamento
  - `_layer_order_int()`, `_layer_display_name()` — helpers de camada
  - `_compute_combo_slug()` — gera slug a partir dos perfis layer2+ (exclui core/transversais)
  - `_get_guide_file_entries()` — normaliza Schema A e Schema B para inventário de arquivos
  - `generate_profile_guide()` — cria `docs/PROFILE-GUIDE-{combo_slug}.md` com 5 seções obrigatórias (idempotente)
- `scripts/scaffold.py` — integração em `flow_compose_profiles()` e `flow_upgrade()`
- `tests/test_smoke_imp29.py` — 33 testes criados
- `docs/TODO.md` — IMP-29 marcado `✅ CONCLUÍDO 2026-03-08`
- `CHANGELOG.md`, `docs/INDEX.md` — atualizados

**Resultado**: 307 testes passando (274 anteriores + 33 novos)

