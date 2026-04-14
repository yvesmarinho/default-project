# Template Versioning and Drift Detection Guide

## Overview

**IMP-65 Fase 1** introduced a template versioning system to prevent projects from missing upstream improvements to SpecKit workflow templates. This guide explains how to detect and understand template drift.

## The Problem

When you create a project with `scaffold.py new`, templates from `.specify/templates/` are copied to your project. However:

- **One-time copy**: Templates are copied only once during project creation
- **No automatic updates**: Future improvements to upstream templates don't reach existing projects
- **Risk of staleness**: Projects can drift from best practices over time

## The Solution: Template Versioning

Each SpecKit template now includes version metadata in YAML frontmatter:

```yaml
---
template_version: "1.0.0"
last_updated: "2026-04-14"
breaking_changes: false
---
```

This allows detection of outdated templates through the `check-templates` command.

---

## Command: `scaffold.py check-templates`

Scans your project's `.specify/templates/` directory and compares versions with the upstream a-default-project templates.

### Basic Usage

```bash
# Check templates in current directory
cd /path/to/your/project
python /path/to/a-default-project/scripts/scaffold.py check-templates

# Check templates in specific directory
python scripts/scaffold.py check-templates --target-dir /path/to/project
```

### Output Formats

#### Text Output (Default)

```
Template Drift Detection
  Upstream: /home/user/a-default-project/.specify/templates
  Local:    /home/user/my-project/.specify/templates
  Templates scanned: 6 upstream, 6 local

✅ All templates are up-to-date!
```

When drift is detected:

```
⚠️  Template Drift Detected: 2 template(s) need attention

📊 Outdated templates (1):
  • spec-template: 1.0.0 → 1.5.0

❌ Missing templates (1):
  • new-template: v1.0.0 (not found in project)

Run 'scaffold.py diff-template <name>' to see changes (Phase 2)
```

#### JSON Output

```bash
python scripts/scaffold.py check-templates --json
```

Output:

```json
{
  "drift_detected": true,
  "total_drifts": 2,
  "outdated_count": 1,
  "missing_count": 1,
  "breaking_changes": false,
  "templates": [
    {
      "name": "spec-template.md",
      "local_version": "1.0.0",
      "upstream_version": "1.5.0",
      "is_outdated": true,
      "is_missing": false,
      "breaking_changes": false
    },
    {
      "name": "new-template.md",
      "local_version": null,
      "upstream_version": "1.0.0",
      "is_outdated": false,
      "is_missing": true,
      "breaking_changes": false
    }
  ]
}
```

### Exit Codes

- **0**: All templates are up-to-date
- **1**: Drift detected (outdated or missing templates)
- **2**: Error during execution

Use in scripts:

```bash
if python scripts/scaffold.py check-templates; then
    echo "Templates are current"
else
    echo "Templates need attention"
fi
```

---

## Understanding Drift Types

### Outdated Templates

Template exists locally but is older than upstream version.

**Example:**
- Local: `spec-template.md` v1.0.0
- Upstream: `spec-template.md` v1.5.0

**Action**: Review changes and consider updating (Phase 3 will provide merge tools).

### Missing Templates

Template exists upstream but not in local project.

**Example:**
- Local: no `checklist-template.md`
- Upstream: `checklist-template.md` v1.0.0

**Action**: New workflow capability available — consider adding to project.

### Breaking Changes

Template update includes breaking changes that require manual intervention.

**Example:**
- Local: `plan-template.md` v1.5.0
- Upstream: `plan-template.md` v2.0.0 (breaking_changes: true)

**Action**: Carefully review changelog before updating.

---

## Version Tracking in `.scaffold-state.yaml`

When you create or update a project, template versions are tracked in `.scaffold-state.yaml`:

```yaml
scaffold_version: "1.0.0"
created_at: "2026-04-14T10:00:00Z"
updated_at: "2026-04-14T14:30:00Z"
project:
  name: my-api
  ...
template_versions:
  spec-template.md: "1.0.0"
  plan-template.md: "1.2.0"
  tasks-template.md: "1.0.0"
  agent-file-template.md: "1.0.0"
  checklist-template.md: "1.0.0"
  constitution-template.md: "1.0.0"
```

This enables:
- **Historical tracking**: Know what versions you started with
- **Audit trail**: Understand when templates were applied
- **Safe updates**: Check if custom modifications exist before applying upstream changes

