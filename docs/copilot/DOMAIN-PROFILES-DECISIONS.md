# Domain Profiles DevOps — Questões e Decisões

**Data**: 2026-02-27
**Atualizado**: 2026-02-27 (D-19 respondida — todas as decisões concluídas)
**Status**: 🟢 Completo — 19 decisões respondidas, 0 abertas
**Referência**: [DOMAIN-PROFILES-STRATEGY.md](DOMAIN-PROFILES-STRATEGY.md)

---

## ⚡ Decisão Imediata (Antes de Criar Qualquer Arquivo)

### D-01 — Por qual domínio começar?

**Contexto**: Há três domínios (programação, infraestrutura, análise). Criar os três de uma vez gera overhead sem validação. Começar por um permite iterar antes de generalizar.

**Opções**:

| Opção | Pro | Contra |
|-------|-----|--------|
| **Infraestrutura primeiro** | É onde o MCP mais agrega (AWS, K8s); é o domínio mais diferente dos outros | Mais complexo para modelar (mais variáveis de ambiente) |
| **Programação primeiro** | Mais fácil de validar (ciclo de feedback rápido com testes) | Menos diferenciação — Copilot já ajuda bem em código sem profile |
| **Análise primeiro** | Menos representado em ferramentas de IA; maior ganho diferencial | Mais difícil de estruturar (outputs menos previsíveis) |

**Pergunta para você**: Qual dos três domínios consome mais energia sua hoje por falta de contexto persistente?

**Resposta**: A melhor forma de resolver esse problema é ter um código python
 como o exemplo `scripts/manage.py`utilizado no projeto `Enterprise-ansible` para guiar o usuário no inicio do projeto.

---

## 🏗️ Questões de Arquitetura

### D-02 — Onde ficam os Domain Profiles?

**Contexto**: Domain Profiles podem viver em dois lugares com comportamentos diferentes no Copilot.

| Local | Lido automaticamente? | Versionável? | Escopo |
|-------|-----------------------|--------------|--------|
| `.github/prompts/domain/` | Sim (via `chat.promptFilesRecommendations`) | Sim | Workspace |
| `docs/copilot/` | Não (referência manual) | Sim | Documentação |
| `.vscode/` | Depende da configuração | Sim | Workspace |

**Decisão necessária**: Usar `.github/prompts/domain/` como local primário (machine-readable) e `docs/copilot/` como documentação longa (human-readable)?

**Resposta**: Aceito a proposta acima, usar `.github/prompts/domain/` e `docs/copilot/`.

---

### D-03 — O `speckit.clarify` deve detectar o domínio ou você declara?

**Contexto**: Há dois modelos de ativação do Domain Profile.

**Modelo A — Declarativo (você ativa)**
```
"Modo: INFRAESTRUTURA. Contexto: instalação Grafana no staging."
```
- Simples, funciona hoje, sem modificar nada
- Depende de disciplina sua para sempre declarar

**Modelo B — Detectivo (clarify pergunta)**
```
speckit.clarify: "Qual tipo de trabalho é este?
(a) Código/programação  (b) Infraestrutura  (c) Análise/investigação"
```
- Requer modificar o `speckit.clarify.prompt.md`
- Garante que nunca esquece de ativar o profile

**Modelo C — Inferido (clarify detecta pelo pedido)**
- Copilot lê o pedido inicial e infere o domínio
- Mais sofisticado, mas pode errar sem fallback

**Decisão necessária**: Qual modelo de ativação adotar inicialmente?

**Resposta**: Deve ser declarado, vide D-01

---

### D-04 — Os Speckit templates (spec, plan, tasks, checklist) devem ter versões por domínio?

**Contexto**: Atualmente há um único template de cada tipo em `.specify/templates/`. Para Domain Profiles serem totalmente efetivos, cada template deveria ter variantes.

**Exemplo do impacto**:

