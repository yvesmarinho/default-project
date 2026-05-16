# IMP-58 — Interview Template: Memory Needs Assessment

**Criado**: 2026-04-05
**Parte de**: IMP-58 — Avaliar necessidade de memória ativa (Fase 2 Engram Integration)
**Duração**: 30-45 minutos por entrevista
**Meta**: 3-5 desenvolvedores entrevistados

---

## 📋 Informações do Entrevistado

- **Nome**: [nome do desenvolvedor]
- **Data da entrevista**: [YYYY-MM-DD]
- **Tempo no projeto**: [N semanas/meses]
- **Função**: [desenvolvedor, arquiteto, tech lead, etc.]
- **Familiaridade com session-search**: [ ] iniciante | [ ] intermediário | [ ] avançado

---

## 🎯 Objetivos da Entrevista

1. Entender **fluxo de trabalho atual** de busca/recuperação de informações
2. Identificar **pain points** com sistema de memória passiva (session-search)
3. Avaliar **interesse real** em memória ativa (Engram/mini-Engram)
4. Coletar **user stories** concretas de uso

---

## ❓ Roteiro de Perguntas

### Seção 1: Uso Atual do Sistema de Busca (10 min)

**1.1 Como você costuma buscar informações sobre decisões/implementações passadas?**

Resposta:
```
[Anotar métodos: session-search, grep, GitHub search, perguntar ao colega, etc.]
```

**Observação do entrevistador**:
```
[Notar se session-search é primeira opção ou fallback]
```

---

**1.2 Pode me contar sobre a última vez que usou `session-search`?**

Resposta:
```
[O que estava procurando? Encontrou? Quanto tempo levou?]
```

**Observação do entrevistador**:
```
[Notar frustração, satisfação, ou indiferença no relato]
```

---

**1.3 Em uma semana típica, quantas vezes você usa session-search?**

- [ ] Nunca
- [ ] 1-2x por semana
- [ ] 3-5x por semana
- [ ] 1-2x por dia
- [ ] 3-5x por dia
- [ ] 5+ vezes por dia

**Nota**: [Se baixa frequência, perguntar POR QUE não usa mais]

---

### Seção 2: Pain Points e Contexto Perdido (15 min)

**2.1 Você já teve situação onde NÃO conseguiu encontrar informação que sabia que existia?**

Resposta:
```
[Exemplos concretos. Se sim, explorar em detalhes.]
```

**Follow-up**: Como você resolveu? Quanto tempo perdeu?

Resposta:
```
[Estratégias alternativas: ler todo DAILY_ACTIVITIES manualmente, perguntar ao time, etc.]
```

---

**2.2 Quais tipos de informação são MAIS DIFÍCEIS de encontrar com session-search?**

Marque todas que se aplicam:
- [ ] Decisões arquiteturais ("por que escolhemos X ao invés de Y?")
- [ ] Contexto de bugs corrigidos ("como foi resolvido bug similar?")
- [ ] Guidelines/padrões do projeto ("qual é o padrão para nomear X?")
- [ ] Dependências entre features ("essa mudança afeta qual outra parte?")
- [ ] Histórico de refactoring ("por que mudamos de abordagem?")
- [ ] Outro: [especificar]

**Exemplo concreto mais recente**:
```
[Pedir para o entrevistado detalhar 1 caso específico]
```

---

**2.3 Quando você está fazendo onboarding em nova funcionalidade, qual o processo?**

Resposta:
```
[Passos: ler código, buscar sessions, perguntar ao time, etc.]
Tempo médio: [X minutos/horas]
```

**Observação do entrevistador**:
```
[Notar se processo parece ineficiente ou otimizado]
```

---

### Seção 3: Cenários de Memória Ativa (15 min)

**3.1 [CENÁRIO 1: Sugestão Automática]**

> Imagine que, durante uma conversa com GitHub Copilot, ele **automaticamente** lembrasse:
>
> _"Você perguntou sobre validação. Em 2026-03-23 (IMP-47), implementamos validador semver
> que lida com pre-releases usando regex XYZ. Quer usar o mesmo padrão?"_

**Pergunta**: Isso seria útil para você? Com que frequência?

- [ ] Não útil — prefiro buscar manualmente quando preciso
- [ ] Ocasionalmente útil — em casos específicos
- [ ] Muito útil — economizaria tempo regularmente
- [ ] Extremamente útil — mudaria meu fluxo de trabalho

**Comentário**:
```
[Por que? Em quais situações específicas ajudaria?]
```

---

**3.2 [CENÁRIO 2: Contexto Proativo]**

> Imagine que, ao abrir um arquivo Python, Copilot mostrasse automaticamente:
>
> _"Decisões relevantes sobre este arquivo:_
> - _2026-04-01: Refatorado para usar dataclasses (IMP-45)_
> - _2026-03-15: Pattern de error handling definido (IMP-38)_
> - _2026-02-20: Adicionado type hints obrigatório (IMP-12)"_

