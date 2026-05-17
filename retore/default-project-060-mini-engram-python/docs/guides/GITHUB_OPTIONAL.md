# Feature: Repositório GitHub Opcional

**Data**: 2026-04-29
**Branch**: 060-mini-engram-python
**Status**: ✅ Implementado e Testado

---

## Objetivo

Tornar o repositório GitHub (`--repo`) opcional durante a criação de projetos com o scaffold. Quando o repositório não for fornecido, o sistema deve:

1. Ignorar ações GitHub-specific (remote, workflows, etc.)
2. Não validar ou tentar acessar GitHub
3. Mostrar "(não configurado)" em vez de links quebrados
4. Criar apenas arquivos de segurança genéricos

---

## Alterações Implementadas

### 1. `scripts/lib/project.py`

#### 1.1. Função `_apply_placeholders()`
**Antes:**
```python
"{{GITHUB_REPO}}": config.github_repo or "",
```

**Depois:**
```python
# Valor para GitHub repo: mostrar link se configurado, senão "(não configurado)"
github_repo_display = config.github_repo if config.github_repo else "(não configurado)"

replacements = {
    ...
    "{{GITHUB_REPO}}": github_repo_display,
}
```

**Motivo:** Melhor experiência do usuário - mostrar "(não configurado)" em vez de célula vazia em tabelas.

#### 1.2. Templates de Segurança
**Antes:** Um único template `_SECURITY_MD` com link obrigatório ao GitHub

**Depois:** Dois templates:
- `_SECURITY_MD_WITH_GITHUB`: Template original com link para Security tab
- `_SECURITY_MD_WITHOUT_GITHUB`: Template genérico com alternativas (email, ticketing, contato direto)

#### 1.3. Função `generate_github_security_files()`
**Antes:** Criava todos os 5 arquivos sempre

**Depois:**
```python
# Arquivo 1: SECURITY.md (raiz do projeto)
# Usa template com GitHub se repositório configurado, senão usa versão genérica
security_md = base / "SECURITY.md"
if config.github_repo:
    content = _apply_placeholders(_SECURITY_MD_WITH_GITHUB, config)
else:
    content = _SECURITY_MD_WITHOUT_GITHUB
results.append(_write_file(security_md, content))

# Arquivos 2-5: Apenas criar se houver repositório GitHub configurado
if not config.github_repo:
    return results

# ... cria CODEOWNERS, dependabot.yml, workflows apenas se houver repo
```

**Motivo:** Evitar criar arquivos GitHub-specific sem repositório configurado.

---

## Componentes Já Preparados (Não Modificados)

### 1. `scripts/lib/git.py`
A função `init_repository()` já tinha lógica condicional:
```python
if config.github_repo:
    _ensure_remote(target, config.github_repo)
```

### 2. `scripts/lib/composer.py`
Já tratava `github_repo` como opcional:
```python
"{{GITHUB_REPO}}": cfg.github_repo or "",
```

### 3. `scripts/lib/ui.py`
O prompt já permitia pular repositório:
```python
github_repo = Prompt.ask(
    "  [cyan]Repositório GitHub[/cyan] [dim](URL ou Enter para pular)[/dim]",
    default=defaults.get("repo") or "",
).strip() or None
```

### 4. `scripts/scaffold.py`
Argumento `--repo` já era opcional (sem `required=True`)

---

## Testes Implementados

### Arquivo: `tests/test_github_repo_optional.py`

**6 testes criados:**

1. ✅ `test_apply_placeholders_with_github_repo`
   - Verifica substituição correta quando há repo
   - Espera: URL completa substituída

2. ✅ `test_apply_placeholders_without_github_repo`
   - Verifica substituição quando repo é None
   - Espera: "(não configurado)"

3. ✅ `test_github_security_files_with_repo`
   - Verifica criação de 5 arquivos quando há repo
   - Valida conteúdo do SECURITY.md com link GitHub
   - Valida criação de CODEOWNERS, dependabot.yml, workflows

