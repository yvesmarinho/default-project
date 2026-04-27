---
date: "2026-04-27"
phase: "Fase 1 - Validação"
tasks: "T004"
projects_analyzed:
  - "poc/objetivo-v2-python-fastapi.md (850 lines)"
  - "poc/objetivo-v2-k8s-helm.md (680 lines)"
  - "poc/objetivo-v2-terraform-aws.md (780 lines)"
status: "in-progress"
---

# Validação Fase 1 — Edge Cases e Learnings

**Objetivo**: Documentar desafios, ambiguidades e melhorias identificadas ao converter 3 projetos template para formato objetivo.yaml v2.0

**Contexto**: T001 (python-fastapi), T002 (k8s-helm), T003 (terraform-aws) foram convertidos manualmente para validar formato antes de implementar parser (Fase 2).

---

## 📊 Resumo Executivo

| Aspecto | Resultado | Ação Necessária |
|---------|-----------|-----------------|
| **Target de linhas** | Todos excederam (2-3x) | ⚠️ Ajustar expectativa ou criar versão "resumida" |
| **YAML frontmatter** | Funcionou bem | ✅ Sem mudanças |
| **Progressive disclosure** | P0/P1/P2 não explícito | ⚠️ Adicionar comentários no template |
| **Seção 5️⃣ Regras de Negócio** | Precisou sub-estrutura | ✅ Padrão "Regra #N" validado |
| **Seção 6️⃣ Estrutura** | Comentários inline essenciais | ✅ Padrão validado |
| **Seção 8️⃣ Próximos Passos** | Checkboxes + Fases funcionam | ✅ Padrão validado |
| **Exemplos inline** | Críticos mas verbosos | ⚠️ Orientação: 1-2 por regra |
| **Tabelas Markdown** | Excelente para métricas | ✅ Padrão validado |
| **Emojis** | Úteis mas podem saturar | ⚠️ Orientação: seções principais apenas |

---

## 🔍 Edge Cases por Categoria

### 1. Target de Linhas vs Realidade

**Problema identificado**:
- **Target esperado**: ~300 linhas (FastAPI), ~280 (Helm), ~320 (Terraform)
- **Realidade**:
  - FastAPI: **850 linhas** (+183% do target)
  - Helm: **680 linhas** (+143% do target)
  - Terraform: **780 linhas** (+144% do target)

**Por que excedeu**:
1. **Projetos realistas requerem detalhamento**:
   - FastAPI: 5 regras de negócio com cenários, validações, outputs esperados
   - Helm: Chart completo com values overrides, templates, annotations
   - Terraform: 3 módulos (VPC/ECS/RDS) com IAM policies, security groups
2. **Exemplos inline aumentam tamanho**:
   - JSON responses (FastAPI): ~50 linhas
   - YAML snippets (Helm): ~80 linhas
   - HCL code blocks (Terraform): ~100 linhas
3. **Seção 8️⃣ Próximos Passos detalhada**:
   - Organização por Fases com checkboxes: ~150 linhas (FastAPI teve 5 fases)

**Impacto**:
- ✅ **Positivo**: Exemplos completos são mais úteis que resumos vagos
- ⚠️ **Negativo**: Tempo de leitura aumenta (15-20 min vs 5 min)

**Recomendações**:
1. **Ajustar expectativa**: Target de ~500 linhas para projetos reais (não 300)
2. **Versão "resumida" opcional**: Apenas P0 (seções 1-3) para overview rápido
3. **Guideline no template**: "Seção 5️⃣: máximo 5 regras, 1-2 exemplos por regra"

---

### 2. YAML Frontmatter — Campos Ambíguos

**Campo**: `generation.generate_spec_on_change`

**Problema**:
- Não ficou claro o que "generate spec" significa:
  - Gerar `spec.md` (SpecKit)?
  - Gerar `objetivo-spec.yaml` (Two-File Architecture)?
  - Triggerar validação automática?

