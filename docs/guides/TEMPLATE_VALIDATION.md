# Template Validation Guide

**Version**: 1.0.0  
**Implementation**: IMP-65-LITE  
**Date**: 2026-04-28

---

## Overview

This guide covers **template validation** and **scaffold logging** for the Enterprise Default Project Template. These tools ensure templates are valid before scaffold and maintain a history of all projects created.

**Components**:
- `scripts/validate-templates.py` — Validate `.specify/templates/`
- `scripts/scaffold_logger.py` — Log scaffold operations
- `scripts/scaffold-query.py` — Query scaffold history
- `logs/scaffolds.yaml` — Scaffold history database

---

## Template Validation

### Purpose

Validate all templates in `.specify/templates/` before scaffold to catch:
- YAML/JSON syntax errors
- Missing required frontmatter fields
- Broken links
- Invalid variable patterns

### Usage

**Basic validation**:
```bash
make validate-templates
# OR
python scripts/validate-templates.py
```

**Validate specific template**:
```bash
python scripts/validate-templates.py --template spec
# Only validates templates matching "spec" (e.g., spec-template.md)
```

**JSON output (for CI/CD)**:
```bash
python scripts/validate-templates.py --json
```

**Strict mode (fail on warnings)**:
```bash
python scripts/validate-templates.py --strict
# Exit code 2 if warnings found
```

### Validation Checks

#### 1. YAML/JSON Syntax

Validates syntax of all `.yaml` and `.json` files:

```yaml
# ✅ Valid YAML
feature:
  id: "001"
  name: "Test"

# ❌ Invalid YAML (indentation error)
feature:
id: "001"  # Bad indentation
  name: "Test"
```

#### 2. Markdown Frontmatter

Checks for required fields in Markdown frontmatter:

```markdown
---
template_version: "2.2.0"    # ✅ Required field present
last_updated: "2026-04-28"
breaking_changes: false
---

# Template Content
```

**Required fields**:
- `template_version` — Semver format (x.y.z)

**Optional but recommended**:
- `last_updated` — ISO date
- `breaking_changes` — Boolean
- `breaking_change_notes` or `breaking_reason` — Required if `breaking_changes: true`

#### 3. Link Validation

Checks Markdown links point to existing files:

```markdown
✅ [Valid link](./objective.yaml)           # File exists
✅ [External link](https://example.com)     # External links OK
❌ [Broken link](./missing.yaml)            # File doesn't exist
```

**Note**: Links in templates may reference files that only exist after scaffold (e.g., `./objetivo.yaml`). These warnings are expected.

#### 4. Variable Validation

Checks variable placeholder format:

```markdown
✅ ${PROJECT_NAME}              # Correct uppercase
✅ $PROJECT_NAME                # Also valid
✅ [PROJECT_NAME]               # Also valid
⚠️  ${project_name}              # Warning: should be uppercase
```

**Convention**: Use `UPPERCASE_SNAKE_CASE` for variables.

### Output

**Console output**:
```
======================================================================
TEMPLATE VALIDATION RESULTS
======================================================================
Files checked: 7

⚠️  WARNINGS (1):
----------------------------------------------------------------------
  .specify/templates/spec-template.md:13
    Broken link: [objetivo.yaml](./objetivo.yaml)
    Details: Target file not found: ...

======================================================================
✅ PASSED (with warnings)
======================================================================
```

**JSON output**:
```json
{
  "success": true,
  "files_checked": 7,
  "errors": [],
  "warnings": [
    {
      "severity": "warning",
      "file": ".specify/templates/spec-template.md",
      "line": 13,
      "message": "Broken link: [objetivo.yaml](./objetivo.yaml)",
      "details": "Target file not found: ..."
    }
  ]
}
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All validations passed |
| 1 | Validation errors found |
| 2 | Warnings found (only with `--strict`) |

### Integration

**Pre-commit hook** (`.pre-commit-config.yaml`):
```yaml
repos:
  - repo: local
    hooks:
      - id: validate-templates
        name: Validate .specify/templates/
        entry: python scripts/validate-templates.py
        language: system
        pass_filenames: false
        always_run: true
```

**GitHub Actions** (`.github/workflows/validate-templates.yml`):
```yaml
name: Validate Templates
on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install pyyaml
      - run: python scripts/validate-templates.py
```

---

## Scaffold Logging

### Purpose

Maintain a historical log of all projects created from this template for:
- Tracking template usage
- Identifying popular profiles
- Auditing project creation
- Analyzing template adoption

### How It Works

**Automatic logging**:
When you create a new project via `scaffold.py`, it automatically logs:
- Project name
- Template version used
- Profile applied
- User who created it
- Path where created
- Timestamp
- Success status

**Log file**: `logs/scaffolds.yaml`

**Example log entry**:
```yaml
scaffolds:
  - id: 1
    timestamp: "2026-04-28T14:30:00Z"
    project_name: "vya-api-users"
    template_version: "2.2.0"
    profile: "python-fastapi"
    created_by: "yves_marinho"
    path: "/home/yves/projects/vya-api-users"
    success: true
    error_message: null
    metadata: {}
```

### Querying Scaffold History

**List recent scaffolds**:
```bash
python scripts/scaffold-query.py --last 30d
python scripts/scaffold-query.py --limit 10
```

**Filter by criteria**:
```bash
# By profile
python scripts/scaffold-query.py --profile python-fastapi

