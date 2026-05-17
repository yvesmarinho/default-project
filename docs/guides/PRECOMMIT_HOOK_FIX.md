# Hook Pre-commit.secrets — Correções de Falso Positivo

**Status**: ✅ RESOLVIDO
**Data**: 2026-04-29
**Commit**: 53a9ac5
**Branch**: 060-mini-engram-python

---

## 📋 Contexto

Durante testes do recurso "GitHub Repositório Opcional", foram detectados 2 erros git ao executar scaffold interativo sem repositório GitHub configurado:

### Erro 1: Hook bloqueando `.git-hooks/pre-commit.secrets`
```
❌ BLOQUEADO: Arquivos sensíveis detectados
Arquivos bloqueados:
  - .git-hooks/pre-commit.secrets
💡 Estes arquivos devem estar em .secrets/
```

### Erro 2: `git reset HEAD` em repositório sem commits
```
fatal: Failed to resolve 'HEAD' as a valid ref.
```

---

## 🔍 Análise

### Erro 1: Falso Positivo
- **Hook**: `.git-hooks/pre-commit.secrets` (scripts/lib/project.py linhas 366-550)
- **Problema**: Padrão `'secret'` na array `SENSITIVE_PATTERNS` estava fazendo match com o próprio arquivo de hook `pre-commit.secrets`
- **Causa**: Hook validava TODOS os arquivos em staging sem exceções para `.git-hooks/`
- **Impacto**: Impossível commitar arquivos do projeto que continham "secret" no nome (mesmo sendo scripts legítimos)

### Erro 2: Comando Git Incompatível
- **Hook**: Mensagem de ajuda quando `.secrets/` detectado em staging
- **Problema**: Comando `git reset HEAD .secrets/` requer que HEAD exista (primeiro commit)
- **Causa**: Repositórios recém-inicializados com `git init` não têm HEAD até o primeiro commit
- **Impacto**: Erro fatal em projetos novos criados sem repositório GitHub

---

## ✅ Solução Implementada

### 1. Exceção para `.git-hooks/`

**Arquivo**: `scripts/lib/project.py` (linhas 393-418)

**Antes**:
```bash
BLOCKED_FILES=()
for pattern in "${SENSITIVE_PATTERNS[@]}"; do
    while IFS= read -r file; do
        [[ -n "$file" ]] && BLOCKED_FILES+=("$file")
    done < <(git diff --cached --name-only | grep -iE "$pattern" || true)
done
```

**Depois**:
```bash
BLOCKED_FILES=()
for pattern in "${SENSITIVE_PATTERNS[@]}"; do
    while IFS= read -r file; do
        # Ignorar arquivos em .git-hooks/ (são scripts de validação, não secrets)
        if [[ "$file" =~ ^\.git-hooks/ ]]; then
            continue
        fi
        [[ -n "$file" ]] && BLOCKED_FILES+=("$file")
    done < <(git diff --cached --name-only | grep -iE "$pattern" || true)
done
```

**Lógica**: Verifica se o arquivo está em `.git-hooks/` antes de adicionar à lista de bloqueados. Scripts de validação não são secrets.

---

### 2. Comando Git Compatível

**Arquivo**: `scripts/lib/project.py` (linhas 383-390)

**Antes**:
```bash
echo "💡 Solução: remova os arquivos do staging:"
echo "   git reset HEAD .secrets/"
```

**Depois**:
```bash
echo "💡 Solução: remova os arquivos do staging:"
echo "   git restore --staged .secrets/"
echo "   # ou: git reset .secrets/"
```

**Mudanças**:
- `git restore --staged` (Git 2.23+): Comando moderno que não requer HEAD
- Fallback: `git reset .secrets/` (sem HEAD): Compatível com repos novos
- Comentário educacional: Explica alternativa

---

## 🧪 Validação

### Testes Criados
**Arquivo**: `tests/test_precommit_hook_git_hooks_exception.py`

| Teste | Objetivo | Status |
|-------|----------|--------|
| `test_hook_ignores_git_hooks_directory` | Verifica exceção `.git-hooks/` | ✅ PASS |
| `test_hook_uses_git_restore_instead_of_reset_head` | Valida comandos compatíveis | ✅ PASS |
| `test_hook_has_sensitive_patterns` | Confirma padrões sensíveis presentes | ✅ PASS |
| `test_hook_validates_secrets_directory` | Verifica bloqueio `.secrets/` | ✅ PASS |
| `test_hook_checks_permissions` | Valida verificação chmod 700 | ✅ PASS |
| `test_hook_exception_pattern_syntax` | Valida sintaxe regex exceção | ✅ PASS |

**Resultado**: 6/6 testes passando

### Comando de Teste
```bash
python -m pytest tests/test_precommit_hook_git_hooks_exception.py -v
```

---

## 📊 Arquivos Alterados

| Arquivo | Alterações | Descrição |
|---------|-----------|-----------|
| `scripts/lib/project.py` | 11 linhas modificadas | Hook pre-commit.secrets com exceção `.git-hooks/` e comando git moderno |
| `tests/test_precommit_hook_git_hooks_exception.py` | 108 linhas adicionadas | Suite de testes validando correções |

---

## 🎯 Impacto

### Funcionalidades Corrigidas
✅ Projetos criados com `scaffold new` (sem --repo) agora funcionam completamente
✅ Hook pre-commit não bloqueia mais seus próprios scripts de validação
✅ Comandos git compatíveis com repositórios recém-inicializados (sem commits)
✅ Mensagens de ajuda educacionais (mostra comando moderno + fallback)

### Segurança Mantida
🔒 Padrões sensíveis continuam sendo validados (`secret`, `password`, `token`, `.env`, etc.)
🔒 Pasta `.secrets/` continua bloqueada
🔒 Validação de permissões 700 mantida
🔒 Apenas `.git-hooks/` (scripts do projeto) é exceção

### Regressão Zero
✅ Todos os testes existentes continuam passando
✅ 6 novos testes garantem correções
✅ Funcionalidade GitHub opcional não afetada

---

## 🧑‍💻 Workflow de Teste

Para validar as correções em ambiente real:

```bash
# 1. Criar projeto interativo SEM repositório GitHub
uv run scripts/scaffold.py new
# (preencher perguntas, deixar repositório vazio)

# 2. Entrar no projeto criado
cd /caminho/projeto-novo

# 3. Executar objetivo-init
uv run scripts/scaffold.py objetivo-init
# (preencher objetivo wizard)

# ✅ ESPERADO: Execução completa SEM erros git
# ✅ Hook pre-commit instalado e funcional
# ✅ Arquivo .git-hooks/pre-commit.secrets commitado com sucesso
```

---

## 📚 Referências

- **Feature relacionada**: [GITHUB_OPTIONAL.md](GITHUB_OPTIONAL.md)
- **Commit correção hook**: 53a9ac5
- **Commit feature opcional**: 626ed5c
- **Branch**: 060-mini-engram-python
- **Data bug reportado**: 2026-04-29

---

## 🔗 Ver Também

- `.git-hooks/pre-commit.secrets` — Hook instalado em novos projetos
- `scripts/lib/project.py` — Código fonte do hook (lines 366-550)
- `setup_secrets_security()` — Função que instala hook (lines 2100-2220)
- `tests/test_github_repo_optional.py` — Testes da feature opcional
