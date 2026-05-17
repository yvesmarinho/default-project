# IMP-65 Multi-Perspective Debate — Real-World Test Strategy

**Session**: 2026-04-21
**Agent**: template-architect
**Mode**: debate
**Participants**: 4 perspectives (Architecture, DevEx, Security, Governance)

---

## Proposta: Execute Real-World Template Update Test on Existing Project

**Context**: IMP-65 Phase 4 is complete with 151 tests, but has never been tested on a real existing project with customizations. We need to validate that the template update system works as designed in production scenarios.

**Proposed Test Plan**:

1. **Setup Test Project** (30 min)
   - Clone or create project with python-fastapi profile
   - Add realistic customizations to templates:
     - Custom security checklist in spec-template
     - Project-specific deployment steps in plan-template
     - Custom task categories in tasks-template
   - Commit baseline state

2. **Simulate Upstream Update** (15 min)
   - Create "upstream" template updates:
     - Add new sections (e.g., "Performance Criteria")
     - Update existing sections (e.g., expand "Technical Approach")
     - Modify frontmatter (version bump to 1.5.0)

3. **Execute Update Workflow** (45 min)
   - Run `scaffold.py check-templates`
   - Run `scaffold.py diff-template` for each outdated template
   - Run `scaffold.py merge-template --auto` for clean merges
   - Run `scaffold.py merge-template --interactive` for conflicts
   - Document all output, errors, warnings

4. **Validation** (60 min)
   - Verify customizations preserved
   - Verify new upstream sections added
   - Verify `.scaffold-state.yaml` updated correctly
   - Run project build/test suite
   - Check for regressions
   - Document edge cases

5. **Report & Improve** (30 min)
   - Write test report with findings
   - Create regression tests for issues
   - Update documentation
   - Recommend improvements

**Total Time**: 3 hours

---

## 🏛️ Perspectiva 1 — Arquitetura/Core

### Vantagens

✅ **Validates Core Design Assumptions**
- Tests whether three-way merge correctly preserves customizations
- Validates version comparison logic in real scenario
- Confirms `.scaffold-state.yaml` tracking works as designed

✅ **Exposes Edge Cases**
- Real customizations may have patterns we didn't anticipate
- Conflict resolution may encounter scenarios not covered in unit tests
- State tracking may have gaps not visible in isolated tests

✅ **Proves Agnostic Separation**
- If test works with python-fastapi, proves profile independence
- Confirms core doesn't leak profile-specific logic
- Validates contract between core and profiles

### Riscos

⚠️ **May Discover Fundamental Issues**
- If three-way merge fails to preserve customizations → Core logic bug
- If state tracking is incorrect → Need to redesign tracking mechanism
- If version comparison mishandles edge cases → Breaking change needed

⚠️ **Test Environment Mismatch**
- Test project may not represent real production patterns
- Customizations may be too simple/complex compared to reality
- Single profile test may miss multi-profile interactions

### Restrições para o Core

**Non-Negotiables That Must Hold**:

1. **Customizations MUST be preserved** — Any loss = critical failure
2. **State tracking MUST be accurate** — Wrong versions = system broken
3. **Merge MUST be deterministic** — Same inputs = same output
4. **Backups MUST be created** — No backup = data loss risk

**Acceptable Failures**:
- Sub-optimal conflict markers (can improve UX)
- Missing progress indicators (DevEx issue, not correctness)
- No automated changelog (nice-to-have)

**Unacceptable Failures**:
- Silent overwrite of customizations
- Incorrect version tracking
- Merge produces different output on retry
- No backup created before destructive operation

### Arquitetura — Recomendações

1. **Pre-Test**: Create comprehensive test fixtures
   ```python
   # tests/fixtures/real_world_project/
   ├── .specify/templates/  # With realistic customizations
   ├── .scaffold-state.yaml # Proper version tracking
   └── src/                  # Working code that can build/test
   ```

