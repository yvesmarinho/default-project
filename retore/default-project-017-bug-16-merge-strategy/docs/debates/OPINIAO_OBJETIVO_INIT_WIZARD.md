# Análise: Proposta de Geração objetivo-init.yaml via Wizard

**Data**: 2026-04-28
**Autor**: GitHub Copilot
**Status**: ✅ RECOMENDADO

---

## Resumo da Proposta

O usuário propôs:

1. Gerar arquivo de melhorias (Opção A) para futuro
2. Criar `template-bases/objetivo-init-template.yaml`
3. Alterar wizard para gerar `objetivo-init.yaml` (YAML puro)
4. Usar `scaffold objetivo-validate` para validação
5. Usar `scaffold objetivo-generate` para gerar spec final

---

## Opinião: ✅ EXCELENTE PROPOSTA — Pragmática e Viável

### Por que recomendo FORTEMENTE:

#### 1. **Não quebra workflow existente** ✅
- `objetivo-validate` e `objetivo-generate` **já existem e funcionam**
- Projetos atuais usam `objetivo-init.yaml` v1.0
- Zero breaking changes

#### 2. **Resolve problema real imediato** ✅
- Wizard v2.0 atual perde **69% de informação crítica**
- objetivo-init.yaml v1.0 captura **13/13 campos necessários**
- Pipeline completo: `wizard → validate → generate → new project`

#### 3. **Formato comprovado** ✅
- objetivo-init.yaml já validado em projeto Chatwoot Migration
- Formato YAML puro é familiar para devs
- Estrutura estável há 6+ meses

#### 4. **Evolução incremental permitida** ✅
- Possibilita melhorias graduais (adicionar campos)
- Não bloqueia migração futura para v3.0 (Markdown Híbrido)
- Permite convivência temporária de formatos

#### 5. **Fix do bug CWD incluído** ✅
- Wizard agora usa `Path.cwd()` corretamente
- Arquivo gerado no diretório onde usuário executou comando
- Wrapper `~/.local/bin/scaffold` funciona corretamente

---

## Comparação: v1.0 (Atual) vs v2.0 (Incompleto)

| Aspecto | objetivo-init.yaml v1.0 | objetivo.yaml v2.0 |
|---------|-------------------------|-------------------|
| **Formato** | YAML puro (98 linhas) | Markdown Híbrido (335 linhas) |
| **Campos capturados** | 13/13 (100%) | 4/13 (31%) |
| **Validação** | ✅ `objetivo-validate` funciona | ⚠️ Parcial |
| **Geração de spec** | ✅ `objetivo-generate` funciona | ❌ Não implementado |
| **Status** | ✅ Estável, produção | ⚠️ Protótipo incompleto |
| **Pipeline completo** | ✅ wizard → validate → generate → new | ❌ Quebrado após wizard |
| **Legibilidade** | 🟡 YAML aninhado (menos legível) | ✅ Markdown + emojis (mais legível) |
| **Manutenção** | ✅ Simples (1 template) | ⚠️ Complexo (múltiplos parsers) |

**Veredicto**: v1.0 é **mais completo e funcional**, mesmo sendo menos legível.

---

## Arquitetura da Solução Implementada

```
┌─────────────────────────────────────────────────────────────┐
│  Usuario executa: scaffold objetivo-init                    │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  ObjetivoWizard                                             │
│  - template: template-bases/objetivo-init-template.yaml     │
│  - perguntas: 15 perguntas (6 P0 + 9 P1)                   │
│  - output: CWD/objetivo-init.yaml                          │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  Arquivo gerado: objetivo-init.yaml (YAML puro)            │
│  - description, specification, rules                        │
│  - folder_structure, expected_outcome                       │
│  - infrastructure, profile, features_to_implement           │
│  - pending_tasks                                            │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  Validação: scaffold objetivo-validate --file objetivo.yaml │
│  - Schema YAML válido ✅                                    │
│  - Campos obrigatórios preenchidos ✅                       │
│  - Consistência (profiles × features) ✅                    │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  Geração: scaffold objetivo-generate --input objetivo.yaml  │
│  - Converte objetivo-init.yaml → objetivo-spec.yaml        │
│  - Auto-detecta profiles (dba, devops, python, etc)        │
│  - Mapeia features_to_implement → spec.features            │
│  - Gera personas baseado em roles                          │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  Criação de projeto: scaffold new --config objetivo-spec    │
│  - Aplica profiles corretos                                │
│  - Gera estrutura de pastas                                │
│  - Configura ferramentas (MCP, VS Code, CI/CD)             │
└─────────────────────────────────────────────────────────────┘
```