**Pergunta**: Você usaria esse tipo de contexto?

- [ ] Não — seria ruído/distração
- [ ] Raramente — só em arquivos críticos
- [ ] Frequentemente — na maioria dos arquivos
- [ ] Sempre — quero contexto automático

**Comentário**:
```
[Como isso mudaria (ou não) sua forma de trabalhar?]
```

---

**3.3 [CENÁRIO 3: Perguntas Naturais]**

> Ao invés de buscar manualmente, você poderia perguntar ao Copilot:
>
> _"Por que decidimos usar FastAPI ao invés de Flask?"_
>
> E ele responderia com base em decisões documentadas nas sessões.

**Pergunta**: Isso substituiria sua necessidade de session-search?

- [ ] Não — ainda preferiria busc ar manualmente
- [ ] Parcialmente — usaria ambos
- [ ] Sim — usaria só perguntas naturais
- [ ] Depende — explicar:

Comentário:
```
[Quais vantagens/desvantagens você vê?]
```

---

### Seção 4: Trade-offs e Preocupações (5 min)

**4.1 Memória ativa pode ter overhead (performance, complexidade, custo). Qual limite você aceitaria?**

Performance:
- [ ] Até +0.5s de latência em respostas do Copilot
- [ ] Até +2s de latência
- [ ] Até +5s de latência
- [ ] Não aceito latência adicional

Complexidade:
- [ ] OK se for transparente (zero configuração)
- [ ] OK se tiver configuração simples (5 min setup)
- [ ] OK se exigir aprendizado (30 min tutorial)
- [ ] Não aceito complexidade adicional

**Comentário**:
```
[O que seria deal-breaker para você?]
```

---

**4.2 Preocupações com segurança/privacidade de dados?**

- [ ] Sem preocupações — projeto open source
- [ ] Pequenas preocupações — desde que dados fiquem locais
- [ ] Grandes preocupações — não quero histórico persistente
- [ ] Blocker — não confiaria em sistema de memória

**Comentário**:
```
[O que te deixaria confortável? Ex: auditoria, controle de retenção, etc.]
```

---

### Seção 5: Priorização e Decisão (5 min)

**5.1 Se você tivesse budget para 1 única melhoria no sistema de documentação/memória, qual seria?**

- [ ] Melhorar session-search existente (scope, performance, etc.) → IMP-57 done
- [ ] Implementar memória ativa (sugestões, contexto proativo) → IMP-59
- [ ] Melhorar documentação/templates das sessões → IMP-48/49/50 done
- [ ] Outro: [especificar]

**Justificativa**:
```
[Por que essa é sua prioridade #1?]
```

---

**5.2 Na sua opinião, qual a MAIOR lacuna no sistema atual?**

Resposta:
```
[Pain point mais crítico que precisa resolver]
```

---

## 📊 Análise Pós-Entrevista (Preenchida pelo Entrevistador)

### Scoring

| Dimensão | Score (1-5) | Evidência |
|----------|-------------|-----------|
| **Frequência de uso atual** | [1-5] | [citar resposta 1.3] |
| **Frustração com sistema atual** | [1-5] | [citar pain points seção 2] |
| **Interesse em memória ativa** | [1-5] | [citar cenários seção 3] |
| **Willingness to pay overhead** | [1-5] | [citar trade-offs seção 4] |
| **Prioridade relativa** | [1-5] | [citar 5.1] |

**Score Total**: [soma] / 25

**Classificação**:
- ≥20/25: **Alta necessidade** de memória ativa
- 15-19/25: **Necessidade moderada**
- <15/25: **Baixa necessidade** (IMP-51 v2.0 suficiente)

### Principais Insights

```
[3-5 insights-chave desta entrevista]

1. [Insight 1]
2. [Insight 2]
3. [Insight 3]
```

### Quotes Marcantes

```
[Citações diretas que ilustram necessidade ou falta dela]

"[Quote 1]"

"[Quote 2]"
```

### Recomendação Individual

- [ ] **GO**: Este usuário se beneficiaria significativamente de memória ativa
- [ ] **NEUTRAL**: Indiferente, aceitaria mas não é crítico
- [ ] **NO-GO**: Sistema atual é suficiente para este usuário

**Justificativa**:
```
[Explicar recomendação baseada em evidências]
```

---

## 🔗 Próximos Passos

1. Salvar este arquivo como: `docs/IMP-58_INTERVIEW_[nome].md`
2. Adicionar ao git após preencher
3. Após 3-5 entrevistas, consolidar em `IMP-58_MEMORY_ASSESSMENT_REPORT.md`
4. Aplicar decision gate criteria

---

**Status**: 🟡 Template pronto para uso
**Última atualização**: 2026-04-05