# By user
python scripts/scaffold-query.py --user yves_marinho

# By project name (supports wildcard)
python scripts/scaffold-query.py --project "vya-*"

# Only successful scaffolds
python scripts/scaffold-query.py --success

# Only failed scaffolds
python scripts/scaffold-query.py --failed
```

**Statistics**:
```bash
python scripts/scaffold-query.py --stats
```

Example output:
```
======================================================================
SCAFFOLD STATISTICS
======================================================================
Total scaffolds: 15
Success rate: 93.3%
Recent activity (30 days): 5

By Profile:
  python-fastapi                          8
  typescript-next                         4
  terraform-aws                           3

By User:
  yves_marinho                           12
  other_user                              3
======================================================================
```

**Export to CSV**:
```bash
python scripts/scaffold-query.py --export scaffolds.csv
```

**JSON output**:
```bash
python scripts/scaffold-query.py --json --limit 5
```

### Query Options

| Option | Description | Example |
|--------|-------------|---------|
| `--project NAME` | Filter by project name (wildcard `*` supported) | `--project "vya-*"` |
| `--profile PROFILE` | Filter by profile | `--profile python-fastapi` |
| `--user USER` | Filter by user | `--user yves_marinho` |
| `--success` | Show only successful scaffolds | `--success` |
| `--failed` | Show only failed scaffolds | `--failed` |
| `--last PERIOD` | Last N days/weeks/months | `--last 30d`, `--last 2w` |
| `--limit N` | Limit results | `--limit 10` |
| `--stats` | Show statistics | `--stats` |
| `--export FILE` | Export to CSV | `--export scaffolds.csv` |
| `--json` | Output as JSON | `--json` |

---

## Common Workflows

### Before Creating New Project

**Validate templates**:
```bash
make validate-templates
# OR
python scripts/validate-templates.py
```

If validation fails, fix errors before scaffold.

### After Improving Templates

**Re-validate**:
```bash
python scripts/validate-templates.py
```

**Commit with validation**:
```bash
make validate-templates && git add .specify/templates/ && git commit -m "feat(templates): improve spec template"
```

### Analyzing Template Usage

**Which profiles are most popular?**
```bash
python scripts/scaffold-query.py --stats
```

**How many projects created this month?**
```bash
python scripts/scaffold-query.py --last 30d
```

**Find all Python FastAPI projects**:
```bash
python scripts/scaffold-query.py --profile python-fastapi
```

**Export for analysis**:
```bash
python scripts/scaffold-query.py --export /tmp/scaffolds.csv
# Open in Excel/Google Sheets for analysis
```

---

## Troubleshooting

### Validation Fails with "YAML syntax error"

**Problem**: Template has invalid YAML.

**Solution**: Check indentation and quotes:
```yaml
# ❌ Bad
feature:
id: "001"  # Wrong indentation

# ✅ Good
feature:
  id: "001"
```

### Validation Warns "Broken link"

**Problem**: Link points to non-existent file.

**Solution**:
- If link is correct but file created during scaffold, ignore warning
- If link is broken, fix it

### Scaffold Logger Not Working

**Problem**: `logs/scaffolds.yaml` not updated after scaffold.

**Solution**:
1. Check file permissions: `ls -la logs/scaffolds.yaml`
2. Verify integration: `grep scaffold_logger scripts/lib/flows/new_project.py`
3. Check for errors in scaffold output

### Query Returns No Results

**Problem**: No scaffolds match filter criteria.

**Solution**:
1. List all scaffolds: `python scripts/scaffold-query.py --limit 100`
2. Check filter syntax: `--project "vya-*"` (with quotes)
3. Verify log file exists: `cat logs/scaffolds.yaml`

---

## Best Practices

### Template Validation

✅ **DO**:
- Run `make validate-templates` before committing template changes
- Add pre-commit hook for automatic validation
- Use `--strict` mode in CI/CD
- Fix errors immediately (don't ignore)

❌ **DON'T**:
- Commit templates without validation
- Ignore validation warnings
- Disable validation checks

### Scaffold Logging

✅ **DO**:
- Keep `logs/scaffolds.yaml` in version control
- Export to CSV periodically for backup
- Review statistics monthly

❌ **DON'T**:
- Delete `logs/scaffolds.yaml` (historical data)
- Manually edit log file (corruption risk)
- Store sensitive data in log (e.g., credentials)

---

## Performance

### Validation

- **7 templates**: ~0.1s
- **50 templates**: ~1s
- **Bottleneck**: Link validation (file I/O)

### Logging

- **Write**: ~1ms per scaffold
- **Query**: <1ms (100 entries), ~10ms (1000 entries)
- **Bottleneck**: YAML serialization (for 1000+ entries, consider JSON)

---

## Next Steps

- **P2 Enhancement**: Add email notifications for failed scaffolds
- **P2 Enhancement**: Dashboard for scaffold analytics
- **P2 Enhancement**: Integration with project tracking system

---

## References

- **IMP-65-LITE Spec**: [specs/065-template-validation-lite/spec.md](../../specs/065-template-validation-lite/spec.md)
- **POC Learnings**: [docs/reference/POC-LEARNINGS.md](../reference/POC-LEARNINGS.md) (when CI/CD makes sense)
- **POC-1 to POC-4**: [poc/imp65-p1-validation/](../../poc/imp65-p1-validation/) (reference implementation)
