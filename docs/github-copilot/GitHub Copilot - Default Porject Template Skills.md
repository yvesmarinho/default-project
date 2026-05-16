---
title: "GitHub Copilot - Default Porject Template Skills"
source: "https://github.com/copilot/c/adc155ab-ce73-4725-a352-201de6420ab5"
author:
  - "[[GitHub]]"
published:
created: 2026-03-07
description: "GitHub is where people build software. More than 150 million people use GitHub to discover, fork, and contribute to over 420 million projects."
tags:
  - "clippings"
---
Estou desenvolvendo um template de projeto agnóstico. Server para programador, devops, infraestrutura, analise geral, etc. Já enriqueci o Copilot Code com minhas experiências. Qual habilidade/profissional seria necessário para tanalisar e trazer mais funcionalidades a esse template. Que deve continuar agnóstico mas na execução do código que transforma o template em projeto deve ter possbilidade de focar numa determinada área, linguagem, etc. Isso é um debate, não há necessidade de códigos.

Você está descrevendo duas coisas ao mesmo tempo:

1. **Um “template base” (agnóstico)** que serve para praticamente qualquer projeto (software, infra, data, devops, pesquisa, etc.).
2. **Um “motor de instanciação”** (um scaffold/bootstraper) que, na hora de gerar um projeto real, consegue **aplicar perfis**: área (devops/data/backend/segurança), linguagem (Go/Python/Rust/Node), plataforma (K8s/AWS/on-prem), maturidade (MVP/enterprise), compliance (LGPD/SOC2), etc.

Para analisar isso e trazer funcionalidades sem “poluir” a agnosticidade do template, o conjunto de habilidades mais valioso não é um único “cargo”, mas uma **combinação de perfis**. Abaixo vai um mapa bem direto do “quem” e “por quê”, e como eu organizaria o debate.

---

## 1) Profissional-chave: “Template/Scaffolding Architect” (ou “Platform Tooling Engineer”)

Na prática, esse é o perfil que mais faz diferença: alguém que entende **plataformas internas**, **tooling**, **experiência do desenvolvedor (DevEx)** e **arquitetura de templates**.

### Responsabilidades reais desse perfil

- Definir a **arquitetura do template**: o que é core (agnóstico) vs. o que é plug-in/perfil.
- Definir o “contrato” do motor:
	- inputs (config, prompts, arquivos declarativos)
	- outputs (árvore gerada, artefatos, pipelines)
	- hooks (pré/pós geração)
- Evitar “opiniões acopladas” no core e empurrar opinião para **plugins**.
- Criar padrões de testabilidade do template (sim, templates também precisam de testes).
- Definir estratégia de versionamento, migração e compatibilidade.

### Por que ele é crucial para você

Porque o risco maior do teu template não é “faltar feature”; é virar um *monólito de template* impossível de manter, onde:

- cada nova linguagem quebra um pedaço,
- cada área adiciona mais 20 flags,
- e o template fica “agnóstico” só no nome.

Esse perfil é o guardião da separação: **core minimalista + extensões evolutivas**.

---

## 2) Profissional de suporte obrigatório: “Developer Experience (DevEx) / UX de CLI”

Se o motor “transforma template em projeto”, então o produto real é a **experiência de geração**.

### O que esse profissional adiciona

- Projeto de CLI (comandos, subcomandos, flags, auto-complete, config layering).
- UX de prompts (quando perguntar, quando inferir, quando falhar).
- Ergonomia: logs claros, modo `--dry-run`, modo `--explain`, modo `--json` para automação, saída determinística.
- Documentação orientada a “primeiros 10 minutos”.
- Estratégia “non-interactive” (CI) vs. “interactive” (humano).

### Pergunta que ele vai fazer que normalmente ninguém faz

“Quantos passos e quantas decisões o usuário tem que tomar para gerar um projeto que compila/roda/deploya?”

Se a resposta for “muitas”, o template vira *burocracia*.

---

## 3) Profissional que define “agnosticidade de verdade”: “Systems/Infra Generalist” (SRE/Infra Architect)

Esse perfil ajuda a manter o template útil para “programador, devops, infraestrutura, análise geral”.

### O que ele traz

- Padrões transversais que servem para todos:
	- logging/observabilidade (mesmo que seja “stubs”)
	- CI/CD “mínimo viável”
	- convenções de ambiente (dev/stage/prod)
	- segurança baseline (secrets, least privilege, linters, SBOM)
	- documentação operacional (“runbook”)
