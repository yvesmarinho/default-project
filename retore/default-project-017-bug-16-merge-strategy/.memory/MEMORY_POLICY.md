# Memory Policy — Security and Usage Guidelines

**Status**: 🔒 MANDATORY (enforced by pre-commit hooks)
**Scope**: All memories in `.memory/memories/`
**Compliance**: LGPD, GDPR, Principle IV (Zero-Trust on Secrets)

---

## 🚨 Principle IV: Zero-Trust on Secrets

> No credential, token, API key, password, or secret of any kind ever enters the codebase — not in source files, not in templates, not in domain profiles, not in generated scaffold output, **and not in memory files**.

This principle applies **EQUALLY** to `.memory/memories/` as it does to source code.

---

## ❌ NEVER Save in Memory

### 1. Credentials

| Type | Examples | ❌ NEVER | ✅ INSTEAD |
|------|----------|---------|-----------|
| **Passwords** | Database passwords, admin passwords | `password: MyP@ssw0rd` | `password: stored in .secrets/.db_pass` |
| **API Keys** | AWS keys, GitHub tokens, Stripe keys | `api_key: sk_live_1234abcd` | `API key: env var API_KEY` |
| **Tokens** | JWT secrets, OAuth tokens, session tokens | `jwt_secret: super-secret-key` | `JWT secret: Vault path secret/app/jwt` |
| **Connection Strings** | Database URLs with embedded passwords | `postgresql://user:pass@host/db` | `DB URL: .secrets/.db_url (gitignored)` |
| **SSH Keys** | Private keys, deploy keys | `-----BEGIN RSA PRIVATE KEY-----` | `SSH key: ~/.ssh/deploy_key` |
| **Certificates** | SSL certs, client certs | `-----BEGIN CERTIFICATE-----` | `Cert: stored in .secrets/ssl/` |

### 2. Personally Identifiable Information (PII)

| Type | Examples | ❌ NEVER | ✅ INSTEAD |
|------|----------|---------|-----------|
| **Email** | User emails, contact info | `user@example.com` | `user email: stored in database` |
| **Phone Numbers** | Mobile, landline | `+55 11 98765-4321` | `phone: user-provided (not logged)` |
| **CPF/SSN** | Tax IDs, national IDs | `123.456.789-00` | `CPF: validated but not stored` |
| **IP Addresses** | User IPs, server IPs (if sensitive) | `192.168.1.100` | `IP: anonymized in logs` |
| **Names** | Full names (if sensitive context) | `John Doe from Acme Corp` | `user: authenticated via SSO` |

**LGPD Compliance**: Storing PII in memory without consent = Article 46 violation.

### 3. Dangerous Command Outputs

❌ **NEVER** save output from:

```bash
# Secrets exposure
kubectl get secret -o yaml
cat .env
printenv | grep SECRET
aws sts get-session-token
terraform show

# PII exposure
SELECT * FROM users WHERE email = '...'
curl https://api.example.com/users/123  # if returns PII

# Verbose logs with embedded data
docker logs app-container --tail 1000
journalctl -u myapp -n 500
```

### 4. Proprietary Code (Full Implementations)

❌ **NEVER** save entire proprietary algorithms:

```markdown
❌ WRONG:
# Proprietary Algorithm
```python
def secret_sauce(data):
    # Company's secret algorithm (10 years of R&D)
    step1 = data * MAGIC_CONSTANT
    step2 = apply_secret_transform(step1)
    return optimize_with_ml_model(step2)
```
```

✅ **CORRECT**:
```markdown
# Algorithm Decision
Use proprietary ML optimization algorithm (implemented in `src/core/optimizer.py`).
Rationale: 40% faster than open-source alternatives, validated in IMP-XX.
```

---

## ✅ WHAT TO Save in Memory

### 1. Architectural Decisions

```markdown
# Decision: Use PostgreSQL Over MySQL

## Context
Need ACID transactions, JSONB support, and full-text search.

## Decision
Use PostgreSQL 15 as primary database.

## Rationale
- JSONB: Native JSON storage with indexing (better than MySQL's JSON type)
- FTS: Built-in full-text search (ts_vector)
- Extensions: PostGIS for geo data, pg_stat_statements for monitoring

## Consequences
- Requires PostgreSQL in production (add to Terraform)
- Team needs PostgreSQL training (schedule workshop)
```

### 2. Code Patterns and Best Practices

```markdown
# Pattern: Repository Pattern for Database Access

## Usage
All database access goes through repository classes, not direct ORM queries.

## Example
```python
# ✅ CORRECT
class UserRepository:
    def find_by_email(self, email: str) -> Optional[User]:
        return self.session.query(User).filter_by(email=email).first()

# ❌ WRONG (direct ORM in controller)
user = session.query(User).filter_by(email=email).first()
```

## Benefits
- Testability: Mock repository, not ORM
- Flexibility: Swap ORM without changing controllers
- Consistency: Centralized query logic
```

### 3. Troubleshooting and Learnings

