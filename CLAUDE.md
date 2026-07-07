# CLAUDE.md

## 1. Missão
Este repositório utiliza agentes e skills para desenvolvimento orientado a qualidade, previsibilidade e rastreabilidade.
Toda mudança deve priorizar: **clareza de domínio**, **segurança de alteração**, **testabilidade** e **handoff eficiente**.

## 2. Regras Globais
1. Nunca implementar sem entendimento de contexto:
   - Ler `CONTEXT.md`
   - Ler ADRs relevantes em `docs/adr/`
2. Toda demanda deve ter escopo explícito:
   - objetivo
   - não-objetivo
   - critérios de aceite
   - riscos
3. Alterações devem ser incrementais (fatias verticais pequenas).
4. Toda decisão arquitetural relevante deve atualizar ADR.
5. Ao concluir trabalho, sempre produzir handoff estruturado.

## 3. Fluxo Padrão (obrigatório)
1. `grill-with-docs`
2. `to-prd`
3. `to-issues`
4. `tdd`
5. `diagnose` (quando necessário)
6. revisão arquitetural (`zoom-out` mental + ADR)
7. `handoff`

## 4. Critérios de Qualidade
- Compila/builda sem erro
- Testes de unidade e integração relevantes passando
- Regressão básica validada
- Logs e mensagens de erro acionáveis
- Documentação mínima atualizada (`CONTEXT.md`/ADR/RUNBOOK)

## 5. Política de Mudança
- Preferir baixo acoplamento e alta coesão
- Evitar abstração prematura
- Evitar “big bang refactor”
- Proteger contratos públicos (APIs/eventos/esquemas)
- Mudanças breaking exigem plano de migração

## 6. Convenções de Entrega
Toda entrega deve incluir:
1. Resumo do problema
2. Estratégia adotada
3. Arquivos alterados
4. Riscos remanescentes
5. Próximos passos recomendados
