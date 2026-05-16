# BUG-05: Wizard objetivo-init não gera arquivo com informações inseridas

**Data**: 2026-04-28
**Severidade**: 🔴 Alta (bloqueia workflow completo)
**Status**: ✅ RESOLVIDO (2026-04-29)
**Afeta**: `scaffold objetivo-init`

---

## 📝 Descrição

O wizard `scaffold objetivo-init` executa sem erros, mas o arquivo gerado (`objetivo-draft.yaml` ou `objetivo-init.yaml`) **não contém as informações inseridas pelo usuário** durante as perguntas interativas.

---

## ✅ Resolução (2026-04-29)

### Causa Raiz Identificada

**Problema**: Mapeamento incorreto entre placeholders das perguntas e placeholders do template.

- ❌ Perguntas usavam `{{ANSWER_1}}`, `{{ANSWER_2}}`, `{{ANSWER_3}}`
- ❌ Template esperava `{{DESCRIPTION}}`, `{{FEATURE_1}}`, `{{RULE_1}}`
- ❌ Resultado: Substituição nunca acontecia

### Correções Implementadas

#### 1. **Atualização dos Placeholders das Perguntas** (`scripts/lib/objetivo_wizard.py`)

```python
# ANTES:
placeholder="{{ANSWER_1}}"  # ❌ Não existe no template

# DEPOIS:
placeholder="{{DESCRIPTION}}"  # ✅ Corresponde ao template
```

Placeholders corrigidos:
- `q1_what`: `{{ANSWER_1}}` → `{{DESCRIPTION}}`
- `q3_scope_included`: `{{ANSWER_3}}` → `{{FEATURE}}` (expansão multiline)
- `q4_constraints`: `{{ANSWER_4}}` → `{{CONSTRAINT}}` (expansão multiline)
- `q5_business_rules`: `{{ANSWER_5}}` → `{{RULE}}` (expansão multiline)
- `q8_infrastructure`: `{{INFRASTRUCTURE_1}}` → `{{INFRASTRUCTURE}}` (expansão)
- `q10_expected_outcome`: `{{EXPECTED_OUTCOME_1}}` → `{{EXPECTED_OUTCOME}}` (expansão)

#### 2. **Função `_render_template()` Melhorada**

Nova lógica implementada:
1. ✅ Substituição de placeholders simples (`{{DESCRIPTION}}`, `{{RESPONSE}}`)
2. ✅ **Expansão multiline → múltiplos placeholders**:
   - Input: `{{FEATURE}}` = "Feature 1\nFeature 2\nFeature 3"
   - Output: `{{FEATURE_1}}` = "Feature 1", `{{FEATURE_2}}` = "Feature 2", `{{FEATURE_3}}` = "Feature 3"
3. ✅ Valores padrão para placeholders sem perguntas
4. ✅ Limpeza de placeholders não substituídos (regex)

```python
def _render_template(self, answers: WizardAnswers) -> str:
    # ...
    # Process multiline expansion
    if '\n' in value and base_placeholder in ['FEATURE', 'RULE', 'CONSTRAINT', ...]:
        lines = [line.strip() for line in value.split('\n') if line.strip()]
        for i, line in enumerate(lines, start=1):
            numbered_placeholder = f"{{{{{base_placeholder}_{i}}}}}"
            processed_placeholders[numbered_placeholder] = line
```

#### 3. **Simplificação do Template** (`template-bases/objetivo-init-template.yaml`)

- ✅ Removidos placeholders complexos sem suporte (PROFILE com múltiplos campos, PENDING_TASK)
- ✅ Adicionados valores padrão para profile e pending_tasks
- ✅ Template agora corresponde às capabilities do wizard

#### 4. **Suite de Testes Criada** (`tests/test_bug05_objetivo_wizard_placeholders.py`)

4 testes implementados:
- ✅ `test_simple_placeholder_replacement()` - Placeholders simples
- ✅ `test_multiline_placeholder_expansion()` - Expansão multiline
- ✅ `test_default_placeholders()` - Valores padrão
- ✅ `test_no_unreplaced_placeholders()` - Nenhum `{{PLACEHOLDER}}` no output

**Resultado**: 4/4 testes passando ✅

### Arquivos Modificados

- `scripts/lib/objetivo_wizard.py` (7 placeholders corrigidos + nova lógica de rendering)
- `template-bases/objetivo-init-template.yaml` (simplificação de seções complexas)
- `tests/test_bug05_objetivo_wizard_placeholders.py` (novo - 4 testes)

---

## 🔍 Reprodução (ANTES da correção)

### Passos

```bash
cd ~/DevOps/Projetos/knowledge-harvester-library
scaffold objetivo-init
```

**Comportamento esperado**:
- Wizard pergunta 15 questões (6 P0 + 9 P1)
- Usuário responde cada pergunta
- Arquivo `objetivo-init.yaml` é gerado com **respostas do usuário**

