# BUG Report — 2026-05-13

**Data**: 2026-05-13  
**Sessão**: Correções BUG-11/12/13/14  
**Status**: 🔴 PENDENTE (3 bugs identificados)

---

## 🐛 BUG-15: Pasta logs/ não criada automaticamente pelo scaffold

### Descrição
A pasta `logs/` não está sendo criada automaticamente na raiz do projeto durante `scaffold new`, embora seja padrão do template (junto com `tmp/`).

### Comportamento Esperado
- ✅ `tmp/` criado na raiz (com README.md)
- ✅ `logs/` criado na raiz (com README.md ou .gitkeep)

### Comportamento Atual
- ✅ `tmp/` criado corretamente
- ❌ `logs/` NÃO criado

### Impacto
- **Severidade**: P1 (Média)
- **Afeta**: Todos projetos novos criados com scaffold
- **Workaround**: Criar manualmente `mkdir logs && touch logs/.gitkeep`

### Arquivos Relacionados
- `scripts/lib/project.py` — Função `create_structure()` ou constante `DIRS_TO_CREATE`
- `scripts/lib/flows/new_project.py` — Workflow de criação

### Passos para Reproduzir
1. Executar `scaffold new --ci --name test-bug15 --domain programming --language python`
2. Verificar `ls -la test-bug15/`
3. Observar que `logs/` não existe

### Sugestão de Correção
Adicionar `logs/` em `DIRS_TO_CREATE` junto com:
```python
DIRS_TO_CREATE = [
    # ... existentes ...
    "tmp",
    "logs",  # ← ADICIONAR
]
```

---

## 🐛 BUG-16: Session-start-first não cria .venv automaticamente

### Descrição
O ritual `session-start-first.prompt.md` foi atualizado (Passo 1.1) para instruir criação de venv, mas **não executa automaticamente** — depende de ação manual do agente.

### Comportamento Esperado
- ✅ Agente executa `uv venv` automaticamente no Passo 1.1
- ✅ `.venv/` criado e ativado
- ✅ Dependências instaladas via `uv pip install -r requirements.txt` (se existir)

### Comportamento Atual
- ⚠️ Passo 1.1 existe mas não é executado automaticamente
- ❌ `.venv/` não criado (requer intervenção manual)
- ❌ Usuário precisa solicitar explicitamente

### Impacto
- **Severidade**: P2 (Baixa) — workaround simples
- **Afeta**: Primeira sessão de novos projetos
- **Workaround**: Executar manualmente `uv venv && source .venv/bin/activate`

### Arquivos Relacionados
- `.github/prompts/session-start-first.prompt.md` — Passo 1.1 (linhas ~180-195)
- Possível solução: Script `scripts/init_all_systems.py` (já existe, verificar se cria venv)

### Análise
O Passo 1.1 foi adicionado com BUG-13, mas é apenas **instrucional** (não executado automaticamente).

**Duas abordagens possíveis**:
1. **Instrucional** (atual): Agente lê e executa quando solicitado
2. **Automatizado**: Script Python que cria venv + instala deps

### Sugestão de Correção
**Opção A** (mais simples):
- Adicionar checklist item: "Executar Passo 1.1 — criar venv"
- Tornar explícito que é ação obrigatória

**Opção B** (automação):
- Modificar `scripts/init_all_systems.py` para incluir venv creation
- Adicionar flag `--create-venv` ao script

---

## 🐛 BUG-17: Interface do chat em Inglês (deveria ser Português)

### Descrição
As mensagens e interface do GitHub Copilot Chat aparecem em **Inglês**, quando o esperado seria **Português** (usuário brasileiro, projeto brasileiro).

### Comportamento Esperado
- ✅ Mensagens do chat em Português (pt-BR)
- ✅ Comandos e sugestões em Português
- ✅ Respostas respeitam idioma do usuário

### Comportamento Atual
- ❌ Interface em Inglês
- ❌ Mensagens system em Inglês

### Impacto
- **Severidade**: P2 (Baixa) — não afeta funcionalidade
- **Afeta**: Experiência do usuário (UX)
- **Tipo**: Configuração VS Code / GitHub Copilot

