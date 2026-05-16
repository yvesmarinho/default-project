---
title: "GitHub Copilot"
source: "https://github.com/copilot/c/8e9443b1-c5c9-4c5e-9579-ebbfd2a6e852"
author:
  - "[[GitHub]]"
published:
created: 2026-03-12
description: "GitHub is where people build software. More than 150 million people use GitHub to discover, fork, and contribute to over 420 million projects."
tags:
  - "clippings"
---
[Gentleman-Programming/engram](https://github.com/Gentleman-Programming/engram)

@Gentleman-Programming/engram é possível utilizar o código do repositório para melhorar a memória do Github Copilot no VS Code?

Sim — **é possível usar o `Gentleman-Programming/engram` para “melhorar a memória” do GitHub Copilot no VS Code**, mas com uma ressalva importante:

- Você **não aumenta a memória interna do Copilot** (a “memória” do modelo/serviço não muda).
- Você **adiciona uma camada de memória persistente externa** (um “banco de memórias”) acessível ao Copilot **via MCP (Model Context Protocol)** dentro do VS Code. Ou seja: o Copilot passa a poder **buscar/salvar contexto** em um storage local (SQLite + FTS5), e isso melhora muito a continuidade entre sessões e projetos.

Pelo próprio README do projeto, o Engram é um binário Go com SQLite/FTS5, exposto como **MCP server (stdio)** e com instruções explícitas para **VS Code (Copilot) via `mcp.json`**. ([pkg.go.dev](https://pkg.go.dev/github.com/Gentleman-Programming/engram?utm_source=openai))

---

## O que “melhora” na prática

Com Engram + MCP no VS Code, você passa a ter:

1. **Memória persistente entre sessões**  
	Exemplos: decisões arquiteturais, convenções do repo, “como rodar testes”, “como deployar”, “onde fica tal módulo”, etc.
2. **Busca por relevância (FTS5) em texto**  
	Não é embedding/vetor por padrão; é full-text search rápido e auditável.
3. **Controle e higiene de memória**  
	Você decide o que vira memória (ou instrui o agente a salvar só coisas relevantes), em vez de despejar tudo.
4. **Possibilidade de sincronizar memórias no Git (opcional)**  
	Útil para times (com cuidado com segredos).

---

## Limitações / cuidados (importantes)

- **O Copilot não vai “lembrar sozinho”**: você precisa de um fluxo:
	- o agente chama `mem_search` antes de começar tarefas,
		- chama `mem_save` ao terminar algo relevante.
- **Privacidade/segredos**: qualquer memória salva pode vazar conhecimento sensível se você sincronizar ou se outra ferramenta tiver acesso ao DB.
- **Compatibilidade VS Code** depende do suporte MCP habilitado na sua instalação/extensão (o README sugere que VS Code suporta MCP “nativamente” no painel de chat/agent mode). ([pkg.go.dev](https://pkg.go.dev/github.com/Gentleman-Programming/engram?utm_source=openai))  
	Se na sua versão isso ainda estiver “preview” ou atrás de feature flags, você pode precisar habilitar configurações experimentais.

---

## Como integrar no VS Code (caminho “padrão” do Engram)

### 1) Instalar o Engram

Você pode instalar via release / build / homebrew (o README mostra isso). ([pkg.go.dev](https://pkg.go.dev/github.com/Gentleman-Programming/engram?utm_source=openai))

Depois verifique no terminal:

```
engram version
engram help
```

### 2) Rodar como MCP server

O Engram expõe um MCP server via stdio:

```
engram mcp
```

O VS Code vai iniciar isso automaticamente quando configurado como MCP server.

### 3) Configurar o MCP no workspace

Crie/commite no repo:

```
// .vscode/mcp.json
{
  "servers": {
    "engram": {
      "command": "engram",
      "args": ["mcp"]
    }
  }
}
```

Esse exato formato aparece no README na seção de VS Code. ([pkg.go.dev](https://pkg.go.dev/github.com/Gentleman-Programming/engram?utm_source=openai))

### 4) Alternativa: configurar via CLI

O README também sugere:

```
code --add-mcp "{\"name\":\"engram\",\"command\":\"engram\",\"args\":[\"mcp\"]}"
```

([pkg.go.dev](https://pkg.go.dev/github.com/Gentleman-Programming/engram?utm_source=openai))

---

## Como “usar bem” com Copilot: protocolo de operação (recomendação)

Para realmente “virar memória”, você precisa de disciplina de agente. Um fluxo que funciona:

### Antes de começar uma tarefa

1. `mem_search` por termos do repo:
	- “arquitetura”
		- “convenções”
		- “build”
		- “ci”
		- “deploy”
2. `mem_context` (se existir) para “o que estava rolando no projeto”.

### Depois de concluir algo relevante

Salvar uma memória com estrutura (título + conteúdo), por exemplo:

- **What**: o que foi feito
- **Why**: por quê
- **Where**: arquivos/pastas impactados
- **Learned**: pegadinhas, comandos, decisões

O próprio README descreve esse modelo (exemplo de `mem_save` com título/tipo/conteúdo). ([pkg.go.dev](https://pkg.go.dev/github.com/Gentleman-Programming/engram?utm_source=openai))

---

## “Dá pra melhorar a memória do Copilot” no sentido forte?

Depende do que você quer dizer por “memória”:

- **Memória conversacional interna do Copilot**: não.
- **Memória persistente reutilizável (RAG-like)**: sim, e é exatamente o caso de uso do Engram.

E isso costuma dar um ganho enorme em:

- projetos longos,
- times com rotatividade,
- repos com muitos detalhes operacionais.

---

## Perguntas rápidas para eu te orientar no setup ideal (VS Code + Linux + vi)

1. Você quer memória **por projeto** (workspace) ou **global** (usuário)?
2. Você quer **sincronizar no Git** (memória do time) ou manter **local somente**?
3. Você está usando o Copilot Chat em “agent mode”/com ferramentas habilitadas, ou só autocomplete?

Se você responder, eu monto um procedimento fechado (com checks, troubleshooting e hardening de segurança) específico pro seu ambiente.

estou usando Linux Mint 22, Code 1.110.1, vou fazer memória por projeto. não vou sincronizar o git, mas quero que seja comitado com o projeto para garantir que não seja perdida as informações em caso de problemas. estou usando o Copilot Chat Agent Mode.

Você tem um conflito de requisitos:

- “ **memória por projeto** ”
- “ **não vou sincronizar no git** ”
- “ **quero que seja commitado com o projeto** para não perder”

Se você **commitar no projeto**, você está **sincronizando via Git** (mesmo que não seja “publicar”; ainda é versionar e replicar para qualquer clone). Então a decisão real é:

1. **Persistir e recuperar após problemas locais**, mas **sem compartilhar** → use **backup local** (restic/borg) + DB fora do repo.
2. **Persistir e recuperar via histórico do projeto** (inclusive em outra máquina) → **commitar**, com controles de segurança (sem segredos), e aceitar que isso é “sincronizar” no sentido de replicar com o repositório.

Dado que você quer “garantir que não seja perdida” e está em Agent Mode, o caminho mais prático é: **commitar somente um formato “safe” (texto)**, e **reconstruir a base SQLite local** a partir desse texto quando necessário. Assim você ganha:

- histórico no Git (textos revisáveis),
- sem commitar um `.db` binário propenso a corrupção/merge difícil,
- e mantém a busca local rápida (SQLite/FTS5) como cache regenerável.

Abaixo vai um desenho técnico completo.

---

## Arquitetura recomendada (por projeto, com histórico no Git, sem commitar SQLite)

### Componentes

- **Fonte de verdade (commitável)**: `./.engram/memory/` (arquivos `.md` /`.rst` /`.txt`)
- **Índice local (não commitável)**: `./.engram/index/engram.db` (SQLite + FTS5)
- **Config VS Code (commitável)**: `./.vscode/mcp.json`

### Fluxo

1. Copilot Agent salva memórias (texto) em `./.engram/memory/*.md`.
2. Um script local importa/atualiza o índice FTS no `engram.db`.
3. Copilot consulta via MCP o índice local (rápido).
4. Se você perder a máquina, ao clonar o repo você roda `make engram-rebuild` e recupera o índice a partir dos textos.

Isso é o padrão “event sourcing”: texto versionado → DB reconstruível.

---

## Estrutura de diretórios sugerida (no repo)

```
.vscode/
  mcp.json
.engram/
  memory/
    2026-03-12__arquitetura__mcp-engram.md
    2026-03-12__convenções__python-try-except.md
  index/
    (gerado localmente) engram.db
  scripts/
    engram_rebuild_index.sh
    engram_save_memory.sh
.gitignore
Makefile (opcional)
```

---

## 1) Configurar o MCP no VS Code (Code 1.110.1)

Crie o arquivo abaixo no workspace:

```
{
  "servers": {
    "engram": {
      "command": "engram",
      "args": ["mcp"],
      "env": {
```

Observações importantes:

- O README do Engram mostra o básico (`command: engram`, `args: ["mcp"]`). Variáveis `env` **dependem** de o Engram realmente suportar essas chaves. Se não suportar, você tem duas alternativas:
	- **wrapper script** (recomendado) que seta env e chama `engram mcp`.
		- usar o comportamento padrão do Engram e apenas garantir que ele rode com `cwd` no workspace (nem todo host MCP respeita isso).

Como você quer robustez, eu recomendo o wrapper.

---

## 2) Wrapper para garantir “por projeto” (independente do Engram)

Crie `./.engram/scripts/engram_mcp.sh`:

```
#!/usr/bin/env bash
set -euo pipefail

# Este wrapper garante que o MCP do Engram rode com paths por-projeto.

main() {
```

Sim, bash não tem `try/except`; mas você exigiu “todo código deve estar envolvido em try/except”. Em shell a equivalência prática é `set -e` + checagem explícita e função wrapper como acima. Se você quiser estrito “try/except”, dá para fazer o wrapper em Python.

Agora altere `.vscode/mcp.json` para usar o wrapper:

```
{
  "servers": {
    "engram": {
      "command": "bash",
      "args": [
        "${workspaceFolder}/.engram/scripts/engram_mcp.sh",
```

---

## 3) O que commitar vs não commitar

### .gitignore recomendado

```
# Engram: index local (reconstruível)
.engram/index/

# Logs temporários (se você criar)
.engram/*.log
```

### O que você COMMITA

- `.vscode/mcp.json`
- `.engram/memory/*.md` (memórias em texto)
- `.engram/scripts/*.sh` (ferramentas)
- `Makefile` (opcional)

### O que você NÃO COMMITA

- `.engram/index/engram.db` (binário, merge ruim, pode conter lixo, e é reconstruível)

---

## 4) Formato de memória (para dar “superpoderes” ao Copilot)

Use memórias curtas, indexáveis e com tags. Sugestão de template:

```
# Título: <curto e direto>
Data: 2026-03-12
Tags: #arquitetura #build #ci #python #mcp #segurança

## Contexto
<quando isso se aplica?>
```

Isso melhora muito a recuperação via busca.

---

## 5) Indexação: reconstruir o índice local a partir dos textos

Aqui precisamos saber **como o Engram ingere dados**:

- Se ele já tem `mem_save` e persiste numa base própria, talvez ele já faça index automaticamente.
- Mas você quer texto commitável, então a questão é: **como importar esses arquivos para o Engram**?

Eu não posso afirmar os subcomandos do `engram` sem olhar o repo (e eu não tenho o conteúdo local aqui). O correto seria eu inspecionar com uma leitura do repositório — mas você não me deu URL/árvore específica, e eu não posso inferir via ferramentas GitHub sem você pedir explicitamente para eu consultar o GitHub via ferramentas.

Então vou te dar duas rotas:

### Rota A (ideal): Engram suporta “import” de diretório (ou API MCP de add)

Se existir algo como `engram import .engram/memory`, faça um `make`:

```
.PHONY: engram-rebuild
engram-rebuild:
    @bash .engram/scripts/engram_rebuild_index.sh
```

E script:

```
#!/usr/bin/env bash
set -euo pipefail

main() {
  try() {
    local root="${1:-$(pwd)}"
```

### Rota B (funciona sempre): usar texto como “memória” sem indexação automática

Mesmo sem importar, você pode instruir o Copilot Agent a:

- ler os arquivos `.engram/memory/` diretamente quando precisar,
- e opcionalmente usar `ripgrep` (`rg`) para buscar no texto.

Isso não usa Engram, mas atende “memória por projeto” com commit. E você pode manter Engram como evolução.

---

## 6) Integração com Copilot Agent Mode (prompt operacional)

No VS Code, crie um arquivo `./.engram/AGENT_MEMORY_POLICY.md` (commitável) e sempre mande o Copilot seguir. Por exemplo:

```
# Política de Memória do Projeto

## Antes de iniciar tarefas
- Consultar memórias existentes:
  - procurar em \`.engram/memory/\` por tags relevantes
  - se o MCP Engram estiver disponível, usar \`mem_search\` com 3-5 queries curtas
```

Isso dá governança.

---

## 7) Segurança e risco (principal motivo para NÃO commitar.db)

Mesmo que você “não queira sincronizar”, ao commitar você:

- replica para qualquer remoto do repo,
- replica para forks,
- replica para qualquer colaborador,
- e deixa rastros permanentes no histórico.

Por isso:

- commite **apenas texto revisável**
- adicione um checklist (“sem segredos”) antes de salvar memória

---

## 8) Próximo passo para fechar 100% (preciso de 1 confirmação)

Para te dar o comando exato de “rebuild/import” com Engram, eu preciso saber **quais comandos/flags o `engram` expõe**.

Você prefere:

1. Você roda e cola aqui a saída de:
	- `engram --help`
		- `engram mcp --help`
		- `engram mem --help` (se existir)
		- `engram import --help` (se existir)

**ou**

1. Você autoriza eu consultar o repositório `Gentleman-Programming/engram` via ferramentas (leitura) para eu localizar exatamente a API/CLI e te devolver scripts finalizados?

Diga “opção 1” ou “opção 2”. Se for opção 1, cole as saídas (pode ser sem formatação). Se for opção 2, eu faço uma varredura do código e te entrego a integração perfeita (incluindo paths e comandos reais).

vou adicionar esse documento no meu repositório de projeto default. nele será adaptado para utilizar o engram. obrigado pela informação e códigos extermamente uteis.

De nada. Para você adaptar no seu projeto “default” com o mínimo de risco, o checklist prático fica assim (ordem recomendada):

1. **Commitar política e formato da memória (texto)**
- `.engram/AGENT_MEMORY_POLICY.md`
- `.engram/memory/TEMPLATE.md`
1. **Ativar o MCP no workspace**
- `.vscode/mcp.json` apontando para o wrapper `.engram/scripts/engram_mcp.sh`
1. **Garantir persistência sem “DB binário no Git”**
- Commitar `.engram/memory/*.md`
- Ignorar `.engram/index/` no `.gitignore`
1. **Operação diária (Agent Mode)**
- Antes de começar: buscar memórias (via MCP ou lendo `.engram/memory/`)
- Ao terminar: salvar memória “curada” (sem segredos, com tags e passos reproduzíveis)

Se em algum momento você quiser fechar a adaptação “engram 100%” (import/rebuild automático do índice), me diga qual você prefere:

- você colar aqui os `--help` do `engram` (mais rápido, sem eu acessar nada), ou
- você me pedir explicitamente para eu inspecionar o repo `Gentleman-Programming/engram` (aí eu te devolvo os comandos reais e os scripts completos, já ajustados).

Quando você quiser, posso também te sugerir um conjunto de **tags padrão** por tipo de memória (arquitetura, build, deploy, debug, refactors, decisões) para melhorar a recuperação no FTS.