- Capacidade de “agnóstico” sem ser “vazio”: o template tem esqueleto sólido.

---

## 4) Profissionais por “domínio” (plug-ins): especialistas por trilha

Aqui é onde você ganha funcionalidades **sem perder agnosticidade**: cada um contribui com um **plugin/perfil**.

### 4.1 Backend/Software Architect (por linguagem/ecossistema)

- Perfis: `python-fastapi`, `go-chi`, `node-nest`, `rust-axum`, etc.
- Estruturas de projeto idiomáticas
- Padrões de testes, lint, formatação, packaging
- Dockerfile multistage e devcontainers

### 4.2 DevOps / K8s / Cloud Architect

- Perfis: `k8s`, `terraform-aws`, `terraform-azure`, `ansible`, `nomad`, `helm`, `argocd`
- Pipelines por estratégia (GitOps vs. push deploy)
- Padrões de IaC e organização de módulos

### 4.3 Data/Analytics Engineer / MLOps Engineer

- Perfis: `data-pipeline`, `dbt`, `airflow`, `spark`, `mlops`
- Estruturas para notebooks vs. pipelines
- Reprodutibilidade (lockfiles, ambientes)

### 4.4 AppSec / Security Engineer (muito valioso)

- Baselines: SAST, secret scanning, dependabot/renovate, SBOM, assinatura, políticas
- Threat modeling “lite” por tipo de projeto
- Regras de hardening para CI e containers

### 4.5 Technical Writer / Docs Engineer (não subestime)

- Transformar o template em algo “consumível”
- Padrões de docs: ADRs, runbooks, troubleshooting, onboarding
- Documentação gerada a partir do perfil escolhido (importante)

---

## 5) “Profissional” que quase ninguém inclui e faz falta: “Release / Maintainer / Librarian”

Um template agnóstico é um produto que vai envelhecer rápido se não tiver governança.

### O que ele define

- Versionamento semântico do template e do motor
- Compatibilidade de perfis (matriz)
- Política de depreciação
- Changelog e migrações
- Testes de regressão do gerador (snapshot tests/fixture tests)
- Curadoria do que entra no core vs plugin

Sem isso, vira um acúmulo de contribuições “boas” mas incompatíveis.

---

## 6) Estrutura ideal de time (se você quiser um “stack” completo)

Se fosse montar um “squad mínimo” para evoluir isso com qualidade:

1. **Platform Tooling Engineer / Template Architect** (dono do core e do motor)
2. **DevEx/CLI Engineer** (UX, interface, config, automação)
3. **SRE/Infra Generalist** (baseline universal)
4. **Security Engineer** (baseline e perfis de compliance)
5. **1–2 especialistas por domínio** (backend, data, k8s/cloud) criando perfis
6. **Maintainer/Release + Docs Engineer** (pode ser part-time, mas é fundamental)

---

## 7) Debate: como manter “agnóstico” e ainda “focado” na execução?

A forma madura de fazer isso é:

- **Core minimalista**: só convenções universais e infraestrutura do gerador.
- **Perfis como plugins**: cada perfil injeta:
	- arquivos
	- patches em arquivos existentes
	- dependências
	- pipelines
	- docs específicas
- **Composição**: permitir combinar perfis:
	- `python-fastapi + postgres + k8s + observability`
- **Regras de compatibilidade**:
	- alguns perfis são mutuamente exclusivos
	- outros são complementares
- **Camadas** (layering):
	- base → linguagem → framework → plataforma → compliance

Isso evita o “mega-template” e vira uma **plataforma de templates**.

---

## 8) Perguntas para orientar o próximo passo (para você escolher “quem contratar/consultar”)

1. Seu motor hoje é mais próximo de:
- “copiar pasta e substituir variáveis”  
	ou
- “aplicar operações declarativas (merge/patch/hook) com composição de perfis”?
1. Você quer suportar:
- só “criação inicial”  
	ou
- “re-aplicar perfil” depois (upgrade/migração do projeto gerado)?
1. Quais são seus “não negociáveis” do core?
- Estrutura de repo? Licença? CI mínimo? Editorconfig? Makefile? Task runner? Doc skeleton?
1. Qual é o seu público primário: dev, devops, data, security?
- Mesmo sendo agnóstico, um template sempre tem **usuário primário**.

Se você responder essas 4, eu consigo te dizer com mais precisão **qual perfil vem primeiro** (e quais vêm depois), e também **qual arquitetura de perfis** reduz complexidade no longo prazo.