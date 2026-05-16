---
title: "VS Code MCP JSON error"
source: "https://github.com/copilot/c/7d3a5dbe-a6ef-4fff-b44e-3374207bc0d0"
author:
published:
created: 2026-05-11
description: "GitHub is where people build software. More than 150 million people use GitHub to discover, fork, and contribute to over 420 million projects."
tags:
  - "clippings"
---
no Code o servidor MCP memory apresento o erro no arquivo mcp.json, como resolvo. Unexpected non-whitespace character after JSON at position 127 (line 1 column 128)

Esse erro significa que o arquivo `mcp.json` está com **JSON inválido**: existe algum caractere extra depois do fim de um valor JSON válido, ou a estrutura foi escrita como se fosse JavaScript/JSONC, mas o parser espera **JSON puro**.

## O que o erro quer dizer

A mensagem:

> `Unexpected non-whitespace character after JSON at position 127 (line 1 column 128)`

normalmente indica um destes casos:

1. **Dois objetos JSON no mesmo arquivo**
	```
	{"a": 1}{"b": 2}
	```
2. **Vírgula sobrando no final**
	```
	{
	  "a": 1,
	}
	```
3. **Comentário em JSON**
	```
	{
	  // comentário
	  "a": 1
	}
	```
4. **Texto extra após fechar o objeto**
	```
	{
	  "a": 1
	} erro
	```
5. **Aspas erradas ou chave fechada cedo demais**

---

## Como corrigir

### 1\. Valide o arquivo

No Linux, rode:

```
python -m json.tool mcp.json
```

ou com `jq`:

```
jq . mcp.json
```

Se houver erro, ele aponta onde o JSON quebra.

---

### 2\. Verifique a posição exata

O parser informou:

- **position 127**
- **line 1 column 128**

Isso sugere fortemente que seu arquivo está **em uma única linha**. Então abra no `vi` e formate:

```
vi mcp.json
```

No `vi`, procure pela coluna aproximada ou reformate visualmente. Se estiver tudo numa linha, copie o conteúdo para um formatador JSON ou use:

```
python - <<'PY'
import json
from pathlib import Path

p = Path("mcp.json")
data = json.loads(p.read_text())
print(json.dumps(data, indent=2, ensure_ascii=False))
PY
```

Se falhar, o erro será reproduzido.

---

## Exemplo de JSON inválido e corrigido

### Inválido

```
{"mcpServers":{"memory":{"command":"npx","args":["-y","@modelcontextprotocol/server-memory"]}}},
```

O problema acima é a **vírgula extra no final**.

### Corrigido

```
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    }
  }
}
```

---

## Outro erro muito comum em mcp.json

### Inválido

```
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    }
  }
}
{
  "outro": true
}
```

Você tem **dois blocos JSON separados** no mesmo arquivo.

### Corrigido

Tudo deve estar dentro de **um único objeto raiz**:

```
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    }
  },
  "outro": true
}
```

---

## Se você estiver usando VS Code / Cursor / cliente MCP

Muitos arquivos `mcp.json` aceitam apenas **JSON puro**, então:

- **não use comentários** `//` ou `/* */`
- **não use vírgula final**
- **não duplique chaves no nível raiz**
- **não deixe texto fora do objeto JSON**

---

## Exemplo válido de mcp.json para memory

Um exemplo comum e válido é:

```
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-memory"
      ]
    }
  }
}
```

Se precisar de persistência/configuração extra, a estrutura depende do servidor, mas o formato JSON precisa continuar estritamente válido.

---

## Como diagnosticar rápido no Linux

### Com jq

```
jq . mcp.json
```

### Com Python

```
python -m json.tool mcp.json
```

### Mostrar caracteres estranhos

Às vezes há lixo invisível no arquivo:

```
cat -A mcp.json
```

ou:

```
sed -n '1p' mcp.json | fold -w 120
```

---

## No vi, como achar e corrigir

Se o conteúdo estiver em uma linha só:

1. abra:
	```
	vi mcp.json
	```
2. vá para o início:
	```
	gg
	```
3. tente identar com `%` para casar chaves e localizar fechamento incorreto
4. se quiser, cole o conteúdo em um formatador JSON externo ou use `jq`:
	```
	jq . mcp.json > /tmp/mcp.pretty.json
	```

