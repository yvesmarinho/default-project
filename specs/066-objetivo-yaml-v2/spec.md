---
template_version: "2.2.0"
last_updated: "2026-04-27"
breaking_changes: false
---

# Feature Specification: objetivo.yaml v2.0 — Human-Readable Format

**Feature ID**: 066-objetivo-yaml-v2
**Feature Branch**: `066-objetivo-yaml-v2`
**Created**: 2026-04-27
**Status**: Draft → Approved
**Business Objective**: See debate docs/debates/DEBATE-OBJETIVO-YAML-HUMAN-READABLE-COMPLETO.md
**Input**: User feedback on objetivo-init.yaml complexity

---

## Business Context (from debate analysis)

**Problem**: Formato atual objetivo.yaml v1.0 é "difícil de entender e preencher" especialmente para iniciantes. 18 campos obrigatórios, fronteira ambígua entre input humano e geração Copilot, zero exemplos inline, YAML aninhado técnico demais.

**Value Proposition**: 
- **-75% tempo de preenchimento** (45-60 min → 10-15 min)
- **-89% taxa de erro** (38% → 4% campos obrigatórios)
- **+171% NPS** (28 → 76 satisfação)
- **-81% taxa de abandono** (42% → 8% primeira tentativa)

**Success Metrics**:
- ✅ 100% projetos novos usam v2.0 após 4 semanas de lançamento
- ✅ <15 min tempo médio de preenchimento (iniciantes)
- ✅ <5% taxa de erro em campos obrigatórios
- ✅ NPS >70 (satisfação com formato)

**Key Personas**:
1. **DevOps Iniciante** (20% usuários) — Primeira vez usando template, precisa de exemplos claros
2. **Programador Intermediário** (50% usuários) — Conhece projeto, quer preencher rápido sem burocracia
3. **Tech Lead Avançado** (30% usuários) — Quer controle fino sobre perfis, validação, estrutura

**Initial Decisions** (from user feedback):
- ✅ **Formato híbrido** (YAML frontmatter + Markdown body) — Aprovado Q1
- ✅ **Progressive disclosure 3 níveis** (P0/P1/P2) — Aprovado Q2
- ✅ **Emojis como orientação visual** — Aprovado Q3 ("ajuda")
- ✅ **Arquitetura two-file** (objetivo.yaml humano + objetivo-spec.yaml máquina) — Aprovado Q4
- ✅ **Validação inline** (comentários `<!-- REQUIRED -->`) — Aprovado Q5 ("ajuda")

---

## Performance Criteria

### Response Time Requirements
- **Parser execution**: Parse objetivo.yaml v2.0 < 100ms
- **Validation**: Validate P0/P1/P2 fields < 50ms
- **Generation**: Generate objetivo-spec.yaml < 200ms

### Throughput & Scalability
- **File size**: Support objetivo.yaml até 10KB (≈350 linhas)
- **Concurrent generation**: Handle 10+ projetos simultâneos sem degradação

### Reliability
- **Backward compatibility**: Parser detecta v1.0 e oferece migração automática
- **Error handling**: Mensagens de erro claras com linha/coluna/exemplo de correção

### Resource Constraints
- **Dependencies**: Zero dependências externas (stdlib Python only)
- **Memory**: <10MB para parse + validação + geração

### Accessibility Criteria
- **Wizard interativo**: Keyboard navigation completa
- **Erros de validação**: Screen reader friendly (NVDA/JAWS/VoiceOver)
- **Exemplos inline**: Color contrast 4.5:1 mínimo

### Monitoring & Observability
- **Metrics**: Track tempo_preenchimento, taxa_erro, campos_p0_vazios, abandono_secao
- **Logging**: Structured logging com correlation ID por projeto
- **Alerting**: Alert se taxa_erro >10% ou tempo_preenchimento >20 min

---

## User Scenarios & Testing

### 🎯 US1 (P1 - MVP): Criar objetivo.yaml v2.0 para projeto simples

**Persona**: DevOps Iniciante
**Goal**: Criar primeiro objetivo.yaml sem erros em <15 min
**Preconditions**: Nenhum objetivo.yaml existente

**Steps**:
1. Criar novo arquivo `objetivo.yaml`
2. Copiar template v2.0 (de exemplo ou `scaffold.py objetivo-init`)
3. Preencher 3 campos P0 obrigatórios:
   - ## 1️⃣ O que este projeto faz?
   - ## 2️⃣ Qual problema resolve?
   - ## 3️⃣ Escopo do Projeto
4. Salvar arquivo
5. Validar com `scaffold.py objetivo-validate`

**Expected Output**:
```
✅ objetivo.yaml válido!
   - 3/3 campos P0 preenchidos
   - 0 erros de sintaxe
   - Formato: v2.0 (Markdown Híbrido)
   
📋 Próximos passos:
   - Adicione seções P1 (opcionais): Restrições, Regras de Negócio
   - Gere spec: scaffold.py objetivo-generate
```

**Acceptance Criteria**:
- ✅ Template tem exemplos inline em TODAS seções P0
- ✅ Validação mostra erros específicos por linha (não genérico)
- ✅ Tempo de preenchimento <15 min (medido)
- ✅ Taxa de erro <5% em campos P0