| Template | Genérico (hoje) | Com Domain Profiles |
|----------|-----------------|---------------------|
| `spec-template.md` | Requisitos funcionais genéricos | Infra: recursos, SLO, segurança / Código: interfaces, comportamentos / Análise: escopo, hipóteses |
| `checklist-template.md` | Checklist genérico de done | Infra: `terraform plan`, `helm lint`, alerta, runbook / Código: testes, lint, tipos / Análise: hipótese validada, owner definido |

**Opções**:
- **A**: Criar templates específicos por domínio (`.specify/templates/infra/`, `code/`, `analysis/`)
- **B**: Criar um único template com seções condicionais por domínio (mais complexo de manter)
- **C**: Manter templates genéricos e deixar o Domain Profile instruir o agente a preencher conforme o contexto (menor esforço inicial)

**Resposta**: Opção C. O Objetivo é ter o template de projeto universal. Utilizar Prompt files, Skilss, Instructions and Rules e o que mais for necessário para tornar o ambiente e a IA focado na necessidade do projeto.
Ter templates com questinamento, dessa forma a IA toma as decisões e atualiza todos os demais arquivos necessários. No projeto `enterprise-ansible`pedi para criar uma código python para ajudar o usuário a fornecer as informações necessárias a cada uma das tarefas. Vide D-01.

---

### D-05 — Nível de detalhe dos Domain Profiles

**Contexto**: Profiles muito longos sobrecarregam o contexto e podem ser ignorados. Profiles muito curtos não discriminam bem.

**Pergunta**: Qual é o nível certo de detalhe para o seu caso?

| Nível | O que contém | Tamanho estimado |
|-------|-------------|------------------|
| **Essencial** | Cloud provider, ferramenta IaC, ambiente, naming convention, DoD | ~50 linhas |
| **Completo** | Tudo acima + exemplos, anti-patterns, referências internas, políticas de segurança | ~150-200 linhas |
| **Dinâmico** | Apenas o esqueleto e os valores são injetados via MCP ou variáveis de sessão | ~30 linhas + dados externos |

**Resposta**: Completo e Dinâmico, não importa o tamanho do arquivo. O foco principal é ter memórias completas dos itens e das ações tomadas por sessão.

---

## 🔌 Questões sobre MCP

### D-06 — Quais MCP Servers ativar primeiro?

**Contexto**: O `.vscode/mcp.json` tem 7 servidores configurados (comentados). Ativar todos de uma vez é arriscado e dificulta diagnosticar problemas.

| MCP | Domínio | Dependência | Risco |
|-----|---------|-------------|-------|
| `memory` | Todos | `npx` | Baixo |
| `sequential-thinking` | Todos | `npx` | Baixo |
| `filesystem` | Todos | `npx` | Médio (escopo de acesso) |
| `github` | Código, Análise | `GITHUB_PERSONAL_ACCESS_TOKEN` | Médio |
| `aws` | Infraestrutura | AWS credentials | Alto (ações reais) |
| `kubernetes` | Infraestrutura | kubeconfig | Alto (ações reais) |
| `brave-search` | Análise | `BRAVE_API_KEY` | Baixo |

**Decisão necessária**: Ativar `memory` e `sequential-thinking` imediatamente (já configurados como ativos)? Quais mais ativar na próxima sessão?

**Resposta**: Eu que memória, para que seja carregado o profile de cada projeto, sem a necessidade de ter de informar tudo novamente.
Os prompts abaixo são um exemplo de como a memória e importante nos meu projetos:

#### Inicio
```
- iniciar mcp.
- Recuperar dados da sessão anterior na memória mcp e nos arquivos README, INDEX e TODO na raiz do projeto. E os arquivos DAYLI_ACTIVITIES_YYYY-MM-DD.md, SESSION_REPORT_YYYY-MM-DD.md, FINAL_STATUS_YYYY-MM-DD.md na pastas docs/SESSION/YYY-MM-DD.
- carregar na memória as instruções contidas nos arquivos .copilot-strict-rules.md, .copilot-strict-enforcement.md, .copilot-rules.md.
- procure por arquivos com informações de credenciais e conteúdo sensível e mover pasta ".secrets", verifique se a pasta ".secrets" está no ".gitignore". proteja as informações.
- ao gerar arquivos utilizar as pastas corretas para manter o projeto organizado.
- Organizar os arquivos que estão na raiz do projeto nas devidas pastas, não deixar a raiz do projeto desorganizada.
```

