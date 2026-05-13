# Diretório tmp/

Este diretório contém arquivos temporários e scripts de desenvolvimento que não fazem parte da estrutura principal do projeto.

## Propósito

- Scripts Python de diagnóstico e teste temporários
- Versões de desenvolvimento de ferramentas (antes de instalação/integração)
- Arquivos de teste e validação
- Protótipos e experimentos
- Alternativa mais segura ao `/tmp/` do sistema para arquivos temporários do projeto

## Conteúdo Atual (2026-05-13)

```
tmp/
├── README.md                    # Este arquivo
├── scaffold-wrapper-v2.1.sh     # Wrapper scaffold v2.1 (correção preserva cwd)
├── scaffold-wrapper-v2.sh       # Wrapper scaffold v2.0 (BUGADO - não usar)
└── test_upgrade_force.py        # Script de teste para scaffold upgrade --force
```

### scaffold-wrapper-v2.1.sh
Versão corrigida do wrapper global para `scaffold.py`. Preserva o working directory (corrige bug da v2.0).

**Instalação**:
```bash
cp tmp/scaffold-wrapper-v2.1.sh ~/.local/bin/scaffold
chmod +x ~/.local/bin/scaffold
```

**Status**: ✅ Instalado e funcionando (instalado em 2026-05-13)

### scaffold-wrapper-v2.sh
⚠️ **VERSÃO COM BUG** — Usava `uv run --directory` que mudava cwd incorretamente.
**NÃO USAR** — Mantido apenas para referência histórica.

### test_upgrade_force.py
Script de teste para validar comportamento de `scaffold upgrade --force`.
Desenvolvido durante correção do BUG-11/12/13.

## Documentação Organizada (2026-05-13)

Documentação de sessão movida para:
- ✅ `docs/SESSIONS/2026-05-13/` — Atividades diárias e recovery

Documentação técnica movida para:
- ✅ `docs/implementations/` — Bug fixes, code reviews, testes, validações
- ✅ `docs/planning/` — Análises técnicas e planos de correção

## Uso em Scripts

Scripts devem usar `./tmp/` em vez de `/tmp/` para arquivos temporários do projeto:

```bash
# ❌ Evite
temp_file="/tmp/myfile.txt"

# ✅ Prefira
temp_file="./tmp/myfile.txt"
```

## Limpeza

Este diretório é automaticamente limpo por:
- `.github/prompts/session-end.prompt.md` (ritual de fim de sessão)
- `scripts/cleanup-tmp.sh` (pode ser executado manualmente)

Revise periodicamente e:
- ✅ Mova documentação relevante para `docs/` (última organização: 2026-05-13)
- Mova scripts úteis para `scripts/` ou instale como ferramentas
- Remova arquivos obsoletos ou temporários
- Mantenha apenas protótipos ativos e ferramentas de desenvolvimento

## .gitignore

Todos os arquivos neste diretório são ignorados pelo git (exceto este README).