**Comportamento observado**:
- Wizard pergunta as questões ✅
- Usuário responde ✅
- Arquivo `objetivo-draft.yaml` é gerado ✅
- **MAS**: Arquivo contém **placeholders vazios** (ex: `{{PROJECT_NAME}}`, `{{DESCRIPTION}}`) ao invés das respostas

---

## 🧪 Evidência

### Arquivo gerado (exemplo)

```yaml
# /home/yves_marinho/DevOps/Projetos/knowledge-harvester-library/objetivo-draft.yaml
prompt:
  role: user
  content:
    description: "{{DESCRIPTION}}"  # ❌ Deveria ter resposta do usuário
    specification:
      - project_name: "{{PROJECT_NAME}}"  # ❌ Deveria ter resposta
      - response: "{{RESPONSE}}"  # ❌ Deveria ter resposta
```

### Arquivo esperado (exemplo)

```yaml
prompt:
  role: user
  content:
    description: "Agregador local de conhecimento a partir de repositórios Git"
    specification:
      - project_name: "knowledge-harvester-library"
      - response: "código python 3.12+, JSON/JSONL, YAML"
```

---

## 🔎 Análise Técnica

### Arquivos envolvidos

1. **`scripts/lib/objetivo_wizard.py`**
   - Função: `_render_template(answers: WizardAnswers) -> str`
   - Linha ~340-365: Substituição de placeholders
   - **Suspeita**: Mapeamento incorreto entre respostas e placeholders

2. **`template-bases/objetivo-init-template.yaml`**
   - Contém placeholders: `{{PROJECT_NAME}}`, `{{DESCRIPTION}}`, etc
   - **Suspeita**: Placeholders podem não corresponder aos usados no wizard

3. **`scripts/lib/flows/objetivo_init.py`**
   - Função: `flow_objetivo_init(args) -> int`
   - Linha ~41: Chamada `wizard.run(output_path)`
   - **Suspeita**: Answers pode não estar sendo populado corretamente

### Hipóteses de Causa Raiz

#### Hipótese 1: Mapeamento placeholder ≠ ID de pergunta ❌

```python
# objetivo_wizard.py - _build_questions()
WizardQuestion(
    id="q1_description",
    placeholder="{{DESCRIPTION}}",  # Placeholder esperado
    ...
)

# objetivo_wizard.py - _render_template()
for question in self.questions:
    placeholder = question.placeholder
    value = self.answers.answers.get(placeholder)  # ❌ Busca por "{{DESCRIPTION}}"
    # MAS answers pode estar armazenado como "q1_description"
```

**Verificação necessária**:
```python
# Em run(), verificar se answers é populado assim:
self.answers.answers[question.placeholder] = answer  # ✅ Correto
# OU
self.answers.answers[question.id] = answer  # ❌ Errado (causa o bug)
```

#### Hipótese 2: Template não carregado corretamente ❌

```python
# objetivo_wizard.py - __init__()
self.template_path = template_path or (
    Path(__file__).parent.parent.parent / "template-bases" / "objetivo-init-template.yaml"
)

# Verificação: o arquivo existe e é legível?
# Verificação: template_content é lido corretamente em _render_template()?
```

#### Hipótese 3: Ctrl+C salvou draft antes de completar perguntas ⚠️

```python
# objetivo_wizard.py - run()
except KeyboardInterrupt:
    self.save_draft()  # Salva answers parciais
    return 1
```

**Verificação necessária**:
- Usuário pressionou Ctrl+C durante wizard?
- Draft foi salvo com respostas parciais (primeiras perguntas) ou vazias?

#### Hipótese 4: Função `_render_template()` não substitui corretamente ❌

```python
# objetivo_wizard.py - _render_template()
def _render_template(self, answers: WizardAnswers) -> str:
    template = self.template_path.read_text(encoding='utf-8')

    # Substituição de metadados
    template = template.replace("{{PROJECT_NAME}}", answers.project_name or "")
    # ❌ Se answers.project_name é None, substitui por ""

    # Substituição de respostas
    for question in self.questions:
        placeholder = question.placeholder
        value = answers.answers.get(placeholder)  # ❌ Pode retornar None
        if value:
            template = template.replace(placeholder, value)
        # ❌ Se value é None, placeholder fica no arquivo
```

**Problema identificado**:
- Se `answers.answers.get(placeholder)` retorna `None`, o `if value:` **não entra** e o placeholder **não é substituído**
- Resultado: arquivo final contém `{{DESCRIPTION}}` ao invés de valor real

---

## 🐛 Causa Raiz Provável

**Alta probabilidade**: Função `_render_template()` não está substituindo placeholders porque:

1. **Respostas não estão sendo armazenadas em `answers.answers` com a chave correta**
   ```python
   # Em run(), pode estar fazendo:
   self.answers.answers[question.id] = answer  # ❌ Errado
   # Deveria ser:
   self.answers.answers[question.placeholder] = answer  # ✅ Correto
   ```

2. **OU**: Metadados do projeto não estão sendo salvos em `WizardAnswers`
   ```python
   # Em run(), pode estar faltando:
   self.answers.project_name = resposta_nome_projeto
   self.answers.project_title = resposta_titulo
   # etc
   ```

