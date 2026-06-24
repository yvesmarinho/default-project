# Mapeamento de Dados Pessoais (LGPD — Art. 37)

> Documento obrigatório conforme Art. 37 da Lei nº 13.709/2018 (LGPD).
> Mantenha atualizado a cada alteração de tratamento de dados.
> **Versão**: 1.0.0 | **Responsável**: [DPO / Responsável pelo Tratamento]

---

## 1. Informações do Controlador

| Campo | Valor |
|-------|-------|
| **Razão Social** | [NOME DA EMPRESA] |
| **CNPJ** | [XX.XXX.XXX/XXXX-XX] |
| **DPO (Encarregado)** | [Nome] — [email@empresa.com] |
| **Data da última revisão** | [AAAA-MM-DD] |

---

## 2. Inventário de Dados Pessoais

### 2.1. Tabela de Mapeamento

| ID | Categoria | Dado Pessoal | Finalidade (Art. 7º) | Base Legal | Retenção | Compartilhado com | Transferência Internacional |
|----|-----------|--------------|----------------------|------------|----------|-------------------|-----------------------------|
| D001 | Identificação | Nome completo | Cadastro de usuário | Consentimento (Art. 7º, I) | 5 anos | — | Não |
| D002 | Identificação | E-mail | Comunicação operacional | Execução de contrato (Art. 7º, V) | 5 anos | Provedor de e-mail | Sim — [país/mecanismo] |
| D003 | Identificação | CPF | Faturamento / KYC | Obrigação legal (Art. 7º, II) | 10 anos | Receita Federal (obrigação) | Não |
| D004 | Financeiro | Dados de cartão | Processamento de pagamento | Execução de contrato (Art. 7º, V) | Não armazenado (tokenizado) | Gateway de pagamento | Sim — PCI DSS |
| D005 | Comportamental | Logs de acesso | Segurança e auditoria | Legítimo interesse (Art. 7º, IX) | 1 ano | — | Não |
| D006 | Sensível | [Dado sensível] | [Finalidade específica] | Consentimento específico (Art. 11, I) | [Período] | [Destinatário] | [Sim/Não] |

> **Dados sensíveis** (Art. 5º, II): origem racial, convicção religiosa, opinião política, saúde, vida sexual, dados genéticos/biométricos, filiação sindical. Requerem base legal do Art. 11.

---

## 3. Bases Legais Utilizadas (Art. 7º)

| Código | Base Legal | Descrição | Casos de Uso no Sistema |
|--------|------------|-----------|------------------------|
| BL-01 | Art. 7º, I — Consentimento | Titular autorizou expressamente | Newsletters, marketing, cookies não essenciais |
| BL-02 | Art. 7º, II — Obrigação legal | Lei exige o tratamento | Emissão de NF, recolhimento de tributos |
| BL-03 | Art. 7º, V — Execução de contrato | Necessário para cumprir contrato | Login, perfil, pagamento, entrega |
| BL-04 | Art. 7º, IX — Legítimo interesse | Interesse legítimo prevalece | Logs de segurança, prevenção a fraude |
| BL-05 | Art. 11, I — Consentimento específico | Dados sensíveis com consentimento | [Caso de uso específico] |

---

## 4. Ciclo de Vida dos Dados

```
Coleta → Uso → Armazenamento → Compartilhamento → Eliminação
  ↓          ↓         ↓                ↓                ↓
Consentimento  Finalidade   Criptografia    Contrato DPA    Prazo vencido
/ Base Legal   delimitada   + controle      com terceiros   ou revogação
               (Art. 6º)    de acesso                       de consentimento
```

---

## 5. Operadores e Terceiros (Art. 7º, § 1º)

| Fornecedor | Categoria | País | Dados Compartilhados | Contrato DPA | Cláusulas Padrão |
|-----------|-----------|------|----------------------|--------------|-------------------|
| [AWS / GCP / Azure] | Cloud provider | [EUA] | Dados armazenados em infra | Sim | SCCs (EU) / Privacy Shield |
| [SendGrid / Mailgun] | E-mail transacional | [EUA] | Nome + e-mail | Sim | SCCs |
| [Stripe / PagSeguro] | Pagamentos | [EUA/BR] | Dados de cartão (tokenizado) | Sim | PCI DSS |
| [Datadog / Sentry] | Observabilidade | [EUA] | Logs (mascarados) | Sim | SCCs |
| [Analytics] | Análise de comportamento | [—] | IDs anônimos / pseudonimizados | Sim | — |

---

## 6. Medidas Técnicas e Organizacionais (Art. 46)

### 6.1. Técnicas
- [ ] Criptografia em repouso (AES-256 ou equivalente)
- [ ] Criptografia em trânsito (TLS 1.2+ obrigatório, TLS 1.3 preferido)
- [ ] Pseudonimização de dados em ambientes não-produtivos
- [ ] Controle de acesso baseado em papéis (RBAC) com MFA obrigatório
- [ ] Logs de auditoria com hash para imutabilidade
- [ ] Mascaramento de dados em logs (CPF, e-mail, cartão não aparecem em plain text)
- [ ] Gestão de segredos via vault (nunca hardcoded)
- [ ] Análise de vulnerabilidades automatizada (SAST + SCA no CI/CD)

### 6.2. Organizacionais
- [ ] Privacy by Design e Privacy by Default (Art. 46, § 2º)
- [ ] Treinamento anual de equipe em LGPD
- [ ] DPO designado e contato público disponível
- [ ] Registro de incidentes (timeline + impacto)
- [ ] Processo de atendimento de direitos dos titulares (prazo: 15 dias — Art. 18)
- [ ] DPIA (Avaliação de Impacto) para tratamentos de risco elevado (Art. 38)

---

## 7. Direitos dos Titulares (Art. 18)

| Direito | Prazo de Atendimento | Canal | Processo |
|---------|---------------------|-------|---------|
| Confirmação de tratamento | 15 dias | [email/portal] | `scripts/lgpd/data-subject-request.py` |
| Acesso aos dados | 15 dias | [email/portal] | Exportar dados do titular |
| Correção | 15 dias | [email/portal] | Formulário de atualização |
| Anonimização / Bloqueio / Eliminação | 15 dias | [email/portal] | Processo de exclusão lógica/física |
| Portabilidade | 15 dias | [email/portal] | Exportar JSON/CSV |
| Revogação de consentimento | Imediato | [email/portal] | Preferências de privacidade |
| Oposição | 15 dias | [email/portal] | Avaliação de base legal alternativa |

---

## 8. Transferência Internacional de Dados (Art. 33)

| Destino | País | Mecanismo de Adequação |
|---------|------|------------------------|
| [Serviço X] | [Nome do País] | Cláusulas Contratuais Padrão (CCP/SCCs) |
| [Serviço Y] | [Nome do País] | País com nível adequado de proteção |
| [Serviço Z] | [Nome do País] | Consentimento específico do titular |

---

## 9. Histórico de Revisões

| Data | Versão | Responsável | Alteração |
|------|--------|-------------|-----------|
| [AAAA-MM-DD] | 1.0.0 | [Nome] | Criação do documento |
| [AAAA-MM-DD] | 1.1.0 | [Nome] | [Descrição da alteração] |
