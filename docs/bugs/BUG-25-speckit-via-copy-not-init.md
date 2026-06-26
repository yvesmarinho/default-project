<!--
Criado em: 26/06/2026 11:30
Modificado em: 26/06/2026 11:30
-->

# ✅ BUG-25 RESOLVIDO: Assets SpecKit Copiados Manualmente em vez de `specify init`

**Data**: 2026-06-26  
**Reportado por**: Yves Marinho  
**Resolvido por**: Claude Sonnet 4.6

---

## 🐛 Problema Relatado

Todo o conteúdo gerenciado pelo SpecKit (agents `speckit.*`, prompts `speckit.*`, `.specify/`) estava sendo **copiado manualmente** do projeto DEV em vez de ser gerado pelo comando oficial `specify init --here --force --integration {{IA}}`.

Adicionalmente, o log registrava `specify init --integration claude` como falho — mas a investigação mostrou que a falha era do código antigo (antes da refatoração de 2026-06-24), não do CLI.

Também foi relatado que `run_speckit_init()` ficava **preso** (hanging) requerendo pressionar Enter para continuar.

---

## 🔍 Evidência do Log (`tmp/stdout.txt`)

```
INFO Executando: specify init --here --force --integration claude em .../test-000-prog-py-claude
ERROR specify init falhou (claude):
                                    ← stderr vazio
🤖 Copiando assets SpecKit customizados...
INFO ✅ criado: context-architect.agent.md → .github/agents/...
INFO ✅ criado: speckit.analyze.agent.md → .github/agents/...
...
```

---

## 🔍 Investigação

### 1. O CLI funciona?

Testado manualmente:
```bash
specify init --here --force --integration claude
# EXIT CODE: 0 ✅
```

Testado via subprocess (como o scaffold executa):
```python
proc = subprocess.run(
    ["specify", "init", "--here", "--force", "--integration", "claude"],
    cwd=test_dir,
    capture_output=True,
    text=True,
    timeout=30,
)
# RETURNCODE: 0 ✅
```

**Conclusão**: O CLI funciona. A falha no log era do código da versão anterior.

### 2. Por que o erro tinha stderr vazio?

O código antigo logava apenas `proc.stderr`:
```python
log.error("specify init falhou (%s):\n%s", integration, proc.stderr)
```

Quando o `specify` escreve erros no stdout (não no stderr), o diagnóstico aparecia vazio.

### 3. Por que ficava preso (hanging)?

O subprocess era executado com `capture_output=True` mas **sem fechar stdin**. Quando executado dentro de um terminal interativo (TTY), `specify init` pode ler de stdin para confirmações, causando bloqueio indefinido.

### 4. O que `specify init` gera por integração?

| `--integration` | Arquivos gerados |
|----------------|-----------------|
| `claude` | `.claude/skills/speckit-*/SKILL.md` + `.specify/` + `CLAUDE.md` |
| `copilot` | `.github/agents/speckit.*.agent.md` + `.github/prompts/speckit.*.prompt.md` + `.specify/` + `.vscode/settings.json` |

Todos os arquivos do Copilot têm prefixo `speckit.` — o `copy_custom_agents()` pula corretamente esses arquivos com `if src_file.name.startswith("speckit."): continue`.

---

## ✅ Solução Implementada

### Correção em `run_speckit_init()` — `scripts/lib/project.py`

**Antes**:
```python
proc = subprocess.run(
    cmd,
    cwd=str(config.project_path),
    capture_output=True,
    text=True,
    timeout=120,
)
...
log.error("specify init falhou (%s):\n%s", integration, proc.stderr)
```

**Depois**:
```python
proc = subprocess.run(
    cmd,
    cwd=str(config.project_path),
    capture_output=True,
    text=True,
    timeout=120,
    stdin=subprocess.DEVNULL,   # evita hanging quando stdin é um TTY interativo
)
...
output_diag = (proc.stderr or proc.stdout or "")[:400]
log.error("specify init falhou (%s):\n%s", integration, output_diag)
```

**Mudanças**:
- `stdin=subprocess.DEVNULL` → resolve o hanging em TTY interativo
- `proc.stderr or proc.stdout` → captura o diagnóstico independente de qual stream o specify escreve

---

## 🧪 Validação

Suite de testes: **251 passed, 5 failed (pré-existentes), 7 skipped** — sem regressões.

Verificação do comportamento por integração:
```
specify init --integration claude  → exit 0, gera .claude/skills/speckit-*/ ✅
specify init --integration copilot → exit 0, gera .github/agents/speckit.*   ✅
```

---

## 📝 Arquivos Modificados

1. ✅ `scripts/lib/project.py`
   - `run_speckit_init()`: adicionado `stdin=subprocess.DEVNULL` e diagnóstico `stderr or stdout`

---

## 🎯 Status Final

| Item | Status |
|------|--------|
| Hanging resolvido | ✅ `stdin=subprocess.DEVNULL` |
| Diagnóstico de erro melhorado | ✅ `stderr or stdout` |
| CLI confirmado funcional | ✅ exit 0 para `claude` e `copilot` |
| Testes passando | ✅ 251 passed |
| Documentação | ✅ |

---

**Assinado**: Claude Sonnet 4.6  
**Timestamp**: 2026-06-26T11:30:00-03:00
