---
title: "GitHub Copilot"
source: "https://github.com/copilot/c/d1fbc5b6-07fe-436b-b595-3e1f07955fc2"
author:
  - "[[GitHub]]"
published:
created: 2026-02-27
description: "GitHub is where people build software. More than 150 million people use GitHub to discover, fork, and contribute to over 420 million projects."
tags:
  - "clippings"
---
eu utilizo o VS Code no Linux Mint 22.3. notei as opções abaixo no chat com o Copilot. Informe o que são; - Custom agents - Prompt files - Skilss - Instructions and Rules - Hooks - MCP Servers - Tools sets - Diagnostics - Chat settings

A seguir vai uma visão **técnica e detalhada** do que esses itens normalmente significam **no contexto do GitHub Copilot Chat / Copilot “agent mode” dentro do VS Code** (especialmente nas versões mais novas). Alguns nomes e capacidades variam conforme versão/edição (Copilot Individual/Business/Enterprise), mas a ideia geral é esta.

---

## 1) Custom agents (Agentes personalizados)

São **personas/“modos de operação”** configuráveis que mudam **como o Copilot raciocina, age e responde** para certos tipos de tarefa.

Em termos práticos, um *custom agent* costuma definir:

- **Objetivo** (ex.: “especialista em backend”, “revisor de PR”, “SRE”, “arquiteto”, “security auditor”).
- **Ferramentas permitidas** (ex.: pode usar terminal? pode editar arquivos? pode rodar testes?).
- **Estilo de resposta** (mais curto, mais formal, mais detalhado, linguagem PT/EN etc.).
- **Políticas e limites** (o que evitar, o que sempre fazer).

Em ambientes “agentic”, um agent pode:

- Planejar subtarefas,
- Navegar no workspace,
- Propor/editar múltiplos arquivos,
- Executar ações (dependendo das permissões e do VS Code).

**Para que serve:** padronizar comportamento e *workflow* do Copilot para sua equipe/projeto (ex.: um agent “Revisor de Segurança” sempre verifica OWASP, configurações, secrets, etc.).

---

## 2) Prompt files (Arquivos de prompt)

São arquivos no repositório/workspace que funcionam como **“prompts persistentes” versionáveis**. Eles colocam “contexto e regras” perto do código.

Normalmente incluem:

- Convenções do projeto (arquitetura, pastas, estilo),
- Requisitos (ex.: “usar pytest”, “não usar lib X”),
- Restrições (ex.: “não modificar migrações”),
- Como escrever testes, logs, mensagens de commit,
- Padrões de segurança.

**Diferença para instruções do chat:** prompt files são **compartilháveis via Git**, revisáveis em PR, e podem ser aplicados a múltiplas conversas.

Em muitos setups, esses arquivos ficam em locais como:

- `.github/`
- `.vscode/`
- Raiz do repositório
- Pastas dedicadas a “prompts” (depende do produto/configuração)

---

## 3) Skills (Habilidades)

“Skills” são **capacidades especializadas** que o Copilot/agent pode acionar para executar uma tarefa melhor do que só “gerar texto”.

Exemplos típicos:

- **Code search** (buscar símbolos, classes, referências),
- **Explicar código** com contexto do workspace,
- **Refatorar** preservando testes,
- **Gerar testes** coerentes com o framework do repo,
- **Criar/atualizar arquivos**,
- **Interagir com GitHub** (issues/PRs), quando integrado.

Pense em *skills* como “módulos de competência” do agente: algumas são apenas “técnicas de raciocínio”, outras são ligadas a ferramentas reais.

---

## 4) Instructions and Rules (Instruções e Regras)

É a camada de **governança/política** que orienta o comportamento.

Normalmente existem níveis:

- **Product/system** (hard rules do provedor; segurança, privacidade, etc.)
- **Organização/Enterprise** (políticas corporativas, compliance)
- **Workspace/Repo** (regras do projeto)
- **Usuário** (suas preferências)

Exemplos do que pode estar aqui:

- “Nunca sugerir credenciais em texto”
- “Usar Python 3.12”
- “Preferir libs padrão”
- “Respostas sempre em PT-BR”
- “Sempre escrever testes”
- “Não alterar arquivos em `vendor/` ”

**Por que aparece no UI:** porque o Copilot está se tornando “mais agente” e precisa deixar claro **quais regras estão em vigor**.

---

## 5) Hooks

Hooks são **gatilhos** executados em eventos do fluxo de trabalho do Copilot/agent.

Eventos típicos:

- Antes/depois de uma edição em arquivo
- Antes/depois de executar comandos (quando permitido)
- Antes de submeter um conjunto de mudanças
- Ao abrir uma conversa/ao trocar de contexto

Usos comuns:

- Rodar formatação (ex.: `ruff format`, `prettier`)
- Rodar lint/test antes de “finalizar”
- Validar que não houve inclusão de segredo (secret scanning local)
- Verificar convenções do repo

**Analogia:** como “Git hooks”, mas aplicados ao workflow do *agent*.

---

## 6) MCP Servers (Model Context Protocol servers)

MCP (Model Context Protocol) é um padrão para conectar modelos/agents a **fontes externas de contexto e ações** via servidores.

Um MCP Server normalmente expõe:

- **Resources** (dados/contexto: docs, tickets, páginas internas, inventário)
- **Tools** (ações: criar ticket, consultar API interna, buscar em base de conhecimento, consultar Kubernetes, etc.)
- **Prompts** (templates prontos)

Exemplos do mundo real:

- MCP para Jira/Confluence
- MCP para uma base interna de documentação
- MCP para APIs da empresa
- MCP para cloud (listar buckets, verificar logs, etc.)

**Ponto crítico:** MCP é a ponte para o Copilot “enxergar” e atuar em sistemas externos, com controle de autenticação/permissões.

---

## 7) Tool sets (Conjuntos de ferramentas)

É um agrupamento/seleção do que o Copilot/agent pode usar em um determinado contexto.

Por exemplo, um tool set pode habilitar:

- “workspace tools” (ler/escrever arquivos)
- “terminal tools” (rodar comandos)
- “git tools” (diff, status, branch)
- “web tools” (buscar documentação online)
- “issue tracker tools” (GitHub issues/Jira)

E desabilitar outras para reduzir risco.

**Por que isso importa:** controlar **superfície de ação** do agente (segurança) e melhorar previsibilidade.

---

## 8) Diagnostics (Diagnósticos)

Área para inspecionar e depurar o comportamento do Copilot/agent.

Pode incluir:

- Estado da sessão (modo agent/chat)
- Quais instruções estão ativas
- Quais ferramentas foram chamadas (e com quais parâmetros)
- Logs de falhas de tool/MCP
- Latência, erros de autenticação, timeouts
- Problemas de indexação (ex.: o Copilot não “vê” o repo direito)

**Para você (Linux + VS Code):** é útil quando o Copilot não consegue rodar algo, não encontra arquivos, ou uma integração (MCP) falha.

---

## 9) Chat settings (Configurações do chat)

Configurações que afetam **o comportamento conversacional** e integração com o editor.

Exemplos típicos:

- Idioma das respostas
- Nível de detalhe
- Se pode usar contexto do workspace automaticamente
- Se pode sugerir edições diretas (inline edits)
- Modelo selecionado (quando o produto permite escolher)
- Preferência por explicações vs. apenas código
- Privacidade (ex.: não enviar trechos grandes, limites, etc.)

---

## Como isso tudo se conecta (visão “arquitetural”)

Em geral, o pipeline mental é:

1. **Chat settings** definem comportamento geral.
2. **Instructions & Rules** impõem restrições e padrões.
3. O **agent** (default ou **custom agent**) recebe o objetivo.
4. Ele chama **skills** e **tools** (via **tool sets**) para executar passos.
5. Se precisar de contexto externo, chama **MCP servers**.
6. **Hooks** automatizam ações ao longo do fluxo.
7. **Diagnostics** permite auditar e debugar tudo.