#### Inicio - primeira vez
```
- iniciar mcp.
- Gerar os arquivos os arquivos README, INDEX e TODO na raiz do projeto. Os arquivos DAYLI_ACTIVITIES_YYYY-MM-DD.md, SESSION_REPORT_YYYY-MM-DD.md, FINAL_STATUS_YYYY-MM-DD.md na pastas docs/SESSION/YYY-MM-DD.
- carregar na memória as instruções contidas nos arquivos .copilot-strict-rules.md, .copilot-strict-enforcement.md, .copilot-rules.md.
- procure por arquivos com informações de credenciais e conteúdo sensível e mover pasta ".secrets", verifique se a pasta ".secrets" está no ".gitignore". proteja as informações.
- ao gerar arquivos utilizar as pastas corretas para manter o projeto organizado.
- Criar branch do repositório Github
```

#### Termino
```
- Encerrar a sessão de hoje.
- Atualizar, se necessário for, .copilot-strict-rules.md, .copilot-strict-enforcement.md, .copilot-rules.md.
- Gerar/Atualuizar os arquivos os arquivos README, INDEX e TODO na raiz do projeto, DAYLI_ACTIVITIES_YYYY-MM-DD.md
- Atualizar detalhadamente os arquivos DAYLI_ACTIVITIES_YYYY-MM-DD.md, SESSION_REPORT_YYYY-MM-DD.md, FINAL_STATUS_YYYY-MM-DD.md na pastas docs/SESSION/YYY-MM-DD.
- Atualizar, se necessário for, detalhadamente com as informações do dia nos arquivos README, INDEX e TODO na raiz do projeto.
- procure por arquivos com informações de credenciais e conteúdo sensível e mover pasta ".secrets", verifique se a pasta ".secrets" está no ".gitignore". proteja as informações.
- Organizar os arquivos nas devidas pastas para não deixar a raiz do projeto desorganizada.
- Atualizar repositório git.
```

---

### D-07 — Como gerenciar credenciais de MCP por projeto?

**Contexto**: Para MCP servers como AWS e GitHub, as credenciais variam por projeto. Você alterna entre projetos frequentemente.

**Opções**:
- **A**: Variáveis de ambiente por workspace via `.secrets/.env` (carregado com `direnv` ou `mise`)
- **B**: AWS profiles nomeados (`~/.aws/credentials`) + `AWS_PROFILE` no `.vscode/mcp.json`
- **C**: Um MCP server de vault (HashiCorp Vault MCP, quando disponível) que centraliza credenciais

**Pergunta para você**: Como você gerencia credenciais de cloud hoje entre projetos?

**Resposta**: ainda não tenho um cofre centralizado. utilizo a pasta .secrets para manter os dados só no projeto, a pasta e os arquivos estão no gitignore.

---

## 🔄 Questões de Processo

### D-08 — Como iniciar uma sessão quando os Domain Profiles estiverem prontos?

**Contexto**: Precisa de um ritual de início de sessão que seja rápido e consistente.

**Proposta de ritual (para validar)**:
```
1. Abrir o projeto no VS Code
2. Declarar o domínio ativo: "Modo: INFRAESTRUTURA"
3. Especificar o contexto: "Projeto: cliente X, ambiente: staging, cloud: AWS"
4. Invocar: @speckit.clarify "instalar Grafana com Helm no namespace monitoring"
5. Speckit assume a partir daí
```

**Perguntas**:
- Esse ritual parece realista para o seu fluxo diário?
- Existe um caso de uso em que você precisa de dois domínios na mesma sessão?

---