---

## Melhorias Implementadas

### 1. Template objetivo-init-template.yaml ✅
- Localização: `template-bases/objetivo-init-template.yaml`
- Placeholders: `{{PROJECT_NAME}}`, `{{DESCRIPTION}}`, `{{RESPONSE}}`, etc
- Campos: 13 blocos (completo)

### 2. Wizard Modificado ✅
- 15 perguntas totais:
  - **P0 (obrigatório)**: 6 perguntas (nome, tipo, o que faz, response, expected_outcome, features)
  - **P1 (opcional)**: 9 perguntas (problema, regras, docstyle, infra, profiles, etc)
- Output: `objetivo-init.yaml` (YAML puro, não Markdown)
- CWD fix: Usa `Path.cwd()` em vez de path relativo

### 3. Mensagens Atualizadas ✅
- Banner: "Wizard objetivo-init.yaml v1.0"
- Próximos passos: `scaffold objetivo-validate --file objetivo-init.yaml`

---

## Roadmap Futuro (Opcional)

### Fase 1: Consolidar v1.0 (Atual — 2026-04-28)
- ✅ Wizard gera objetivo-init.yaml
- ✅ Validação funciona
- ✅ Geração de spec funciona
- ✅ Pipeline completo testado

### Fase 2: Melhorias Incrementais (Q2 2026)
- [ ] Adicionar mais campos ao template (se necessário)
- [ ] Melhorar validações (linting YAML)
- [ ] Adicionar auto-complete para profiles

### Fase 3: Migração para v3.0 (Q3 2026 — Opcional)
- [ ] Implementar Markdown Híbrido Completo
- [ ] Parser bidirecional (YAML ↔ Markdown)
- [ ] Migração automática v1.0 → v3.0
- [ ] Deprecar formato v1.0 gradualmente

---

## Riscos e Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Usuários confundem v1.0 vs v2.0 | Média | Baixo | Documentação clara + banner do wizard |
| Breaking change futuro (v1→v3) | Alta | Médio | Migração automática + período de transição |
| Template fica desatualizado | Baixa | Baixo | Versionamento no próprio arquivo |

---

## Decisão Final

**Status**: ✅ **APROVADO E IMPLEMENTADO**

**Justificativa**:
1. Resolve problema real imediato (wizard v2.0 incompleto)
2. Mantém compatibilidade com tools existentes (validate/generate)
3. Formato comprovado e estável
4. Permite evolução incremental
5. Fix crítico do CWD incluído

**Próximos passos**:
1. ✅ Testar wizard com projeto real
2. ✅ Validar arquivo gerado
3. ✅ Gerar spec a partir do objetivo-init.yaml
4. [ ] Documentar workflow completo
5. [ ] Deprecar README que menciona objetivo.yaml v2.0

---

## Conclusão

A proposta do usuário é **pragmática, viável e resolve problema real**. Ao invés de forçar um formato v2.0 incompleto que perde 69% de informação, a solução usa formato v1.0 comprovado com wizard interativo melhorado.

**Recomendação**: ✅ **MANTER ESSA ABORDAGEM**

O formato Markdown Híbrido v3.0 pode ser desenvolvido paralelamente como melhoria futura, mas não deve bloquear o trabalho atual.
