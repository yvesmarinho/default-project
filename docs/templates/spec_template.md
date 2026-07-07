# Spec - <PROJECT_NAME>

## 1. Metadados da Especificação

- **Projeto:** `<PROJECT_NAME>`
- **Slug:** `<PROJECT_SLUG>`
- **Versão do projeto:** `<PROJECT_VERSION>`
- **Status:** `<PROJECT_STATUS>`
- **Data da spec:** `<YYYY-MM-DD>`
- **Responsável:** `<PROJECT_OWNER_OR_TEAM>`
- **Framework de especificação:** `<SPEC_FRAMEWORK>`

---

## 2. Resumo Executivo

### 2.1 Descrição

<PROJECT_DESCRIPTION>

### 2.2 Problema

<PROBLEM_STATEMENT>

### 2.3 Valor entregue

<BUSINESS_VALUE>

### 2.4 Objetivo principal

<PRIMARY_GOAL>

---

## 3. Contexto do Projeto

### 3.1 Domínio

`<DOMAIN>`

### 3.2 Tipo de projeto

`<PROJECT_TYPE>`

### 3.3 Usuários-alvo

#### Usuário 1
- **Papel:** `<USER_ROLE_1>`
- **Nível:** `<beginner|intermediate|advanced>`
- **Descrição:** `<USER_DESCRIPTION_1>`

#### Usuário 2
- **Papel:** `<USER_ROLE_2>`
- **Nível:** `<beginner|intermediate|advanced>`
- **Descrição:** `<USER_DESCRIPTION_2>`

### 3.4 Casos de uso principais

1. `<PRIMARY_USE_CASE_1>`
2. `<PRIMARY_USE_CASE_2>`
3. `<PRIMARY_USE_CASE_3>`

---

## 4. Escopo

### 4.1 Em escopo

- `<IN_SCOPE_1>`
- `<IN_SCOPE_2>`
- `<IN_SCOPE_3>`
- `<IN_SCOPE_4>`
- `<IN_SCOPE_5>`

### 4.2 Fora de escopo

- `<OUT_OF_SCOPE_1>`
- `<OUT_OF_SCOPE_2>`
- `<OUT_OF_SCOPE_3>`

---

## 5. Objetivos e Resultados Esperados

### 5.1 Critérios de sucesso

- `<SUCCESS_CRITERION_1>`
- `<SUCCESS_CRITERION_2>`
- `<SUCCESS_CRITERION_3>`

### 5.2 Entregáveis

- `<DELIVERABLE_1>`
- `<DELIVERABLE_2>`
- `<DELIVERABLE_3>`

### 5.3 Cenários de demonstração

- `<DEMO_SCENARIO_1>`
- `<DEMO_SCENARIO_2>`

---

## 6. Requisitos Funcionais

### RF-001 - <FUNCTIONAL_REQUIREMENT_1_TITLE>

**Descrição:**  
<FUNCTIONAL_REQUIREMENT_1_DESCRIPTION>

**Entradas esperadas:**  
- `<FR1_INPUT_1>`
- `<FR1_INPUT_2>`

**Saídas esperadas:**  
- `<FR1_OUTPUT_1>`
- `<FR1_OUTPUT_2>`

**Regras associadas:**  
- `<FR1_RULE_1>`
- `<FR1_RULE_2>`

---

### RF-002 - <FUNCTIONAL_REQUIREMENT_2_TITLE>

**Descrição:**  
<FUNCTIONAL_REQUIREMENT_2_DESCRIPTION>

**Entradas esperadas:**  
- `<FR2_INPUT_1>`
- `<FR2_INPUT_2>`

**Saídas esperadas:**  
- `<FR2_OUTPUT_1>`
- `<FR2_OUTPUT_2>`

**Regras associadas:**  
- `<FR2_RULE_1>`
- `<FR2_RULE_2>`

---

### RF-003 - <FUNCTIONAL_REQUIREMENT_3_TITLE>

**Descrição:**  
<FUNCTIONAL_REQUIREMENT_3_DESCRIPTION>

**Entradas esperadas:**  
- `<FR3_INPUT_1>`
- `<FR3_INPUT_2>`

**Saídas esperadas:**  
- `<FR3_OUTPUT_1>`
- `<FR3_OUTPUT_2>`

**Regras associadas:**  
- `<FR3_RULE_1>`
- `<FR3_RULE_2>`

---

## 7. Requisitos Não Funcionais

### RNF-001 - Segurança

- `<SECURITY_REQUIREMENT_1>`
- `<SECURITY_REQUIREMENT_2>`
- `<SECURITY_REQUIREMENT_3>`

### RNF-002 - Desempenho

- `<PERFORMANCE_CONSTRAINT_1>`
- `<PERFORMANCE_CONSTRAINT_2>`
- `<PERFORMANCE_CONSTRAINT_3>`

