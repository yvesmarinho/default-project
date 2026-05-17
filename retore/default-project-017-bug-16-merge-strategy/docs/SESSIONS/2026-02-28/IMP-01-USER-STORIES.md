# 📖 IMP-01 — User Stories: `scaffold.py`

**Data**: 2026-02-28
**Versão**: 1.0.0
**Status**: 😂 Revisado — entradas corrigidas (scaffold.py direto, sem make)
**Debate de origem**: [IMP-01-DEBATE.md](IMP-01-DEBATE.md)
**Spec técnica**: [IMP-01-SPEC.md](IMP-01-SPEC.md)

---

## 👤 Personas

| Persona | Descrição |
|---------|-----------|
| **Yves (Dev/DevOps)** | Usuário principal — cria e mantém múltiplos projetos, alterna entre domínios (programação, infra, análise), usa VS Code + Copilot diariamente |
| **CI/CD Pipeline** | Sistema automatizado que clona o template e inicializa projetos sem interação humana |

---

## 📚 User Stories

---

### US-01 — Criar novo projeto a partir do template

**Como** Yves,
**Quero** rodar um único comando (`uv run scripts/scaffold.py`) no repositório recém-clonado,
**Para** ter o projeto completamente configurado sem precisar lembrar de múltiplos passos manuais.

> **Por quê não `make init`?**
> O `Makefile` é o dono de build/test/CI. O `scaffold.py` é o dono do scaffolding do projeto.
> Domínios separados = zero ambiguidade sobre onde está a lógica.

#### Critérios de Aceite

- [ ] `uv run scripts/scaffold.py` abre o script em modo interativo
- [ ] `python scripts/scaffold.py` funciona como alternativa (deps já instaladas)
- [ ] O script me guia com perguntas claras, exibindo sugestão de valor padrão entre `[colchetes]`
- [ ] Ao final, exibo um resumo visual de tudo que foi criado
- [ ] A estrutura de pastas completa é criada corretamente (ver FEATURE-03 no DEBATE)
- [ ] Posso cancelar a qualquer momento com `CTRL+C` sem deixar o projeto em estado inconsistente

#### Fluxo Feliz

```
$ uv run scripts/scaffold.py

  ╭─────────────────────────────────────────╮
  │  🚀 Enterprise Project Scaffold  v1.0    │
  ╰─────────────────────────────────────────╯

  [1] Criar novo projeto
  [2] Verificar links do projeto atual
  [3] Gerar .copilot-rules para este projeto
  [4] Sair

  Escolha: 1

  Nome do projeto (slug kebab-case): my-api-v2
  Título legível [My Api V2]: My API v2
  Descrição breve: REST API for payments processing
  Repositório GitHub (Enter para pular): https://github.com/user/my-api-v2
  Domínio [1] Programação [2] Infraestrutura [3] Análise: 1
  Linguagem [1] Python [2] TypeScript [3] Go [4] Outro: 1
  Dir. compartilhado [~/Documentos/DevOps/.copilot-shared]: (Enter)

  ┌─ Resumo ──────────────────────────────────────────────────┐
  │  Projeto : my-api-v2                                       │
  │  Domínio : Programação                                     │
  │  Lang    : Python                                          │
  │  Repo    : https://github.com/user/my-api-v2              │
  └────────────────────────────────────────────────────────────┘

  Confirmar? (s/n): s

  ✅ docs/                     criado
  ✅ .github/prompts/domain/   criado
  ✅ .secrets/                 criado
  ✅ README.md                 criado
  ✅ docs/INDEX.md             criado
  ✅ docs/TODO.md              criado
  ✅ .copilot-rules.md         symlink → ../.copilot-shared/.copilot-rules.md
  ✅ .copilot-strict-rules.md  symlink → ../.copilot-shared/.copilot-strict-rules.md
  ✅ .copilot-rules-my-api-v2.md gerado
  ✅ git init                  inicializado
  ✅ git remote add origin     https://github.com/user/my-api-v2

  🎉 Projeto my-api-v2 criado com sucesso!

  📋 Próximos passos:
     1. Abra o arquivo .copilot-rules-my-api-v2.md e adicione regras específicas
     2. Configure o .vscode/mcp.json com suas credenciais
     3. Execute: make check-links para verificar os symlinks
```

---

### US-02 — Verificar se os symlinks Copilot estão funcionando

**Como** Yves,
**Quero** checar rapidamente se os arquivos `.copilot-*` estão linkados corretamente,
**Para** não perder tempo debugando por que o Copilot não está seguindo as regras.

#### Critérios de Aceite

- [ ] `uv run scripts/scaffold.py --check` exibe status de cada symlink em tabela colorida
- [ ] Links ok → ✅ verde
- [ ] Links quebrados → ❌ vermelho com caminho do target esperado
- [ ] Links faltando → ⚠️ amarelo com instrução de como criar
- [ ] Saída legível por humanos; código de saída 0 se tudo ok, 1 se algum problema
- [ ] Pode ser rodado quantas vezes quiser (operação de leitura, nada é modificado)

#### Fluxo Feliz

```
$ uv run scripts/scaffold.py --check

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  🔗 Verificação de Symlinks Copilot — my-api-v2                         │
  ├──────────────────────────────────┬────────────┬──────────────────────── ┤
  │  Arquivo                         │  Status    │  Target                 │
  ├──────────────────────────────────┼────────────┼─────────────────────────┤
  │  .copilot-rules.md               │  ✅ OK     │  .../.copilot-rules.md  │
  │  .copilot-git-rules.md           │  ✅ OK     │  .../.copilot-rules.md  │
  │  .copilot-strict-enforcement.md  │  ❌ QUEBRADO│  target não existe      │
  │  .copilot-strict-rules.md        │  ⚠️ FALTANDO│  symlink não criado     │
  │  .copilot-file-rules.sh          │  ✅ OK     │  .../.copilot-rules.md  │
  └──────────────────────────────────┴────────────┴─────────────────────────┘

  2 problemas encontrados. Execute: `uv run scripts/scaffold.py` para recriar os symlinks.
```