---

## Automation and CI/CD

### Pre-commit Hook

Check for template drift before committing:

```bash
# .git/hooks/pre-commit
#!/bin/bash
if ! python scripts/scaffold.py check-templates; then
    echo "⚠️  Template drift detected. Run 'scaffold.py check-templates' for details."
    exit 1
fi
```

### GitHub Actions Workflow

```yaml
name: Check Template Drift
on: [push, pull_request]
jobs:
  check-templates:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Checkout a-default-project
        uses: actions/checkout@v3
        with:
          repository: your-org/a-default-project
          path: upstream-template
      - name: Check drift
        run: |
          cd upstream-template
          python scripts/scaffold.py check-templates --target-dir ../. --json > drift.json
          cat drift.json
      - name: Fail on drift
        run: |
          if jq -e '.drift_detected == true' drift.json; then
            echo "::error::Template drift detected"
            exit 1
          fi
```

---

## Command: `scaffold.py diff-template`

**IMP-65 Fase 2** — Shows detailed differences between local and upstream template versions.

### Basic Usage

```bash
# Show colored diff in terminal
python scripts/scaffold.py diff-template spec-template

# Export diff to markdown file
python scripts/scaffold.py diff-template spec-template --format markdown --output drift-report.md

# Generate HTML side-by-side diff
python scripts/scaffold.py diff-template spec-template --format html --output diff.html

# Check template in specific project directory
python scripts/scaffold.py diff-template plan-template --target-dir /path/to/project
```

### Output Formats

#### 1. Colored Terminal (Default)

```bash
python scripts/scaffold.py diff-template spec-template
```

Output:

```
Parsing template versions...
Generating diff for spec-template.md...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Template Diff: spec-template.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Metadata
  Local version:    1.0.0
  Upstream version: 1.5.0
  Outdated:         TRUE

📊 Statistics
  + 12 lines added
  - 2 lines removed
  ~ 5 lines modified
  ━━━━━━━━━━━━━━━━━
  Total: 19 changes

⚠️ Customizations Detected
  Your template has local modifications
  Review diff carefully before updating

🔍 Unified Diff
───────────────────────────────────────────────────
--- local/spec-template.md (1.0.0)
+++ upstream/spec-template.md (1.5.0)
@@ -15,6 +15,18 @@
 ## Overview
 Brief description of the feature.
 
+## Performance Criteria
+Define performance requirements:
+- Response time
+- Throughput
+- Resource usage
+
+## Security Considerations
+- Authentication requirements
+- Authorization model
+- Data encryption
+- Audit logging
+
 ## Technical Approach
 How will it be built?
───────────────────────────────────────────────────

💡 Impact Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Template:  spec-template.md
Versions:  1.0.0 → 1.5.0
Changes:   19 total (12 added, 2 removed, 5 modified)

⚠️ Customizations Detected
  Local template has custom modifications
  Manual review required before updating

Recommendations:
  1. Review diff above to understand upstream changes
  2. Identify which customizations to preserve
  3. Use Phase 3 merge command (when available) to combine changes
  4. Test thoroughly after applying updates
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### 2. Markdown Export

Perfect for documentation, PR reviews, and archival:

```bash
python scripts/scaffold.py diff-template spec-template --format markdown --output drift-analysis.md
```

Generates structured markdown:

```markdown
# Template Diff: spec-template.md

## Metadata
- **Template**: spec-template.md
- **Local Version**: 1.0.0
- **Upstream Version**: 1.5.0
- **Outdated**: TRUE
- **Customizations Detected**: TRUE

## Statistics
- Lines added: 12
- Lines removed: 2
- Lines modified: 5
- Total changes: 19

## Diff
\```diff
--- local/spec-template.md (1.0.0)
+++ upstream/spec-template.md (1.5.0)
@@ -15,6 +15,18 @@
 ## Overview
 Brief description of the feature.
 
+## Performance Criteria
+Define performance requirements:
+- Response time
+- Throughput
...
\```

## Impact Report
[Full impact analysis with recommendations]
```

#### 3. HTML Side-by-Side

Best for visual review:

```bash
python scripts/scaffold.py diff-template spec-template --format html --output review.html
```

Opens in browser showing color-coded side-by-side comparison.

### Use Cases

