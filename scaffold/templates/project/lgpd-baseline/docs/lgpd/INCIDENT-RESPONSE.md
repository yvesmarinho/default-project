# Plano de Resposta a Incidentes de Dados Pessoais (LGPD — Art. 48)

> **Versão**: 1.0.0 | **Responsável**: [DPO / CISO]
> Conforme Art. 48 da Lei nº 13.709/2018, incidentes relevantes devem ser
> comunicados à ANPD e aos titulares em **prazo razoável** (Resolução CD/ANPD nº 2/2022: até 3 dias úteis para notificação preliminar).

---

## 1. Critérios de Acionamento

Um incidente de dados pessoais é acionado quando há:

| Evento | Acionamento |
|--------|-------------|
| Acesso não autorizado a dados pessoais | **Imediato** |
| Vazamento de dados (dump de banco, arquivo exposto) | **Imediato** |
| Perda/destruição acidental de dados | **Imediato** |
| Alteração não autorizada de dados pessoais | **Imediato** |
| Indisponibilidade prolongada de dados (> 24h) | **Imediato** |
| Ransomware ou malware com acesso a dados pessoais | **Imediato** |

---

## 2. Fases do Plano

### FASE 1 — Detecção e Triagem (0–2 horas)

**Responsável**: Engenharia / SOC (quem detectou)

- [ ] Registrar data/hora exata da detecção
- [ ] Isolar sistemas afetados (sem desligar logs)
- [ ] Preservar evidências: logs, snapshots, hashes de arquivos
- [ ] Notificar imediatamente: DPO + CISO + Gestor direto
- [ ] Abrir ticket de incidente: `[LGPD-INC-AAAA-NNN]`
- [ ] Classificar severidade (ver Seção 4)

### FASE 2 — Contenção (2–8 horas)

**Responsável**: Time de Segurança + Engenharia

- [ ] Revogar acessos comprometidos
- [ ] Bloquear vetores de entrada identificados
- [ ] Snapshot do ambiente antes de qualquer remediação
- [ ] Identificar categorias e volume de dados afetados
- [ ] Identificar titulares afetados (total estimado)
- [ ] Avaliar risco de dano (Art. 48, § 2º): discriminação, dano financeiro, dano à reputação

### FASE 3 — Avaliação e Notificação (8–72 horas)

**Responsável**: DPO + Jurídico

- [ ] Documentar escopo completo do incidente
- [ ] Avaliar obrigatoriedade de notificação à ANPD (Art. 48):
  - Incidente com **risco ou dano relevante** → notificação obrigatória
  - Prazo: **3 dias úteis** (notificação preliminar) via portal ANPD
- [ ] Avaliar obrigatoriedade de comunicação aos titulares (Art. 48, § 1º)
- [ ] Redigir comunicação para ANPD usando template `ANPD-NOTIFICATION.md`
- [ ] Se necessário: comunicar titulares em linguagem acessível

### FASE 4 — Remediação (72 horas – 30 dias)

**Responsável**: Engenharia + Segurança

- [ ] Corrigir vulnerabilidade de origem
- [ ] Implementar controles preventivos adicionais
- [ ] Verificar outros sistemas com exposição similar
- [ ] Atualizar mapeamento de dados (`DATA-MAPPING.md`)
- [ ] Conduzir postmortem sem punição

### FASE 5 — Lições Aprendidas (30–45 dias)

**Responsável**: DPO + Engenharia + Gestão

- [ ] Documentar lições aprendidas
- [ ] Atualizar este plano se necessário
- [ ] Reportar ao conselho/diretoria
- [ ] Atualizar treinamentos da equipe
- [ ] Encerrar formalmente o ticket: `[LGPD-INC-AAAA-NNN]`

---

## 3. Canais de Comunicação por Severidade

| Severidade | Canal | Tempo Máximo de Resposta |
|-----------|-------|--------------------------|
| CRÍTICO (P1) | Telefone + Slack #security-incident | 30 minutos |
| ALTO (P2) | Slack #security-incident + E-mail | 2 horas |
| MÉDIO (P3) | E-mail + ticket | 8 horas |
| BAIXO (P4) | Ticket | 48 horas |

---

## 4. Critérios de Severidade

| Severidade | Critério |
|-----------|---------|
| **CRÍTICO** | > 10.000 titulares afetados, ou dados sensíveis (Art. 5º, II), ou vazamento público |
| **ALTO** | 1.000–10.000 titulares, ou dados financeiros, ou acesso interno malicioso |
| **MÉDIO** | 100–1.000 titulares, ou dados de identificação sem dados sensíveis |
| **BAIXO** | < 100 titulares, sem dados sensíveis, sem risco de dano imediato |

---

## 5. Contatos de Emergência

| Papel | Nome | Contato |
|-------|------|---------|
| DPO | [Nome] | [email] / [telefone] |
| CISO / Responsável de Segurança | [Nome] | [email] / [telefone] |
| Jurídico | [Nome/Escritório] | [email] / [telefone] |
| CEO / Responsável pelo Tratamento | [Nome] | [email] / [telefone] |
| ANPD (notificação) | — | [portal.anpd.gov.br](https://www.gov.br/anpd) |

---

## 6. Template de Notificação à ANPD (Art. 48)

```
NOTIFICAÇÃO DE INCIDENTE — ANPD

Controlador: [NOME DA EMPRESA] — CNPJ [XX.XXX.XXX/XXXX-XX]
DPO: [Nome] — [email]
Data/hora do incidente: [AAAA-MM-DD HH:MM]
Data/hora da detecção: [AAAA-MM-DD HH:MM]
Data desta notificação: [AAAA-MM-DD]

NATUREZA DO INCIDENTE:
[Acesso não autorizado / Vazamento / Perda / Alteração / Indisponibilidade]

DADOS AFETADOS:
- Categorias: [nome, e-mail, CPF, dados sensíveis...]
- Volume estimado de titulares: [número]
- Período de exposição: [início] até [fim/containment]

CAUSE RAIZ (preliminar):
[Descrição técnica resumida]

MEDIDAS TOMADAS:
[Contenção, revogação de acessos, patches aplicados...]

RISCO DE DANO AOS TITULARES:
[Discriminação / Dano financeiro / Dano à reputação / Violação de privacidade / Descrição]

MEDIDAS DE MITIGAÇÃO PARA OS TITULARES:
[Monitoramento de crédito / Reset de senhas / Comunicação direta / Outras]

PRÓXIMOS PASSOS:
[Investigação forense em andamento / Patch liberado / ...]
```

---

## 7. Histórico de Incidentes

| ID | Data | Severidade | Titulares Afetados | ANPD Notificada | Status |
|----|------|-----------|-------------------|-----------------|--------|
| LGPD-INC-[ANO]-001 | [Data] | [P1-P4] | [Nº] | [Sim/Não/N/A] | Encerrado |