---

### US-03 — Recriar `.copilot-rules-[projeto].md` sem recriar todo o projeto

**Como** Yves,
**Quero** poder regenerar o arquivo de regras Copilot específico do projeto,
**Para** quando eu quiser atualizar os metadados sem fazer um setup completo.

#### Critérios de Aceite

- [ ] Opção [3] no menu ou `uv run scripts/scaffold.py --mode generate-rules` regenera apenas o `.copilot-rules-*.md`
- [ ] Se o arquivo já existe, pergunta antes de sobrescrever
- [ ] Exibe o caminho do arquivo gerado ao final

---

### US-04 — Inicializar projeto via pipeline CI/CD sem interação humana

**Como** a Pipeline de CI,
**Quero** passar todos os parâmetros do projeto por linha de comando,
**Para** criar a estrutura do projeto sem nenhum prompt interativo.

#### Critérios de Aceite

- [ ] `--ci` flag desativa todos os prompts
- [ ] Campos obrigatórios ausentes causam erro claro e código de saída 1
- [ ] Campos opcionais ausentes usam valores padrão sem erro
- [ ] Saída em texto plano (sem cores ANSI) quando `TERM=dumb` ou `NO_COLOR=1`

#### Exemplo de Uso

```bash
python scripts/scaffold.py --ci \
  --name my-new-service \
  --domain programming \
  --language python \
  --repo https://github.com/org/my-new-service \
  --shared-dir /opt/copilot-shared \
  --target-dir /opt/projects/my-new-service
```

---

### US-05 — Não perder trabalho existente ao rodar o script novamente

**Como** Yves,
**Quero** rodar `uv run scripts/scaffold.py` num projeto já inicializado não destrua nada,
**Para** poder rodar o script de setup com segurança mesmo em projetos em andamento.

#### Critérios de Aceite

- [ ] Arquivos existentes → `skipped` (não sobrescritos)
- [ ] Pastas existentes → mantidas sem erro
- [ ] Symlinks corretos → `skipped`
- [ ] Git já inicializado → `skipped` (sem `git init` duplo)
- [ ] Ao final, lista mostra quais itens foram criados e quais foram pulados
- [ ] O script **não** pede confirmação antes de pular — pular é sempre seguro

---

### US-06 — Entender o que o script faz antes de executar

**Como** Yves (ou um novo colaborador),
**Quero** rodar `python scripts/scaffold.py --help` e entender tudo,
**Para** não precisar ler código ou documentação externa para usar o script.

#### Critérios de Aceite

- [ ] `--help` mostra todos os modos e flags com descrições claras em português
- [ ] Exemplos de uso incluídos na ajuda
- [ ] `--version` mostra versão do script

---

### US-07 — Ver o log do que foi feito

**Como** Yves,
**Quero** consultar um arquivo de log com o histórico de execuções do `scaffold.py`,
**Para** ter rastreabilidade de quando e como os projetos foram criados.

#### Critérios de Aceite

- [ ] Log em `scripts/logs/scaffold.log` (respeitando o `.gitignore` para `*.log`)
- [ ] Cada execução começa com uma linha de separação e timestamp
- [ ] Nível WARNING por padrão; DEBUG com `--debug` flag
- [ ] Log não cresce indefinidamente — rotaciona em 2MB, mantém 3 arquivos

---

## 🗺️ Mapa de Cobertura: User Stories × Features

| User Story | FEAT-01 Novo Projeto | FEAT-02 Symlinks | FEAT-03 Estrutura | FEAT-04 Rules | FEAT-05 Check | FEAT-06 CLI |
|------------|:-------------------:|:----------------:|:-----------------:|:-------------:|:-------------:|:-----------:|
| US-01 | ✅ | ✅ | ✅ | ✅ | — | ✅ |
| US-02 | — | — | — | — | ✅ | ✅ |
| US-03 | — | — | — | ✅ | — | ✅ |
| US-04 | ✅ | ✅ | ✅ | ✅ | — | ✅ |
| US-05 | ✅ | ✅ | ✅ | ✅ | — | — |
| US-06 | — | — | — | — | — | ✅ |
| US-07 | ✅ | ✅ | ✅ | ✅ | ✅ | — |

---

## 📋 Backlog de User Stories Futuras (post-MVP)

| ID | Como | Quero | Para | Fase |
|----|------|-------|------|------|
| US-08 | Yves | Ver a estrutura do projeto sendo criada em tempo real (árvore animada) | Ter feedback visual imediato | Fase 3 (TUI) |
| US-09 | Yves | O `scaffold.py` criar o repositório no GitHub automaticamente | Ter o repositório pronto sem sair do terminal | Fase 3 |
| US-10 | Yves | O `scaffold.py` gravar o profile do projeto no MCP `memory` | A IA carregar contexto do projeto automaticamente na próxima sessão | Fase 3 |
| US-11 | Yves | Ver histórico de todos os projetos criados pelo `scaffold.py` | Ter um inventário de projects | Fase 2 |

---

*Arquivo gerado em 2026-02-28 | Feature Engineer | Sessão: [DAILY_ACTIVITIES_2026-02-28.md](DAILY_ACTIVITIES_2026-02-28.md)*
