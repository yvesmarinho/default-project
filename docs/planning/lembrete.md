# Projeto Default Project
# Relação das alterações/correções necessárias.

<!--
Criado em: 01/01/2026 00:00
Modificado em: 26/06/2026 16:00
-->

---

## Duvidas

---

## BUG/Correção

### TaskList — Bugs do Scaffold (novo projeto)

- [x] **BUG-scaffold-claude-agents** `P0` ✅ **RESOLVIDO 26/06/2026** — `copy_speckit()` copia agents (`.github/agents/`) e prompts (`.github/prompts/`) para projetos com `ai_assistant=claude`. Esses são assets exclusivos do GitHub Copilot e **não devem existir** em projetos Claude.
  - **Correção aplicada** (`scripts/lib/project.py`):
    - `copy_speckit()` → agora copia apenas perfis de domínio (`.github/prompts/domain/`) para TODAS as IAs
    - `copy_custom_agents()` → nova função: copia agents customizados (non-`speckit.*`) para `claude`, `copilot`, `both`; ignora `none`
    - `run_speckit_init()` → executa `specify init --integration <IA>` que gera `speckit.*` gerenciados pelo CLI

- [x] **BUG-speckit-via-copy-not-init** `P0` ✅ **RESOLVIDO 26/06/2026** — Todo conteúdo do SpecKit estava sendo copiado manualmente em vez de gerado pelo `specify init`.
  - **Investigação**:
    - `specify init --here --force --integration claude` funciona (exit 0) quando testado como subprocess com `capture_output=True`
    - **Causa do hanging**: stdin herdado do processo pai (TTY interativo) → corrigido com `stdin=subprocess.DEVNULL`
    - **Causa do stderr vazio**: ao falhar, `specify` escreve no stdout; corrigido logando `stderr or stdout` no diagnóstico
    - A falha histórica do teste era do código antigo (antes da refatoração); o CLI funciona corretamente
  - **Separação confirmada** (`specify init --integration copilot` gera apenas arquivos `speckit.*`; nosso `copy_custom_agents()` pula `speckit.*`):
    - `claude` → `.claude/skills/speckit-*/SKILL.md` + `.specify/`
    - `copilot` → `.github/agents/speckit.*.agent.md` + `.github/prompts/speckit.*.prompt.md` + `.specify/`

---

### TaskList — Bugs e Melhorias Gerais

#### Segurança

- [x] **P0 — pre-commit: bloquear IPs internos e credenciais** ✅ **RESOLVIDO 26/06/2026**
  - Hook atualizado com varredura de **conteúdo** dos arquivos staged (Git Guardian rules)
  - Detecta: IPs RFC 1918 (10.x, 172.16-31.x, 192.168.x), loopback, link-local
  - Detecta: chaves PEM, AWS keys, GitHub tokens, credenciais em URL, Bearer tokens, senhas literais
  - Arquivos: `scripts/lib/project.py` (`_PRE_COMMIT_SECRETS_HOOK`) + `scripts/git-hooks/pre-commit`
  - Hook instalado em `.git/hooks/pre-commit` do projeto DEV

#### Templates e Profiles

- [x] **Ansible no `devops-infrastructure`** ✅ Já presente
  - `scaffold/templates/speckit/prompts/domain/devops-infrastructure.prompt.md` já cobre Ansible extensivamente (ansible-lint, playbooks, vault, dry-run)
  - **Verificar se é necessário um perfil separado** `ansible.yaml` similar ao `k8s-helm.yaml` / `terraform-aws.yaml`

- [x] **criar `objetivo-init-minimal.yaml`** ✅ **CONCLUÍDO 26/06/2026**
  - Template enriquecido criado em `scaffold/templates/objetivo/objetivo-init-minimal.yaml`
  - Seções incorporadas do arquivo externo: `regras_projeto`, `regras_gerais`, `ai_safety_instructions`, `infrastructure` (com hardware_spec), `profile` (detalhado com expertise_by_domain), `expected_outcome` (com success_criteria e quality_gates), `pending_tasks` por fases
  - Arquivo de referência: `/home/yves_marinho/Documentos/DevOps/Projetos/ai-local-setup/objetivo-init-minimal.yaml`

