---
title: "GitHub Copilot"
source: "https://github.com/copilot/c/a4bab3bd-4a46-4f94-a5b4-bdd7a4f416a5"
author:
published:
created: 2026-05-14
description: "GitHub is where people build software. More than 150 million people use GitHub to discover, fork, and contribute to over 420 million projects."
tags:
  - "clippings"
---
Para **iniciar automaticamente os servidores MCP ao abrir o workspace no VS Code**, o caminho principal é:

1. definir os servidores no arquivo **`.vscode/mcp.json`** do projeto;
2. habilitar a configuração **`chat.mcp.autostart`** no escopo do workspace;
3. garantir que o workspace esteja **trusted** e que você já tenha **confirmado trust** para esses servidores quando solicitado pela primeira vez. ([code.visualstudio.com](https://code.visualstudio.com/docs/copilot/customization/mcp-servers?featured_on=talkpython&utm_source=openai))

## Resposta curta

No seu workspace, configure algo como:

```json
{
  "chat.mcp.autostart": true
}
```

e mantenha seus servidores em:

```json
{
  "servers": {
    "meu-servidor": {
      "command": "python",
      "args": ["server.py"]
    }
  }
}
```

Depois disso, ao abrir o workspace, o VS Code pode iniciar automaticamente os servidores MCP configurados, desde que a confiança do workspace/servidor já tenha sido concedida. ([code.visualstudio.com](https://code.visualstudio.com/docs/copilot/customization/mcp-servers?featured_on=talkpython&utm_source=openai))

---

## O que exatamente controla o autostart

A documentação mais recente do VS Code indica a configuração **`chat.mcp.autostart`** como a responsável pelo comportamento de autostart dos servidores MCP. O release notes do VS Code 1.103 descreve que antes era necessário refresh manual, e que agora o autostart pode ser configurado por essa setting. ([code.visualstudio.com](https://code.visualstudio.com/updates/v1_103?utm_source=openai))

Há um detalhe importante: a documentação de “Add and manage MCP servers” e a de “MCP configuration reference” descrevem isso como **experimental** e associam a setting ao comportamento de iniciar/reiniciar servidores quando mudanças de configuração são detectadas. Na prática, essa é a configuração oficial hoje para evitar ter de subir manualmente os MCP servers no workspace. ([code.visualstudio.com](https://code.visualstudio.com/docs/copilot/customization/mcp-servers?featured_on=talkpython&utm_source=openai))

---

## Estrutura recomendada no workspace

### 1) Arquivo.vscode/mcp.json

É nele que você declara os servidores MCP no escopo do projeto/workspace. O VS Code reconhece esse arquivo como a configuração de MCP do workspace. ([code.visualstudio.com](https://code.visualstudio.com/api/extension-guides/mcp?utm_source=openai))

Exemplo mínimo:

```json
{
  "servers": {
    "filesystem-tools": {
      "command": "node",
      "args": ["./tools/mcp/filesystem-server.js"]
    },
    "python-tools": {
      "command": "python3",
      "args": ["./tools/mcp/server.py"]
    }
  }
}
```

### 2) Arquivo.vscode/settings.json

Defina o autostart no escopo do workspace:

```json
{
  "chat.mcp.autostart": true
}
```

A documentação de settings do VS Code confirma que configurações em `.vscode/settings.json` são **workspace settings**, válidas especificamente quando aquele workspace é aberto. ([code.visualstudio.com](https://code.visualstudio.com/docs/getstarted/settings?force_isolation=true&utm_source=openai))

---

## Passo a passo prático

### Opção A — via arquivos do projeto

Crie:

```
seu-projeto/
└── .vscode/
    ├── mcp.json
    └── settings.json
```

Conteúdo de `settings.json`:

```json
{
  "chat.mcp.autostart": true
}
```

Conteúdo de `mcp.json`:

```json
{
  "servers": {
    "meu-mcp": {
      "command": "uvx",
      "args": ["meu-servidor-mcp"]
    }
  }
}
```

Abra o workspace. Na primeira vez que o servidor for iniciado após ser adicionado ou alterado, o VS Code pode pedir confirmação de confiança para o servidor. Sem essa confiança, ele não será iniciado. ([code.visualstudio.com](https://code.visualstudio.com/docs/copilot/customization/mcp-servers?featured_on=talkpython&utm_source=openai))

---

## Sobre trust: esse é o ponto que normalmente “quebra” o autostart

Mesmo com `chat.mcp.autostart` habilitado, o VS Code trata servidores MCP com cuidado por razões de segurança. A documentação informa que:

- ao adicionar ou alterar um MCP server no workspace, você precisa confirmar que **confia** nele;
- se não confiar, o servidor **não inicia**;
- isso é ainda mais importante com autostart ativo. ([code.visualstudio.com](https://code.visualstudio.com/docs/copilot/customization/mcp-servers?featured_on=talkpython&utm_source=openai))

Além disso, se o workspace estiver em **Restricted Mode** / sem confiança, vários recursos que executam código ou comandos ficam limitados. O modelo geral de Workspace Trust do VS Code impacta esse comportamento. ([code.visualstudio.com](https://code.visualstudio.com/docs/editing/workspaces/workspace-trust?utm_source=openai))

### Em termos práticos

Se “não está iniciando sozinho”, verifique nesta ordem:

1. o workspace está aberto como pasta/workspace real;
2. existe `.vscode/mcp.json`;
3. existe `.vscode/settings.json` com `chat.mcp.autostart`;
4. o workspace é confiável;
5. você já aceitou o trust do servidor MCP;
6. o binário/comando configurado existe no ambiente do VS Code. ([code.visualstudio.com](https://code.visualstudio.com/docs/editing/workspaces/workspaces?utm_source=openai))

---

## Como verificar se o servidor foi detectado

O próprio VS Code documenta formas de gerenciar e inspecionar servidores MCP:

- abrir o arquivo `.vscode/mcp.json`;
- usar os comandos para **start/stop/restart**;
- usar **MCP: List Servers**;
- ver logs em **Show Output** quando houver erro. ([code.visualstudio.com](https://code.visualstudio.com/api/extension-guides/mcp?utm_source=openai))

Então, para diagnosticar:

1. `Ctrl+Shift+P`
2. execute **`MCP: List Servers`**
3. selecione o servidor
4. veja status e **Show Output** se houver falha. ([code.visualstudio.com](https://code.visualstudio.com/docs/copilot/customization/mcp-servers?featured_on=talkpython&utm_source=openai))

---

## Exemplo mais realista para ambiente Linux

Como você é usuário avançado de Linux, provavelmente vale preferir caminhos previsíveis, wrappers simples e evitar dependência implícita de shell interativo.

Exemplo:

```json
{
  "servers": {
    "local-python-mcp": {
      "command": "/usr/bin/python3",
      "args": [
        "/home/voce/projetos/app/.tools/mcp/server.py"
      ]
    },
    "node-mcp": {
      "command": "/usr/bin/node",
      "args": [
        "/home/voce/projetos/app/.tools/mcp/index.js"
      ]
    }
  }
}
```

### Por que isso ajuda?

No VS Code, especialmente em Linux, o ambiente de execução do app pode não refletir exatamente seu shell do `bash` / `zsh` / `fish`. Então usar caminhos absolutos reduz erro de `PATH`, `pyenv`, `nvm`, `uv`, `poetry`, etc. Isso é uma inferência prática de operação, não uma citação literal da documentação. A parte documentada é que o VS Code executa os servidores a partir da configuração MCP; portanto, a robustez da resolução do comando depende do ambiente disponível ao VS Code. ([code.visualstudio.com](https://code.visualstudio.com/api/extension-guides/mcp?utm_source=openai))

---

## Se você usa.code-workspace

Se em vez de abrir uma pasta você usa um arquivo `.code-workspace`, as **workspace settings** continuam sendo o local correto para a configuração de autostart, porque o VS Code suporta configurações específicas por workspace e restaura esse contexto ao abrir o workspace. ([code.visualstudio.com](https://code.visualstudio.com/docs/editing/workspaces/workspaces?utm_source=openai))

Nesse caso, você pode colocar a setting no próprio arquivo `.code-workspace`:

```json
{
  "folders": [
    { "path": "." }
  ],
  "settings": {
    "chat.mcp.autostart": true
  }
}
```

E manter o `.vscode/mcp.json` na raiz do projeto, se esse for o modelo usado no seu setup. A documentação oficial enfatiza `.vscode/mcp.json` como configuração de workspace para MCP servers. ([code.visualstudio.com](https://code.visualstudio.com/docs/copilot/customization/mcp-servers?featured_on=talkpython&utm_source=openai))

---

## Diferença entre “workspace MCP servers” e “plugin MCP servers”

A documentação recente também distingue **plugin MCP servers**, que iniciam automaticamente quando o plugin é habilitado, dos **workspace MCP servers**, que seguem o fluxo de trust/autostart/configuração do workspace. Se o seu caso é “ao abrir um projeto”, você está falando do segundo modelo: **workspace MCP servers**. ([code.visualstudio.com](https://code.visualstudio.com/docs/copilot/customization/agent-plugins?utm_source=openai))

---

## Melhor prática operacional

Eu recomendo este conjunto:

### .vscode/settings.json

```json
{
  "chat.mcp.autostart": true
}
```

### .vscode/mcp.json

```json
{
  "folders": [
    { "path": "." }
  ],
  "settings": {
    "chat.mcp.autostart": true
  }
}
```

### Checklist

- abra o projeto como workspace;
- confirme **Workspace Trust**;
- confirme trust do servidor MCP na primeira execução;
- valide no **MCP: List Servers**;
- se falhar, abra **Show Output**. ([code.visualstudio.com](https://code.visualstudio.com/docs/copilot/customization/mcp-servers?featured_on=talkpython&utm_source=openai))

---

## Resposta objetiva à sua pergunta

**Sim: para iniciar automaticamente os servidores MCP quando o workspace abrir, use `chat.mcp.autostart` nas configurações do workspace e defina os servidores em `.vscode/mcp.json`.** O autostart só funciona de forma efetiva se o workspace e os servidores forem confiáveis/trusted. ([code.visualstudio.com](https://code.visualstudio.com/docs/copilot/customization/mcp-servers?featured_on=talkpython&utm_source=openai))

Se você quiser, eu posso te entregar agora um **exemplo completo e pronto** de:

1. `.vscode/mcp.json`
2. `.vscode/settings.json`
3. um wrapper shell para Linux
4. e uma versão pensada para abrir no VS Code via `code .` usando `vi` no fluxo de terminal.