---

## Perguntas rápidas para eu ajustar ao seu caso (Linux Mint 22.3 + VS Code)

Para eu te explicar com precisão **do seu ambiente** (Copilot no VS Code muda bastante por versão), me diga:

1. Qual versão do VS Code (`Help → About`) e do “GitHub Copilot” extension?
2. Você usa Copilot Individual ou via organização (Business/Enterprise)?
3. Você está vendo isso na UI do **Copilot Chat** normal ou do **Agent Mode** (quando disponível)?

Se você responder, eu descrevo **o que exatamente está habilitado pra você**, o que é só “feature flag” visível no menu, e como configurar/usar cada item no Linux Mint.

Qual versão do VS Code (Help → About) e do “GitHub Copilot” extension? V 1.109.5 (sempre atualizado pelo pacotde apt) Você usa Copilot Individual ou via organização (Business/Enterprise)? Individual Você está vendo isso na UI do Copilot Chat normal ou do Agent Mode (quando disponível)? Vi essas opções no chat do Copilot dentro do VS Code.

Com VS Code **1.109.5** (canal apt) + Copilot **Individual**, essas opções que você viu no painel do **Copilot Chat** no VS Code representam, em grande parte, a “infraestrutura” nova do Copilot (chat + modo agente + extensibilidade). Mesmo no plano Individual, muita coisa aparece na UI porque o VS Code/Copilot compartilha o mesmo “esqueleto” de recursos; o que muda é **o que fica habilitado** (por permissões, disponibilidade regional, feature flags e se você instalou extensões/servidores MCP).

Abaixo explico cada item com foco no **VS Code** e no que normalmente você consegue fazer no **Individual**.

---

## 1) Custom agents

No VS Code, “custom agents” são **configurações de agentes** (perfis) que você escolhe para conversar/trabalhar.

### O que muda quando você escolhe um agent

- **Objetivo e “papel”**: ex. “code reviewer”, “pair programmer”, “security”.
- **Estratégia**: mais perguntas antes de agir, ou agir direto.
- **Formato**: respostas curtas vs. longas, mais código vs. mais explicação.
- **Ferramentas** (quando disponível): se pode ou não fazer edições, rodar ações, etc.

### No Copilot Individual

- Você normalmente consegue usar **agentes padrão** oferecidos pela extensão.
- “Custom” pode significar:
	- agentes fornecidos por extensões,
	- ou agentes definidos por configuração local (depende do build/flags).
- Nem sempre dá para “criar” agentes complexos via UI sem recursos enterprise; às vezes aparece o menu, mas as opções avançadas ficam limitadas.

**Resumo:** é um seletor de “modo/personalidade/capacidades” do Copilot.

---

## 2) Prompt files

São arquivos no seu projeto (workspace) que o Copilot lê para obter **contexto persistente**.

### Para que servem

- Evitar repetir: “use pytest”, “padrão de logs”, “não use ORM X”.
- Garantir consistência: arquitetura, convenções, camadas.
- Padronizar respostas para todo mundo do repo (se versionado).

### Como isso aparece no VS Code

O Copilot Chat pode:

- Detectar automaticamente arquivos “conhecidos” de instrução, ou
- Permitir que você aponte “prompt files” manualmente (depende da versão).

**Resumo:** “documentos de instrução do projeto” que alimentam o chat.

---

## 3) Skills

No VS Code/Copilot, “skills” são **capacidades internas** (ou plugáveis) que o Copilot usa para cumprir tarefas.

Exemplos típicos de skills no contexto do editor:

- **Pesquisar símbolos/arquivos** no workspace (indexação).
- **Gerar/ajustar código** mantendo estilo do repo.
- **Explicar um trecho selecionado** com base em referências.
- **Refatorar** (às vezes com múltiplos arquivos).

No Individual, você usa skills “por trás” sem perceber; o menu indica que o Copilot está organizado em “competências” e pode habilitar/desabilitar algumas dependendo do cenário.

**Resumo:** “o que o Copilot sabe fazer” como módulos.

---