Se `jq` falhar, o JSON está quebrado mesmo.

---

## Causa mais provável no seu caso

Como o erro é:

> `Unexpected non-whitespace character after JSON`

a **causa mais provável** é uma destas duas:

- **vírgula sobrando no final**
- **conteúdo extra depois do `}` final**

---

## O que fazer agora

Se quiser resolver objetivamente:

1. abra o `mcp.json`
2. remova qualquer:
	- comentário
		- vírgula final
		- bloco JSON duplicado
		- texto após a última `}`
3. valide com:
	```
	jq . mcp.json
	```

---

## Se quiser, eu posso ir direto ao ponto

Cole aqui o conteúdo exato do seu `mcp.json` e eu:

- identifico o erro na posição exata,
- devolvo a versão corrigida,
- e explico tecnicamente por que quebrou.

```
{
  "servers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"],
      "type": "stdio"
    },
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"],
      "type": "stdio"
    }
  }
}
```
esse é o conteudo do mcp.json, o Code não assinala erro no arquivo aberto. só o MCP server memory ve o erro. os comandos informados acima nenhum apresentou erro na validação.

O seu `mcp.json` **está sintaticamente válido como JSON**. O erro então **não é de JSON visível nesse trecho**, mas de uma destas situações:

1. o processo que lê o arquivo está recebendo **outro conteúdo além desse JSON**;
2. existe **BOM / caractere invisível / lixo no arquivo**;
3. o cliente MCP/Code está lendo **outro arquivo** ou uma versão antiga;
4. o erro não está no arquivo inteiro, mas em **algum campo que o servidor trata como JSON adicional**;
5. o parser do lado do `memory` está tentando interpretar **saída extra no stdout** como JSON.

Como você disse que:

- o editor **não marca erro**;
- `jq` / `python -m json.tool` **validam**;
- o erro aparece **no MCP server memory**,

a hipótese **mais forte** é:

> **o problema provavelmente não é o `mcp.json` em si, mas alguma saída extra misturada na comunicação stdio do servidor MCP**  
> ou então um **caractere invisível no arquivo** que os validadores comuns toleram/mostram de forma pouco evidente.

---

## Diagnóstico técnico

Seu arquivo:

```
{
  "servers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"],
      "type": "stdio"
    },
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"],
      "type": "stdio"
    }
  }
}
```

está correto como JSON puro.

Então o erro:

> `Unexpected non-whitespace character after JSON at position 127 (line 1 column 128)`

fica suspeito por dois motivos:

## 1\. A mensagem cita line 1

Seu JSON está formatado em múltiplas linhas. Se o parser reporta **line 1**, isso sugere que ele pode estar lendo:

- o conteúdo **minificado**;
- ou uma **string JSON serializada em linha única**;
- ou **não está lendo esse arquivo exatamente como você vê**.

## 2\. “after JSON”

Isso é típico quando o parser recebe algo assim:

```
{"jsonrpc":"2.0","id":1,"result":{...}}INFO extra
```

ou:

```
{"a":1}{"b":2}
```

ou:

```
{"a":1}\u0000
```

ou ainda:

```
{"a":1}npm notice ...
```

Isso acontece muito com integrações MCP via `stdio` quando algum processo escreve logs em **stdout**, e o cliente espera receber **apenas mensagens JSON-RPC**.

---

## Hipótese principal: problema no stdout do npx

Como você está usando:

```
"command": "npx",
"args": ["-y", "@modelcontextprotocol/server-memory"]
```

o `npx` pode, em alguns cenários, emitir mensagens extras como:

- `npm notice`
- `npm warn`
- progresso
- logs de instalação
- mensagens de cache
- output de diagnóstico

Se isso sair em **stdout** em vez de **stderr**, quebra o protocolo MCP, porque o cliente espera JSON limpo.

## Exemplo prático

O cliente espera algo como:

```
{"jsonrpc":"2.0","method":"initialize","params":{...}}
```

mas recebe:

```
npm warn exec The following package was not found and will be installed: @modelcontextprotocol/server-memory
{"jsonrpc":"2.0","method":"initialize","params":{...}}
```

A primeira linha já destrói o parser.

---

## Como confirmar isso

## Teste 1: rodar manualmente o comando

No terminal:

```
npx -y @modelcontextprotocol/server-memory
```

Veja se aparece qualquer saída como:

- warnings do npm
- notices
- mensagens informativas
- banner textual

Se aparecer algo no terminal **antes de qualquer handshake**, já é forte indício.

## Teste 2: separar stdout de stderr

Use:

```
npx -y @modelcontextprotocol/server-memory 1>/tmp/memory.stdout 2>/tmp/memory.stderr
```

Depois veja:

```
cat /tmp/memory.stdout
cat /tmp/memory.stderr
```

### Interpretação

- se `/tmp/memory.stdout` tiver texto não-JSON, esse é o problema;
- se somente `/tmp/memory.stderr` tiver warnings, normalmente tudo bem;
- se houver output em stdout como `npm notice`, a integração pode falhar.

---

## Outra hipótese forte: BOM ou caractere invisível no arquivo

Mesmo com JSON válido, pode existir:

- **UTF-8 BOM**
- `\r` inesperado
- caractere não imprimível
- lixo após o fechamento `}`

## Como verificar

### 1\. Mostrar bytes

```
xxd -g 1 -c 32 mcp.json | head
```

Se o arquivo começar com:

```
ef bb bf
```

isso é **BOM UTF-8**.

### 2\. Mostrar caracteres invisíveis

```
cat -A mcp.json
```

Procure por:

- `^M`
- caracteres estranhos
- símbolos após a última chave

### 3\. Ver tamanho real e fim do arquivo

```
tail -c 32 mcp.json | xxd -g 1
```

Isso ajuda a ver se existe lixo depois do `}`.

## Como remover BOM

```
sed -i '1s/^\xEF\xBB\xBF//' mcp.json
```

Ou regrave em UTF-8 sem BOM.

---

## Outra possibilidade: a chave esperada não é "servers"

Dependendo do cliente MCP, o campo esperado pode ser:

- `"mcpServers"`
- e não `"servers"`

Você mostrou:

```
{
  "servers": {
    ...
  }
}
```

Em vários clientes e exemplos, o formato mais comum é:

```
{
  "mcpServers": {
    ...
  }
}
```

## Importante

Isso **não geraria exatamente um erro de JSON parse** por si só.  
Geraria mais um erro de schema/configuração. Mas se o cliente pega esse campo, serializa ou mescla configs de forma interna, pode haver efeito colateral.

Então vale testar a troca.

### Versão recomendada

```
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-memory"
      ],
      "type": "stdio"
    },
    "sequential-thinking": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-sequential-thinking"
      ],
      "type": "stdio"
    }
  }
}
```

---

## Outra possibilidade: o “Code” está lendo outro arquivo

Como o editor não marca erro, mas o runtime acusa, confirme:

- qual é o caminho exato do `mcp.json`;
- se existe outro arquivo:
	- `~/.config/...`
		- workspace `.vscode/...`
		- config global do app
		- config do extension host

## Procure arquivos MCP no sistema

```
find ~ -type f \( -name "mcp.json" -o -name "*mcp*" \) 2>/dev/null
```

E também:

```
grep -R "\"server-memory\"" ~ 2>/dev/null
```

Pode haver uma cópia antiga sendo usada.

---

## Diagnóstico mais provável no seu caso real

Pelo padrão do erro e pelo fato do JSON validar, eu classificaria as causas por probabilidade:

## Mais provável

### 1\. npx emitindo texto extra no stdout

Principal suspeito.

## Muito provável

### 2\. cliente espera "mcpServers" e não "servers"

Vale corrigir imediatamente.

## Provável

### 3\. caractere invisível/BOM

Especialmente se o arquivo foi editado por ferramenta diferente.

## Possível

### 4\. outro arquivo sendo carregado

Muito comum em setups com config global + workspace.

---

## Correção recomendada em ordem prática

## Passo 1 — trocar servers por mcpServers

Teste este conteúdo exato:

```
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-memory"
      ],
      "type": "stdio"
    },
    "sequential-thinking": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-sequential-thinking"
      ],
      "type": "stdio"
    }
  }
}
```

---

## Passo 2 — regravar o arquivo sem BOM

No Linux:

```
cp mcp.json mcp.json.bak
python3 - <<'PY'
from pathlib import Path
import json

p = Path("mcp.json")
data = json.loads(p.read_text(encoding="utf-8-sig"))
p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("OK")
PY
```