---

### 🎯 US2 (P1 - MVP): Converter objetivo.yaml v1.0 → v2.0

**Persona**: Programador Intermediário
**Goal**: Migrar projeto existente v1.0 para v2.0 sem perda de informação
**Preconditions**: Projeto com `objetivo.yaml` v1.0 (YAML puro)

**Steps**:
1. Rodar `scaffold.py objetivo-migrate`
2. Revisar `objetivo.yaml.v2` gerado
3. Comparar side-by-side v1.0 vs v2.0
4. Aprovar migração (sobrescreve `objetivo.yaml`)

**Expected Output**:
```
🔄 Migração objetivo.yaml v1.0 → v2.0

Arquivo analisado: objetivo.yaml (125 linhas)
✅ Campos extraídos: 18/18
✅ Mapeamento completo:
   - prompt.content.description → ## 1️⃣ + ## 2️⃣
   - specification.project_name → YAML frontmatter
   - rules → ## 5️⃣ Regras de Negócio
   - out-scope → ## 3️⃣ Escopo (Excluído ❌)

📄 Arquivo gerado: objetivo.yaml.v2 (342 linhas)

Revisar? [y/N]: y
Aceitar? [y/N]: y

✅ Migração completa! objetivo.yaml atualizado para v2.0
```

**Acceptance Criteria**:
- ✅ 100% dos campos v1.0 migrados (zero perda)
- ✅ Mapeia corretamente `prompt.content.description` → seções 1-3
- ✅ Preserva `rules` → seção 5️⃣
- ✅ Preserva `out-scope` → seção 3️⃣ Excluído ❌
- ✅ Gera preview side-by-side antes de sobrescrever

---

### 🎯 US3 (P1 - MVP): Gerar objetivo-spec.yaml a partir de objetivo.yaml v2.0

**Persona**: Tech Lead Avançado
**Goal**: Gerar arquivo máquina objetivo-spec.yaml para Copilot processar
**Preconditions**: `objetivo.yaml` v2.0 válido (P0 preenchido)

**Steps**:
1. Rodar `scaffold.py objetivo-generate`
2. Aguardar geração de `objetivo-spec.yaml`
3. Verificar arquivo gerado
4. Usar em workflows SpecKit (`speckit.constitution`, `speckit.clarify`, etc)

**Expected Output**:
```
🔨 Gerando objetivo-spec.yaml...

✅ objetivo.yaml lido (342 linhas)
✅ Validação P0: 3/3 campos OK
✅ Validação P1: 2/5 campos preenchidos (Restrições, Regras)
✅ Validação P2: 1/4 campos preenchidos (Estrutura de Pastas)

📄 Arquivo gerado: objetivo-spec.yaml (87 linhas)
   - profiles: [python_developer, backend_architect]
   - features: 3 features extraídas
   - personas: 2 personas identificadas
   - restrictions: 5 restrições técnicas

✅ Pronto para uso com:
   - speckit.constitution
   - speckit.clarify
   - speckit.specify
```

**Acceptance Criteria**:
- ✅ Gera YAML técnico válido (schema compliant)
- ✅ Extrai perfis automaticamente de seção 7️⃣ (Tecnologias)
- ✅ Identifica features de seção 3️⃣ (Escopo Incluído)
- ✅ Identifica personas de seção 2️⃣ (Problema)
- ✅ Mapeia restrições de seção 4️⃣ → contracts/non-functional
- ✅ Adiciona header `# ⚠️ Gerado automaticamente - NÃO editar!`

---

### 🎯 US4 (P2): Wizard interativo para criar objetivo.yaml v2.0

**Persona**: DevOps Iniciante
**Goal**: Criar objetivo.yaml respondendo perguntas (sem editar arquivo manualmente)
**Preconditions**: Nenhum objetivo.yaml existente

**Steps**:
1. Rodar `scaffold.py objetivo-init --interactive`
2. Responder 3 perguntas P0:
   - "O que este projeto faz? (1 frase)"
   - "Qual problema resolve? (1-2 parágrafos)"
   - "O que está NO escopo? (lista de itens)"
3. [Opcional] Responder perguntas P1:
   - "Há restrições técnicas? (performance, segurança, compliance)"
   - "Há regras de negócio complexas?"
4. Wizard gera `objetivo.yaml` com respostas + exemplos

**Expected Output**:
```
🧙 Wizard objetivo.yaml v2.0

Vou fazer 3 perguntas obrigatórias. Pressione Enter para pular opcionais.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 Seção 1/3: O que este projeto faz?

Em uma frase, descreva o que o projeto faz:
> API REST para gerenciar usuários e autenticação JWT

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 Seção 2/3: Qual problema resolve?

Em 1-2 parágrafos, explique o problema:
> Sistema legado tem autenticação basic auth insegura.
> Precisamos migrar para JWT mantendo sessões ativas.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 Seção 3/3: Escopo do Projeto

O que ESTÁ no escopo? (lista, Enter para próximo item, linha vazia para terminar)
> Autenticação JWT
> CRUD de usuários
> Migração de sessões ativas
> 

✅ 3/3 campos P0 preenchidos!

Adicionar seções opcionais? [y/N]: n

📄 Arquivo gerado: objetivo.yaml (298 linhas)

✅ Pronto! Próximos passos:
   - Revisar: cat objetivo.yaml
   - Validar: scaffold.py objetivo-validate
   - Gerar spec: scaffold.py objetivo-generate
```