## 4) Instructions and Rules

É o conjunto de **regras ativas** que governam o comportamento do Copilot naquela conversa/workspace.

Fontes comuns:

- Preferências do usuário (idioma, estilo)
- Regras do workspace/repo
- Regras do produto (segurança, privacidade)
- Regras de extensões (ex.: uma extensão impõe padrões)

Você viu isso porque o VS Code está dando mais transparência: “quais instruções estão valendo agora?”.

**Resumo:** “políticas” e “convenções” que o Copilot deve obedecer.

---

## 5) Hooks

Hooks são **gatilhos automáticos** no fluxo do agent/chat.

Eventos possíveis:

- Antes/depois de aplicar uma sugestão no código
- Antes/depois de rodar uma ação/ferramenta
- Ao concluir uma tarefa

Uso típico:

- Autoformat/lint/test após gerar código
- Checar padrões do repo
- Validar que não introduziu segredos

### No Individual

Pode aparecer, mas:

- hooks avançados podem depender de modo agente, permissões e integrações.
- alguns hooks só ficam ativos se você habilitar features específicas.

**Resumo:** “automação baseada em eventos” acoplada ao trabalho do Copilot.

---

## 6) MCP Servers

MCP Servers são servidores que implementam o **Model Context Protocol**, permitindo ao Copilot acessar **contexto e ferramentas externas**.

Pense assim: sem MCP, o Copilot vê basicamente:

- seu chat,
- arquivos abertos/selecionados,
- e recursos internos do VS Code.

Com MCP, ele pode (se autorizado):

- Consultar documentação interna/externa estruturada
- Interagir com APIs (Jira, Confluence, GitHub, Kubernetes, etc.)
- Buscar dados em bancos/serviços (controlado por permissões)

### No Individual

Você pode usar MCP se:

- o VS Code/Copilot da sua versão suportar,
- e você configurar/instalar um MCP server (local ou remoto),
- e der credenciais/permissões.

**Resumo:** “conectores” padronizados para dados e ações fora do editor.

---

## 7) Tool sets

Tool sets são **conjuntos de ferramentas** que o Copilot/agent pode usar.

Exemplos de ferramentas (internas/externas):

- Ler/escrever arquivos do workspace
- Rodar comandos (terminal) — quando habilitado
- Pesquisar no repositório
- Chamar MCP tools (vindas de MCP servers)

Um “tool set” pode ser:

- “Somente leitura” (baixo risco)
- “Edição de arquivos” (médio risco)
- “Terminal + edição + rede” (alto poder/alto risco)

**Resumo:** “perfil de permissões e capacidades de ferramentas”.

---

## 8) Diagnostics

É a área para **auditar e depurar** o Copilot Chat/Agent.

Normalmente mostra:

- Estado de sessão (chat vs agent)
- Quais rules/instructions foram aplicadas
- Quais tools foram chamadas (e erros)
- Falhas de indexação do workspace
- Logs de MCP (se houver)

Para você, isso é essencial quando:

- Copilot “não encontra” arquivos
- MCP falha
- sugestões parecem ignorar regras do projeto

**Resumo:** “logs e telemetria local do Copilot no VS Code”.

---

## 9) Chat settings

Configurações específicas do chat do Copilot dentro do VS Code.

Costuma incluir:

- Idioma das respostas
- Nível de detalhamento
- Se pode usar contexto do workspace automaticamente
- Se permite sugerir/aplicar mudanças
- Seleção de modelo (quando disponível)
- Comportamento de privacidade/telemetria (dependendo do produto)

**Resumo:** “preferências do chat” (como ele conversa e usa contexto).

---

## O que é mais provável no seu cenário (Individual + Linux Mint + VS Code 1.109.5)

- Você está vendo uma UI unificada que suporta **chat normal e modo agente**.
- Nem tudo estará 100% habilitado para agir (especialmente itens como hooks automáticos e tool sets “mais perigosos”), mas a **estrutura aparece**.
- **MCP Servers** é o item mais “novo” e mais dependente de configuração manual/instalação.

