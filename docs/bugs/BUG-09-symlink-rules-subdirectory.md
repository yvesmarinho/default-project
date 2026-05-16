# BUG-09 — Symlink .copilot-rules.md Fails on Upgrade (Path Resolution)

**Status**: ✅ RESOLVIDO (2026-05-12)
**Severity**: P1 MEDIUM (blocks scaffold upgrade for all projects)
**Discovered**: 2026-05-12 durante upgrade de sistema-deploy-automatizado
**Fixed in**: Commit TBD (2026-05-12)

---

## 🐛 Problema

### Sintoma
O comando `scaffold --upgrade` falhava em criar o symlink `.copilot-rules.md` com o seguinte warning:

```
⚠️  Arquivo ausente em shared: /home/yves_marinho/Documentos/DevOps/.copilot-shared/.copilot-rules.md
```

E na tabela de resultados:
```
│ symlink  │ .copilot-rules.md  │ skipped  │ arquivo ausente em shared: ...  │
```

### Comportamento Esperado
Symlink deveria ser criado apontando para:
```
/home/yves_marinho/Documentos/DevOps/.copilot-shared/rules/.copilot-rules.md
```

### Comportamento Real
Código estava procurando o arquivo em:
```
/home/yves_marinho/Documentos/DevOps/.copilot-shared/.copilot-rules.md
```

---

## 🔍 Análise Root Cause

### Código Problemático
**Arquivo**: `scripts/lib/links.py` (linha ~53)

```python
for name in SHARED_COPILOT_FILES:
    src = shared / name  # ❌ ERRADO: procurava na raiz do shared_dir
    dst = target / name
```

### Por Que Aconteceu
A estrutura do diretório `.copilot-shared/` foi organizada em subdiretórios:
```
.copilot-shared/
├── docs/
├── rules/                      ← arquivos .copilot-* ficam aqui
│   ├── .copilot-rules.md
│   ├── .copilot-strict-rules.md
│   └── ...
├── scripts/
└── templates/
```

Mas o código não foi atualizado para refletir essa estrutura.

### Histórico
- A estrutura original (IMP-01, 2026-02-28) tinha os arquivos na raiz
- Em algum momento foi reorganizado com subdiretorios (rules/, scripts/, etc.)
- O código de `links.py` não foi atualizado

---

## ✅ Solução Implementada

### Correção
**Arquivo**: `scripts/lib/links.py` (linha 54)

```python
for name in SHARED_COPILOT_FILES:
    # Os arquivos compartilhados estão em shared_dir/rules/
    src = shared / "rules" / name  # ✅ CORRETO: busca em rules/ subdirectory
    dst = target / name
```

### Validação
**Teste**: `tests/test_bug09_symlink_rules_subdirectory.py`

Dois casos de teste:
1. ✅ `test_symlink_points_to_rules_subdirectory`: Verifica que symlink aponta para `rules/` subdirectory
2. ✅ `test_symlink_skipped_when_file_missing_in_shared`: Verifica comportamento quando arquivo não existe

**Execução manual de upgrade**:
```bash
scaffold --upgrade  # em sistema-deploy-automatizado
```

**Resultado**:
```
│ symlink  │ .copilot-rules.md  │ skipped  │ symlink ok  │
```

Symlink criado:
```bash
ls -la .copilot-rules.md
lrwxrwxrwx → .copilot-rules.md -> ../../.copilot-shared/rules/.copilot-rules.md
```

---

## 📊 Impact Assessment

### Quem Foi Afetado
- ✅ **Nenhum projeto existente**: Bug só afetava novos upgrades
- ⚠️ **Projetos em POC**: sistema-deploy-automatizado era o primeiro a testar upgrade após fix de infraestrutura

### Severidade Justificada (P1 MEDIUM)
- **P1** (não P0) porque:
  - Não quebra projetos existentes
  - Workaround manual: criar symlink com `ln -s`
  - Scaffold new (não upgrade) não era afetado
- **MEDIUM** (não HIGH) porque:
  - Upgrade continua funcionando (apenas 1 symlink falta)
  - Projetos podem trabalhar sem `.copilot-rules.md` (usando regras locais)

---

## 🎓 Lessons Learned

### Prevenção Futura
1. ✅ **Teste de integração criado**: `test_bug09_symlink_rules_subdirectory.py`
2. ✅ **Documentação atualizada**: Este arquivo
3. 📝 **TODO**: Adicionar validação de estrutura de `.copilot-shared/` no setup

### Código Relacionado
- `scripts/lib/links.py`: setup_symlinks(), check_symlinks()
- `scripts/lib/config.py`: SHARED_COPILOT_FILES, DEFAULT_SHARED_DIR
- `.copilot-shared/rules/`: Estrutura de arquivos compartilhados

---

## 📝 Timeline

| Data | Evento |
|------|--------|
| 2026-05-12 09:00 | Bug descoberto durante session start |
| 2026-05-12 12:15 | Root cause identificado (código procurava em local errado) |
| 2026-05-12 12:20 | Fix aplicado em `links.py` |
| 2026-05-12 12:25 | Teste criado e validado |
| 2026-05-12 12:30 | Documentação completa |
| 2026-05-12 TBD  | Commit e push |

---

## ✅ Verification Checklist

- [x] Bug reproduzido e confirmado
- [x] Root cause identificado
- [x] Fix implementado
- [x] Teste de regressão criado
- [x] Teste manual executado (upgrade em sistema-deploy-automatizado)
- [x] Documentação criada
- [ ] Commit com mensagem descritiva
- [ ] Push para origin

---

*Bug Report completo | BUG-09 | 2026-05-12*