Isso:

- lê suportando BOM;
- reserializa em JSON limpo;
- grava em UTF-8 normal.

---

## Passo 3 — testar se o npx cospe texto

```
npx -y @modelcontextprotocol/server-memory 1>/tmp/memory.stdout 2>/tmp/memory.stderr
```

Depois:

```
wc -c /tmp/memory.stdout /tmp/memory.stderr
sed -n '1,20p' /tmp/memory.stdout
sed -n '1,20p' /tmp/memory.stderr
```

Se houver mensagens não-JSON no `stdout`, achamos o problema.

---

## Passo 4 — instalar o pacote antes e evitar comportamento do npx

Muitas vezes o problema some quando você evita a instalação/resolução dinâmica do `npx`.

### Instale globalmente

```
npm install -g @modelcontextprotocol/server-memory @modelcontextprotocol/server-sequential-thinking
```

Depois use algo mais direto no config, por exemplo:

```
{
  "mcpServers": {
    "memory": {
      "command": "@modelcontextprotocol/server-memory",
      "type": "stdio"
    },
    "sequential-thinking": {
      "command": "@modelcontextprotocol/server-sequential-thinking",
      "type": "stdio"
    }
  }
}
```

## Se o binário não entrar no PATH

Descubra onde foi instalado:

```
npm root -g
npm bin -g
```

ou:

```
which server-memory
which @modelcontextprotocol/server-memory
```

Se necessário, aponte caminho absoluto do executável.

---

## Forma mais robusta para Linux avançado

Se você quer evitar `npx` em ambiente de editor/host MCP, eu recomendo:

1. instalar o servidor previamente;
2. usar **caminho absoluto** do executável;
3. manter stdout absolutamente limpo.

Exemplo conceitual:

```
{
  "mcpServers": {
    "memory": {
      "command": "/home/SEU_USUARIO/.npm-global/bin/server-memory",
      "type": "stdio"
    }
  }
}
```

O nome exato do binário depende do pacote instalado.

---

## Comandos de troubleshooting que eu executaria

## Ver bytes do arquivo

```
xxd -g 1 -c 32 mcp.json
```

## Validar JSON com leitura tolerante a BOM

```
python3 - <<'PY'
from pathlib import Path
import json

raw = Path("mcp.json").read_bytes()
print(raw[:8])
data = json.loads(raw.decode("utf-8-sig"))
print("json ok")
print(data.keys())
PY
```

## Ver se há caracteres após o fim

```
python3 - <<'PY'
from pathlib import Path
raw = Path("mcp.json").read_bytes()
print("len =", len(raw))
print("tail =", raw[-20:])
PY
```

## Capturar output do memory

```
npx -y @modelcontextprotocol/server-memory >/tmp/out.log 2>/tmp/err.log
```

## Inspecionar

```
sed -n '1,80p' /tmp/out.log
sed -n '1,80p' /tmp/err.log
```

---

## Minha recomendação objetiva

Faça nesta ordem:

1. **troque `"servers"` por `"mcpServers"`**;
2. **regrave o arquivo sem BOM**;
3. **pare de usar `npx` temporariamente** e teste com pacote previamente instalado;
4. **capture stdout/stderr** do `server-memory` para ver se há texto extra;
5. confirme se o Code está usando **esse arquivo exato**.

---

## Arquivo que eu sugiro testar primeiro

```
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-memory"
      ],
      "type": "stdio"
    },
    "sequential-thinking": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-sequential-thinking"
      ],
      "type": "stdio"
    }
  }
}
```

---

## Se ainda falhar

Aí o próximo alvo é quase certamente **stdout poluído** pelo `npx` ou pelo pacote.

Nesse caso, me mande o resultado destes comandos:

```
xxd -g 1 -c 32 mcp.json | head -n 5
cat -A mcp.json
npx -y @modelcontextprotocol/server-memory 1>/tmp/memory.stdout 2>/tmp/memory.stderr
sed -n '1,50p' /tmp/memory.stdout
sed -n '1,50p' /tmp/memory.stderr
```

e eu consigo te dizer com bastante precisão se o problema é:

- schema do config,
- encoding/BOM,
- stdout contaminado,
- ou binário MCP incompatível com o cliente.