# Session Documentation Security Scan Job Template

**Part of**: IMP-49 — Sistema de documentação incremental — Integração
**Created**: 2026-04-03
**Status**: Template pronto para integração no ci-template.yml após restauração

---

## 📋 Objetivo

Adicionar job `session-docs-scan` ao workflow `.github/workflows/ci-template.yml` para escanear automaticamente documentação de sessões em busca de dados sensíveis expostos acidentalmente.

---

## 🔧 Template do Job

Adicionar o seguinte job ao `.github/workflows/ci-template.yml`:

```yaml
  session-docs-scan:
    name: 🛡️ Session Docs Security Scan
    runs-on: ubuntu-latest
    if: |
      github.event_name == 'push' ||
      github.event_name == 'pull_request'

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history needed for gitleaks

      - name: Install gitleaks
        run: |
          wget -qO- https://github.com/gitleaks/gitleaks/releases/download/v8.18.0/gitleaks_8.18.0_linux_x64.tar.gz | tar xvz
          sudo mv gitleaks /usr/local/bin/
          gitleaks version

      - name: Scan session documentation
        run: |
          if [ -d "docs/SESSIONS" ]; then
            echo "🔍 Scanning docs/SESSIONS/ for sensitive data exposure..."
            gitleaks detect \
              --config .gitleaks-session-docs.toml \
              --source docs/SESSIONS/ \
              --report-path gitleaks-session-docs-report.json \
              --report-format json \
              --verbose \
              --exit-code 1

            EXIT_CODE=$?

            if [ $EXIT_CODE -eq 0 ]; then
              echo "✅ No sensitive data found in session documentation"
            elif [ $EXIT_CODE -eq 1 ]; then
              echo "❌ SECURITY ALERT: Sensitive data detected in session documentation!"
              echo ""
              echo "📄 Detected issues:"
              cat gitleaks-session-docs-report.json | jq -r '.[] | "  • \(.RuleID): \(.File):\(.StartLine)"'
              echo ""
              echo "🔧 Action required:"
              echo "  1. Review the files listed above"
              echo "  2. Remove/sanitize sensitive data (replace with <REDACTED>, example.com, etc)"
              echo "  3. Commit the sanitized version"
              echo ""
              echo "📖 Security guidelines: docs/SESSION_DOCS_STYLE_GUIDE.md (Anti-Patterns section)"
              exit 1
            else
              echo "⚠️ Gitleaks scan encountered an error (exit code: $EXIT_CODE)"
              exit $EXIT_CODE
            fi
          else
            echo "ℹ️ No docs/SESSIONS/ directory found - skipping scan"
          fi

      - name: Upload scan report (if violations found)
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: gitleaks-session-docs-report
          path: gitleaks-session-docs-report.json
          retention-days: 30

      - name: Comment PR with violations (if PR and violations)
        if: failure() && github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');

            if (fs.existsSync('gitleaks-session-docs-report.json')) {
              const report = JSON.parse(fs.readFileSync('gitleaks-session-docs-report.json', 'utf8'));

              if (report.length > 0) {
                const violations = report.map(v =>
                  `- **${v.RuleID}**: \`${v.File}:${v.StartLine}\` - ${v.Description}`
                ).join('\n');

                const comment = `## 🛡️ Session Documentation Security Violations Detected

${violations}

**Action Required**: Review and sanitize the files above before merging.

📖 See: [Session Documentation Style Guide](docs/SESSION_DOCS_STYLE_GUIDE.md)

**Common fixes**:
- Replace real credentials with \`<REDACTED>\` or \`<API_KEY>\`
- Use \`example.com\`, \`example.org\` for email domains
- Use RFC 5737 IPs: \`192.0.2.1\`, \`198.51.100.1\`, \`203.0.113.1\`
- Use relative paths instead of absolute paths
`;

                github.rest.issues.createComment({
                  owner: context.repo.owner,
                  repo: context.repo.repo,
                  issue_number: context.issue.number,
                  body: comment
                });
              }
            }
```

---

## 📍 Posicionamento no Workflow

Adicionar o job `session-docs-scan` **após** o job `security-scan` e **antes** de `test` no arquivo `ci-template.yml`.

Ordem sugerida dos jobs:
```yaml
jobs:
  security-scan:
    # ... (job existente)

  session-docs-scan:  # ← ADICIONAR AQUI
    # ... (template acima)

  test:
    # ... (job existente)
```

---

## 🔗 Dependências

### Arquivos necessários:
- ✅ `.gitleaks-session-docs.toml` (criado em IMP-49 subtarefa 3)
- ✅ `docs/SESSION_DOCS_STYLE_GUIDE.md` (criado em IMP-48)
- ⏳ `.github/workflows/ci-template.yml` (será restaurado do commit `dce227b`)

### GitHub Actions:
- `actions/checkout@v4`
- `actions/upload-artifact@v4`
- `actions/github-script@v7`

### Ferramentas externas:
- `gitleaks` v8.18.0+ (instalado via wget no job)
- `jq` (pré-instalado no ubuntu-latest runner)

---

## ✅ Checklist de Integração

Quando restaurar os workflows (após IMP-49, IMP-50, IMP-51):

- [ ] Workflow ci-template.yml restaurado do commit `dce227b`
- [ ] Job `session-docs-scan` adicionado conforme template acima
- [ ] Arquivo `.gitleaks-session-docs.toml` presente na raiz do projeto
- [ ] Testar workflow com PR contendo session docs (positivo e negativo)
- [ ] Verificar se relatório JSON é gerado corretamente em caso de violações
- [ ] Verificar se comentário em PR funciona (se aplicável)
- [ ] Atualizar `docs/CI-CD-RESTORATION-GUIDE.md` com referência ao novo job

---

## 🧪 Teste Local

Para testar o scan localmente antes de commitar:

```bash
# 1. Instalar gitleaks (se necessário)
# macOS:
brew install gitleaks

# Linux:
wget -qO- https://github.com/gitleaks/gitleaks/releases/download/v8.18.0/gitleaks_8.18.0_linux_x64.tar.gz | tar xvz
sudo mv gitleaks /usr/local/bin/

# 2. Executar scan localmente
gitleaks detect \
  --config .gitleaks-session-docs.toml \
  --source docs/SESSIONS/ \
  --verbose

# 3. Interpretar resultado
# Exit code 0 = ✅ Clean (no issues)
# Exit code 1 = ❌ Violations found
# Exit code 2+ = ⚠️ Error in scan
```

---

## 📝 Notas de Implementação

### Performance
- Scan é rápido: ~1-3 segundos para até 100 arquivos markdown
- Full git history necessário (fetch-depth: 0)

### Segurança
- Job falha intencionalmente (exit 1) se violações forem encontradas
- Relatório JSON armazenado como artifact (retention: 30 dias)
- PR recebe comentário automático com detalhes das violações

### Manutenção
- Atualizar versão do gitleaks periodicamente: `v8.18.0` → `v8.20.0+`
- Adicionar novas rules ao `.gitleaks-session-docs.toml` se novos padrões surgirem
- Revisar allowlist se houver muitos false positives

---

*Template criado para IMP-49 | Session: 2026-04-03*