**Acceptance Criteria**:
- ✅ Wizard faz exatamente 3 perguntas P0 (não mais)
- ✅ Permite pular seções P1/P2 (Enter vazio)
- ✅ Gera arquivo com exemplos inline mesmo para seções não preenchidas
- ✅ Mostra preview do arquivo antes de salvar
- ✅ Keyboard navigation completa (Tab, Enter, Ctrl+C para cancelar)

---

### 🎯 US5 (P2): Validar objetivo.yaml v2.0 com mensagens claras

**Persona**: Programador Intermediário
**Goal**: Corrigir erros de validação rapidamente
**Preconditions**: `objetivo.yaml` v2.0 com erros

**Steps**:
1. Editar `objetivo.yaml` (adicionar erro proposital: seção 1️⃣ vazia)
2. Rodar `scaffold.py objetivo-validate`
3. Ver mensagem de erro detalhada
4. Corrigir erro seguindo exemplo sugerido
5. Re-validar até passar

**Expected Output**:
```
❌ objetivo.yaml inválido!

Erro #1: Seção P0 obrigatória vazia
   Localização: linha 15-18
   Seção: ## 1️⃣ O que este projeto faz?
   
   ❌ Encontrado:
   15 | ## 1️⃣ O que este projeto faz?
   16 | 
   17 | **Em uma frase**: 
   18 |
   
   ✅ Esperado:
   **Em uma frase**: API REST para gerenciar usuários e autenticação JWT
   
   💡 Dica: Descreva em 1 frase clara o que o projeto faz.
       Exemplo: "Migra dados entre instâncias Chatwoot mantendo integridade referencial"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total: 1 erro encontrado
```

**Acceptance Criteria**:
- ✅ Mostra linha exata do erro (não apenas "seção 1 inválida")
- ✅ Mostra diff colorido (❌ Encontrado vs ✅ Esperado)
- ✅ Sugere exemplo de correção específico para aquela seção
- ✅ Valida sintaxe YAML frontmatter + Markdown body
- ✅ Detecta seções duplicadas
- ✅ Detecta seções fora de ordem (3️⃣ antes de 2️⃣)

---

## Out of Scope

❌ **Não incluído nesta feature**:
- Migração automática de projetos externos (fora do template)
- Suporte a objetivo.yaml v0.x (versões pré-1.0)
- Interface gráfica (GUI) para wizard
- Integração com VS Code extension (futuro)
- Tradução automática PT-BR ↔ EN (futuro)

---

## Technical Dependencies

**Required**:
- Python >=3.11 (stdlib only, zero external deps)
- PyYAML (já instalado no template)
- pytest (para testes)

**Optional**:
- Rich (para output colorido no wizard) — fallback para print() simples se não disponível

---

## Risks & Mitigations

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Usuários não migram v1.0 → v2.0 | Média | Alto | Wizard de migração automático (US2), alerta deprecation v1.0 após 3 meses |
| Parser tem bugs em edge cases | Média | Médio | Suite completa de testes (15+ cenários), validação em 4 projetos reais (Chatwoot + 3 novos) |
| Formato Markdown dificulta parsing | Baixa | Médio | Usar biblioteca markdown (mistune) para parse confiável, fallback para regex em seções simples |
| Iniciantes ainda acham difícil | Média | Alto | Wizard interativo (US4) como default, documentação com vídeo tutorial |

---

## Success Criteria Summary

✅ **Must Have** (P1 - MVP):
- US1: Criar objetivo.yaml v2.0 para projeto simples (<15 min, <5% erro)
- US2: Converter v1.0 → v2.0 (100% campos migrados)
- US3: Gerar objetivo-spec.yaml (schema compliant)

✅ **Should Have** (P2):
- US4: Wizard interativo (keyboard navigation completa)
- US5: Validação com mensagens claras (linha exata + exemplo)

✅ **Could Have** (P3 - Futuro):
- US6: VS Code extension para preview live
- US7: Template library com 10+ exemplos por domínio
- US8: Telemetria de uso (opt-in) para medir métricas reais

---

## Next Steps

1. ✅ **Fase 1 (2 dias)**: Validação — Converter 3 projetos reais para v2.0 (python-fastapi, k8s-helm, terraform-aws)
2. ⏳ **Fase 2 (1 semana)**: Parser — Implementar `scripts/lib/objetivo_parser.py` + testes
3. ⏳ **Fase 3 (3-4 dias)**: Wizard — Implementar `scaffold.py objetivo-init --interactive`

**Total timeline**: 10-12 dias úteis

Ver [plan.md](./plan.md) para detalhes técnicos e ADRs.
