# 🎭 Debate — Estrutura dos Arquivos `.copilot-*`

**Data**: 2026-02-28
**Contexto**: Os 5 arquivos `.copilot-*` atuais têm atribuições sobrepostas e responsabilidades pouco claras.
**Trigger**: Revisão pré-IMP-01 — o `scaffold.py` vai gerar/gerir esses arquivos; a estrutura precisa ser definida antes da implementação.
**Status**: ✅ Resolvido — todas as 3 decisões confirmadas em 2026-02-28

---

## 📋 Inventário Atual (o que existe hoje)

| Arquivo | Linhas | Tipo | Propósito declarado |
|---------|--------|------|---------------------|
| `.copilot-rules.md` | 206 | Markdown | Regras de ferramentas (create_file, não heredoc) + git |
| `.copilot-git-rules.md` | 505 | Markdown | Regras de git commit + conventional commits |
| `.copilot-strict-rules.md` | 626 | Markdown | Regras críticas de execução + organização de pastas |
| `.copilot-strict-enforcement.md` | 405 | Markdown | Regras de execução + ferramentas VS Code + mover arquivos |
| `.copilot-file-rules.sh` | 168 | Shell script | Checklist de criação de arquivos (documentação, não executável) |

**Total**: 1910 linhas | **Regras**: 5 arquivos

---

## 🔴 Diagnóstico: Sobreposições Identificadas

### Duplicidade confirmada (mesma regra em múltiplos arquivos):

| Regra | Arquivos que a contêm |
|-------|----------------------|
| NUNCA usar `cat << EOF` / `echo >>` | `rules.md` + `file-rules.sh` + `strict-enforcement.md` |
| NUNCA usar `git commit -m` direto | `rules.md` + `git-rules.md` + `strict-enforcement.md` |
| Organização de pastas (onde criar arquivos) | `rules.md` + `strict-rules.md` + `strict-enforcement.md` |
| Ferramentas nativas VS Code vs. CLI | `strict-enforcement.md` (único — mas relacionado a `rules.md`) |
| `.specify/` é exclusivo do SpecKit | `strict-rules.md` + `strict-enforcement.md` |

### Contaminação de projetos externos:

- `.copilot-strict-rules.md` menciona `enterprise-python-n8n-backup`, `session-history/`, `src/enterprise_backup/n8n/` — estrutura de **outro projeto**, não deste template
- `.copilot-strict-rules.md` referencia `specs/001-n8n-backup-module/` — específico de n8n, não genérico
- `.copilot-rules.md` menciona `./scripts/commit-k8s-revision.sh` — script de outro projeto (kubernetes)

### Nomes não revelam responsabilidade:

- `strict-rules` vs. `strict-enforcement` — qual a diferença semântica real? Ambos são "regras obrigatórias"
- `file-rules.sh` é um shell script que **não executa nada** — é documentação disfarçada de script
- `rules.md` deveria ser o principal, mas não é o mais completo

---

## 🎭 Debate — Três Perspectivas

---

### 🏢 1. PROJECT MANAGER

#### 📌 Posição: "Otimizar para manutenção — quem edita o quê, quando?"

**Problema central do PM**:
> "Tenho 1910 linhas de regras para o Copilot. Quando uma regra muda, em quantos arquivos preciso editar? A resposta hoje é: não sei — porque as responsabilidades se sobrepõem."

**Análise de manutenibilidade**:

| Cenário de mudança | Hoje (quantos arquivos) | Ideal (quantos arquivos) |
|--------------------|------------------------|--------------------------|
| Mudar regra de git commit | 3 | 1 |
| Mudar onde sessões são salvas | 3 | 1 |
| Adicionar nova ferramenta proibida | 2 | 1 |
| Criar regra específica do projeto novo | manual em todos | 1 (por projeto) |
| Adicionar regra de nomenclatura | 2 | 1 |

**Custo da situação atual**:
- Regras desatualizadas de outros projetos (n8n, kubernetes) poluem o template genérico
- O `scaffold.py` precisaria gerenciar 5 arquivos distintos com sobreposições — complexidade desnecessária
- Novos projetos herdam lixo de projetos anteriores