---

## Se você quiser, eu posso ser bem objetivo e prático

Diga qual você quer aprofundar primeiro:

1. **Como habilitar/configurar MCP Servers no VS Code** no Linux Mint (incluindo onde fica config, como rodar servidor local, riscos e permissões), ou
2. **Como criar e aplicar prompt files/instructions** para o Copilot sempre seguir suas regras (estilo, padrões, testes), ou
3. **Como ver/usar Diagnostics** para entender o que o Copilot está fazendo e por que ele ignora algo.

Se você mandar um print dessas opções no seu VS Code (painel do chat), eu também consigo mapear exatamente para os componentes/menus da sua versão.

como posso configurar essas opções por projeto, já que sou DevOps, mudo de assunto/código com frequencia.

Você quer “isolar” comportamento do Copilot **por projeto/workspace**, porque como DevOps você alterna entre repositórios/assuntos. No VS Code isso é viável, mas depende de **três camadas**:

1. **Configuração do VS Code por workspace** (`.vscode/settings.json`)
2. **Instruções por repositório** (prompt files / instruction files versionáveis)
3. **Integrações por workspace** (MCP servers e tool sets), quando suportados na sua versão/feature flags

A seguir vai um guia prático e bem técnico, focado no que costuma funcionar no VS Code 1.109.x + Copilot Individual.

---

## 1) Base: usar Workspace Settings (por projeto)

No VS Code, quase tudo que é “configuração” pode ser gravado por projeto em:

- **Workspace**: `<repo>/.vscode/settings.json` (ou arquivo `.code-workspace`)
- **User settings**: global (não é o que você quer)

### Como ajustar

1. Abra o projeto no VS Code
2. `Ctrl+,` (Settings)
3. No topo, mude o escopo para **Workspace** (não User)
4. Pesquise por “copilot”, “chat”, “github copilot”
5. Ajuste o que houver disponível e o VS Code gravará em `.vscode/settings.json`

Isso te dá isolamento imediato por repo.

### O que dá para controlar por workspace (tipicamente)

- Habilitar/desabilitar Copilot em linguagens específicas
- Preferências do Chat (quando expostas como settings)
- (Às vezes) se o chat usa contexto do workspace, etc.

> Observação importante: nem todo item do menu (“Custom agents”, “Hooks”, “Tool sets”) vira setting simples. Parte é “estado do chat”, parte é “capacidade do produto”.

---

## 2) Prompt files / Instructions por projeto (o que mais resolve seu caso)

O que você quer, na prática, é: **cada repo ter suas próprias regras** (estilo, segurança, ferramentas, padrões), para você não ficar reexplicando contexto toda hora.

### Estratégia recomendada

Crie no repositório um arquivo de instruções do Copilot (ou um conjunto). Mesmo que a sua versão não tenha “auto-discovery” perfeito, você pode:

- manter esses arquivos como padrão do repo;
- e copiar/colar ou referenciar no começo da conversa;
- ou usar “Prompt files” quando a UI suportar.

#### Exemplo do que colocar (DevOps)

- Padrões de IaC (Terraform, Ansible)
- Cloud alvo (AWS/Azure/GCP)
- Convenções de naming/tagging
- Regras de segurança (nunca gerar secrets, sempre usar SOPS, Vault, etc.)
- Padrão de pipelines (GitHub Actions/GitLab CI/Jenkins)
- Observabilidade (Prometheus labels, Loki, OpenTelemetry)
- Padrões Kubernetes (kustomize/helm, namespaces, PSP/PSS)
- “Definition of Done” (lint + validate + plan + policy check)

### Onde colocar

Sugestões (versionáveis):

- `.github/copilot-instructions.md` (muito comum em práticas modernas, quando suportado)
- `docs/copilot/` com múltiplos prompts
- `.vscode/` se for algo específico do editor

Mesmo que o nome exato que o Copilot auto-leia varie, **o efeito organizacional** é excelente: ao entrar no repo, você tem “a cartilha” pronta.

---

## 3) Custom agents por projeto: o que é realista hoje

