# RUNBOOK.md

## 1. Fluxo de Execução Operacional

### Etapa 1 — Entendimento
- Ler `CONTEXT.md`
- Identificar invariantes e contratos sensíveis
- Rodar skill `grill-with-docs`

### Etapa 2 — Especificação
- Rodar `to-prd`
- Validar:
  - objetivo / não-objetivo
  - aceite
  - riscos
  - dependências

### Etapa 3 — Planejamento de Execução
- Rodar `to-issues`
- Criar slices verticais pequenas e independentes

### Etapa 4 — Implementação
- Rodar `tdd`
- Ciclo curto: red → green → refactor
- Commits pequenos e reversíveis

### Etapa 5 — Diagnóstico (se necessário)
- Rodar `diagnose`
- Reproduzir, minimizar, instrumentar, corrigir, validar

### Etapa 6 — Encerramento
- Atualizar docs mínimas
- Rodar `handoff` com resumo completo

## 2. Incidentes de Qualidade
Se falhar build/test:
1. Pausar feature nova
2. Priorizar estabilização
3. Gerar relatório de causa raiz
4. Registrar prevenção em ADR/RUNBOOK

## 3. Checklist de Release
- [ ] Testes relevantes OK
- [ ] Sem mudanças breaking não documentadas
- [ ] Observabilidade mínima validada
- [ ] Handoff concluído