### D-09 — Como lidar com trabalho que cruza domínios?

**Contexto**: Algumas tarefas cruzam fronteiras. Exemplo: "criar um script Python que provisiona recursos AWS via boto3" — é código ou infra?

**Opções**:
- **A**: Declarar o domínio primário e mencionar explicitamente o secundário no contexto
- **B**: Criar um quarto profile: `devops-hybrid.md` para casos de sobreposição
- **C**: Compor profiles: "Use programação como base + seção de segurança de infra"

**Resposta**: Opção **A**. É o meu jeito de trabalhar, não misturando profiles.

---

### D-10 — O `.copilot-rules.md` deve referenciar os Domain Profiles?

**Contexto**: Atualmente `.copilot-rules.md` tem regras de organização de pastas e commits, mas não menciona Domain Profiles. Se um Domain Profile contradisser uma regra base, qual prevalece?

**Princípio proposto**: Foundation (Camada 1) sempre prevalece. Domain Profiles (Camada 2) adicionam contexto, nunca sobrescrevem regras base.

**Decisão necessária**: Documentar essa hierarquia explicitamente no `.copilot-rules.md`?

**Resposta**: Eu utilizo o `.copilot-rules.md` para instruções genéricasa de comportamento, os arquivos `.copilot*.md` ficam em uma pasta e tem um link simbólico na pasta do projeto.
Mantemos essa estrutura e criar um arquivo `.copilot-rules*.md` especifico no projeto, com as instruções de cada projeto (dentro da pasta do projeto).
Conservando as instruções genéricas e as especificas de cada projeto.

---

---

## 🆕 Questões Novas — Emergentes de D-11 a D-15

> Três inconsistências identificadas na análise das respostas finais.

---

### D-16 — O `manager.py` substitui ou chama o `init-new-project.sh`?

**Contexto**: A resposta de D-14 Q3 diz: “o `init-new-project.sh` será parte do código `manager.py`”. Isso implica que o script shell seria absorvido pelo Python. Mas o `init-new-project.sh` é referenciado diretamente no `Makefile` (`make init`) e no `README.md`.

**Inconsistência**: Se `manager.py` absorve o `init-new-project.sh`, o `Makefile` quebra e o `README` fica desatualizado. Se os dois coexistem, há duplicação de responsabilidade.

**Três modelos possíveis**:

| Modelo | Comportamento | Impacto no Makefile |
|--------|--------------|--------------------|
| **A — Substituição** | `manager.py` faz tudo; `init-new-project.sh` é removido | `make init` vira `python scripts/manager.py` |
| **B — Orquestração** | `manager.py` coleta dados e chama `init-new-project.sh` ao final | `make init` continua igual; `manager.py` é a interface |
| **C — Coexistência** | `init-new-project.sh` para uso direto/CI; `manager.py` para uso interativo | Dois entry points com comportamentos distintos |

**Pergunta**: Qual modelo? — Modelo B parece o mais seguro: `manager.py` é a interface interativa que ao final dispara o shell script com os parâmetros coletados.
**Resposta**: `manager.py` é a interface interativa que ao final, com os parâmetros coletados gera toda a estrutura do projeto. O `init-new-project.sh` seré incorporado pelo `manager.py`.

---

### D-17 — Criar repositório Git no início ou push no término? São coisas diferentes

**Contexto**: A pergunta de D-13 Q2 era: *“O prompt de Termino deve incluir push para o repositório Git automaticamente?”*

A resposta foi: *“Sim, para cada início de projeto devo criar um repositório específico.”*

**Inconsistência**: A resposta trata de **criar** o repositório (ação de setup inicial), não de **push diário** ao encerrar sessão. São duas operações Git distintas em momentos distintos:

| Operação | Quando | Executor |
|----------|--------|----------|
| `git init` + criar repo no GitHub | Primeira vez — setup do projeto | `manager.py` (via `init-new-project.sh`) |
| `git add` + `commit` + `push` | Todo término de sessão | `session-end.prompt.md` instrui o Copilot |