No Copilot Individual, “custom agents” frequentemente são:

- seleção de agentes fornecidos pelo produto
- agentes expostos por extensões
- alguns cenários permitem “templates” e perfis, mas nem sempre versionáveis por repo

### O que você pode fazer por projeto (workaround robusto)

- Criar “perfis” via *prompt file* e iniciar a conversa com:
	- “Use as instruções do arquivo X e atue como SRE/DevOps…”
- Ter 2 ou 3 arquivos padrão:
	- `PROMPT-devops.md`
	- `PROMPT-security.md`
	- `PROMPT-review.md`

E você escolhe conforme o repo.

---

## 4) MCP Servers por projeto (quando disponível)

Se o seu VS Code/Copilot estiver com MCP habilitado, o ideal é:

- ter uma configuração por workspace apontando para MCP servers diferentes (por exemplo, um MCP para AWS em um repo e outro MCP para Kubernetes em outro)

O problema: **o formato e local exato da configuração MCP** ainda varia por versões/implementações. Em geral, existem dois modelos:

1. **Config global do VS Code/Extensão** (User settings) – ruim para seu caso
2. **Config por workspace** (preferível) – quando suportado

### Estratégia DevOps segura

- Use MCP por projeto apenas para coisas “read-only” ou bem controladas
- Prefira tool sets restritos (sem ações destrutivas)
- Separe credenciais por workspace (profiles AWS, kubeconfig específico, etc.)

---

## 5) Tool sets e Hooks por projeto (prática recomendada)

Quando hooks/tool sets estão disponíveis, o melhor uso em DevOps é padronizar automações “pós-geração”:

- Se o Copilot criar Terraform: rodar `terraform fmt` + `terraform validate`
- Se criar Helm chart: rodar `helm lint`
- Se mexer em YAML K8s: rodar `kubeconform` / `kubeval` / `kustomize build`
- Se mexer em Ansible: `ansible-lint`
- Se mexer em Python: `ruff`, `pytest`

Mesmo que o Copilot não acione hooks automaticamente, você pode configurar **tasks por workspace** e rodar com 1 comando.

### VS Code Tasks por projeto (muito útil)

Crie `.vscode/tasks.json` com tarefas “validate”, “lint”, “plan”.

Isso não é “hook do Copilot” necessariamente, mas é o equivalente prático: após o Copilot gerar algo, você roda a task do projeto.

---

## 6) Um modelo operacional (que funciona mesmo sem features “mágicas”)

Para cada repo/workspace, crie:

1. `.vscode/settings.json`
	- habilita/desabilita Copilot por linguagem conforme repo
2. `docs/copilot/` com prompts:
	- `base.md` (regras gerais)
	- `devops.md` (padrões DevOps)
	- `security.md` (hardening/policy)
3. `.vscode/tasks.json` com:
	- `lint`, `validate`, `test`, `plan`
4. (opcional) `.vscode/extensions.json` recomendando extensões do repo
5. (opcional) arquivo `.envrc` /direnv ou `mise` /asdf para padronizar runtime por repo

Esse kit te dá “projeto autocontido”.

---

## 7) Eu consigo te dizer exatamente o que dá para setar por workspace no seu VS Code

Mas preciso de um detalhe: o VS Code expõe settings específicos com nomes exatos.

Faça assim no seu projeto:

1. Abra Settings (`Ctrl+,`)
2. Procure por: **“copilot”**, **“github.copilot”**, **“chat”**, **“copilot chat”**
3. No canto direito de um setting, clique na engrenagem → **Copy Setting as JSON**
4. Cole aqui os nomes das chaves (só as chaves, sem valores sensíveis)

Com isso eu:

- te devolvo um `.vscode/settings.json` por projeto bem estruturado
- te digo quais dessas opções do menu (agents/prompt files/skills/hooks/MCP/tool sets) são de fato configuráveis na sua instalação e quais são apenas UI/feature flag.

Se você preferir, envie um print da tela de settings filtrada por “copilot” (pode ocultar info pessoal).