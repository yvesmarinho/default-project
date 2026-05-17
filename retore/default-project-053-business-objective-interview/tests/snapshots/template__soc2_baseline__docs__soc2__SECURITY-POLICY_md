# Política de Segurança da Informação

> **[NOME DA EMPRESA]** — Versão: 1.0.0 | Data: [AAAA-MM-DD]
> Escopo: SOC 2 Type II — Critérios de Serviço de Confiança (TSC)
> Aprovado por: [Nome / Cargo] | Revisão anual obrigatória

---

## 1. Objetivo e Escopo

Esta política define os controles de segurança da informação para garantir conformidade com os **Trust Services Criteria (TSC)** do SOC 2, cobrindo:

- **CC** — Controles Comuns (Common Criteria)
- **A** — Availability (Disponibilidade)
- **PI** — Processing Integrity (Integridade de Processamento)
- **C** — Confidentiality (Confidencialidade)
- **P** — Privacy (Privacidade)

**Escopo do sistema**: [descrever o sistema/serviço auditado, ex: "API de gestão financeira hospedada na AWS"]

---

## 2. Controles de Acesso Lógico (CC6)

### 2.1. Princípio do Menor Privilégio (Least Privilege)
- Todos os acessos são concedidos com o **mínimo de privilégio necessário** para a função
- Revisão trimestral de permissões por gestor responsável
- Acessos de administrador são individuais (nunca compartilhados) e justificados por ticket

### 2.2. Autenticação Multifator (MFA)
| Sistema | MFA Obrigatório | Exceções |
|---------|----------------|---------|
| Console AWS / GCP / Azure | ✅ Sim | Nenhuma |
| GitHub / GitLab | ✅ Sim | Nenhuma |
| VPN corporativa | ✅ Sim | Nenhuma |
| Sistemas de produção (SSH) | ✅ Sim — chaves + Bastion | Nenhuma |
| Ferramentas internas (Jira, Slack) | ✅ Sim (SSO) | Break-glass documentado |

### 2.3. Gerenciamento de Credenciais
- Senhas armazenadas exclusivamente em gestor de senhas aprovado (ex: 1Password, Bitwarden Teams)
- Proibido: senha em código-fonte, planilhas, e-mails, chats
- Credenciais de serviço: rotação obrigatória a cada **90 dias** ou imediatamente após incidente
- Segredos em produção: exclusivamente via vault (AWS Secrets Manager, HashiCorp Vault, GCP Secret Manager)

### 2.4. Onboarding e Offboarding
```
Onboarding:  Ticket de acesso → aprovação gestor → provisionamento → MFA → treinamento segurança
Offboarding: Desligamento confirmado → revogação de TODOS os acessos em < 24h → audit log
```

---

## 3. Gerenciamento de Mudanças (CC8)

### 3.1. Processo de Deploy
Todas as mudanças em ambiente de produção devem seguir:

1. **Código**: Pull Request com peer review (mínimo 1 aprovador)
2. **Testes**: CI/CD com cobertura mínima de [X]% + testes de segurança
3. **Staging**: Deploy em staging obrigatório antes de produção
4. **Aprovação**: Lead técnico + Product Owner para mudanças de alto impacto
5. **Rollback**: Plano de rollback documentado antes de qualquer deploy

### 3.2. Ambientes
| Ambiente | Acesso | Dados Reais Permitidos |
|----------|--------|------------------------|
| Desenvolvimento | Dev team (MFA) | ❌ Nunca — usar fixtures |
| Staging | Dev + QA (MFA) | ❌ Nunca — usar dados mascarados |
| Produção | Ops + SRE (MFA + aprovação) | ✅ Somente quando necessário |

### 3.3. Infraestrutura como Código (IaC)
- Toda infraestrutura deve ser declarada em código (Terraform, Pulumi, CDK)
- Proibido provisionar recursos manualmente em produção sem documentação / ticket
- Drift detection automatizado (ex: `terraform plan` no CI)

---

## 4. Monitoramento e Logging (CC7)

### 4.1. Logs Obrigatórios

| Evento | Retenção Mínima | Alertas |
|--------|----------------|---------|
| Autenticações (sucesso e falha) | 12 meses | Falhas em sequência (> 5 em 1h) |
| Acessos a dados sensíveis | 12 meses | Acesso fora do horário comercial |
| Deploys em produção | 24 meses | Qualquer deploy não planejado |
| Erros de aplicação (5xx) | 3 meses | Taxa > 1% por 5 minutos |
| Mudanças em IAM/RBAC | 24 meses | Qualquer elevação de privilégio |
| Acesso ao banco de dados | 6 meses | Queries em volume anormal |