4. ✅ `test_github_security_files_without_repo`
   - Verifica criação de apenas 1 arquivo quando não há repo
   - Valida SECURITY.md genérico (sem link GitHub)
   - Valida que arquivos .github NÃO foram criados

5. ✅ `test_project_config_github_repo_none`
   - Verifica que ProjectConfig aceita None

6. ✅ `test_project_config_github_repo_empty_string`
   - Verifica tratamento de string vazia como falsy

**Resultado:** Todos os 6 testes passaram ✅

---

## Uso

### Com repositório GitHub
```bash
./scripts/scaffold.py new \
  --ci \
  --name my-project \
  --domain programming \
  --language python \
  --repo https://github.com/org/my-project
```

**Resultado:**
- Git remote configurado
- SECURITY.md com link para Security tab
- CODEOWNERS criado
- dependabot.yml criado
- Workflows de segurança criados

### Sem repositório GitHub (novo comportamento)
```bash
./scripts/scaffold.py new \
  --ci \
  --name my-project \
  --domain programming \
  --language python
# --repo omitido
```

**Resultado:**
- Git inicializado localmente (sem remote)
- SECURITY.md genérico criado
- Tabelas mostram "Repositório: (não configurado)"
- Arquivos .github/CODEOWNERS, dependabot.yml, workflows NÃO criados

---

## Validação

### Testes Automatizados
```bash
python -m pytest tests/test_github_repo_optional.py -v
# ============================== 6 passed in 0.04s ===============================
```

### Inspeção Manual
1. Criar projeto sem `--repo`
2. Verificar que `docs/PROJECT_CREATION_SUMMARY.md` mostra "(não configurado)"
3. Verificar que `.github/CODEOWNERS` não existe
4. Verificar que `SECURITY.md` não tem link quebrado

---

## Impacto em Arquivos Existentes

### Projetos Já Criados
- Não afetados (arquivos já existem, não serão recriados)

### Projetos Futuros
- Projetos **com** `--repo`: comportamento inalterado
- Projetos **sem** `--repo`: agora funcionam corretamente

---

## Próximos Passos (Opcional)

### Linting Warnings (não-crítico)
Há alguns warnings de estilo em arquivos relacionados:
- `test_objetivo_wizard_complete_poc.py`: encoding, f-strings não interpoladas
- `objetivo_wizard.py`: import datetime não usado
- Diversos: Exception genérico (catch Exception as e)

**Prioridade:** Baixa (todos são warnings de estilo, não erros funcionais)

### Documentação Adicional
- ✅ Criar guia de uso em `docs/guides/GITHUB_OPTIONAL.md` (este arquivo)
- ⏸️ Atualizar README.md com exemplos sem `--repo` (opcional)

---

## Referências

- **Arquivo de testes:** [tests/test_github_repo_optional.py](../../tests/test_github_repo_optional.py)
- **Código modificado:** [scripts/lib/project.py](../../scripts/lib/project.py) linhas 45-62, 1264-1355, 2164-2203
- **Configuração:** [scripts/lib/config.py](../../scripts/lib/config.py) linha 134 (github_repo: str | None)
- **UI Prompt:** [scripts/lib/ui.py](../../scripts/lib/ui.py) linha 238-241

---

## Checklist de Implementação

- [x] Modificar `_apply_placeholders()` para mostrar "(não configurado)"
- [x] Criar template `_SECURITY_MD_WITH_GITHUB`
- [x] Criar template `_SECURITY_MD_WITHOUT_GITHUB`
- [x] Atualizar `generate_github_security_files()` com lógica condicional
- [x] Criar testes de unidade (6 testes)
- [x] Validar todos os testes (6/6 passando)
- [x] Documentar feature em `docs/guides/GITHUB_OPTIONAL.md`
- [ ] Commit e push (pendente)
- [ ] Atualizar `docs/TODO.md` (pendente)
- [ ] Atualizar sessão em `docs/SESSIONS/2026-04-29/` (pendente)
