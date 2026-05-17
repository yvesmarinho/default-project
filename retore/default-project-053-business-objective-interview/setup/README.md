# Setup Scripts — Legacy & Deprecated

Esta pasta contém **scripts de setup legados** que foram absorvidos pelo `scripts/scaffold.py`.

---

## 🚫 Status: DEPRECATED

Todos os scripts nesta pasta são **mantidos apenas para referência e compatibilidade**. O uso recomendado é através de `scripts/scaffold.py`.

---

## Scripts Legados

### 1. `init-new-project.sh` ⚠️ DEPRECATED

**Funcionalidade original:**
- Inicializar novo projeto a partir do template
- Configurar symlinks `.copilot-*`
- Substituir placeholders
- Limpar histórico Git
- Executar `make init`

**Substituído por:**
```bash
# Novo comando (interativo)
uv run scripts/scaffold.py new

# Ou subcomando direto
uv run scripts/scaffold.py new --name meu-projeto --domain devops --language python
```

**Referências antigas no Makefile:**
```makefile
# DEPRECATED - Use scaffold.py
make init-new-project NAME=meu-projeto
```

---

### 2. `setup-project-links.sh` ⚠️ DEPRECATED

**Funcionalidade original:**
- Criar symlinks de arquivos compartilhados (`.copilot-rules.md`, etc.)
- Verificar integridade do diretório compartilhado
- Criar estrutura compartilhada se ausente

**Substituído por:**
```bash
# Automático durante scaffold.py new
# Ou explicitamente:
uv run scripts/scaffold.py check
```

**Observação:** O `scaffold.py` usa a biblioteca Python `scripts/lib/links.py` que implementa a mesma funcionalidade com melhor error handling e logging.

---

### 3. `check-project-links.sh` ⚠️ DEPRECATED

**Funcionalidade original:**
- Verificar status dos symlinks `.copilot-*`
- Detectar links quebrados ou ausentes
- Reportar inconsistências

**Substituído por:**
```bash
uv run scripts/scaffold.py check
```

**Equivalente no Makefile:**
```makefile
make check-links    # Chama scaffold.py check internamente
```

---

## Migração Completa

| Script Legado | Comando Novo | Status |
|---------------|--------------|--------|
| `./setup/init-new-project.sh X` | `uv run scripts/scaffold.py new --name X` | ✅ Substituído |
| `./setup/setup-project-links.sh` | `uv run scripts/scaffold.py check` | ✅ Substituído |
| `./setup/check-project-links.sh` | `uv run scripts/scaffold.py check` | ✅ Substituído |
| `make init-new-project NAME=X` | `uv run scripts/scaffold.py new --name X` | ⚠️ Deprecated |

---

## Por que foram deprecados?

1. **Duplicação lógica**: Mesma funcionalidade em Bash e Python
2. **Manutenibilidade**: Python é mais testável e modular
3. **Consistência**: `scaffold.py` é o **ponto único de entrada**
4. **Features**: scaffold.py adiciona validação, dry-run, profiles, etc.

---

## Quando remover?

Estes scripts serão **removidos** após:
- ✅ Sprint 6 validado com scaffold.py em produção
- ✅ Documentação atualizada (README, docs/, Makefile)
- ✅ Nenhuma dependência externa restante

**Estimativa de remoção:** Sprint 7 ou 8 (pós-estabilização do scaffold.py)

---

## Suporte

Para problemas com scaffold.py ou migração dos scripts legados, consulte:
- Documentação: [docs/TEMPLATE_USAGE.md](../docs/TEMPLATE_USAGE.md)
- Spec técnico: [docs/SESSIONS/2026-02-28/IMP-01-SPEC.md](../docs/SESSIONS/2026-02-28/IMP-01-SPEC.md)
- Issues: Criar issue no repositório