**Decisão necessária** (duas perguntas independentes):
1. O `manager.py` deve criar o repositório no GitHub automaticamente (via `gh` CLI ou API)?
2. O `session-end.prompt.md` deve incluir `git push` como última etapa do ritual de término?

**Resposta**:
1 - O repositório sera criado manualmente por mim e informado os dados no `manager.py`
2 - Sim
---

### D-18 — Prompts específicos por tipo de projeto: centralizados fora do repo ou dentro do template?

**Contexto**: A resposta de D-13 Q1 diz: *“prompts específicos por tipo de projeto devem ser centralizados (como o `.copilot-rules*`) sendo replicado para todos os projetos que utilizam esse prompt.”*

**Inconsistência com D-02**: D-02 decidiu que os Domain Profiles ficam em `.github/prompts/domain/` *dentro do projeto*. Mas D-13 diz que prompts específicos ficam *centralizados fora* (como os symlinks de `.copilot-rules*`).

Isso cria duas categorias que precisam ser explicitadas:

| Categoria | Exemplo | Onde vive | Como chega ao projeto |
|-----------|---------|-----------|----------------------|
| **Genéricos de operação** | `session-start.prompt.md`, `session-end.prompt.md` | Centralizado (`.copilot-shared/prompts/`) | Symlink na pasta do projeto |
| **Domain Profiles** | `devops-infrastructure.prompt.md` | Centralizado (`.copilot-shared/prompts/domain/`) | Symlink em `.github/prompts/domain/` |
| **Específicos do projeto** | `.copilot-rules-[projeto].md` | Dentro do projeto (`.vscode/`) | Gerado pelo `manager.py` |

**Decisão necessária**: Os Domain Profiles (decidídos em D-02 como `.github/prompts/domain/`) são parte do template (versionados no repo) ou ficam no centralizado e chegam via symlink?

- **Opción Repo**: Ficam no template — cada projeto tem sua cópia; atualizações são manuais por projeto
- **Opção Central**: Ficam no `.copilot-shared/`; chegam via symlink; atualização automática para todos os projetos

**Resposta**: Ficam no repositório.

---

---

## 🆕 Questão Nova — Emergente de D-16

---

### D-19 — O `manager.py` também absorve `setup-project-links.sh` e `check-project-links.sh`?

**Contexto**: D-16 decidiu que `manager.py` absorve `init-new-project.sh` (Modelo A — Substituição). Mas existem dois outros scripts no template com responsabilidades distintas:

| Script | Função atual |
|--------|--------------|
| `init-new-project.sh` | Cria estrutura de pastas e arquivos base — ✅ absorvido pelo `manager.py` |
| `setup-project-links.sh` | Cria os symlinks de `.copilot-rules*` do diretório centralizado para o projeto |
| `check-project-links.sh` | Valida se os symlinks estão ativos e corretos |

**A questão**: `setup-project-links.sh` é um passo natural do onboarding (o `manager.py` deveria chamá-lo automaticamente ao final da coleta de dados). `check-project-links.sh` é uma utilidade de diagnóstico que pode ser mantida como target do `Makefile` independentemente.

**Opções**:

| Opção | `setup-project-links.sh` | `check-project-links.sh` |
|-------|--------------------------|---------------------------|
| **A — Absorção total** | Lógica migrada para `manager.py`; script removido | Lógica migrada para `manager.py --check`; script removido |
| **B — Chamada pelo manager** | `manager.py` chama o script como etapa do fluxo | Permanece como `make check-links` independente |
| **C — Independentes** | Permanece como passo manual pós-onboarding | Permanece como `make check-links` independente |

**Sugestão**: Opção B para `setup-project-links.sh` (é parte natural do fluxo de setup) e Opção C para `check-project-links.sh` (é diagnóstico, não faz sentido no fluxo interativo).

**Pergunta**: Concorda com a sugestão Opção B + C, ou prefere absorção total (A)?
**Resposta**: O `manager.py` é o correto. Os codigo shell scripts anterioires serão convertidos para python no `manager.py`.