- [x] **atualizar `objetivo-init-template.yaml`** ✅ **CONCLUÍDO 26/06/2026**
  - Worktree template atualizado: `.claude/worktrees/agent-a11d9f5d8c2bbb800/template-bases/objetivo-init-template.yaml`
  - Sincronizado com o novo `objetivo-init-minimal.yaml` (mesmo conteúdo enriquecido)

- [x] **`objetivo-init.yaml` sem seção `infrastructure`** ✅ **CONCLUÍDO 26/06/2026**
  - Seção `infrastructure:` removida de `scaffold/templates/objetivo/examples/objetivo-init.yaml`
  - Mesma remoção em `.claude/worktrees/agent-a11d9f5d8c2bbb800/template-bases/examples/objetivo-init.yaml`
  - Dados hardcoded (AWS EKS, RDS) não pertencem ao exemplo genérico

#### Session Start First (`session-start-first.prompt.md`)

- [x] **Sequência incorreta de criação do `.venv` com `uv`** ✅ **CONCLUÍDO 26/06/2026**
  - Corrigido: `uv init` → `uv venv` no Passo 1.1 e no checklist
  - Arquivo: `scaffold/templates/speckit/prompts/session-start-first.prompt.md`

- [x] **Pipeline de verificação do `.venv` no `.gitignore`** ✅ **CONCLUÍDO 26/06/2026**
  - Substituído `grep -q ".venv" .gitignore && echo...` por bloco Python (`pathlib.Path`)
  - Arquivo: `scaffold/templates/speckit/prompts/session-start-first.prompt.md`

- [x] **Pipeline de verificação de pacotes desatualizados** ✅ **CONCLUÍDO 26/06/2026**
  - Substituído `uv pip list | head -20` por Python com `subprocess.run` + slice de lista
  - Arquivo: `scaffold/templates/speckit/prompts/session-start-first.prompt.md`

- [x] **Instrução de substituição de `curl` por Python** ✅ **CONCLUÍDO 26/06/2026**
  - Adicionado callout `⚠️ Regra de Segurança` logo após o `curl` de instalação do `uv`
  - Explica que curl é exclusivo do bootstrap; todas as outras requisições HTTP → Python + requests + `.secrets/`
  - Arquivo: `scaffold/templates/speckit/prompts/session-start-first.prompt.md`

#### Session Start (`session-start..md` / `session-start-first.prompt.md`)

- [x] **`SESSION_DOCS_STYLE_GUIDE.md` ausente em projetos recém-criados** ✅ **CONCLUÍDO 26/06/2026**
  - `setup_project_docs()` agora copia `docs/guides/SESSION_DOCS_STYLE_GUIDE.md` para novos projetos (passo 2b)
  - Caminho corrigido em `session-start.prompt.md`: `docs/SESSION_DOCS_STYLE_GUIDE.md` → `docs/guides/SESSION_DOCS_STYLE_GUIDE.md` (2 ocorrências)
  - Testes: 31 passed (smoke suite), sem regressões

- [x] **Session Time Tracker — integração automática com `session.start`** ✅ **CONCLUÍDO 26/06/2026**
  - Adicionado **Passo 0** em `session-start.prompt.md`: dispara `session-time-tracker.py start` automaticamente, antes da escolha QUICK/COMPLETO
  - Passo 0 marcado ✅ em AMBOS os modos na tabela de passos
  - Passo 6.5 simplificado: apenas verifica session-index (start já ocorreu no Passo 0)
  - Checklists Final (Quick e Completo) atualizados com item de confirmação

#### MCP / Scripts