2. **During Test**: Instrument with detailed logging
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)  # Capture all operations
   ```

3. **Post-Test**: Create regression tests from findings
   ```python
   # For each edge case discovered:
   def test_real_world_edge_case_N():
       """Regression test for edge case found in real-world test."""
       # Reproduce issue
       # Assert correct behavior
   ```

---

## 🖥️ Perspectiva 2 — DevEx/UX

### Impacto na Experiência

✅ **Validates User Workflow**
- Tests actual command sequence a developer would use
- Validates error messages are helpful in context
- Confirms documentation matches reality

✅ **Measures Real Metrics**
- Time to complete update (target: < 5 min)
- Number of manual steps required
- Clarity of conflict resolution prompts
- Effort to verify success

✅ **Identifies UX Gaps**
- Missing progress indicators become obvious
- Confusing error messages stand out
- Documentation gaps are exposed

### Riscos UX

⚠️ **May Reveal Poor DevEx**
- If process takes > 10 minutes → Too slow for adoption
- If conflicts are confusing → Users will avoid updates
- If verification is unclear → Users won't trust system

⚠️ **Documentation May Be Insufficient**
- Written docs may not match actual experience
- Missing troubleshooting for common errors
- No runbook for production scenarios

### Ergonomia e Automação

**Current State Assessment**:

| UX Aspect | Current | After Test | Gap |
|-----------|---------|------------|-----|
| Time to update | ❓ Unknown | ✅ Measured | Need benchmark |
| Steps required | ❓ Unknown | ✅ Counted | Need reduction |
| Error clarity | ❓ Assumed good | ✅ Validated | Need examples |
| Documentation accuracy | ❓ Untested | ✅ Verified | Need updates |

**DevEx Metrics to Capture**:

1. **Efficiency**:
   - Total time for complete update
   - Time spent on manual conflict resolution
   - Time spent on verification

2. **Clarity**:
   - Were errors self-explanatory?
   - Were next steps obvious?
   - Was success confirmation clear?

3. **Confidence**:
   - Did backup make user feel safe?
   - Was dry-run preview helpful?
   - Were changes reviewable before apply?

### DevEx — Recomendações

1. **Capture Screen Recording**
   - Record entire test session
   - Review for confusion points
   - Identify where user hesitates

2. **Think-Aloud Protocol**
   - Narrate thought process during test
   - Note questions that arise
   - Document assumptions made

3. **Stopwatch Measurements**
   - Time each command
   - Time conflict resolution
   - Time verification steps

4. **Exit Survey**
   ```markdown
   Rate 1-10:
   - How confident are you the update succeeded?
   - How clear were error messages?
   - How easy was conflict resolution?
   - Would you recommend this workflow?
   ```

---

## 🔒 Perspectiva 3 — Segurança

### Riscos de Segurança Introduzidos

✅ **Positive Security Implications**
- Real-world test validates backup safety net works
- Confirms no silent overwrites that could delete security policies
- Tests conflict detection for security-critical sections

⚠️ **Security Risks to Test**

**1. Customization Loss Risk**
```markdown
# Scenario: Project has custom security review section
## Security Review
- [ ] Custom AppSec checklist
- [ ] Threat model reviewed
- [ ] Pen-test completed

# If merge overwrites this → Security policy deleted
```

**Test**: Verify custom security sections are preserved.

**2. Conflict Resolution Security**
```markdown
# Scenario: Conflict in security section
<<<<<<< LOCAL
- [ ] Authentication: OAuth2 + MFA required
=======
- [ ] Authentication: Basic auth supported
>>>>>>> UPSTREAM

# User must choose OAuth2 (more secure)
```

**Test**: Ensure conflict markers clearly show security implications.

**3. Breaking Change Safety**
```yaml
---
template_version: "2.0.0"
breaking_changes: true  # Removes deprecated security checks
---
```

**Test**: Confirm breaking changes require explicit approval.

### Baseline de Segurança Afetada

**Security Baselines to Validate**:

1. **Backup Integrity**
   - Are backups created before every destructive operation?
   - Are backups immutable (not overwritten)?
   - Can backups be restored reliably?

2. **Audit Trail**
   - Is update activity logged? (Currently: NO ❌)
   - Can we trace who updated what? (Currently: NO ❌)
   - Can we replay/verify updates? (Currently: NO ❌)

3. **Access Control**
   - Who can trigger template updates? (Currently: Anyone with file access)
   - Should breaking changes require approval? (Currently: NO ❌)

### Segurança — Recomendações

1. **Test Security-Critical Customizations**
   ```markdown
   Add to test project:
   - Custom authentication requirements
   - Custom authorization policies
   - Custom encryption standards
   - Custom audit logging requirements
   ```

2. **Validate No Security Regression**
   ```bash
   # Before update
   grep -r "OAuth2" .specify/templates/

   # After update
   grep -r "OAuth2" .specify/templates/
   # → Must still exist
   ```

3. **Document Security Update Workflow**
   ```markdown
   # For security-critical templates:
   1. Requires security team review
   2. Requires approval in ticket
   3. Must run on staging first
   4. Requires post-update security scan
   ```

4. **Implement Audit Logging** (Post-Test Action)
   ```yaml
   # .scaffold-audit.yaml (to be implemented)
   updates:
     - timestamp: "2026-04-21T10:00:00Z"
       user: "yves_marinho"
       template: "spec-template.md"
       old_version: "1.0.0"
       new_version: "1.5.0"
       conflicts: 0
       justification: "IMP-65 testing"
   ```

---

## 📦 Perspectiva 4 — Governança

### Versionamento e Compatibilidade

✅ **Validates Version Tracking**
- Tests semantic version comparison works correctly
- Confirms `.scaffold-state.yaml` is updated properly
- Validates base template storage for three-way merge

✅ **Tests Compatibility Matrix**
- If python-fastapi v2.0 requires spec-template v1.5+
- Validate that check detects incompatibility
- Validate that merge applies required changes

### Manutenibilidade

✅ **Real-World Validation Improves Maintainability**
- Documented edge cases help future maintainers
- Regression tests prevent regressions
- Real-world examples improve documentation

⚠️ **May Expose Maintenance Burden**
- If manual conflict resolution is common → High maintenance
- If updates frequently break builds → Adoption risk
- If documentation is wrong → Maintenance debt

### Migração

**Critical Test for Migration**:

The test project should simulate a **pre-IMP-65 project** (no version metadata) to validate migration path:

```yaml
# Initial state (pre-IMP-65):
# - Templates have no frontmatter
# - .scaffold-state.yaml has no template_versions
# - No template_bases stored