**Solução encontrada** (aplicada nos 3 POCs):
- Mantive `generate_spec_on_change: false` em todos (valor conservador)
- Assumo que "spec" = `objetivo-spec.yaml` (Two-File)

**Recomendação**:
- Adicionar comentário inline no template:
  ```yaml
  generation:
    generate_spec_on_change: false  # Auto-gera objetivo-spec.yaml ao salvar (futuro)
  ```

---

**Campo**: `validation.level`

**Problema**:
- Valores possíveis não documentados (apenas "strict" usado)
- O que é "strict" vs "permissive" vs "off"?

**Solução encontrada**:
- Usei `level: "strict"` em todos (padrão mais seguro)

**Recomendação**:
- Adicionar enum no comentário:
  ```yaml
  validation:
    level: "strict"  # Options: strict (bloqueia erros), permissive (warns), off
  ```

---

**Campo**: `project.type`

**Problema**:
- Valores livres vs enum pré-definido?
- Usei: `backend-api`, `deployment-chart`, `infrastructure-code`
- Mas poderiam ser: `api`, `chart`, `infra`?

**Solução encontrada**:
- Segui padrão kebab-case descritivo

**Recomendação**:
- Criar lista de types comuns no template (comentário):
  ```yaml
  project:
    type: "backend-api"  # Comum: backend-api, frontend-spa, cli-tool, library, deployment-chart, infrastructure-code
  ```

---

### 3. Progressive Disclosure — P0/P1/P2 Não Explícito

**Problema**:
- Template não indica quais seções são P0, P1, P2
- Apenas referência no design docs (`COMPARACAO.md`)
- Usuário precisa adivinhar: "Seção 4️⃣ é P1 ou P2?"

**Impacto**:
- Durante conversão, precisei consultar design docs múltiplas vezes

**Solução aplicada nos POCs**:
- Adicionei comentários inline:
  ```markdown
  ## 1️⃣ O que este projeto faz?  <!-- P0 -->
  ## 4️⃣ Restrições e Requisitos  <!-- P1 -->
  ## 6️⃣ Estrutura de Pastas      <!-- P2 -->
  ```

**Recomendação**:
- Template final deve incluir `<!-- P0 -->`, `<!-- P1 -->`, `<!-- P2 -->` em cada heading
- Ou adicionar seção no topo do template:
  ```markdown
  <!-- Progressive Disclosure:
       P0 (essencial): Seções 1-3
       P1 (contextual): Seções 4-5
       P2 (avançado): Seções 6-9
  -->
  ```

---

### 4. Seção 5️⃣ Regras de Negócio — Estrutura

**Problema**:
- Um único bloco de texto para múltiplas regras fica confuso
- Exemplos inline misturados com validações

**Solução encontrada** (aplicada em todos POCs):
- Sub-estrutura **"Regra #N: Nome da Regra"**:
  ```markdown
  ### Regra #1: Registro de Usuários (Self-Registration)
  
  **Cenário**: ...
  
  **Validações**:
  - ✅ Email: formato válido
  - ❌ Emails temporários bloqueados
  
  **Output esperado**:
  ```json
  { "id": "uuid", ... }
  ```
  
  **Regra de auditoria**:
  - ✅ Log em `audit_logs`
  ```

**Padrão validado**:
- ✅ **Sub-headers** (`### Regra #N`) funcionam muito bem
- ✅ **Checklist visual** (✅ ❌ ⚠️) facilita scan rápido
- ✅ **Code blocks** para outputs esperados são críticos

**Recomendação**:
- Adicionar no template guidance:
  ```markdown
  ## 5️⃣ Regras de Negócio
  
  <!-- Organize como:
       ### Regra #1: Nome Descritivo
       **Cenário**: Quando X acontece
       **Validações**: Lista de checks
       **Output esperado**: Exemplo concreto
  -->
  ```

---

### 5. Seção 6️⃣ Estrutura de Pastas — Comentários Inline

