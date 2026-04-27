# Se você quiser, eu desenho uma integração para o seu ambiente
## Proposição orientada a um workflow integrado “mínimo viável” (prático)

> **Objetivo:** complementar o **SpecKit** com o **Superpowers** de forma incremental, com o menor atrito possível, preservando a estrutura do SpecKit (artefatos) e adicionando disciplina de execução (qualidade) via Superpowers.

---

## 1. Premissas e princípios

### 1.1. Papéis de cada ferramenta (para evitar conflitos)
- **SpecKit** é o *dono do processo e dos artefatos*:
  - Constituição/princípios do projeto
  - `spec.md` (requisitos, user stories)
  - `plan.md` (plano técnico)
  - `tasks.md` (tarefas executáveis)
- **Superpowers** é o *dono da disciplina de execução*:
  - TDD real (RED/GREEN/REFACTOR)
  - Revisão estruturada (antes e depois)
  - Verificação (“não declarar pronto sem evidência”)
  - Subagentes (quando fizer sentido)

### 1.2. Regra de ouro: evitar “drift”
Se durante a implementação surgir requisito novo/descoberta relevante:
- **atualizar `spec.md` e/ou `plan.md` primeiro**
- só depois continuar implementação

Isso mantém rastreabilidade e reduz retrabalho.

---

## 2. Workflow integrado “mínimo viável” (prático)

### Visão geral (pipeline curto)
1. **Constituição** (SpecKit)
2. **Especificação** (SpecKit)
3. **Plano técnico** (SpecKit)
4. **Tarefas** (SpecKit)
5. **Gate de qualidade pré-código** (Superpowers)
6. **Implementação TDD** (Superpowers)
7. **Verificação final** (Superpowers)

O “MVP” aqui é introduzir Superpowers em **dois gates**: antes de codar e antes de finalizar.

---

## 3. Entregáveis do MVP (o que “tem que existir” no repo)

### 3.1. Artefatos mínimos (SpecKit)
- Uma constituição/princípios (governança de engenharia)
- Para uma feature:
  - `spec.md`
  - `plan.md`
  - `tasks.md`

### 3.2. Evidências mínimas (Superpowers)
- Testes escritos antes do código (onde aplicável)
- Evidência de execução:
  - logs de teste
  - checklist de revisão/verificação preenchido (pode ser em PR description)

---

## 4. “Gate 1���: revisão pré-código (Superpowers)

### Objetivo
Impedir que a execução comece com:
- tarefas vagas
- tarefas sem critérios de verificação
- plano sem riscos/decisões explícitas
- ausência de estratégia de testes

### Checklist mínimo
- O `plan.md` declara:
  - arquitetura proposta e fronteiras de módulos
  - decisões de stack e justificativas
  - riscos técnicos e mitigação
- O `tasks.md` tem:
  - tarefas pequenas (2–15 min quando possível)
  - ordem coerente (dependências)
  - caminhos de arquivo/locais claros
  - passo de verificação por tarefa (ex.: “rodar `pytest -q`”, “executar `make lint`”)

**Critério de aprovação:** se uma pessoa (ou subagente) conseguir executar as tarefas sem “adivinhar” o que fazer.

---

## 5. Implementação TDD (Superpowers)

### Objetivo
Garantir RED/GREEN/REFACTOR real, evitando:
- “testes depois”
- “um commit enorme”
- “mudanças sem cobertura”

### Regras operacionais (mínimas)
- Para cada unidade de comportamento:
  1. escrever teste falhando
  2. implementar mínimo para passar
  3. refatorar mantendo verde
- Ciclos curtos com validação local:
  - `pytest -q` (ou comando equivalente)
  - linters/formatters quando existirem

---

## 6. “Gate 2”: verificação final (Superpowers)

### Objetivo
Não declarar pronto só porque “parece funcionar”.

### Checklist mínimo
- **Aderência ao spec:** tudo que está em `spec.md` relevante para a entrega está atendido
- **Aderência ao plan:** não houve desvio arquitetural sem registrar
- **Qualidade mínima:**
  - testes passam
  - lint/format passam (se aplicável)
  - nenhum “TODO crítico” ficou para trás
- **Evidência anexada:**
  - saída de testes e comandos usados
  - notas do que foi verificado manualmente (se existir UI)

---

## 7. Operação no dia a dia (Linux/terminal/vi)

### Sugestão de convenção
- editar artefatos em `vi`
- rodar comandos via `make` quando possível (padroniza)
- guardar checks no PR/commit message

Exemplo de rotina:
- `vi spec.md`
- `vi plan.md`
- `vi tasks.md`
- `pytest -q`
- `make lint` (se existir)
- `make test` (se existir)

---

## 8. Perguntas que eu preciso para “desenhar a integração no seu ambiente” (próximo passo)

Responda objetivamente:

1) Qual agente/CLI você usa com SpecKit (Copilot CLI, Claude Code, Cursor etc.)?
2) Você quer enforcement **hard** (bloqueia merge via CI) ou **soft** (checklist/recomendação)?
3) O repo é greenfield ou brownfield?
4) Qual comando padrão de testes/lint vocês adotam (ou desejam adotar) neste repo Python?
5) Vocês usam GitHub Actions? Se sim, qual workflow deve receber os gates?

Com isso eu consigo:
- propor a estrutura final de docs e templates
- definir “gates” em CI com critério objetivo
- sugerir um Makefile mínimo (test/lint/format)
- e um padrão de PR description para evidência.
