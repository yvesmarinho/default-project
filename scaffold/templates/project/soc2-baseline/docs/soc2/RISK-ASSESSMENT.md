# Avaliação de Riscos (SOC 2 — CC3)

> **[NOME DA EMPRESA]** — Versão: 1.0.0 | Data: [AAAA-MM-DD]
> Responsável: [CISO / Tech Lead] | Revisão: semestral obrigatória
> Critério SOC 2: CC3 — Risk Assessment

---

## 1. Metodologia

Utilizamos a metodologia qualitativa **NIST SP 800-30 + ISO 31000**:

```
Risco = Probabilidade × Impacto

Probabilidade: 1 (Improvável) → 5 (Quase certo)
Impacto:       1 (Insignificante) → 5 (Catastrófico)
Nível de Risco: 1-4 (Baixo), 5-9 (Médio), 10-15 (Alto), 16-25 (Crítico)
```

---

## 2. Registro de Riscos

### 2.1. Riscos de Segurança da Informação

| ID | Ameaça | Ativo em Risco | Prob. | Impacto | Risco | Controle Existente | Gap | Ação |
|----|--------|---------------|-------|---------|-------|-------------------|-----|------|
| R001 | Credencial comprometida | Produção / dados de clientes | 3 | 5 | **15 — Alto** | MFA, rotação 90d, vault | Alertas de anomalia | Implementar SIEM alerta |
| R002 | Dependência com CVE crítico | Aplicação | 4 | 4 | **16 — Crítico** | pip-audit no CI | SLA remediação não formal | Formalizar SLA 7d |
| R003 | Exfiltração por insider | Dados confidenciais | 2 | 5 | **10 — Alto** | RBAC + logs | DLP não implementado | Avaliar DLP |
| R004 | Indisponibilidade de região cloud | Serviço | 2 | 4 | **8 — Médio** | Multi-AZ | Sem multi-region | Avaliar custo/benefício |
| R005 | SQL Injection / XSS | Aplicação | 3 | 4 | **12 — Alto** | ORM + validação Pydantic | DAST não automatizado | Adicionar ZAP ao CI |
| R006 | Acesso não autorizado a backup | Dados de backup | 2 | 5 | **10 — Alto** | Criptografia backup | Acesso não monitorado | Adicionar alertas S3 |
| R007 | Configuração incorreta de IAM | Infra | 3 | 4 | **12 — Alto** | IaC revisado | Drift não detectado | Implementar drift detection |
| R008 | Phishing → comprometimento de conta | Colaborador | 4 | 3 | **12 — Alto** | MFA + treinamento | Sem simulação de phishing | Executar phishing sim. anual |
| [R009] | [Ameaça específica do negócio] | [Ativo] | [1-5] | [1-5] | [—] | [Controles] | [Gap] | [Ação] |

### 2.2. Riscos de Disponibilidade

| ID | Ameaça | Serviço | Prob. | Impacto | Risco | RTO Atual | RPO Atual | Ação |
|----|--------|---------|-------|---------|-------|-----------|-----------|------|
| A001 | Falha de AZ principal | API / DB | 2 | 4 | **8 — Médio** | [X]h | [Y]h | Testar failover trimestralmente |
| A002 | DB corruption | Banco principal | 1 | 5 | **5 — Médio** | [X]h | [Y]h | Restore test mensal |
| A003 | DDoS | API Gateway | 3 | 3 | **9 — Médio** | [X]min | N/A | WAF + rate limiting |
| A004 | Pipeline CI/CD quebrado | Deploys | 3 | 2 | **6 — Médio** | [X]h | N/A | Runbook de rollback manual |

---

## 3. Plano de Tratamento de Riscos

| ID Risco | Estratégia | Responsável | Prazo | Status |
|----------|-----------|-------------|-------|--------|
| R001 | Mitigar — implementar alerta SIEM | [Nome] | [Data] | ⏳ Planejado |
| R002 | Mitigar — formalizar SLA 7d em SECURITY-POLICY.md | [Nome] | [Data] | ⏳ Planejado |
| R003 | Aceitar — avaliar DLP Q[X]/[Ano] | [Nome] | [Data] | ✅ Aceito |
| R004 | Aceitar — custo de multi-region não justificado atualmente | [Nome] | [Data] | ✅ Aceito |
| R005 | Mitigar — adicionar OWASP ZAP ao CI de staging | [Nome] | [Data] | ⏳ Em andamento |
| R006 | Mitigar — habilitar S3 access logging + CloudTrail | [Nome] | [Data] | ⏳ Planejado |
| R007 | Mitigar — implementar `terraform plan` drift check semanal | [Nome] | [Data] | ✅ Concluído |
| R008 | Mitigar — executar simulação de phishing anual | [Nome] | [Data] | ⏳ Q[X]/[Ano] |

---

## 4. Apetite a Risco

| Nível | Decisão |
|-------|---------|
| **Crítico (16–25)** | Tratamento obrigatório em < 30 dias |
| **Alto (10–15)** | Tratamento obrigatório em < 90 dias ou aceite formal com revisão semestral |
| **Médio (5–9)** | Tratar no próximo ciclo de planejamento ou aceitar com justificativa |
| **Baixo (1–4)** | Monitorar; tratar conforme disponibilidade |

---

## 5. Responsabilidades na Gestão de Riscos

| Papel | Responsabilidade |
|-------|-----------------|
| CISO / Tech Lead | Ownership do registro de riscos; aprovar aceitações |
| Engenharia | Implementar controles técnicos |
| Gestão / CEO | Aceitar riscos residuais acima do apetite |
| Auditor Externo | Revisar registro anualmente (para SOC 2 Type II) |

---

## 6. Histórico de Revisões

| Data | Versão | Responsável | Alteração |
|------|--------|-------------|-----------|
| [AAAA-MM-DD] | 1.0.0 | [Nome] | Criação do registro |
| [AAAA-MM-DD] | 1.1.0 | [Nome] | Adicionado R009 — [descrição] |
