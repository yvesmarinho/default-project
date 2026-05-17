# Templates Adaptáveis por Demanda DevOps — Speckit + Copilot

**Data**: 2026-02-27
**Contexto**: Debate sobre estratégia de Domain Profiles para DevOps flutuante
**Status**: 📋 Em análise — ver [DOMAIN-PROFILES-DECISIONS.md](DOMAIN-PROFILES-DECISIONS.md)

---

## O Problema Central

O DevOps não é uma função, é um **contexto flutuante**. Numa mesma semana você pode:

- Depurar Python num pipeline de ML
- Escrever um módulo Terraform para AWS
- Analisar logs de um incidente de produção
- Revisar uma arquitetura de Kubernetes proposta por outro time
- Criar um runbook para operação de um produto instalado

Cada um desses contextos tem **linguagem, artefatos, riscos e "definition of done" completamente diferentes**. O que o Copilot precisa saber sobre cada um também é diferente.

**O problema atual**: sem templates, você reexplica contexto do zero a cada conversa.

---

## O que é o Speckit no Projeto — e Por que é a Peça Certa

O projeto já tem:

| Localização | O que contém |
|-------------|-------------|
| `.github/agents/` | Agentes especializados por fase: analyze, implement, plan, clarify, specify, tasks, checklist |
| `.github/prompts/` | Prompts correspondentes por atividade |
| `.specify/templates/` | Templates de spec, plan, checklist, tasks |

O Speckit é uma **framework de raciocínio estruturado**: divide o trabalho em fases:

```
clarify → analyze → specify → plan → tasks → implement → checklist
```

Isso é poderoso porque **cada fase pode ter um perfil de comportamento diferente**.

A questão central: como personalizar essas fases por *tipo de demanda DevOps*?

---

## A Arquitetura de Templates Adaptáveis — Três Camadas

### Camada 1 — Foundation (universal, por workspace)
Regras que valem em qualquer projeto: como fazer commits, como organizar pastas, o que nunca fazer.

**Você já tem:** `.copilot-strict-rules.md`, `.copilot-rules.md`, `.copilot-strict-enforcement.md`

### Camada 2 — Domain Profile (por tipo de trabalho)
Perfis de contexto específicos por domínio de trabalho DevOps.

| Profile | Quando usar |
|---------|-------------|
| `devops-programming.md` | Está escrevendo código: Python, scripts, automações |
| `devops-infrastructure.md` | Está em infra: Terraform, Helm, Kubernetes, instalações |
| `devops-analysis.md` | Está analisando: logs, incidentes, arquitetura, métricas |

### Camada 3 — Context Injection (por projeto/demanda específica)
Detalhes do projeto concreto: cliente, ambiente, versões, restrições. Preenchidos no início de cada sessão, ou coletados automaticamente via `speckit.clarify`.

---

## Como o Speckit Resolve a Adaptação

O agente `speckit.clarify` existe exatamente para isso: **antes de qualquer trabalho substantivo**, ele faz as perguntas certas para determinar o contexto.

**Fluxo ideal com Domain Profiles:**

1. Você diz: "preciso instalar o Grafana no cluster de staging"
2. `speckit.clarify` detecta — isso é infra — e puxa `devops-infrastructure.md`
3. Pergunta: qual Kubernetes distro? Helm ou manifests? Namespace? Ingress controller?
4. `speckit.specify` documenta os requisitos no formato correto para infra
5. `speckit.plan` gera o plano considerando restrições do ambiente
6. `speckit.tasks` divide em tarefas com critérios de Done para ops (health check, alertas, runbook)

Sem esse mecanismo, você faz tudo isso manualmente a cada conversa.

---

## O que Falta no Template Atual

### Lacuna 1 — Domain Profiles não existem
Os `.github/prompts/` atuais são orientados ao workflow do Speckit, mas não ao **contexto de domínio DevOps**. Sabem *como* trabalhar, mas não *em qual mundo* estão trabalhando.

### Lacuna 2 — `speckit.clarify` sem detecção de domínio
Para ser verdadeiramente adaptável, o agente de clarificação precisaria identificar se a demanda é "código", "infra" ou "análise" e ramificar o comportamento.

### Lacuna 3 — Checklists genéricos
Um checklist de "done" para código Python é diferente de um para módulo Terraform e diferente de um para análise de incidente. O checklist atual é provavelmente genérico demais.

---

## A Diferença Real Entre os Três Modos DevOps

### Modo Programação

| Aspecto | Conteúdo |
|---------|----------|
| **Copilot precisa saber** | Linguagem, framework, versão, estrutura de testes, estilo de código, onde está o código, convenções de import |
| **Definition of Done** | Testes passando, lint OK, cobertura mínima, PR description completa |
| **Speckit spec contém** | Requisitos funcionais, interfaces, comportamentos esperados, edge cases |
| **Speckit plan contém** | Componentes a criar, sequência de implementação, dependências |
| **Checklist contém** | `pytest` OK, `ruff` OK, types anotados, docstrings, testes de integração |

### Modo Infraestrutura