**Posição do PM**:
> "Dois arquivos. Um genérico (nunca muda depois de estável). Um por projeto (editado pelo dev conforme o projeto evolui). Qualquer coisa além disso precisa de justificativa muito forte."

---

### 👨‍💻 2. DEVELOPER

#### 📌 Posição: "Separar por eixo de mudança — o que muda junto deve ficar junto"

**Análise técnica**:

O princípio de design relevante aqui é o **Separation of Concerns** aplicado a dados de configuração:

```
Eixo 1 — Quem é responsável pela mudança?
  ├─ Yves (usuário) → regras de comportamento do Copilot (genéricas)
  └─ scaffold.py   → arquivo de identidade do projeto (gerado + editado)

Eixo 2 — Com que frequência muda?
  ├─ Raramente  → regras comportamentais consolidadas (ferramentas, git, pastas)
  └─ Por projeto → perfil do projeto, convenções específicas, domain profile ativo

Eixo 3 — É genérico ou específico?
  ├─ Genérico → compartilhado via symlink de .copilot-shared/
  └─ Específico → gerado por scaffold.py, vive no projeto, editado pelo dev
```

**Mapeamento atual → eixos**:

| Arquivo atual | Eixo real | Problema |
|---------------|-----------|---------|
| `.copilot-rules.md` | Genérico comportamental | OK, mas incompleto — falta o que está em strict-enforcement |
| `.copilot-git-rules.md` | Genérico comportamental | OK — mas 505 linhas para git é excessivo; pode ser seção de rules.md |
| `.copilot-strict-rules.md` | Genérico comportamental | Contaminado por dados de outros projetos |
| `.copilot-strict-enforcement.md` | Genérico comportamental | Duplica os outros três |
| `.copilot-file-rules.sh` | Genérico comportamental | Duplica rules.md; `.sh` para documentação é anti-padrão |

**Conclusão do Developer**:
> "Todos os 5 arquivos são 'genérico comportamental'. Nenhum é específico do projeto. O arquivo específico do projeto (`.copilot-rules-[projeto].md`) ainda não existe de forma padronizada — é criado manualmente, sem template. O `scaffold.py` precisa de uma estrutura limpa para implementar."

**Proposta técnica do Developer**:

```
.copilot-shared/                          ← Repositório central compartilhado
├── .copilot-rules.md                     ← ÚNICO arquivo de regras comportamentais
│                                            (consolida: rules + git-rules + strict-rules
│                                             + strict-enforcement + file-rules.sh)
└── (outros arquivos compartilhados futuros)

[projeto]/
├── .copilot-rules.md                     ← symlink → shared (regras genéricas)
└── .copilot-rules-[projeto].md           ← gerado por scaffold.py (específico)
```

**Por que `.copilot-file-rules.sh` deve ser abolido**:
- É um `bash` file que nunca é executado — é documentação
- Documentação em `.sh` viola o princípio do menor espanto
- O conteúdo está 100% duplicado em `.copilot-rules.md`

---

### 🧩 3. FEATURE ENGINEER (Perspectiva do Usuário/Copilot)

#### 📌 Posição: "O Copilot precisa de clareza, não volume — menos arquivos, mais autoridade"

**Como o Copilot consome esses arquivos**:

O Copilot carrega os arquivos `.copilot-*` no contexto da sessão. O problema não é só de manutenção — é de **eficácia**:

> "Quando o Copilot tem 1910 linhas de regras em 5 arquivos com sobreposições, acontece **dilution de autoridade**: regras conflitantes ou repetidas fazem o modelo tratar as instruções como ruído, não como sinal."

**Hierarquia de leitura ideal** (do ponto de vista do Copilot):

```
Sessão iniciada
  │
  ├─ Ler: .copilot-rules.md           → "Como devo me comportar em qualquer projeto"
  │        (regras comportamentais — ferramentas, git, pastas, nomenclatura)
  │
  └─ Ler: .copilot-rules-[projeto].md → "Quem é ESTE projeto e suas regras específicas"
           (identidade, domain profile, convenções locais)
```

