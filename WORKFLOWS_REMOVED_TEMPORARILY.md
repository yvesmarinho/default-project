# ⚠️ Workflows CI/CD Temporariamente Desabilitados

**Data:** 2026-03-31  
**Status:** 🔴 Workflows removidos durante desenvolvimento ativo  
**Previsão de retorno:** Após conclusão do core (Q2 2026)

---

## 🎯 Por Que os Workflows Foram Removidos?

Durante a fase inicial de desenvolvimento do template, decidiu-se **temporariamente desabilitar** os workflows de CI/CD para:

1. **Focar no desenvolvimento essencial** (scaffold.py, MCP, documentação)
2. **Reduzir ruído de notificações** durante experimentação
3. **Economizar GitHub Actions minutes** (100% de economia)

---

## 📋 O Que Isso Significa?

### Para desenvolvedores do template:
- ❌ Testes **não** executam automaticamente em commits
- ❌ Security scans **não** rodam automaticamente  
- ❌ Coverage **não** é medido no CI
- ✅ Testes **podem** ser executados localmente: `make test-cov`
- ✅ Security scan manual disponível: `make security-scan` (quando implementado)

### Para usuários do template:
- ❌ Projetos scaffolded **não** terão workflows GitHub Actions por padrão
- ⚠️ Será necessário configurar CI/CD manualmente em projetos
- ✅ Workflows **funcionais** estarão disponíveis no git (commit `dce227b`)

---

## 🔄 Como Restaurar os Workflows?

### Restauração Rápida (15 minutos)

Consulte o guia completo: **[docs/CI-CD-RESTORATION-GUIDE.md](docs/CI-CD-RESTORATION-GUIDE.md)**

**TL;DR:**
```bash
# Restaurar workflows funcionais do git
git checkout dce227b -- .github/workflows/
git commit -m "feat(ci): restaurar workflows CI/CD"
git push origin master
```

---

## ⚠️ Riscos Durante Este Período

| Risco | Severidade | Mitigação |
|-------|-----------|-----------|
| Vulnerabilidades não detectadas | 🔴 ALTO | Revisar PRs Dependabot manualmente |
| Regressões não detectadas | 🟠 MÉDIO | Executar `make test-cov` antes de commits |
| Baseline enterprise comprometida | 🟡 BAIXO | Documentar status temporário |

**6 CVEs pendentes:** https://github.com/yvesmarinho/default-project/security/dependabot

---

## 📚 Mais Informações

- **Guia de restauração completo:** [docs/CI-CD-RESTORATION-GUIDE.md](docs/CI-CD-RESTORATION-GUIDE.md)
- **Debate técnico:** [docs/SESSIONS/2026-03-31/DEBATE_CONSOLIDADO_REMOCAO_AUTOMACOES_2026-03-31.md](docs/SESSIONS/2026-03-31/DEBATE_CONSOLIDADO_REMOCAO_AUTOMACOES_2026-03-31.md)
- **Estado dos workflows:** Commit `dce227b` (TOTALMENTE FUNCIONAIS)

---

**Este é um estado temporário.** Os workflows retornarão após conclusão do desenvolvimento core.
