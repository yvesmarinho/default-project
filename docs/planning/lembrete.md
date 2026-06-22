# Projeto Default Project
# Relação das alterações/correções necessárias.

---

## Duvidas
- é possível separa ambiente DEV de VERSÃO, para que cada ambinte tenha os
  arquivos necessários a cada ambiente?

---

## BUG/Correção

- **P0 - atualizar o projeto para utilizar a IA Claude, com configurações globais e locais.**


- completar o modelo `objetivo-init-minimal.yaml` com os dados do arquivos `/home/yves_marinho/Documentos/DevOps/Projetos/ai-local-setup/objetivo-init-minimal.yaml` que está avançado. 

- adicionar instrução para substituir o comando "curl" do linux por código python especifico.

- shell integration:
  [Code shell integration](https://code.visualstudio.com/docs/terminal/shell-integration)
  ```
  [[ "$TERM_PROGRAM" == "vscode" ]] && . "$(code --locate-shell-integration-path zsh)"
  ```

- corrigir a criação do .venv com a sequencia correta do uv:
  - `uv init`
  - `uv venv`

- atualizar lista de pacotes python necessários:
  - flake8

- erro no comando que verifica se os pacotes pythos estão atualizados!! 
  substituir comando com pipeline por shell-script.

- na execução session.start-first apresentou erro no comando pipiline de verificação 
  do `.venv` no arquivo .gitignore. substituir comando com pipeline por shell-script.

- erro no `./scripts/activate-mcp.sh --auto` informa que o JSON não é valido, porém está correto.
  está apresentando erro no servidor Github

- na verificação de pacotes desatualizados do python utiliza comando com pipe, deve ser um código python!

- o `session.start` completo apresentou erro de arquivo faltando em projeto recem criado.
  ```
  SESSION_DOCS_STYLE_GUIDE.md não disponível (projeto não usa template default-project)
  ```

- como usar o scaffold para projetos legados anteriores ao scaffold?

- session time tracker deve guardar a datetime do inicio do session.start para iniciar o time track.

- objetivo-init.yaml mão tem sessão de `infrastructure`


---

## Alterações Futuras

- estrutura do respositório deve ser main, dev e fases. Na automação git, validar se o código está correto para ir para o main.

- shell integration

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