**O que acontece com 5 arquivos e sobreposições**:
- O Copilot não sabe qual arquivo tem "mais autoridade" quando há conflito
- Regras de outros projetos (n8n, kubernetes) são carregadas sem utilidade
- Tempo de contexto desperdiçado com duplicações — tokens que poderiam ser usados para código

**Análise de valor por arquivo atual**:

| Arquivo | Conteúdo único | Conteúdo duplicado | Recomendação |
|---------|----------------|-------------------|--------------|
| `.copilot-rules.md` | ~30% único | ~70% repetido nos outros | **Manter — refatorar como arquivo único** |
| `.copilot-git-rules.md` | 20% único (conventional commits, branch naming) | 80% repetido | **Mesclar em rules.md como seção** |
| `.copilot-strict-rules.md` | 10% único | 90% repetido + lixo de n8n/k8s | **Eliminar — migrar o único para rules.md** |
| `.copilot-strict-enforcement.md` | 30% único (REGRA 0.A, REGRA 0.B) | 70% repetido | **Mesclar em rules.md — manter 0.A e 0.B** |
| `.copilot-file-rules.sh` | 0% único | 100% duplicado | **Eliminar — não acrescenta nada** |

---

## 🔴 Pontos de Tensão

### Tensão 1: Consolidar tudo em 1 arquivo vs. manter separação por tema

| Perspectiva | Posição |
|-------------|---------|
| **PM** | "Dois arquivos é o máximo — um genérico, um por projeto. Mais do que isso é overhead cognitivo." |
| **Developer** | "1 arquivo genérico é tecnicamente suficiente. A separação por tema (`git-rules`, `file-rules`) só tem valor se as seções forem grandes demais para navegar num único arquivo." |
| **Feature Eng.** | "Do ponto de vista do Copilot: 1 arquivo = 1 carga de contexto = 1 autoridade clara. A fragmentação atual dilui o sinal." |

**Resolução proposta**: ✅ **1 arquivo genérico consolidado + 1 arquivo por projeto**

---

### Tensão 2: O que fazer com o conteúdo único de `git-rules.md`?

`git-rules.md` tem conteúdo genuíno que não aparece nos outros:
- Regra de tamanho de linha (≤5 linhas vs. 6+ linhas para textos em terminal)
- Branch naming convention
- Conventional commits reference

| Perspectiva | Posição |
|-------------|---------|
| **PM** | "Não perder esse conteúdo — só mudar onde fica." |
| **Developer** | "Criar seção `## Git Workflow` dentro de `.copilot-rules.md`. Navegável com âncoras." |
| **Feature Eng.** | "505 linhas só de git é excessivo. Refinar para as 20% de regras que têm impacto real no comportamento." |

**Resolução proposta**: ✅ **Migrar para seção em `rules.md`. Descartar redundâncias. Manter regras únicas.**

---

### Tensão 3: O que é "genérico" vs. "específico do projeto"?

| Categoria | Genérico (shared) | Específico (por projeto) |
|-----------|------------------|--------------------------|
| Ferramentas proibidas (heredoc, echo) | ✅ | — |
| Regras de git commit | ✅ | — |
| Ferramentas VS Code nativas | ✅ | — |
| Onde criar arquivos | ✅ (estrutura padrão) | ✅ (se projeto desvia do padrão) |
| Domain profile ativo | — | ✅ |
| Linguagem principal do projeto | — | ✅ |
| Convenções de nomenclatura do projeto | — | ✅ |
| Sessão ativa (data, recovery) | — | ✅ |
| Regras específicas da stack (ex: nunca usar X framework) | — | ✅ |

**Resolução proposta**: ✅ **Linha clara: comportamento do Copilot = genérico; identidade e contexto = específico**

---

## ✅ Consenso: Estrutura Proposta

### De 5 arquivos para 2