### RNF-003 - Robustez

- `<ROBUSTNESS_REQUIREMENT_1>`
- `<ROBUSTNESS_REQUIREMENT_2>`

### RNF-004 - Observabilidade

- `<OBSERVABILITY_REQUIREMENT_1>`
- `<OBSERVABILITY_REQUIREMENT_2>`

### RNF-005 - Manutenibilidade

- `<MAINTAINABILITY_REQUIREMENT_1>`
- `<MAINTAINABILITY_REQUIREMENT_2>`
- `<MAINTAINABILITY_REQUIREMENT_3>`

### RNF-006 - Qualidade Automatizada

- `<LINT_COMMAND>`
- `<TYPECHECK_COMMAND>`
- `<TEST_COMMAND>`
- `<COVERAGE_COMMAND>`
- Cobertura mínima: `<MIN_TEST_COVERAGE>%`

---

## 8. Arquitetura Mínima Obrigatória

### 8.1 Estilo arquitetural

O projeto deve seguir:

- **Layered Architecture**
- **DDD leve**
- **Ports/Adapters simplificado**

### 8.2 Camadas

#### Presentation
Responsável por:
- interface com usuário;
- CLI, API ou UI;
- parsing de argumentos;
- mensagens e renderização.

#### Application
Responsável por:
- orquestração dos casos de uso;
- coordenação entre domínio e infraestrutura;
- DTOs e fluxo operacional.

#### Domain
Responsável por:
- entidades;
- value objects;
- regras de negócio;
- invariantes;
- contratos centrais.

#### Infrastructure
Responsável por:
- acesso a filesystem;
- banco de dados;
- APIs;
- serialização;
- integrações externas;
- mecanismos concretos de persistência.

#### Shared
Responsável por:
- utilitários compartilhados;
- validadores;
- exceções comuns;
- enums e helpers reutilizáveis.

### 8.3 Restrições obrigatórias

- a camada de interface não deve conter regra de negócio;
- a camada de domínio não deve depender diretamente de framework externo;
- integrações externas devem ser encapsuladas;
- contratos devem ser explícitos;
- entradas e saídas críticas devem ser validadas;
- toda saída relevante deve possuir contrato ou schema.

---

## 9. Modelo de Domínio Inicial

### 9.1 Entidades

- `<ENTITY_1>`
- `<ENTITY_2>`
- `<ENTITY_3>`

### 9.2 Value Objects

- `<VALUE_OBJECT_1>`
- `<VALUE_OBJECT_2>`

### 9.3 Serviços de domínio

- `<DOMAIN_SERVICE_1>`
- `<DOMAIN_SERVICE_2>`

### 9.4 Invariantes

- `<INVARIANT_1>`
- `<INVARIANT_2>`
- `<INVARIANT_3>`

---

## 10. Políticas Técnicas Obrigatórias

### 10.1 Política de validação

Toda função, método, classe, comando de entrada e caso de uso deve validar:

- nulidade;
- tipagem;
- vazio;
- formato;
- invariantes de domínio;
- segurança de path, quando aplicável;
- schema, quando aplicável.

### 10.2 Política de tratamento de erro

Toda fronteira externa, operação de I/O e integração com serviço externo deve ter:

- `try/except`;
- logging contextual;
- falha controlada;
- contrato explícito para comportamento em erro.

### 10.3 Política de documentação

- toda função pública deve ser documentada;
- toda classe pública deve ser documentada;
- o estilo deve ser `<DOCSTYLE>`;
- doctest: `<true_or_false>`.

### 10.4 Política de tipagem

- type hints obrigatórios: `<true_or_false>`;
- validação adicional de contratos quando necessário.

---

## 11. Estrutura Recomendada do Projeto

```text
<PROJECT_NAME>/
├── .github/
├── .git-hooks/
├── .memory/
├── .secrets/
├── .session-index/
├── .session-time/
├── .specify/
├── .vscode/
├── docs/
├── logs/
├── schemas/
├── scripts/
├── src/
│   └── <PROJECT_SLUG>/
│       ├── cli/
│       ├── application/
│       │   ├── dto/
│       │   ├── services/
│       │   └── use_cases/
│       ├── domain/
│       │   ├── entities/
│       │   ├── value_objects/
│       │   ├── services/
│       │   ├── rules/
│       │   └── contracts/
│       ├── infrastructure/
│       │   ├── config/
│       │   ├── filesystem/
│       │   ├── integrations/
│       │   └── exporters/
│       ├── shared/
│       └── main.py
├── test/
├── tmp/
├── pyproject.toml
├── README.md
└── objetivo.yaml
```

---

## 12. Backlog Inicial de Funcionalidades

### 12.1 MVP

