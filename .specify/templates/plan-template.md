---
template_version: "1.2.0"
last_updated: "2026-04-23"
breaking_changes: false
---

# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context

<!--
  Capture the technical environment and constraints for this feature.
  Include language, frameworks, deployment target, and performance requirements.
-->

### Stack & Infrastructure

**Language/Version**: [e.g., Python 3.11, Swift 5.9, Rust 1.75 or NEEDS CLARIFICATION]
**Primary Dependencies**: [e.g., FastAPI, UIKit, LLVM or NEEDS CLARIFICATION]
**Database**: [if applicable, e.g., PostgreSQL 15, MongoDB 7, SQLite or N/A]
**Testing Framework**: [e.g., pytest, XCTest, cargo test or NEEDS CLARIFICATION]
**CI/CD Pipeline**: [e.g., GitHub Actions, GitLab CI, Jenkins or NEEDS CLARIFICATION]
**Target Platform**: [e.g., Linux server, iOS 15+, WASM, Docker or NEEDS CLARIFICATION]
**Project Type**: [e.g., library/cli/web-service/mobile-app/compiler/desktop-app or NEEDS CLARIFICATION]

### Performance & Scale

**Performance Goals**: [domain-specific, e.g., 1000 req/s, 10k lines/sec, 60 fps or NEEDS CLARIFICATION]
**Constraints**: [domain-specific, e.g., <200ms p95, <100MB memory, offline-capable or NEEDS CLARIFICATION]
**Scale/Scope**: [domain-specific, e.g., 10k users, 1M LOC, 50 screens or NEEDS CLARIFICATION]
**Monitoring**: [e.g., Prometheus, Datadog, Application Insights or NEEDS CLARIFICATION]

## Architecture Decision Records *(mandatory for architectural features)*

<!--
  DOCUMENT KEY ARCHITECTURAL DECISIONS using the ADR format:
  - Status (Proposed, Accepted, Deprecated, Superseded)
  - Context (why this decision is needed)
  - Decision (what we chose)
  - Rationale (why we chose it - trade-offs, constraints)
  - Consequences (positive/negative impacts)
  - Alternatives Considered (what we rejected and why)

  Reference decisions from objetivo.yaml → decisoes_iniciais if applicable.

  For non-architectural features (e.g., simple bug fixes, UI tweaks), you can skip this section
  or add a note: "No architectural decisions required for this feature."
-->

### ADR-001: [Decision Title]

**Status**: [Proposed | Accepted | Deprecated | Superseded]
**Date**: [YYYY-MM-DD]
**Context**: [What problem/question triggered this decision?]

**Decision**: [What did we decide?]

**Rationale**: [Why did we decide this? What trade-offs were considered?]

**Consequences**:
- ✅ **Positive**:
  - [Benefit 1 - e.g., "Reduces bundle size by 80%"]
  - [Benefit 2 - e.g., "Improves performance by 3x"]
- ⚠️ **Negative**:
  - [Limitation 1 - e.g., "Limited to keyword-based search"]
  - [Limitation 2 - e.g., "Requires manual index rebuild"]

**Alternatives Considered**:
1. **[Alternative A]**: [Why rejected - e.g., "Too complex for current needs"]
2. **[Alternative B]**: [Why rejected - e.g., "Requires external dependency (500MB+)"]

**Related Decisions**: [ADR-XXX, ADR-YYY or "None"]
**Supersedes**: [ADR-XXX if this replaces an earlier decision or "None"]
**Superseded by**: [ADR-XXX if this decision was later replaced or "None"]

---

**Example ADR** (from IMP-51 - Session Search System):

### ADR-001: SQLite FTS5 for Session Search

**Status**: ✅ Accepted
**Date**: 2026-04-05
**Context**: Need full-text search across session documentation (DAILY_ACTIVITIES, docs, specs)

**Decision**: Use SQLite FTS5 instead of embedding-based search (sentence-transformers)

**Rationale**:
- **Pragmatism**: Zero external dependencies (sentence-transformers = 500MB+ models)
- **Performance**: FTS5 meets requirements (<0.1s for complex queries)
- **Simplicity**: Porter stemming + Unicode61 sufficient for PT-BR/EN
- **Cost**: SQLite FTS5 is built-in, no infrastructure cost

**Consequences**:
- ✅ **Positive**:
  - Fast indexing (~1s for 100 blocks)
  - Small database (~100KB for 100 blocks)
  - Easy debugging (SQL queries are readable)
- ⚠️ **Negative**:
  - Limited semantic search (keyword-based, not similarity-based)
  - Queries with hyphens require quotes (e.g., `"IMP-50"`)

**Alternatives Considered**:
1. **sentence-transformers + FAISS**: Rejected due to 500MB+ model overhead
2. **Elasticsearch**: Rejected due to infrastructure complexity
3. **PostgreSQL pg_trgm**: Rejected because not built-in to Python

**Related Decisions**: None
**Supersedes**: None
**Superseded by**: None (may be revisited if semantic search becomes necessary)

---

[Add more ADRs as needed - number sequentially: ADR-002, ADR-003, etc.]

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

[Gates determined based on constitution file]

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
# [REMOVE IF UNUSED] Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [REMOVE IF UNUSED] Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# [REMOVE IF UNUSED] Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure: feature modules, UI flows, platform tests]
```

**Structure Decision**: [Document the selected structure and reference the real
directories captured above]

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