### 4.2. Imutabilidade de Logs
- Logs de auditoria são armazenados em destino separado, com acesso de escrita restrito
- Exemplos: CloudTrail → S3 com Object Lock, Datadog com retenção mínima contratada
- Hash SHA-256 de log batches para verificação de integridade

### 4.3. Alertas e SLAs de Resposta
| Severidade | Exemplo | SLA de Resposta |
|-----------|---------|----------------|
| P1 — Crítico | Credencial vazada, brecha ativa | 30 minutos |
| P2 — Alto | > 10 falhas auth/min, acesso incomum | 2 horas |
| P3 — Médio | Dep. vulnerável HIGH, quota próxima | 8 horas |
| P4 — Baixo | Dep. vulnerável MEDIUM, alerta não urgente | 48 horas |

---

## 5. Gestão de Vulnerabilidades (CC7.1)

### 5.1. Ferramentas Obrigatórias no CI/CD
| Ferramenta | Finalidade | Threshold de Falha |
|-----------|-----------|-------------------|
| Gitleaks / TruffleHog | Secret scanning | Qualquer segredo confirmado |
| Bandit (Python) / ESLint (JS) | SAST | Severidade HIGH |
| pip-audit / npm audit / trivy | SCA (dependências) | CVE CVSS ≥ 9.0 (CRITICAL) |
| Trivy / Grype | Container scanning | CRITICAL em produção |
| OWASP ZAP (staging) | DAST | HIGH em endpoints abertos |

### 5.2. Ciclo de Remediação
| Severidade CVE | Prazo de Remediação |
|---------------|---------------------|
| CRITICAL (CVSS ≥ 9.0) | 7 dias |
| HIGH (CVSS 7.0–8.9) | 30 dias |
| MEDIUM (CVSS 4.0–6.9) | 90 dias |
| LOW (CVSS < 4.0) | Próximo ciclo de manutenção |

---

## 6. Disponibilidade e Continuidade (A1)

### 6.1. RTO / RPO Definidos
| Serviço | RTO (Recovery Time Objective) | RPO (Recovery Point Objective) |
|---------|-------------------------------|--------------------------------|
| [Serviço crítico A] | [Xh] | [Yh] |
| [Serviço crítico B] | [Xh] | [Yh] |
| [Dados críticos] | [Xh] | [Yh] |

### 6.2. Backup e Restore
- Backups automatizados: frequência [diária/horária] com retenção de [X dias]
- Restore testado trimestralmente (não apenas assumido — evidência obrigatória)
- Backups armazenados em região distinta (geo-redundância)
- Backup de segredos/keyvault: procedimento separado documentado

---

## 7. Confidencialidade (C1)

- Dados classificados como **Confidencial** são criptografados em repouso (AES-256) e em trânsito (TLS 1.3)
- Acesso a dados confidenciais requer justificativa e é logado
- Compartilhamento externo apenas com NDA vigente e aprovação do responsável

**Classificação de dados**:
| Nível | Exemplos | Controles |
|-------|---------|----------|
| Público | Docs públicos, landing page | Nenhum especial |
| Interno | Runbooks, roadmap | Acesso limitado à equipe |
| Confidencial | Dados de clientes, segredos de negócio | Criptografia + MFA + log |
| Restrito | Chaves criptográficas, dados sensíveis LGPD | Vault + acesso mínimo + dupla aprovação |

---

## 8. Pentest e Avaliação de Risco

- Pentest externo anual por empresa certificada (CREST/OSCP)
- Resultados classificados e remediados conforme SLA da Seção 5.2
- Relatório de pentest disponível para auditor SOC 2 sob NDA
- Bug bounty: [ativo em / não aplicável]

---

## 9. Responsabilidades

| Papel | Responsabilidade |
|-------|-----------------|
| CISO / Tech Lead | Ownership desta política; aprovar exceções |
| DPO | Intersecção com LGPD/GDPR |
| Engenharia | Implementar e manter controles técnicos |
| RH | Onboarding/offboarding de acessos |
| Todos os colaboradores | Cumprir esta política e reportar incidentes |

---

## 10. Exceções e Revisões

- Exceções devem ser aprovadas pelo CISO com risco documentado e prazo de expiração
- Esta política é revisada **anualmente** ou após qualquer incidente P1/P2
- Versão aprovada arquivada para evidência de auditoria SOC 2

| Revisão | Data | Responsável | Motivo |
|---------|------|-------------|--------|
| 1.0.0 | [AAAA-MM-DD] | [Nome] | Criação inicial |