**Problema**:
- Tree structure sem comentários = difícil entender o que cada arquivo faz
- Exemplo ruim:
  ```
  src/
  ├── main.py
  ├── api/
  │   └── v1/
  │       └── users.py
  ```
  (usuário pensa: "O que tem em users.py?")

**Solução aplicada** (todos POCs):
- **Comentários inline** explicando cada arquivo:
  ```
  src/
  ├── main.py                      # FastAPI app factory com lifespan
  │                                # Registra routers, configura CORS
  │
  ├── api/
  │   └── v1/
  │       └── users.py             # CRUD /users, /users/{id}
  ```

**Padrão validado**:
- ✅ Comentários `# ...` após cada arquivo/pasta
- ✅ Indentação de comentários multi-linha alinhada
- ✅ Separação visual com linha vazia entre blocos

**Recomendação**:
- Template deve incluir exemplo com comentários:
  ```markdown
  ## 6️⃣ Estrutura de Pastas
  
  ```
  projeto/
  ├── src/
  │   ├── main.py              # Ponto de entrada principal
  │   └── core/
  │       └── config.py        # Configurações via env vars
  ```
  
  <!-- Use comentários # para explicar o propósito de cada arquivo -->
  ```

---

### 6. Seção 8️⃣ Próximos Passos — Organização

**Problema**:
- Lista plana de checkboxes fica difícil de navegar (ex: 30 tarefas)

**Solução aplicada** (todos POCs):
- **Organização hierárquica por Fases**:
  ```markdown
  ### Fase 1: Setup Inicial (1 dia)
  
  **Estrutura do projeto**:
  - [ ] Criar estrutura de pastas
  - [ ] Configurar pyproject.toml
  
  **Database setup**:
  - [ ] Configurar SQLAlchemy
  - [ ] Criar migration inicial
  ```

**Padrão validado**:
- ✅ Sub-headers `### Fase N: Nome (tempo estimado)`
- ✅ Sub-sub-headers para agrupar tarefas relacionadas
- ✅ Checkboxes `- [ ]` para tracking
- ✅ Estimativas de tempo por fase (não por task individual)

**Recomendação**:
- Template deve incluir exemplo de organização:
  ```markdown
  ## 8️⃣ Próximos Passos
  
  ### Fase 1: Nome da Fase (tempo estimado)
  
  **Grupo de tarefas**:
  - [ ] Tarefa 1
  - [ ] Tarefa 2
  ```

---

### 7. Exemplos Inline — Code Blocks

**Problema**:
- Sem exemplos = vago ("autenticação JWT" mas como?)
- Muitos exemplos = verboso (código completo de 50 linhas)