| Aspecto | Conteúdo |
|---------|----------|
| **Copilot precisa saber** | Cloud/on-prem, ferramentas IaC, ambiente alvo (dev/staging/prod), política de acesso, onde estão os módulos existentes, padrão de naming/tagging |
| **Definition of Done** | `terraform plan` sem erros, `helm lint` OK, health check do serviço, alerta configurado, runbook atualizado |
| **Speckit spec contém** | Recursos a criar, dependências de infraestrutura, requisitos de segurança, SLO esperado |
| **Speckit plan contém** | Ordem de criação de recursos, rollback plan, janela de manutenção |
| **Checklist contém** | Validação de config, testes de conectividade, alerta criado, runbook criado, change record |

### Modo Análise

| Aspecto | Conteúdo |
|---------|----------|
| **Copilot precisa saber** | O que está sendo analisado (logs? métricas? arquitetura? incidente?), formato de saída esperado (RCA? ADR? relatório executivo?), fontes disponíveis, stakeholders |
| **Definition of Done** | Hipótese documentada, evidências linkadas, recomendação com owner e prazo definidos |
| **Speckit spec contém** | Escopo da análise, perguntas a responder, fontes de dados, formato de entrega |
| **Speckit plan contém** | Sequência de investigação, hipóteses iniciais, critérios de validação |
| **Checklist contém** | Hipótese confirmada/refutada, causa raiz identificada, ação preventiva definida, stakeholders notificados |

---

## Como o MCP Amplifica o Modo Infraestrutura

Para o modo infra, os MCP servers configurados no `.vscode/mcp.json` são diretamente relevantes:

| MCP Server | O que habilita |
|------------|----------------|
| **AWS MCP** | Copilot pergunta: "qual é o estado atual do cluster antes de planejar a mudança?" |
| **Kubernetes MCP** | Copilot verifica se namespace existe, se deployment está healthy, antes de gerar plano |
| **Filesystem MCP** | Copilot analisa módulos Terraform existentes no repo antes de propor novos |

Isso muda o Speckit de um framework de *geração* para um framework de **raciocínio informado**: o agente não supõe o estado do ambiente, ele consulta.

---

## Estrutura de Arquivos Proposta

```
.github/
└── prompts/
    ├── speckit.*.prompt.md              ← já existe (workflow Speckit)
    └── domain/
        ├── devops-programming.prompt.md  ← quando está em código
        ├── devops-infrastructure.prompt.md ← quando está em infra
        └── devops-analysis.prompt.md     ← quando está analisando

docs/
└── copilot/
    ├── DOMAIN-PROFILES-STRATEGY.md     ← este arquivo
    ├── DOMAIN-PROFILES-DECISIONS.md    ← questões e decisões
    ├── DOMAIN-PROGRAMMING.md           ← profile completo: código
    ├── DOMAIN-INFRASTRUCTURE.md        ← profile completo: infra
    └── DOMAIN-ANALYSIS.md              ← profile completo: análise
```

### Como Usar na Prática (antes da automação estar pronta)

```
Início de sessão:
"Estou no modo INFRAESTRUTURA.
Contexto: instalação do Grafana no cluster staging da AWS.
Carregue o profile devops-infrastructure.md e inicie com speckit.clarify."
```

---

## A Limitação Honesta — O que o Copilot Individual não faz automaticamente

Para ser preciso: no Copilot Individual hoje, a **detecção automática de domínio não acontece sozinha**. Você ainda precisa indicar qual profile está ativo.

| O que você pode automatizar | Mecanismo |
|-----------------------------|-----------|
| Profile correto aparece como sugestão | `chat.promptFilesRecommendations` no `settings.json` |
| `speckit.clarify` pergunta o domínio explicitamente | Modificar o prompt de clarificação |
| Templates de spec/plan/tasks por domínio | O agente seleciona com base na resposta ao clarify |

**A automação completa** — "Copilot detecta o contexto sem você dizer nada" — requer:
- Agent customizado (Enterprise/custom), ou
- MCP que leia o contexto do ambiente em tempo real

---

## Síntese

O que está sendo descrito é essencialmente **context switching gerenciado**:
- O mesmo framework de trabalho (Speckit)
- Com *lentes diferentes* aplicadas conforme o domínio

**O Speckit já tem** a estrutura de fases correta.

**O que falta** é a camada de Domain Profiles que popula essas fases com os detalhes certos por tipo de trabalho DevOps.

**O MCP** é o que transforma esses profiles de *estáticos* (você descreve o estado) para *dinâmicos* (o Copilot consulta o estado real).

---

## Referências Internas

- [.copilot-strict-rules.md](../../.copilot-strict-rules.md) — Regras de execução P0
- [.copilot-rules.md](../../.copilot-rules.md) — Regras gerais do projeto
- [.vscode/mcp.json](../../.vscode/mcp.json) — Configuração MCP
- [.github/agents/](../../.github/agents/) — Agentes Speckit
- [.github/prompts/](../../.github/prompts/) — Prompts Speckit
- [DOMAIN-PROFILES-DECISIONS.md](DOMAIN-PROFILES-DECISIONS.md) — Próximos passos
