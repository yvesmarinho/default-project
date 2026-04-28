# Objetivo.yaml Wizard Guide

**Guia completo do wizard interativo para criar arquivos objetivo.yaml v2.0**

---

## 📋 Índice

- [O que é o Wizard](#o-que-é-o-wizard)
- [Quando Usar](#quando-usar)
- [Como Usar](#como-usar)
- [Modos de Operação](#modos-de-operação)
- [Exemplos de Output](#exemplos-de-output)
- [Keyboard Navigation](#keyboard-navigation)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)

---

## O que é o Wizard

O **Objetivo Wizard** é uma ferramenta interativa que guia você na criação de arquivos `objetivo.yaml` v2.0 através de perguntas e respostas via terminal.

**Benefícios:**
- ✅ Não precisa editar YAML manualmente
- ✅ Perguntas guiadas com exemplos contextuais
- ✅ Validação em tempo real
- ✅ Progressive disclosure (P0 → P1 → P2)
- ✅ Suporte a Ctrl+C (draft save) e Ctrl+Z (undo)

**Formato gerado:** Markdown Híbrido (YAML frontmatter + seções numeradas com emoji)

---

## Quando Usar

### ✅ Use o Wizard se você:

- É **iniciante** no formato objetivo.yaml v2.0
- Prefere **interface guiada** a edição manual
- Quer **começar rápido** sem ler toda a especificação
- Precisa de **exemplos contextuais** enquanto preenche
- Está criando um **projeto simples** (1-3 features)

### ❌ NÃO use o Wizard se você:

- É **experiente** com objetivo.yaml e prefere edição direta
- Precisa de **controle total** sobre formatação
- Está criando um **projeto complexo** (5+ features, múltiplos domínios)
- Quer **reutilizar** conteúdo de outros arquivos
- Está **automatizando** em CI/CD (use `--from-file` ao invés)

---

## Como Usar

### Modo Interativo (Padrão)

```bash
# Iniciar wizard interativo
cd /path/to/your/project
scaffold.py objetivo-init

# OU com output customizado
scaffold.py objetivo-init --output meu-objetivo.yaml
```

**Fluxo:**
1. Wizard exibe banner e instruções
2. Coleta metadados do projeto (nome, tipo, domínio, linguagem)
3. Pergunta seções P0 (obrigatórias): 3 perguntas essenciais
4. Pergunta se quer adicionar seções P1 (opcionais)
5. Renderiza template com suas respostas
6. Salva em `objetivo.yaml`

**Tempo estimado:** 5-10 minutos

---

## Modos de Operação

### 1. Interactive (Default)

Wizard completo com perguntas e respostas:

```bash
scaffold.py objetivo-init
```

**Output:**
```
🧙 Wizard objetivo.yaml v2.0

Crie seu arquivo objetivo.yaml respondendo algumas perguntas.
(Ctrl+C: salvar draft | Ctrl+Z: voltar)

Metadados do Projeto

Nome do projeto (kebab-case)
Exemplo: user-management-api
  Resposta: payment-gateway-api

Título legível
Exemplo: API de Gerenciamento de Usuários
  Resposta: API Gateway de Pagamentos

...
```

### 2. Non-Interactive (CI/CD)

Para automação, use arquivo JSON com respostas pré-definidas:

```bash
# 1. Crie answers.json
cat > answers.json <<EOF
{
  "project_name": "payment-gateway-api",
  "project_title": "API Gateway de Pagamentos",
  "project_type": "backend-api",
  "project_domain": "programming",
  "project_language": "python",
  "created_by": "devops-team",
  "answers": {
    "{{ANSWER_1}}": "API RESTful para processar pagamentos via PIX, cartão de crédito e boleto",
    "{{ANSWER_2}}": "Merchants perdem vendas (12%) devido a checkout lento (>8s). Gateway atual tem downtime de 3%.",
    "{{ANSWER_3}}": "- Processamento PIX (P0)\n- Processamento cartão de crédito (P0)\n- Dashboard de transações (P1)"
  }
}
EOF

# 2. Execute wizard em modo non-interactive
scaffold.py objetivo-init --from-file answers.json
```

### 3. Template-Only

Apenas copia o template sem wizard:

```bash
scaffold.py objetivo-init --template-only
```

Útil se você:
- Quer editar manualmente
- Já conhece bem o formato
- Prefere controle total

---

## Exemplos de Output

### Exemplo 1: Backend API (Python)

**Input (wizard):**
- Nome: `user-auth-service`
- Tipo: `backend-api`
- Domínio: `programming`
- Linguagem: `python`
- P0 Q1: "Microserviço de autenticação com JWT e OAuth2"
- P0 Q2: "Sistema atual usa autenticação básica insegura, 20% das contas comprometidas"
- P0 Q3: "Login JWT (P0)\nOAuth2 Google/GitHub (P1)\n2FA (P2)"

**Output gerado (`objetivo.yaml`):**
```yaml
---
version: "2.0"
project:
  name: "user-auth-service"
  title: "Microserviço de Autenticação"
  type: "backend-api"
  domain: "programming"
  language: "python"
created_at: "2026-04-28"
created_by: "devops-team"
---

## 1️⃣ O que este projeto faz?

Microserviço de autenticação com JWT e OAuth2

## 2️⃣ Qual problema resolve?

Sistema atual usa autenticação básica insegura, 20% das contas comprometidas

## 3️⃣ Escopo do Projeto

### ✅ Incluído

- Login JWT (P0)
- OAuth2 Google/GitHub (P1)
- 2FA (P2)

### ❌ Excluído

(Não especificado - preencher manualmente se necessário)
```

---

## Keyboard Navigation

### Atalhos Disponíveis

| Tecla | Ação | Quando usar |
|-------|------|-------------|
| **Enter** | Confirmar resposta | Sempre (terminar input) |
| **Enter Enter** | Terminar multiline | Em perguntas multiline (Q2, Q3, Q4, Q5) |
| **Ctrl+C** | Salvar draft e sair | Se quiser pausar e continuar depois |
| **Ctrl+Z** | Voltar pergunta anterior | Se errou resposta anterior |
| **Tab** | Auto-complete exemplo | Se Rich disponível (experimental) |

### Comportamento Multiline

Perguntas que aceitam múltiplas linhas:
- **Q2:** Qual problema resolve? (1-2 parágrafos)
- **Q3:** O que está NO escopo? (lista de features)
- **Q4:** Há restrições técnicas?
- **Q5:** Há regras de negócio complexas?

**Como usar:**
1. Digite primeira linha
2. Pressione Enter
3. Digite segunda linha
4. Pressione Enter
5. **Pressione Enter novamente (linha vazia) para terminar**

**Exemplo:**
```
O que está NO escopo? (liste features incluídas, Enter vazio para terminar)
Exemplo: Processamento automático de dados (P0)...
(Digite Enter duas vezes para terminar)
  Autenticação JWT (P0)
  OAuth2 Google (P1)
  2FA por SMS (P2)
  
✓ Resposta salva
```

### Draft Save (Ctrl+C)

Se você pressionar **Ctrl+C** durante o wizard:

1. Wizard salva progresso atual em `objetivo-draft.yaml`
2. Exibe mensagem: "📝 Draft salvo: objetivo-draft.yaml"
3. Sai do wizard

**Para continuar depois:**
1. Abra `objetivo-draft.yaml`
2. Complete manualmente as seções faltantes
3. Valide: `scaffold.py objetivo-validate --file objetivo-draft.yaml`

---

## Troubleshooting

### Problema: Rich não disponível

**Sintoma:**
```
ImportError: No module named 'rich'
```

**Solução:**
O wizard funciona **sem Rich** usando print() simples. Você perderá:
- Cores e formatação
- Painel de banner
- Progress indicators

Mas **todas as funcionalidades** principais continuam funcionando.

**Instalar Rich (opcional):**
```bash
pip install rich
```

---

### Problema: Keyboard navigation não funciona

**Sintoma:**
- Ctrl+Z não volta pergunta anterior
- Ctrl+C não salva draft

**Causa:** Terminal não suporta sinais POSIX (Windows CMD, alguns terminais customizados)

**Solução:**
1. Use terminal compatível (bash, zsh, PowerShell 7+)
2. OU use modo non-interactive:
   ```bash
   scaffold.py objetivo-init --from-file answers.json
   ```

---

### Problema: Multiline input não termina

**Sintoma:**
Você pressiona Enter mas wizard continua esperando input.

**Causa:** Precisa pressionar **Enter duas vezes** (linha vazia).

**Solução:**
```
  Linha 1
  Linha 2
  <Enter>  ← primeira vez (nova linha)
  <Enter>  ← segunda vez (termina)
```

---

### Problema: Pergunta obrigatória aceita resposta vazia

**Sintoma:**
Wizard aceita Enter vazio em perguntas P0.

**Causa:** Bug conhecido em versões antigas.

**Solução:**
Atualize scaffold.py:
```bash
git pull origin 060-mini-engram-python
```

---

### Problema: Template não encontrado

**Sintoma:**
```
FileNotFoundError: Template not found: poc/objetivo-v2-template-base.md
```

**Causa:** Executando wizard fora do diretório do template.

**Solução:**
```bash
cd /path/to/a-default-project
scaffold.py objetivo-init
```

---

## FAQ

### 1. Posso editar o arquivo gerado depois?

**Sim!** O wizard gera um arquivo objetivo.yaml válido que você pode editar manualmente. Recomendado:
1. Gerar com wizard (5 min)
2. Refinar manualmente (10 min)
3. Validar: `scaffold.py objetivo-validate`

---

### 2. Como adicionar seções P2 (avançadas)?

O wizard atualmente suporta apenas P0 (obrigatórias) e P1 (contextuais). Para adicionar P2:
1. Complete wizard normalmente
2. Edite `objetivo.yaml` manualmente
3. Adicione seções 6️⃣, 7️⃣, 8️⃣, 9️⃣ conforme necessário

---

### 3. Posso reusar respostas de outro projeto?

**Sim, use modo non-interactive:**
```bash
# 1. Extraia respostas de projeto anterior (manual ou script)
cat > answers.json <<EOF
{
  "project_name": "new-project",
  ...
}
EOF

# 2. Gere novo objetivo.yaml
scaffold.py objetivo-init --from-file answers.json
```

---

### 4. O wizard valida as respostas?

**Parcialmente:**
- ✅ Valida campos obrigatórios (não pode estar vazio)
- ✅ Valida tipos de projeto (deve estar na lista)
- ❌ NÃO valida conteúdo semântico

**Após wizard, sempre valide:**
```bash
scaffold.py objetivo-validate
```

---

### 5. Quanto tempo leva para completar?

| Perfil | P0 apenas | P0 + P1 |
|--------|-----------|---------|
| **Iniciante** | 8-10 min | 12-15 min |
| **Intermediário** | 5-7 min | 8-10 min |
| **Avançado** | 3-5 min | 5-7 min |

**Dica:** Se >15 min, considere edição manual ao invés do wizard.

---

### 6. Como funciona a geração de spec técnico?

Após criar objetivo.yaml com wizard:

```bash
# 1. Validar
scaffold.py objetivo-validate

# 2. Gerar spec técnico
scaffold.py objetivo-generate

# Output: objetivo-spec.yaml
```

O spec técnico é **gerado automaticamente** de objetivo.yaml e inclui:
- Profiles detectados (baseado em type + language)
- Features extraídas (seção 3 "Incluído")
- Personas (seção 5, se preenchida)

---

## Próximos Passos

Após completar o wizard:

1. **Validar:** `scaffold.py objetivo-validate`
2. **Gerar spec:** `scaffold.py objetivo-generate`
3. **Criar projeto:** `scaffold.py new --config objetivo-spec.yaml`

**Documentação relacionada:**
- [Spec 066: objetivo.yaml v2.0](../../specs/066-objetivo-yaml-v2/spec.md)
- [Comparação v1.0 vs v2.0](../debates/COMPARACAO-OBJETIVO-V1-V2.md)
- [README Principal](../../README.md)

---

**Versão:** 1.0 (2026-04-28)
**Spec:** 066-objetivo-yaml-v2
**Autor:** DevOps Team