# After migration:
# - Frontmatter added to all templates
# - .scaffold-state.yaml populated
# - template_bases populated for future merges
```

**Migration Test Checklist**:

- [ ] Can add frontmatter to templates without breaking content?
- [ ] Can populate `.scaffold-state.yaml` retroactively?
- [ ] Can store template bases from current versions?
- [ ] Can detect if migration already complete?
- [ ] Can rollback failed migration?

### Governança — Recomendações

1. **Test Pre-IMP-65 Migration**
   ```bash
   # Create test project without version metadata
   # Run migration tool
   scaffold.py migrate-to-versioned  # Tool to implement

   # Validate results
   scaffold.py check-templates  # Should work
   ```

2. **Document Compatibility Matrix**
   ```markdown
   # Profile-Template Compatibility

   python-fastapi:
     v1.0.0: Requires spec-template >= 1.0.0
     v2.0.0: Requires spec-template >= 1.5.0 (breaking)

   k8s-helm:
     v1.0.0: Requires plan-template >= 1.0.0
     v1.5.0: Requires plan-template >= 1.2.0
   ```

3. **Create Changelog from Test**
   ```markdown
   # CHANGELOG.md

   ## [Unreleased] - IMP-65 Real-World Test

   ### Discovered Issues
   - Edge case with nested conflict markers
   - Unclear error when base template missing

   ### Improvements Needed
   - Better progress indicators
   - Clearer conflict resolution prompts
   ```

---

## ✅ Consenso

**All perspectives agree**:

1. ✅ **Real-world test is CRITICAL** before production rollout
2. ✅ **Test must include realistic customizations** (not toy examples)
3. ✅ **Test must validate preservation of customizations** (non-negotiable)
4. ✅ **Test must measure DevEx metrics** (time, steps, clarity)
5. ✅ **Test must validate security** (no policy deletion)
6. ✅ **Test findings must feed into regression tests**
7. ✅ **Test must validate migration path** for pre-IMP-65 projects

**Areas of tension**:

- **Architecture** wants comprehensive instrumentation → May slow down test
- **DevEx** wants natural user flow → May miss edge cases
- **Security** wants worst-case scenarios → May be unrealistic
- **Governance** wants migration validation → Adds test complexity

**Resolution**: Run test in phases:
1. **Phase 1**: Natural user flow (DevEx focus)
2. **Phase 2**: Edge case exploration (Architecture focus)
3. **Phase 3**: Security scenarios (Security focus)
4. **Phase 4**: Migration validation (Governance focus)

---

## 💡 Próximos Passos Sugeridos

### Immediate (This Session)

1. **Setup Test Project** (30 min)
   - Use python-fastapi profile
   - Add realistic customizations
   - Commit baseline

2. **Execute Update Workflow** (90 min)
   - Run check/diff/merge commands
   - Document all output
   - Note edge cases

3. **Write Test Report** (60 min)
   - Findings per perspective
   - Pass/fail criteria
   - Improvement recommendations

### Post-Test Actions

4. **Create Regression Tests** (2h)
   - One test per edge case discovered
   - Add to test suite
   - Ensure 100% pass rate

5. **Update Documentation** (2h)
   - Fix inaccuracies discovered
   - Add troubleshooting section
   - Add real-world examples

6. **Implement Improvements** (varies)
   - P0 bugs: Fix immediately
   - P1 UX issues: Fix before release
   - P2 nice-to-haves: Backlog

---

## Success Criteria

**Test is successful if**:

✅ All customizations are preserved after merge
✅ New upstream features are added correctly
✅ Project builds and tests pass after update
✅ Total time < 10 minutes (target: 5 minutes)
✅ No silent overwrites occur
✅ Backups are created and restorable
✅ Documentation matches reality
✅ Migration path is clear for pre-IMP-65 projects

**Test reveals issues if**:

⚠️ Any customization is lost
⚠️ Merge produces incorrect output
⚠️ Process takes > 10 minutes
⚠️ Conflicts are confusing
⚠️ Documentation is wrong
⚠️ No clear migration path

**Either outcome is valuable** — we learn and improve!

---

## Conclusion

**Unanimous Recommendation**: ✅ **EXECUTE THE REAL-WORLD TEST**

All four perspectives (Architecture, DevEx, Security, Governance) agree this is the **highest priority action** before declaring IMP-65 production-ready.

**Risk**: Low (test environment, has backups)
**Impact**: High (validates entire system)
**Effort**: 3 hours
**ROI**: Excellent

**Next Step**: Begin test execution immediately.