#### Funcionalidade 1
- **Nome:** `<MVP_FEATURE_1>`
- **Descrição:** `<MVP_FEATURE_1_DESCRIPTION>`
- **Critério de sucesso:** `<MVP_FEATURE_1_SUCCESS>`

#### Funcionalidade 2
- **Nome:** `<MVP_FEATURE_2>`
- **Descrição:** `<MVP_FEATURE_2_DESCRIPTION>`
- **Critério de sucesso:** `<MVP_FEATURE_2_SUCCESS>`

#### Funcionalidade 3
- **Nome:** `<MVP_FEATURE_3>`
- **Descrição:** `<MVP_FEATURE_3_DESCRIPTION>`
- **Critério de sucesso:** `<MVP_FEATURE_3_SUCCESS>`

### 12.2 Funcionalidades secundárias

- `<SECONDARY_FEATURE_1>`
- `<SECONDARY_FEATURE_2>`
- `<SECONDARY_FEATURE_3>`

### 12.3 Futuro

- `<FUTURE_FEATURE_1>`
- `<FUTURE_FEATURE_2>`

---

## 13. Estratégia de Testes

### 13.1 Tipos obrigatórios

- unit
- integration
- contract
- e2e

### 13.2 Meta de cobertura

Cobertura mínima obrigatória de **<MIN_TEST_COVERAGE>%**.

### 13.3 Priorização sugerida

Aplicar TDD principalmente em:
- validações;
- regras de domínio;
- transformações puras;
- contratos críticos;
- parsers;
- classificação e agregação.

---

## 14. Observabilidade e Operação

### 14.1 Logging

- ferramenta: `<LOGGING_TOOL>`;
- eventos obrigatórios:
  - `start_execution`
  - `input_validated`
  - `processing_started`
  - `processing_failed`
  - `output_generated`
  - `execution_summary`

### 14.2 Configuração

- arquivo local de ambiente: `<LOCAL_ENV_FILE_OR_NA>`;
- diretório de secrets: `.secrets/`;
- arquivos de configuração:
  - `<CONFIG_FILE_1>`
  - `<CONFIG_FILE_2>`

### 14.3 Execução e distribuição

- modos de execução:
  - `<EXECUTION_MODE_1>`
  - `<EXECUTION_MODE_2>`
- empacotamento: `<PACKAGING_STRATEGY>`
- distribuição: `<DISTRIBUTION_STRATEGY>`

---

## 15. Critérios de Aceite

### CA-001
Dado `<PRECONDITION_1>`, o sistema deve `<EXPECTED_BEHAVIOR_1>`.

### CA-002
Dado `<PRECONDITION_2>`, o sistema deve `<EXPECTED_BEHAVIOR_2>`.

### CA-003
Dado `<PRECONDITION_3>`, o sistema deve `<EXPECTED_BEHAVIOR_3>`.

### CA-004
Dado `<PRECONDITION_4>`, o sistema deve `<EXPECTED_BEHAVIOR_4>`.

### CA-005
Dado `<PRECONDITION_5>`, o sistema deve `<EXPECTED_BEHAVIOR_5>`.

---

## 16. Assunções

- `<ASSUMPTION_1>`
- `<ASSUMPTION_2>`
- `<ASSUMPTION_3>`

---

## 17. Riscos e Mitigações

### Risco 1
- **Descrição:** `<RISK_1>`
- **Impacto:** `<low|medium|high>`
- **Mitigação:** `<MITIGATION_1>`

### Risco 2
- **Descrição:** `<RISK_2>`
- **Impacto:** `<low|medium|high>`
- **Mitigação:** `<MITIGATION_2>`

### Risco 3
- **Descrição:** `<RISK_3>`
- **Impacto:** `<low|medium|high>`
- **Mitigação:** `<MITIGATION_3>`

---

## 18. Decisões Técnicas Iniciais

1. Linguagem principal: `<PRIMARY_LANGUAGE>`.
2. Gerenciador de pacotes: `<PACKAGE_MANAGER>`.
3. Estilo de documentação: `<DOCSTYLE>`.
4. Arquitetura mínima: camadas + DDD leve + ports/adapters simplificado.
5. Qualidade automatizada obrigatória.
6. Segurança e validação explícita obrigatórias.
7. Modularidade e testabilidade como requisitos estruturais.

---

## 19. Artefatos Derivados Esperados

Após esta especificação, devem ser produzidos:

- `plan.md`
- `tasks.md`
- `docs/architecture/overview.md`
- `docs/decisions/adr-001.md`
- `<OPTIONAL_ARTIFACT_1>`
- `<OPTIONAL_ARTIFACT_2>`

---

## 20. Conclusão

Esta especificação serve como base técnica e operacional para o projeto `<PROJECT_NAME>`, estabelecendo uma linha mínima de qualidade para arquitetura, implementação, testes, segurança, validação, observabilidade e entrega incremental orientada por especificação.