---

## 📋 Resumo de Decisões por Prioridade

### ✅ Resolvidas (18)
| ID | Decisão | Resolução |
|----|---------|----------|
| D-01 | Qual domínio modelar primeiro | Infraestrutura — via `manager.py` fluxo condicional |
| D-02 | Onde ficam os Domain Profiles | `.github/prompts/domain/` + `docs/copilot/` |
| D-03 | Modelo de ativação | Declarativo via `manager.py` |
| D-04 | Templates Speckit por domínio | Opção C — genéricos, Domain Profile instrui o agente |
| D-05 | Nível de detalhe dos profiles | Completo + Dinâmico, foco em memória |
| D-07 | Gerência de credenciais MCP | `.secrets/` por projeto |
| D-09 | Trabalho que cruza domínios | Domínio primário declarado + secundário mencionado |
| D-10 | Hierarquia Foundation > Domain | Symlink genérico + `.copilot-rules-[projeto].md` no projeto |
| D-11 | Escopo do script | `manager.py` menu-driven, fluxo condicional por escolha, gera estrutura base |
| D-12 | MCP `memory` vs. file-based | Manter file-based; MCP `memory` para contexto intra-sessão |
| D-13 | Prompts de sessão como prompt files | Sim — genéricos centralizados + específicos por tipo de projeto centralizados |
| D-14 | Arquivo `.copilot-rules-[projeto].md` | Nome com projeto, em `.vscode/`, gerado pelo `manager.py` |
| D-15 | Script como ponto único de entrada | Modelo X — `manager.py` é o ponto único, fluxo condicional |
| D-16 | Relação `manager.py` / `init-new-project.sh` | Modelo A — `manager.py` substitui e absorve o shell script |
| D-17 | Criar repo vs. push diário | Repo criado manualmente + dados no `manager.py`; `git push` no `session-end.prompt.md` |
| D-18 | Domain Profiles: repo ou centralizado | Ficam no repositório — cada projeto tem sua cópia |
| D-19 | Destino de `setup-project-links.sh` e `check-project-links.sh` | Modelo A — todos os shell scripts absorvidos pelo `manager.py` em Python |

### ✅ Parcialmente Resolvidas → Agora Completas
| ID | Decisão | Resolução Final |
|----|---------|----------------|
| D-01 | Qual domínio modelar primeiro | Infraestrutura primeiro — via `manager.py` fluxo condicional (D-11/D-15/D-16) |
| D-06 | Quais MCP Servers ativar | `memory` + `sequential-thinking` ativos; GitHub MCP não necessário (repo manual) |
| D-08 | Ritual de início de sessão | Definido: `session-start.prompt.md` + `session-start-first.prompt.md`; `manager.py` para setup |

### ✅ Todas as decisões resolvidas — 0 abertas

---

## 🚀 Implementação — Próximos Passos

Todas as 19 decisões estão respondidas. A implementação pode começar:

1. **Implementação `manager.py`** — script Python com fluxo condicional por módulo; absorve `init-new-project.sh`, `setup-project-links.sh` e `check-project-links.sh` (D-11/D-15/D-16/D-19)
2. **Criar os 3 prompt files de sessão** — `session-start.prompt.md`, `session-start-first.prompt.md`, `session-end.prompt.md` (D-13)
3. **Criar os 3 Domain Profile files** — `devops-programming.prompt.md`, `devops-infrastructure.prompt.md`, `devops-analysis.prompt.md` em `.github/prompts/domain/` (D-02/D-18)
4. **Atualizar `Makefile`** — `make init` → `python scripts/manager.py` (D-16)
5. **Criar template `.copilot-rules-[projeto].md`** — gerado pelo `manager.py`, salvo em `.vscode/` (D-14)

---

*Referência: [DOMAIN-PROFILES-STRATEGY.md](DOMAIN-PROFILES-STRATEGY.md)*
