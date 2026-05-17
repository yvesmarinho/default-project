# IMP-65 Scenario 3 — Breaking Change Update

**Session**: 2026-04-23
**Scenario**: Breaking Change Update (Major Version with Deprecation)
**Priority**: P0
**Status**: ⚠️ COMPLETED WITH ISSUE

---

## ⚠️ Critical Issue Discovered

**Issue ID**: BUG-04
**Severity**: P1 (High)
**Component**: Template Merge - Breaking Change Validation

**Description**: The `merge-template --auto` command does NOT block breaking changes. Users can apply major version updates with `--auto` flag without explicitly acknowledging breaking changes using `--breaking-ok`.

**Expected Behavior**: Auto-merge should be rejected when breaking_changes: true, requiring explicit --breaking-ok flag.

**Actual Behavior**: Auto-merge succeeds even with breaking_changes: true.

**Impact**: Users may unknowingly apply breaking changes without reviewing migration notes, potentially breaking existing project files.

**Evidence**:
```bash
# Command executed
python3 ../../scripts/scaffold.py merge-template spec-template --auto

# Output (INCORRECT - should fail)
Merging template: spec-template.md...
Parsing template versions...
  Local version:    1.6.0
  Upstream version: 2.0.0
  Base version:     1.6.0

Performing three-way merge...
✅ Merge completed cleanly (no conflicts)
✅ Merge applied successfully
```

**Expected Output**:
```bash
🚨 BREAKING CHANGE DETECTED
⚠️  Auto-merge blocked for breaking changes
To proceed, use --breaking-ok flag
```

**Recommendation**: Add breaking change validation to merge-template before three-way merge execution.

---

## Objective

Validate that the template synchronization system correctly handles breaking changes, requiring explicit user approval before applying updates that remove or substantially change existing sections.

---

## Test Setup

### Initial State

- **Upstream Template**: `.specify/templates/spec-template.md` v1.6.0
- **Local Template**: `poc/tst-python-fastapi/.specify/templates/spec-template.md` v1.6.0
- **Baseline**: Both synchronized (from Scenario 2)

### Modifications to Create Breaking Change

**Breaking Change Scenario**:
- Add deprecated section to baseline (simulate old template)
- Remove deprecated section in upstream v2.0.0
- Mark breaking_changes: true in frontmatter

#### Step 1: Add Deprecated Section to Local (Simulate Old Version)

Revert local template to include a deprecated section that will be removed in v2.0.0:

```markdown
## Deprecated Section (removed in v2.0)

<!--
  This section is deprecated and will be removed in future versions.
  Use "Performance Criteria" section instead.
-->

### Legacy Performance Notes

- Performance targets should be documented in the new Performance Criteria section
- This section exists for backward compatibility only
- Migration: Move all content to Performance Criteria section above
```

#### Step 2: Mark Upstream as v2.0.0 with Breaking Changes

Update upstream template frontmatter:

```yaml
---
template_version: "2.0.0"
last_updated: "2026-04-23"
breaking_changes: true
breaking_change_notes: |
  - Removed deprecated "Legacy Performance Notes" section
  - All performance requirements must now use "Performance Criteria" section
  - Migration: Review existing specs and move legacy content to new section
---
```

Remove the deprecated section from upstream template.

---

## Test Execution

### Phase 1: Setup Breaking Change

**Steps**:
1. ⏳ Revert local to v1.6.0 with deprecated section
2. ⏳ Update upstream to v2.0.0 (breaking_changes: true)
3. ⏳ Remove deprecated section from upstream
4. ⏳ Add breaking_change_notes to upstream frontmatter

### Phase 2: Detect Breaking Change

**Command**: `check-templates` from poc/tst-python-fastapi/
**Expected Output**:
```
⚠️ Template Drift Detected: 1 template(s) need attention

🚨 Breaking changes detected (1):
  • spec-template.md: 1.6.0 → 2.0.0 (BREAKING)
    ⚠️  Review changes carefully before updating

📋 Breaking change notes:
  - Removed deprecated "Legacy Performance Notes" section
  - All performance requirements must now use "Performance Criteria" section
  - Migration: Review existing specs and move legacy content to new section

Run 'scaffold.py diff-template <name>' to see changes (Phase 2)
```

### Phase 3: Review Diff

**Command**: `diff-template spec-template`
**Expected Behavior**:
- Diff clearly shows section removal
- Breaking change warning highlighted
- Migration guidance displayed