**Solução aplicada** (todos POCs):
- **1-2 exemplos estratégicos por regra/seção**:
  - **JSON response** (FastAPI Regra #1):
    ```json
    {
      "id": "uuid-v4",
      "email": "user@example.com",
      "role": "user"
    }
    ```
  - **YAML snippet** (Helm Regra #4):
    ```yaml
    behavior:
      scaleDown:
        stabilizationWindowSeconds: 300
    ```
  - **HCL code** (Terraform Regra #3):
    ```hcl
    resource "aws_iam_role_policy" "task_policy" {
      policy = jsonencode({ ... })
    }
    ```

**Padrão validado**:
- ✅ Snippets focados (5-15 linhas, não arquivos completos)
- ✅ Comentários inline no código quando necessário
- ✅ Output esperado em formato real (não pseudo-código)

**Guideline descoberto**:
- Máximo **2 code blocks por regra** (evita sobrecarga)
- Preferir **outputs esperados** (JSON, YAML) vs código de implementação
- Se código de implementação necessário → máximo 20 linhas

**Recomendação**:
- Adicionar guideline no template:
  ```markdown
  <!-- Exemplos inline:
       - Use code blocks para outputs esperados (JSON, YAML, etc)
       - Máximo 2 exemplos por regra/seção
       - Foco em snippets (5-15 linhas), não arquivos completos
  -->
  ```

---

### 8. Tabelas Markdown — Uso Efetivo

**Problema**:
- Comparações textuais ficam confusas ("staging tem 1 réplica, prod tem 3...")

**Solução aplicada** (todos POCs):
- **Tabelas para comparações** (Before/After, Staging/Prod, Metrics):

**Exemplo 1 — Métricas** (FastAPI Seção 2️⃣):
```markdown
| **Métrica** | **Sistema Legado** | **Esta API** | **Δ** |
|-------------|---------------------|--------------|-------|
| Tempo login | 800-1200ms          | <100ms       | -90%  |
| Taxa erro   | 12%                 | <1%          | -92%  |
```

**Exemplo 2 — Permissões** (FastAPI Regra #3):
```markdown
| Endpoint | user | admin |
|----------|------|-------|
| GET /users | ✅ (self) | ✅ (todos) |
| DELETE /users | ❌ | ✅ |
```

**Exemplo 3 — Configs por Ambiente** (Terraform Regra #4):
```markdown
| Ambiente | requests.cpu | limits.cpu | multi_az |
|----------|--------------|------------|----------|
| Staging  | 50m          | 200m       | false    |
| Prod     | 100m         | 500m       | true     |
```

**Padrão validado**:
- ✅ Tabelas para comparações lado-a-lado
- ✅ Emojis em cells (✅ ❌) para quick scan
- ✅ Alinhamento de colunas numéricas

**Recomendação**:
- Template deve incluir exemplo de tabela:
  ```markdown
  ## 2️⃣ Qual problema resolve?
  
  | Métrica | Antes | Depois | Δ |
  |---------|-------|--------|---|
  | Tempo   | 5 min | 30s    | -90% |
  ```

---

### 9. Emojis — Saturação Visual

**Problema**:
- Emojis úteis para orientação, mas podem saturar se usados excessivamente
- Exemplo de saturação:
  ```markdown
  ✅ Email válido ✅
  ❌ Não pode ser temporário ❌
  ⚠️ Aviso: máximo 100 caracteres ⚠️
  ```

**Solução aplicada** (todos POCs):
- **Uso moderado e consistente**:
  - Seções principais: 🎯 1️⃣ 2️⃣ ... 9️⃣
  - Checklist: ✅ (incluído), ❌ (excluído), ⚠️ (atenção)
  - Não duplicar emoji no início e fim da mesma linha

**Padrão validado**:
- ✅ Um emoji por linha/item (não duplicar)
- ✅ Emojis de seção (1️⃣-9️⃣) apenas em headers
- ✅ Emojis de status (✅ ❌ ⚠️) em listas

**Guideline descoberto**:
- **Seções**: 🎯 no título principal, 1️⃣-9️⃣ em `## headers`
- **Status**: ✅ sim, ❌ não, ⚠️ atenção (início de linha apenas)
- **Evitar**: 🚀 🔥 💡 etc (distração)

**Recomendação**:
- Template deve incluir guideline:
  ```markdown
  <!-- Emojis:
       - Seções: 🎯 1️⃣ 2️⃣ ... 9️⃣ (headers apenas)
       - Status: ✅ incluído, ❌ excluído, ⚠️ atenção
       - Evite: emojis decorativos excessivos
  -->
  ```

---

### 10. Seção 9️⃣ Contexto Adicional — Conteúdo

**Problema**:
- Nome "Contexto Adicional" muito genérico
- Durante conversão, não ficou claro o que colocar aqui

**Solução aplicada** (todos POCs):
- **Sub-estrutura fixa**:
  ```markdown
  ### Histórico do Projeto
  - Quando criado
  - Parte de qual iniciativa
  
  ### Arquitetura de Referência
  - Pattern usado (ex: Repository + Service Layer)
  - Diagrama ou ASCII art
  
  ### Decisões de Design
  - Por que tecnologia X em vez de Y?
  - Trade-offs importantes
  
  ### Referências Externas
  - Links para docs oficiais
  - Projetos similares
  
  ### Meta-Observação
  - Validação do objetivo.yaml v2.0 em si
  ```

**Padrão validado**:
- ✅ Sub-headers fixas ajudam a preencher
- ✅ "Por que X em vez de Y?" é útil para onboarding
- ✅ "Meta-Observação" fecha o loop (objetivo validando o próprio formato)

**Recomendação**:
- Renomear seção ou adicionar sub-headers sugeridas no template:
  ```markdown
  ## 9️⃣ Contexto Adicional
  
  ### Histórico do Projeto
  <!-- Quando criado, por quê, parte de qual iniciativa -->
  
  ### Decisões de Design
  <!-- Por que tecnologia X em vez de Y? Trade-offs -->
  
  ### Referências Externas
  <!-- Links para docs, projetos similares -->
  ```

---

## 🚀 Melhorias Propostas para Template

### Prioridade Alta (implementar antes de Fase 2)

1. **Adicionar comentários inline no YAML frontmatter**:
   ```yaml
   project:
     type: "backend-api"  # Comum: backend-api, frontend-spa, cli-tool, etc
   
   generation:
     generate_spec_on_change: false  # Auto-gera objetivo-spec.yaml ao salvar
   
   validation:
     level: "strict"  # Options: strict, permissive, off
   ```

2. **Indicar P0/P1/P2 no template** (comentários HTML):
   ```markdown
   ## 1️⃣ O que este projeto faz? <!-- P0 - Essencial -->
   ## 4️⃣ Restrições e Requisitos <!-- P1 - Contextual -->
   ## 6️⃣ Estrutura de Pastas     <!-- P2 - Avançado -->
   ```

3. **Guideline para Seção 5️⃣ Regras de Negócio**:
   ```markdown
   ## 5️⃣ Regras de Negócio
   
   <!-- Organize como:
        ### Regra #1: Nome Descritivo
        **Cenário**: ...
        **Validações**: lista com ✅ ❌
        **Output esperado**: code block
        Máximo 5 regras, 1-2 exemplos por regra
   -->
   ```

4. **Exemplo de Estrutura de Pastas com comentários**:
   ```markdown
   ## 6️⃣ Estrutura de Pastas
   
   ```
   projeto/
   ├── src/
   │   ├── main.py              # Ponto de entrada principal
   │   └── core/
   │       └── config.py        # Configurações via env vars
   ```
   
   <!-- Use comentários # inline para explicar cada arquivo -->
   ```

5. **Ajustar expectativa de linhas**:
   - Remover "Target: ~300 linhas" ou ajustar para **"~500 linhas para projetos reais"**
   - Adicionar nota: "Versão resumida (P0 apenas): ~150 linhas"

---

### Prioridade Média (considerar para v2.1)

6. **Template variant "resumido"**:
   - `objetivo-resumido.yaml`: Apenas seções P0 (1-3)
   - Para casos onde overview rápido é suficiente
   - Converter para completo depois se necessário

7. **Validação de YAML frontmatter com schema**:
   - Criar JSON Schema para frontmatter
   - Validar campos obrigatórios, types, enums
   - Mensagens de erro com linha exata

8. **Exemplos de tabelas no template**:
   - Incluir exemplo de tabela Before/After
   - Exemplo de tabela de permissões
   - Exemplo de configs por ambiente

---

### Prioridade Baixa (nice-to-have)

9. **Linter de emojis**:
   - Validar uso consistente (não duplicar)
   - Alertar se emojis decorativos excessivos

10. **Generator de Seção 9️⃣**:
    - Script que gera "Histórico" automaticamente (git log)
    - Links para docs oficiais baseados em tecnologias da Seção 7️⃣

---

## 📝 Feedback de Conversão Manual

### Facilidades (o que funcionou bem)

1. **YAML frontmatter**: Fácil de preencher, campos intuitivos
2. **Seções numeradas** (1️⃣-9️⃣): Navegação clara, ordem lógica
3. **Checklist visual** (✅ ❌): Quick scan do que está incluído/excluído
4. **Code blocks**: Syntax highlighting automático no VS Code
5. **Tabelas Markdown**: Comparações lado-a-lado são poderosas

### Dificuldades (o que causou fricção)

1. **Decidir profundidade**: Quando parar de detalhar? (ex: Seção 5️⃣ poderia ter 10 regras)
2. **Target de linhas**: Pressão para resumir vs necessidade de completude
3. **Seção 9️⃣**: "Contexto Adicional" é vago, precisei criar sub-estrutura própria
4. **Exemplos inline**: Difícil saber quantos são "suficientes" (usei 1-2 por regra)
5. **P0/P1/P2**: Tive que consultar docs múltiplas vezes (não está no template)

---

## 🎯 Próximos Passos

### T005 — User Testing

- [ ] Recrutar 2-3 usuários (1 iniciante, 1-2 intermediários)
- [ ] Pedir para preencher objetivo.yaml v2.0 para projeto simples (~150 linhas)
- [ ] Medir: tempo de preenchimento, pontos de confusão, campos deixados vazios
- [ ] Coletar feedback: o que foi claro, o que foi confuso, sugestões
- [ ] Documentar resultados neste arquivo (nova seção "User Testing Results")

### Ajustes no Template (antes de Fase 2)

- [ ] Aplicar melhorias Prioridade Alta (items 1-5 acima)
- [ ] Atualizar `specs/066-objetivo-yaml-v2/objetivo.yaml` (meta-example)
- [ ] Validar mudanças com POCs existentes (re-preencher se necessário)

### Fase 2 — Parser Implementation

- [ ] Parser deve suportar comentários HTML `<!-- P0 -->`
- [ ] Validator deve verificar P0 obrigatório (seções 1-3)
- [ ] Mensagens de erro devem referenciar linha exata (parser + line numbers)

---

## 📚 Apêndices

### A. Comparação de Tamanhos

| POC | Target | Real | Excesso | Seções P0 | Seções P1 | Seções P2 |
|-----|--------|------|---------|-----------|-----------|-----------|
| python-fastapi | 300 | 850 | +183% | 220 (~26%) | 280 (~33%) | 350 (~41%) |
| k8s-helm | 280 | 680 | +143% | 180 (~26%) | 240 (~35%) | 260 (~38%) |
| terraform-aws | 320 | 780 | +144% | 200 (~26%) | 260 (~33%) | 320 (~41%) |

**Insight**: Seções P2 (6-9) representam ~40% do conteúdo → validando progressive disclosure.

---

### B. Estatísticas de Code Blocks

| POC | Code Blocks | Linguagens | Linhas de Código | % do Total |
|-----|-------------|------------|------------------|------------|
| python-fastapi | 18 | JSON, Python, Bash | ~180 | 21% |
| k8s-helm | 22 | YAML, Bash | ~220 | 32% |
| terraform-aws | 24 | HCL, Bash, JSON | ~240 | 31% |

**Insight**: ~25-30% do conteúdo são exemplos de código → crítico para clareza.

---

### C. Distribuição de Emojis

| Tipo | Ocorrências | Contexto |
|------|-------------|----------|
| 1️⃣-9️⃣ | 9 por doc | Headers de seção |
| ✅ | ~40 por doc | Checklist incluído, validações |
| ❌ | ~20 por doc | Checklist excluído, anti-patterns |
| ⚠️ | ~10 por doc | Atenção, trade-offs |
| 🎯 | 1 por doc | Título principal |

**Insight**: Emojis usados de forma moderada e consistente.

---

## 🏁 Conclusão

**Status Fase 1**: ✅ **T001-T003 completos**, T004 documentado, **ready for T005 (user testing)**

**Formato v2.0**: ✅ **Validado em 3 domínios** (backend-api, deployment-chart, infrastructure-code)

**Edge cases identificados**: 10 principais, todos com soluções aplicadas e recomendações

**Melhorias propostas**: 5 prioridade alta (implementar antes de Fase 2), 5 prioridade média/baixa (v2.1)

**Próximo milestone**: T005 (user testing) → ajustes finais → **Fase 2 (Parser implementation)**