#### 1. Before Updating Template

```bash
# Check what changed in upstream
python scripts/scaffold.py diff-template spec-template

# If changes look good:
# (Phase 3 — coming soon)
# python scripts/scaffold.py merge-template spec-template
```

#### 2. Code Review Documentation

```bash
# Generate diff report for PR
python scripts/scaffold.py diff-template plan-template \
  --format markdown \
  --output docs/SESSIONS/2026-04-14/template-drift-review.md

# Commit to repository
git add docs/SESSIONS/2026-04-14/template-drift-review.md
git commit -m "docs: template drift analysis for plan-template"
```

#### 3. CI/CD Validation

```bash
# In CI pipeline
python scripts/scaffold.py diff-template spec-template --format markdown > drift.md

# Parse statistics from markdown
if grep -q "Total changes: 0" drift.md; then
  echo "✅ Template up-to-date"
else
  echo "⚠️ Template drift detected"
  cat drift.md >> $GITHUB_STEP_SUMMARY
fi
```

#### 4. Batch Analysis

```bash
# Check all templates
for template in spec-template plan-template tasks-template; do
  echo "Analyzing $template..."
  python scripts/scaffold.py diff-template $template \
    --format markdown \
    --output "drift-reports/${template}-diff.md"
done
```

### Customization Detection

The diff command uses heuristics to distinguish between:

1. **Upstream improvements**: New sections, updated guidance
2. **Your customizations**: Project-specific content you added

**Phase 2 Heuristic**: Compares local-only vs upstream-only content
**Phase 3 (Future)**: Three-way merge with base template tracking

### Integration with check-templates

Workflow pattern:

```bash
# 1. Detect drift
python scripts/scaffold.py check-templates

# Output:
# ⚠️ Template Drift Detected: 2 template(s) need attention
# 📊 Outdated templates (1):
#   • spec-template: 1.0.0 → 1.5.0

# 2. Analyze specific template
python scripts/scaffold.py diff-template spec-template

# 3. Export for review
python scripts/scaffold.py diff-template spec-template \
  --format markdown \
  --output docs/template-review.md

# 4. Merge changes (Phase 3)
# python scripts/scaffold.py merge-template spec-template --interactive
```

---

## Roadmap: Future Phases

### Phase 3: Three-Way Merge (IMP-65 Fase 3)

```bash
# Merge upstream changes while preserving customizations (coming soon)
python scripts/scaffold.py merge-template spec-template
python scripts/scaffold.py merge-template --all  # All templates
python scripts/scaffold.py merge-template --breaking  # Only breaking changes
```

Will provide:
- Automatic merging of non-conflicting changes
- Interactive conflict resolution
- Backup/rollback capability
- Custom modification preservation

### Phase 4: Automated Drift Monitoring (IMP-65 Fase 4)

- Weekly automated checks
- Slack/email notifications
- Dashboard with drift status across all projects
- Batch update tools

---

## Best Practices

1. **Check Regularly**: Run `check-templates` monthly or before major releases
2. **Track Versions**: Commit `.scaffold-state.yaml` to version control
3. **Review Before Updating**: Use JSON output to analyze drift programmatically
4. **Document Customizations**: Comment custom changes in templates for easier merging
5. **Test After Updates**: Run full test suite after applying template updates

---

## Troubleshooting

### "No templates found"

**Cause**: `.specify/templates/` directory missing or empty.

**Solution**: Ensure you're in a project created with scaffold.py and templates exist:

```bash
ls .specify/templates/
```

### "Version metadata missing"

**Cause**: Templates created before IMP-65 Fase 1 don't have frontmatter.

**Solution**: Templates will be treated as unversioned (v0.0.0 implied). Consider re-generating from latest upstream.

### "JSON parse error"

**Cause**: Template contains invalid YAML frontmatter.

**Solution**: Check template file for malformed YAML:

```bash
head -n 10 .specify/templates/spec-template.md
```

---

## See Also

- [IMP-65 Full Specification](TODO.md#imp-65) - Implementation plan for all 4 phases
- [TEMPLATE_USAGE.md](TEMPLATE_USAGE.md) - General template usage guide
- [SCAFFOLD_GUIDE.md](SCAFFOLD_GUIDE.md) - Complete scaffold.py reference
- [SpecKit Documentation](docs/copilot/) - Workflow automation guides