### Análise
**Não é bug do template** — é configuração do VS Code ou GitHub Copilot Extension.

### Possíveis Causas
1. `locale.language` do VS Code configurado como `en` ou `en-US`
2. GitHub Copilot Extension detectando idioma errado
3. Sistema operacional em inglês (sobrescreve preferências)

### Arquivos Relacionados
- `.vscode/settings.json` — Pode adicionar `"locale.language": "pt-br"`
- Configuração global do VS Code: `File > Preferences > Settings > Locale`
- GitHub Copilot Extension settings

### Sugestão de Correção
**Opção A** (configuração VS Code):
```json
// .vscode/settings.json
{
  "locale.language": "pt-br",
  "copilot.locale": "pt-BR"  // se existir
}
```

**Opção B** (instrução em copilot-instructions.md):
Adicionar em `.github/copilot-instructions.md`:
```markdown
## Idioma
- Responda sempre em **Português do Brasil (pt-BR)**
- Use terminologia técnica apropriada em português
- Traduza termos técnicos apenas quando houver equivalente consagrado
```

**Opção C** (verificar no início de sessão):
Adicionar em `session-start.prompt.md`:
- Verificar `locale.language` em `.vscode/settings.json`
- Se não for `pt-br`, adicionar

---

## 📊 Resumo

| Bug | Título | Severidade | Tipo | Escopo |
|-----|--------|-----------|------|--------|
| BUG-15 | Pasta logs/ não criada | P1 (Média) | Scaffold | create_structure() |
| BUG-16 | Venv não criado automaticamente | P2 (Baixa) | Ritual | session-start-first |
| BUG-17 | Chat em Inglês | P2 (Baixa) | Configuração | VS Code settings |

### Priorização

**P0 (Crítica)**: Nenhum  
**P1 (Alta)**: BUG-15  
**P2 (Média)**: BUG-16, BUG-17

### Estimativas

- BUG-15: 30min (adicionar logs/ em DIRS_TO_CREATE)
- BUG-16: 1h (avaliar abordagem + implementar)
- BUG-17: 15min (adicionar configuração + instrução)

**Total**: ~2h

---

## 🎯 Ações Recomendadas para Próxima Sessão

### 1. Corrigir BUG-15 (P1)
```bash
# Editar scripts/lib/project.py
# Adicionar "logs" em DIRS_TO_CREATE
# Criar logs/README.md ou logs/.gitkeep
# Testar com scaffold new
```

### 2. Avaliar BUG-16 (P2)
- Decidir: instrucional vs automatizado
- Se automatizado: estender init_all_systems.py
- Se instrucional: enfatizar no checklist

### 3. Corrigir BUG-17 (P2)
```bash
# Adicionar em .vscode/settings.json template:
{
  "locale.language": "pt-br"
}

# Adicionar em copilot-instructions.md:
"Sempre responda em Português do Brasil"
```

---

## 📝 Contexto da Sessão Atual

### Bugs Resolvidos (2026-05-13)
- ✅ BUG-11: Session systems não inicializados
- ✅ BUG-12: Memory system não inicializado  
- ✅ BUG-13: Copilot instructions não persistidas
- ✅ BUG-14: Session scripts missing lib dependencies

### Commits
- `4caadd3` — BUG-13
- `4cf4470` — BUG-11/12 (upgrade paridade)
- `d2afdba` — venv ritual
- `03fcb96` — BUG-14
- `c5c7eca` — lembrete.md atualizado

### Status do Template
- ✅ Session-index funcionando (35 arquivos, 339 blocos)
- ✅ Session-time funcionando (23 sessões rastreadas)
- ✅ Memory system operacional
- ✅ Libs de suporte copiadas (4 módulos)
- ✅ Force parameter corrigido em upgrade
- ⚠️ Logs/ não criado por padrão (BUG-15)
- ⚠️ Venv manual no start-first (BUG-16)
- ⚠️ Chat em inglês (BUG-17)

---

**Relatório gerado**: 2026-05-13 13:30  
**Autor**: GitHub Copilot (Claude Sonnet 4.5)  
**Próxima revisão**: Início da próxima sessão