- [x] **`./scripts/activate-mcp.sh --auto` — erro no servidor GitHub** ✅ **CONCLUÍDO 26/06/2026**
  - **Causa raiz**: `_UNOFFICIAL_GITHUB_ARG_PATTERNS` em `vscode.py` incluía `"github-mcp-server"` sem prefixo — fazia match falso na imagem Docker oficial `ghcr.io/github/github-mcp-server:1.4.0` e a removia como "não oficial"
  - **Correção em `vscode.py`**:
    - Removido `"github-mcp-server"` da lista de padrões não-oficiais
    - Adicionada constante `_OFFICIAL_GITHUB_DOCKER_IMAGE = "ghcr.io/github/github-mcp-server"`
    - `normalize_github_mcp()`: excluir imagem oficial da verificação de padrões
    - Adicionado servidor Docker `"io.github.github/github-mcp-server"` em `_ALL_MCP_SERVERS`
    - `generate_mcp()`: preserva seção `inputs` de arquivos existentes durante merge
  - **`.vscode/mcp.json` atualizado**: servidor Docker adicionado com `${input:github-token}`; seção `inputs` com descrição adequada e `password: true`
  - Testes: 31 passed, sem regressões


#### Scaffold

- [ ] **Como usar o scaffold para projetos legados (anteriores ao scaffold)?**
  - Existe `scaffold.py --objetivo-migrate` para migrar `objetivo.yaml` v1→v2
  - Não há fluxo de "adoção" de projeto legado (equivalente ao `scaffold new` mas retroativo)
  - Decidir: criar comando `scaffold adopt` ou documentar processo manual

- [x] **atualizar lista de pacotes Python necessários: `flake8`** ✅ **CONCLUÍDO 26/06/2026**
  - Diagnóstico: templates `python-flask` e `python-fastapi` já usam `ruff` (que substitui `flake8` + `black` + `isort`); adicionar `flake8` seria redundante
  - Correção: atualizar os prompts para refletir o toolchain real
  - `devops-programming.prompt.md`: tabela, DoD e bloco de comandos atualizados (`flake8` → `ruff check`, `black` → `ruff format`, removido `isort`)
  - `session-end.prompt.md`: `uv run flake8 src/` → `uv run ruff check src/`
  - `CODEOWNERS`: removidas entradas `.flake8`, `.pylintrc`, `.black`; adicionado `pyproject.toml` (onde `ruff` é configurado)


---

## Alterações Futuras

- estrutura do respositório deve ser main, dev e fases. Na automação git, validar se o código está correto para ir para o main.

- shell integration:
  [Code shell integration](https://code.visualstudio.com/docs/terminal/shell-integration)
  ```
  [[ "$TERM_PROGRAM" == "vscode" ]] && . "$(code --locate-shell-integration-path zsh)"
  ```

- Questionar prioridade do projeto em objetivo-init.yaml

- todos os arquivos de template devem estar separados dos arquivos usados no
  projeto, para facilitar distribuição.

- corrigir o objetivo-init-V2.yaml
    - para adiconar a sessão "infrastructure".
    - adiconar padrão de nomenclatura de pastas e arquivos.
    - adicionar padrão de nomenclatura de objetos, classes e funções

- na pasta `./docs` falta as sub-pastas `implemantations`e `bugs`.

- é possivel integrar a atualizações do spec-kit no projeto comando "specify init --here --force --integration copilot"?

- Analisar as informações dos sites abaixo para fazer as devidas atualizações.
  - [Github Copilot Instructions](https://code.visualstudio.com/docs/copilot/customization/custom-instructions)
  - [Agent Skills in VS Vode](https://code.visualstudio.com/docs/copilot/customization/agent-skills) para melhorar a atuação dos agentes.
  - [Custom Agents ](https://code.visualstudio.com/docs/copilot/customization/custom-agents)
  - [manage MCP servers in VS Code](https://code.visualstudio.com/docs/copilot/customization/mcp-servers) habilitar Github MCP para acesso aos repositórios.
  - [Github Copilot in Visual Studio](https://github.blog/changelog/2026-04-30-github-copilot-in-visual-studio-april-update/)

---


## Lembrete das tarefas da sessão (NÃO NECESSITA DE INTERAÇÃO, USO PESSOAL)

---