---

## 🔧 Correção Sugerida

### 1. Adicionar Debug Logging

```python
# scripts/lib/objetivo_wizard.py - _render_template()
def _render_template(self, answers: WizardAnswers) -> str:
    template = self.template_path.read_text(encoding='utf-8')

    # DEBUG: Verificar conteúdo de answers
    print(f"DEBUG: project_name = {answers.project_name}")
    print(f"DEBUG: answers.answers = {answers.answers}")

    # Substituição
    template = template.replace("{{PROJECT_NAME}}", answers.project_name or "MISSING_PROJECT_NAME")

    for question in self.questions:
        placeholder = question.placeholder
        value = answers.answers.get(placeholder)
        print(f"DEBUG: {placeholder} -> {value}")  # DEBUG
        if value:
            template = template.replace(placeholder, value)
        else:
            print(f"WARNING: {placeholder} sem valor!")  # DEBUG

    return template
```

### 2. Verificar armazenamento de respostas

```python
# scripts/lib/objetivo_wizard.py - run()
# Linha ~420-450
for question in p0_questions:
    answer = self._ask_question(question)
    if answer:
        # ✅ VERIFICAR: usar placeholder, não question.id
        self.answers.answers[question.placeholder] = answer
        self.answer_stack.append((question, answer))
```

### 3. Garantir fallback para placeholders não preenchidos

```python
# scripts/lib/objetivo_wizard.py - _render_template()
# Substituir None por string indicativa
for question in self.questions:
    placeholder = question.placeholder
    value = answers.answers.get(placeholder) or f"[TODO: {question.prompt[:30]}]"
    template = template.replace(placeholder, value)
```

---

## ✅ Verificação da Correção

### Teste 1: Wizard completo

```bash
cd /tmp/test-wizard
scaffold objetivo-init

# Responder todas perguntas
# Verificar se objetivo-init.yaml contém respostas reais (não placeholders)
grep -E '\{\{.*\}\}' objetivo-init.yaml  # ❌ Não deve retornar nada
```

### Teste 2: Wizard cancelado (Ctrl+C)

```bash
cd /tmp/test-wizard-cancel
scaffold objetivo-init

# Responder 3 perguntas
# Pressionar Ctrl+C

# Verificar se objetivo-draft.yaml contém respostas parciais
grep -E '\{\{.*\}\}' objetivo-draft.yaml  # ⚠️ Pode conter placeholders não respondidos
```

### Teste 3: Verificar logs de debug

```bash
scaffold objetivo-init 2>&1 | tee wizard-debug.log

# Analisar:
# - "DEBUG: project_name = ..." deve mostrar valor real
# - "DEBUG: {{DESCRIPTION}} -> ..." deve mostrar valor ou None
# - "WARNING: ..." indica placeholders sem valor
```

---

## 📊 Impacto

### Usuários afetados
- ✅ Todos usuários de `scaffold objetivo-init`

### Workflows bloqueados
- ❌ Criação de novo projeto via wizard interativo
- ❌ Pipeline: `objetivo-init → validate → generate → new`

### Workaround disponível
✅ **Sim**: Editar manualmente `objetivo-draft.yaml` e preencher campos (como usuário fez)

---

## 🚦 Prioridade

**P0 - Crítico**: Bloqueia workflow principal de criação de projetos

**Recomendação**: Fix imediato antes de próximo sprint

---

## 📎 Logs e Contexto

### Execução reportada

```bash
# Terminal: knowledge-harvester-library
$ scaffold objetivo-init

# Wizard executou
# Usuário respondeu todas perguntas
# Arquivo gerado: objetivo-draft.yaml
# Conteúdo: placeholders vazios ({{PROJECT_NAME}}, etc)
```

### Ambiente

- **SO**: Linux
- **Python**: 3.12.3
- **Projeto**: knowledge-harvester-library
- **Branch**: (não especificado)
- **Versão scaffold**: (verificar com `scaffold --version`)

---

## 🔗 Referências

- [docs/debates/OPINIAO_OBJETIVO_INIT_WIZARD.md](../debates/OPINIAO_OBJETIVO_INIT_WIZARD.md) - Análise do formato v1.0
- [scripts/lib/objetivo_wizard.py](../../scripts/lib/objetivo_wizard.py) - Implementação do wizard
- [template-bases/objetivo-init-template.yaml](../../template-bases/objetivo-init-template.yaml) - Template com placeholders

---

## 📝 Próximos Passos

1. [ ] Executar wizard com logging de debug habilitado
2. [ ] Verificar se `answers.answers` está populado corretamente
3. [ ] Validar mapeamento `question.id` vs `question.placeholder`
4. [ ] Corrigir `_render_template()` se necessário
5. [ ] Adicionar testes unitários para `_render_template()`
6. [ ] Testar wizard end-to-end após correção

---

**Assignee**: (a definir)
**Sprint**: (a definir)
**Related Issues**: #IMP-66 (objetivo.yaml v2.0)
