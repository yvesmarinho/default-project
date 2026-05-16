# DEPRECATION NOTICE: test-scaffold.yml

**Date:** 2026-03-31
**Reason:** Workflow consolidation - functionality fully covered by ci-template.yml

## Analysis

`test-scaffold.yml` was a simplified workflow that:
- Ran pytest on Python 3.11 only
- Monitored: scripts/**, tests/**, pytest.ini
- No coverage collection
- Single job execution

## Replacement

All functionality is now handled by `.github/workflows/ci-template.yml` which provides:
- ✅ Test execution on Python 3.10, 3.11, 3.12 (matrix)
- ✅ Coverage collection and reporting
- ✅ Monitors same paths + additional (profile-descriptors, pyproject.toml, workflows)
- ✅ Additional jobs: cli-smoke, lint, integration
- ✅ Better CI/CD pipeline structure

## Impact

- **No functionality lost** - ci-template.yml is a superset
- **Reduced CI minutes** - no duplicate runs
- **Easier maintenance** - single workflow to update

## Migration

No action required. Existing PRs and pushes will automatically use ci-template.yml.

---

Ref: docs/SESSIONS/2026-03-31/ERROR_REPORT_2026-03-31.md - IMP-02