```markdown
# Learning: SSL Certificate Error with Let's Encrypt

## Problem
`curl https://api.example.com` failed with "SSL certificate problem: unable to get local issuer certificate"

## Root Cause
Let's Encrypt changed root CA in 2021. Old systems don't trust new ISRG Root X1.

## Solution
Update ca-certificates package:
```bash
sudo apt update && sudo apt install --reinstall ca-certificates
```

## Prevention
Add to Ansible playbook: ensure ca-certificates >= version X.Y
```

### 4. Team Processes and Checklists

```markdown
# Process: Deployment Checklist

Before deploying to production:

- [ ] All tests passing (CI green)
- [ ] Database migrations tested in staging
- [ ] Feature flags configured
- [ ] Monitoring dashboards updated
- [ ] Rollback plan documented
- [ ] On-call engineer notified
- [ ] Deploy window: outside business hours (18:00-22:00 BRT)
```

### 5. References to Secrets (Not the Secrets Themselves)

```markdown
# Database Credentials Management

## Location
- **Local dev**: `.secrets/.db_credentials` (gitignored)
- **Staging**: AWS Secrets Manager `staging/database/credentials`
- **Production**: AWS Secrets Manager `prod/database/credentials`

## Rotation
Rotate credentials every 90 days (automated via AWS Lambda).
See: `docs/CREDENTIAL_ROTATION.md`

## Access
Request production DB access via Jira ticket (Security team approval required).
```

---

## 🔍 Automatic Detection

### Pre-commit Hook

The `.git/hooks/pre-commit` script scans `.memory/memories/` for secrets before allowing commit:

```bash
#!/usr/bin/env bash
# .git/hooks/pre-commit

if git diff --cached --name-only | grep -q '^\.memory/memories/'; then
    echo "🔍 Scanning memory files for secrets..."

    # Use gitleaks
    gitleaks protect --staged --config .gitleaks-memory.toml --source .memory/memories/

    if [ $? -ne 0 ]; then
        echo "❌ COMMIT BLOCKED: Secrets detected in .memory/memories/"
        echo "Remove secrets and try again."
        exit 1
    fi

    echo "✅ No secrets detected"
fi
```

### Gitleaks Configuration

`.gitleaks-memory.toml` defines patterns for memory-specific secret detection:

```toml
[extend]
useDefault = true

[[rules]]
id = "memory-api-key"
description = "API key in memory files"
regex = '''(api[_-]?key|apikey)\s*[=:]\s*['"]?([a-zA-Z0-9_-]{20,})['"]?'''
path = '''\.memory/memories/.*\.md'''

[[rules]]
id = "memory-password"
description = "Password in memory files"
regex = '''(password|passwd|pwd)\s*[=:]\s*['"]?([^\s'"]{6,})['"]?'''
path = '''\.memory/memories/.*\.md'''

[[rules]]
id = "memory-connection-string"
description = "Connection string with embedded password"
regex = '''(postgres|mysql|mongodb)://[^:]+:([^@]+)@'''
path = '''\.memory/memories/.*\.md'''

[[rules]]
id = "memory-email"
description = "Email address (potential PII)"
regex = '''\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'''
path = '''\.memory/memories/.*\.md'''
tags = ["pii"]

[[rules]]
id = "memory-cpf"
description = "CPF (Brazilian tax ID)"
regex = '''\b\d{3}\.\d{3}\.\d{3}-\d{2}\b'''
path = '''\.memory/memories/.*\.md'''
tags = ["pii"]
```

### Runtime Sanitization

`scripts/lib/sanitize.py` provides automatic redaction:

```python
from scripts.lib.sanitize import detect_secrets, sanitize

# Before saving memory
content = "Database password: MyP@ssw0rd123"
findings = detect_secrets(content)

if findings:
    print("⚠️  Secrets detected:", findings)
    sanitized_content, warnings = sanitize(content, redact=True)
    # Result: "Database password: [REDACTED]"