**Expected Output**:
```
================================================================================
Template Diff: spec-template.md
================================================================================

Versions:
  Local:    1.6.0
  Upstream: 2.0.0

🚨 BREAKING CHANGE
  breaking_changes: true

Breaking change notes:
  - Removed deprecated "Legacy Performance Notes" section
  - All performance requirements must now use "Performance Criteria" section
  - Migration: Review existing specs and move legacy content to new section

Changes:
  +2 lines added (frontmatter)
  -12 lines removed (deprecated section)
  ~2 lines modified

⚠️  This update may require manual intervention
   Review carefully before applying

Diff:
--------------------------------------------------------------------------------
--- local/spec-template.md
+++ upstream/spec-template.md
@@ -1,6 +1,6 @@
 ---
-template_version: "1.6.0"
+template_version: "2.0.0"
 last_updated: "2026-04-23"
-breaking_changes: false
+breaking_changes: true
 ---

@@ -70,18 +70,6 @@
 - **Storage**: Data growth < [X]GB per month

----
-
-## Deprecated Section (removed in v2.0)
-
-<!--
-  This section is deprecated and will be removed in future versions.
-  Use "Performance Criteria" section instead.
-->
-
-### Legacy Performance Notes
-
-- Performance targets should be documented in the new Performance Criteria section
-- This section exists for backward compatibility only
-
 ---

 ## User Scenarios & Testing *(mandatory)*
--------------------------------------------------------------------------------
```

### Phase 4: Attempt Auto-Merge

**Command**: `merge-template spec-template --auto`
**Expected Behavior**:
- ❌ Auto-merge blocked due to breaking change
- Clear warning message displayed
- Guidance on using --breaking-ok or --force flag
- Migration notes shown

**Expected Output**:
```
Merging template: spec-template.md...
Parsing template versions...
  Local version:    1.6.0
  Upstream version: 2.0.0
  Base version:     1.6.0

🚨 BREAKING CHANGE DETECTED

This update includes breaking changes that may affect existing content.

Breaking change notes:
  - Removed deprecated "Legacy Performance Notes" section
  - All performance requirements must now use "Performance Criteria" section
  - Migration: Review existing specs and move legacy content to new section

⚠️  Auto-merge blocked for breaking changes

To proceed, you must explicitly approve:
  --breaking-ok     Acknowledge breaking changes and proceed
  --force           Force merge (USE WITH CAUTION)
  --dry-run         Preview merge without applying

Example:
  scaffold.py merge-template spec-template --breaking-ok

Abort: Breaking change requires explicit approval
```

### Phase 5: Approve Breaking Change

**Command**: `merge-template spec-template --breaking-ok`
**Expected Behavior**:
- Merge proceeds with explicit approval
- Deprecated section removed
- Version updated to 2.0.0
- Backup created
- Migration notes logged

**Expected Output**:
```
Merging template: spec-template.md...
Parsing template versions...
  Local version:    1.6.0
  Upstream version: 2.0.0
  Base version:     1.6.0

🚨 Breaking change approved (--breaking-ok)

Performing three-way merge...
✅ Merge completed cleanly (no conflicts)

Changes applied:
  - Removed deprecated section (12 lines)
  - Updated version: 1.6.0 → 2.0.0
  - Updated breaking_changes flag: false → true

✅ Merge applied successfully
  Backup: spec-template.backup-20260423-HHMMSS.md
  Updated: spec-template.md
  Version: 1.6.0 → 2.0.0

⚠️  Post-merge action required:
  Review existing spec files for deprecated "Legacy Performance Notes"
  Migrate content to "Performance Criteria" section
```

### Phase 6: Validate Result

**Verification Commands**:
```bash
# 1. Deprecated section removed
grep -A5 "Deprecated Section" .specify/templates/spec-template.md
# Expected: No output (section removed)

grep -A5 "Legacy Performance Notes" .specify/templates/spec-template.md
# Expected: No output (section removed)

# 2. Version updated
grep "template_version:" .specify/templates/spec-template.md
# Expected: "2.0.0"

grep "breaking_changes:" .specify/templates/spec-template.md
# Expected: "true"

# 3. Backup created
ls -la .specify/templates/*.backup-* | tail -1
# Expected: New backup with timestamp

# 4. No drift remaining
python3 ../../scripts/scaffold.py check-templates
# Expected: ✅ All templates up-to-date
```

---