```
.copilot-shared/
└── .copilot-rules.md              ← ÚNICO arquivo genérico
                                     Seções: Ferramentas | Git | Pastas | Nomenclatura | Enforcement
                                     Origem: consolida rules + git-rules + strict-enforcement (partes únicas)
                                     Remove: referências a n8n, kubernetes, enterprise-python-n8n-backup

[projeto]/
├── .copilot-rules.md              ← symlink → shared (regras do Copilot para qualquer projeto)
└── .copilot-rules-[projeto].md    ← gerado por scaffold.py (identidade + específicos deste projeto)
                                     Seções: Identidade | Domain Profile | Estrutura | Regras Específicas
```

### Arquivo genérico — estrutura consolidada de `.copilot-rules.md`

```markdown
# GitHub Copilot — Regras Comportamentais

## 1. Ferramentas de Arquivo (P0)
## 2. Ferramentas Nativas VS Code (P0)
## 3. Git Workflow (P0)
## 4. Organização de Pastas (P1)
## 5. Nomenclatura (P1)
## 6. Enforcement (como agir em violações)
```

### Arquivo específico — estrutura do `.copilot-rules-[projeto].md`

```markdown
# Copilot Rules — [project_title]

## 1. Identidade do Projeto
## 2. Domain Profile Ativo
## 3. Estrutura de Pastas (se desvia do padrão)
## 4. Regras Específicas desta Stack
## 5. Regras Específicas desta Sessão (editável por sessão)
```

---

## 📋 Plano de Ação

| Ação | Impacto | Quando |
|------|---------|--------|
| Refatorar `.copilot-rules.md` — consolidar conteúdo único de todos os 5 arquivos | Alto | IMP-01 (antes de implementar scaffold.py) |
| Eliminar `.copilot-strict-rules.md` — conteúdo migrado + lixo removido | Alto | IMP-01 |
| Eliminar `.copilot-strict-enforcement.md` — conteúdo migrado | Alto | IMP-01 |
| Eliminar `.copilot-file-rules.sh` — 100% duplicado | Médio | IMP-01 |
| Reduzir `.copilot-git-rules.md` para seção em `rules.md` | Médio | IMP-01 |
| Definir template canônico de `.copilot-rules-[projeto].md` | Crítico | IMP-01 (spec para templates.py) |
| Atualizar `scaffold.py` SHARED_COPILOT_FILES para lista de 1 item | Baixo | IMP-01 (implementação) |

---

## 🔗 Impacto no IMP-01 (scaffold.py)

Esta decisão muda diretamente a implementação de `scripts/lib/links.py` e `scripts/lib/templates.py`:

**Antes** (SHARED_COPILOT_FILES atual — 5 itens):
```python
SHARED_COPILOT_FILES = [
    ".copilot-rules.md",
    ".copilot-git-rules.md",
    ".copilot-strict-enforcement.md",
    ".copilot-strict-rules.md",
    ".copilot-file-rules.sh",
]
```

**Depois** (estrutura proposta — 1 item):
```python
SHARED_COPILOT_FILES = [
    ".copilot-rules.md",   # único arquivo genérico consolidado
]
```

O `scaffold.py` se torna mais simples: cria 1 symlink genérico + gera 1 arquivo específico. Zero ambiguidade.

---

## 🎯 Decisão Necessária

Antes de continuar com IMP-01, responder:

1. **[x]** ✅ **DECIDIDO**: Consolidação aprovada — 5 arquivos → 1 genérico (`.copilot-rules.md`) + 1 por projeto (`.copilot-rules-[proj].md`)
2. **[x]** ✅ **DECIDIDO**: `.copilot-file-rules.sh` será removido — conteúdo 100% duplicado, anti-padrão de documentação em `.sh`
3. **[x]** ✅ **DECIDIDO**: A refatoração de `.copilot-rules.md` acontece **ANTES** da implementação do `scaffold.py` — IMP-13 é pré-requisito de IMP-01

---

*Arquivo gerado em 2026-02-28 | Sessão: [DAILY_ACTIVITIES_2026-02-28.md](DAILY_ACTIVITIES_2026-02-28.md)*