```

---

## 📊 Compliance Requirements

### LGPD (Lei Geral de Proteção de Dados — Brazil)

**Article 46**: Personal data requires **explicit consent** and **purpose limitation**.

**Implications for memory**:
- ❌ Cannot save user emails, CPFs, phone numbers without consent
- ❌ Cannot save user behavior data (logs, analytics) without anonymization
- ✅ Can save aggregate statistics (e.g., "10 users reported bug X")
- ✅ Can save pseudonymized IDs (e.g., "user_id: 42" if no reverse mapping stored)

### GDPR (General Data Protection Regulation — EU)

**Article 25**: Privacy by design and default.

**Implications for memory**:
- ❌ Default: Do NOT save PII
- ✅ If PII is necessary, implement: encryption at rest, access controls, retention limits
- ✅ Right to erasure: Must be able to delete memory files containing user data

### SOC2 Type II

**Control**: Logical access controls.

**Implications for memory**:
- ✅ `.memory/memories/` should have `.github/CODEOWNERS` if committed:
  ```
  .memory/memories/project/** @tech-leads
  .memory/memories/team/**    @engineering-managers
  ```
- ✅ Production secrets must NEVER appear in memory (violates CC6.1 — Confidentiality)

---

## 🛠️ Enforcement Mechanisms

### 1. Pre-commit Hook (Blocking)

```bash
# Install pre-commit hook
make install-git-hooks
```

Automatically scans memory files before commit. **Blocks commit if secrets detected.**

### 2. CI Pipeline (Verification)

```yaml
# .github/workflows/security-scan.yml
name: Security Scan

on:
  pull_request:
    paths:
      - '.memory/memories/**'

jobs:
  gitleaks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Scan memory files
        uses: gitleaks/gitleaks-action@v2
        with:
          config-path: .gitleaks-memory.toml
          source: .memory/memories/
```

### 3. Runtime Validation (mem_save.py)

```bash
# mem_save.py automatically scans content
python scripts/mem_save.py \
  --title "Database Config" \
  --content "password: MyP@ssw0rd"

# Output:
# ⚠️  WARNING: Secrets detected in content:
#     - password: MyP@ssw0rd
# ❌ BLOCKED: Cannot save memory with secrets
# Use --sanitize to auto-redact, or remove secrets manually
```

### 4. Regular Audits

```bash
# Scan all existing memories
make memory-audit
```

Output:
```
🔍 Auditing .memory/memories/ for secrets...

Scanning 47 files...
  ✅ project/2026-04-20__api-pattern.md: CLEAN
  ✅ project/2026-04-15__database-migration.md: CLEAN
  ⚠️  team/2026-03-10__onboarding-guide.md: WARNING (contains email address)
  ❌ sessions/2026-02-05__debug-session.md: FAILED (contains API key)

Summary:
  Clean: 45
  Warnings: 1 (PII detected)
  Failures: 1 (secrets detected)

Action required:
  - Review team/2026-03-10__onboarding-guide.md and redact email
  - Review sessions/2026-02-05__debug-session.md and remove API key
```

---

## 📚 Training and Awareness

### For Developers

**Before saving a memory, ask yourself**:

1. ❓ Does this content contain **credentials** (passwords, keys, tokens)?
   - YES → ❌ Do NOT save. Reference location instead.
   - NO → Proceed to #2

2. ❓ Does this content contain **PII** (emails, names, IDs)?
   - YES → ❌ Anonymize or exclude. Check LGPD compliance.
   - NO → Proceed to #3

3. ❓ Does this content expose **proprietary algorithms** or trade secrets?
   - YES → ⚠️ Save high-level decision only, not full implementation.
   - NO → ✅ Safe to save!

4. ❓ Is this content **valuable for the team** (not just personal notes)?
   - YES → Save to `.memory/memories/project/` or `.memory/memories/team/`
   - NO → Save to `.memory/memories/sessions/` (personal, not committed)

### For Reviewers

When reviewing PRs that modify `.memory/memories/`:

- ✅ Check for secrets (gitleaks should catch, but manual review is good)
- ✅ Check for PII (emails, phone numbers, IDs)
- ✅ Check for proprietary code (full implementations vs high-level decisions)
- ✅ Check for value (is this useful for team, or just noise?)

---

## 🔗 Related Policies

- [Principle IV: Zero-Trust on Secrets](../docs/CONVENTIONS.md#principle-iv-zero-trust-on-secrets)
- [CREDENTIAL_ROTATION.md](../docs/CREDENTIAL_ROTATION.md)
- [SECURITY_SESSION_DOCS.md](../docs/SECURITY_SESSION_DOCS.md)
- [.gitleaks-session-docs.toml](../.gitleaks-session-docs.toml)

---

## ❓ FAQ

### Q: What if I accidentally saved a secret?

**A**:

1. **Immediately remove the secret** from the memory file
2. **Commit the fix** with message: `security: remove leaked secret from memory`
3. **Rotate the secret** (change password, revoke API key, etc.)
4. **Purge from Git history** (if already pushed):
   ```bash
   git filter-repo --path .memory/memories/path/to/file.md --invert-paths
   git push --force
   ```

### Q: Can I save sanitized/redacted secrets?

**A**: No. Even `password: [REDACTED]` reveals **metadata** (that a password exists). Instead:

❌ `password: [REDACTED]`
✅ `password: stored in .secrets/.db_pass (gitignored)`

### Q: What about session logs (debugging output)?

**A**: Session logs often contain **secrets or PII**. Rules:

- ✅ Save **high-level summary** ("Error: SSL handshake failed")
- ❌ Save **full logs** (may contain credentials, IPs, emails)

If you need full logs for debugging:
1. Save to `.memory/memories/sessions/` (personal, NOT committed)
2. Add to `.gitignore`: `.memory/memories/sessions/*debug*`
3. Delete after debugging is done

---

**Version**: 1.0.0 (IMP-59 Phase 3)
**Last updated**: 2026-04-20
**Policy owner**: AppSec + template-architect