## Expected vs Actual Results

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| Breaking Change Flag | ✅ Detected by check-templates | ✅ PASS | 🔴 BREAKING displayed |
| Breaking Change Notes | ✅ Shown in check-templates | ✅ PASS | Notes displayed in frontmatter |
| Diff Shows Removal | ✅ Deprecated section highlighted | ✅ PASS | 13 lines removed clearly shown |
| Auto-merge Blocked | ❌ Blocked with clear message | ❌ **FAIL** | **BUG-04: Auto-merge NOT blocked** |
| --breaking-ok Flag | ✅ Required for approval | ❌ **FAIL** | **BUG-04: Flag not validated** |
| Merge with Approval | ✅ Succeeds with flag | ✅ PASS | Merge succeeded (but --auto shouldn't) |
| Deprecated Section Removed | ✅ Section no longer present | ✅ PASS | grep count = 0 |
| Version Update | ✅ 1.6.0 → 2.0.0 | ✅ PASS | template_version: "2.0.0" |
| breaking_changes Flag | ✅ Set to true | ✅ PASS | breaking_changes: true |
| Backup Created | ✅ Timestamp backup | ✅ PASS | spec-template.backup-20260423-113144.md |
| No Drift Remaining | ✅ Check passes | ✅ PASS | ✅ All templates up-to-date |

---

## Issues Encountered

### Issue Log

#### 1. Base State Configuration Challenge
**Phase**: Setup
**Time**: 11:05-11:23 (18 min)
**Issue**: Initial test execution didn't properly configure the three-way merge base. The deprecated section existed in both local and upstream initially, causing merge to keep it.

**Root Cause**: Scenario required:
- Base v1.6.0 WITH deprecated section
- Local v1.6.0 WITH deprecated section (unchanged from base)
- Upstream v2.0.0 WITHOUT deprecated section (removed from base)

Initial setup had upstream still containing the section.

**Resolution**:
1. Removed deprecated section from upstream template
2. Restored local from backup
3. Manually updated .scaffold-state.yaml base to v1.6.0 with deprecated section
4. Re-executed merge successfully

**Lesson Learned**: Three-way merge requires careful base state management. The base must represent the common ancestor state for proper merge behavior.

---

#### 2. BUG-04: Auto-merge Not Blocked for Breaking Changes ⚠️

**Phase**: Auto-merge Block Test
**Time**: 11:31 (2 min)
**Severity**: P1 (High)

**Issue**: `merge-template --auto` accepts breaking changes without requiring `--breaking-ok` flag.

**Expected Behavior**:
```bash
python3 scaffold.py merge-template spec-template --auto

🚨 BREAKING CHANGE DETECTED
⚠️  Auto-merge blocked for breaking changes
To proceed, use --breaking-ok flag
```

**Actual Behavior**:
```bash
python3 scaffold.py merge-template spec-template --auto

Performing three-way merge...
✅ Merge completed cleanly (no conflicts)
✅ Merge applied successfully
```

**Impact**:
- Users can unknowingly apply breaking changes
- Migration notes may be ignored
- Existing project files may break without warning

**Validation Commands**:
```bash
# Breaking change IS detected
python3 scaffold.py check-templates
# Output: spec-template.md: 1.6.0 → 2.0.0 🔴 BREAKING ✅

# Breaking change IS shown in diff
python3 scaffold.py diff-template spec-template
# Output: Shows removal, breaking_change_notes ✅

# But auto-merge is NOT blocked
python3 scaffold.py merge-template spec-template --auto
# Output: ✅ Merge completed cleanly ❌ SHOULD FAIL
```

**Recommendation**: Add validation in `merge-template` flow:
```python
# In merge-template command before three-way merge:
if upstream_version.breaking_changes and not args.breaking_ok:
    ui.error("🚨 BREAKING CHANGE DETECTED")
    ui.info(upstream_version.breaking_change_notes)
    ui.error("⚠️  Auto-merge blocked for breaking changes")
    ui.info("To proceed, use --breaking-ok flag")
    return 1
```

**Follow-up Required**:
- [ ] Create BUG-04 branch
- [ ] Implement breaking change validation
- [ ] Add test case for blocking behavior
- [ ] Verify --breaking-ok flag works
- [ ] Re-run Scenario 3 after fix

---

## Success Criteria

- [x] **SC-1**: Breaking change warning displayed in check-templates ✅
- [x] **SC-2**: Breaking change notes clearly shown ✅
- [ ] **SC-3**: Auto-merge blocked without explicit approval ❌ **BUG-04**
- [ ] **SC-4**: --breaking-ok flag required to proceed ❌ **BUG-04**
- [x] **SC-5**: Diff clearly shows removed section ✅
- [x] **SC-6**: Migration guidance provided ✅
- [x] **SC-7**: Merge succeeds with --breaking-ok flag ✅ (worked but shouldn't need flag)
- [x] **SC-8**: Deprecated section completely removed ✅
- [x] **SC-9**: Version and breaking_changes flag updated correctly ✅
- [x] **SC-10**: Backup created before merge ✅

**Result**: 8/10 criteria passed (2 failures due to BUG-04)

---

## Time Tracking

| Phase | Estimated | Actual | Notes |
|-------|-----------|--------|-------|
| Setup | 10 min | 18 min | Multiple iterations to fix base state |
| Detection | 2 min | 2 min | check-templates worked perfectly |
| Diff Review | 3 min | 3 min | diff-template showed clear removal |
| Auto-merge Block Test | 2 min | 2 min | **BUG-04 discovered** |
| Approval and Merge | 3 min | 3 min | Merge worked (incorrectly allowed) |
| Validation | 5 min | 5 min | All checks passed |
| Documentation | 10 min | 5 min | Report update |
| **Total** | **35 min** | **38 min** | +3 min due to base state debugging |

---

## Next Steps

After Scenario 3 completion:
1. ✅ Mark Scenario 3 complete in TODO.md
2. ✅ Update session summary
3. ➡️ Proceed to Scenario 4: Multiple Template Updates

---

**Report Created**: 2026-04-23 11:05
**Last Updated**: 2026-04-23 11:43
**Status**: ⚠️ COMPLETED WITH ISSUE (BUG-04 discovered)
