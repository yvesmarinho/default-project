# GOVERNANCE.md

## 1. Objetivo
Definir governança operacional de agentes/skills para manter qualidade, segurança e previsibilidade.

## 2. Princípios
- Prompt/skill é ativo de engenharia (versionado, revisado, auditável).
- Cada skill deve ter:
  - entrada clara
  - saída clara
  - critérios de pronto
- Nenhum agente “faz tudo”.

## 3. Papéis de Agentes
- Planner Agent: clareza de problema e escopo
- Architecture Agent: consistência estrutural
- Implementation Agent: execução incremental + testes
- Debug/Perf Agent: diagnóstico e performance
- Quality/Review Agent: revisão técnica e riscos
- Handoff Agent: transferência de contexto

## 4. Política de Versionamento de Skills
- Toda skill deve conter:
  - versão
  - changelog resumido
  - exemplos de uso
- Mudanças grandes exigem revisão por pelo menos 1 mantenedor técnico.

## 5. Critérios de Pronto por Issue
- Critérios de aceite atendidos
- Testes relevantes passando
- Sem regressão óbvia
- Documentação mínima atualizada
- Handoff final produzido

## 6. KPIs Operacionais
- Lead time por issue
- Taxa de retrabalho em PR
- Defeitos pós-merge
- % de issues com aceite explícito
- % de entregas com handoff completo

## 7. Cadência de Revisão
- Semanal: revisar métricas e gargalos
- Quinzenal: revisar skills
- Mensal: revisar arquitetura/ADRs
