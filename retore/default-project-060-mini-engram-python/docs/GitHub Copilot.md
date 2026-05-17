---
title: "Code Flask8 error - solution"
source: "https://github.com/copilot/c/7aaaf543-22d8-4254-930a-cabe8297ac7e"
created: 2026-05-06
---
```
Linting failed with error:
Traceback (most recent call last):
  File "/home/yves_marinho/.vscode/extensions/ms-python.flake8-2026.5.11251004/bundled/libs/flake8/plugins/reporter.py", line 34, in make
    format_plugin = reporters[format_name]
                    ~~~~~~~~~^^^^^^^^^^^^^
KeyError: "'%(row)d,%(col)d,%(code).1s,%(code)s:%(text)s'"

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/yves_marinho/.vscode/extensions/ms-python.flake8-2026.5.11251004/bundled/tool/lsp_server.py", line 330, in _linting_helper
    result = _run_tool_on_document(document, use_stdin=False)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/yves_marinho/.vscode/extensions/ms-python.flake8-2026.5.11251004/bundled/tool/lsp_server.py", line 757, in _run_tool_on_document
    return tool_server.execute_tool(
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/yves_marinho/.vscode/extensions/ms-python.flake8-2026.5.11251004/bundled/libs/vscode_common_python_lsp/server.py", line 373, in execute_tool
    result = run_module(
             ^^^^^^^^^^^
  File "/home/yves_marinho/.vscode/extensions/ms-python.flake8-2026.5.11251004/bundled/libs/vscode_common_python_lsp/runner.py", line 91, in run_module
    runpy.run_module(module, run_name="__main__")
  File "<frozen runpy>", line 229, in run_module
  File "<frozen runpy>", line 88, in _run_code
  File "/home/yves_marinho/.vscode/extensions/ms-python.flake8-2026.5.11251004/bundled/libs/flake8/__main__.py", line 7, in <module>
    raise SystemExit(main())
                     ^^^^^^
  File "/home/yves_marinho/.vscode/extensions/ms-python.flake8-2026.5.11251004/bundled/libs/flake8/main/cli.py", line 23, in main
    app.run(argv)
  File "/home/yves_marinho/.vscode/extensions/ms-python.flake8-2026.5.11251004/bundled/libs/flake8/main/application.py", line 198, in run
    self._run(argv)
  File "/home/yves_marinho/.vscode/extensions/ms-python.flake8-2026.5.11251004/bundled/libs/flake8/main/application.py", line 186, in _run
    self.initialize(argv)
  File "/home/yves_marinho/.vscode/extensions/ms-python.flake8-2026.5.11251004/bundled/libs/flake8/main/application.py", line 172, in initialize
    self.make_formatter()
  File "/home/yves_marinho/.vscode/extensions/ms-python.flake8-2026.5.11251004/bundled/libs/flake8/main/application.py", line 72, in make_formatter
    self.formatter = reporter.make(self.plugins.reporters, self.options)
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/yves_marinho/.vscode/extensions/ms-python.flake8-2026.5.11251004/bundled/libs/flake8/plugins/reporter.py", line 40, in make
    format_plugin = reporters["default"]
                    ~~~~~~~~~^^^^^^^^^^^
KeyError: 'default'
```
Corria o erro acima que está ocorrendo contantemente no code 1.118.1

O seu erro **não é do seu código Python**: é uma falha de configuração/compatibilidade do **Flake8 “embutido” na extensão `ms-python.flake8` do VS Code** (no seu caso, `ms-python.flake8-2026.5.11251004`) ao tentar montar o **formatter/reporter**. O traceback mostra dois sintomas-chave:

1. Ele tenta buscar um “format plugin” pelo nome:
- `format_name = "'%(row)d,%(col)d,%(code).1s,%(code)s:%(text)s'"`
- e faz `reporters[format_name]` ⇒ **KeyError**
2. Ao cair no fallback, tenta usar `reporters["default"]` ⇒ **KeyError: 'default'**

Isso indica que o Flake8 que está rodando **não tem registrado** os reporters esperados, ou está sendo invocado com uma opção que **não corresponde a um reporter válido** (ex.: `--format` / `format` com uma *string* de template, quando a versão/empacotamento espera um *nome* de plugin), e ainda por cima o bundle está sem “default reporter” (ou o registro falhou).

A correção prática é: **parar de depender do Flake8 embutido da extensão** e/ou **ajustar a configuração de formato** para algo suportado, garantindo que exista um reporter válido.

Abaixo vão correções efetivas (em ordem de recomendação), com passos objetivos para VS Code 1.118.1.

---

## 1) Correção mais estável (recomendada): usar Flake8 do seu ambiente (venv/pipx) e não o “bundled”

### 1.1. Instale/garanta flake8 no seu ambiente

Exemplos (escolha um):

**A) venv do projeto**

```
python -m venv .venv
. .venv/bin/activate
python -m pip install -U pip
python -m pip install -U flake8
flake8 --version
```

**B) pipx (global, isolado)**

```
pipx install flake8
pipx run flake8 --version
```

### 1.2. Configure o VS Code para usar o executável do ambiente

No `.vscode/settings.json` do workspace (recomendado), configure para apontar para o binário do seu ambiente.

Exemplo com venv local `.venv` em Linux:

```
{
  // Garanta que o Python do workspace é o da venv (isso já ajuda outras extensões)
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",

  // Para a extensão de flake8: a chave exata pode variar por versão,
  // mas normalmente existe opção para o caminho do executável.
  // Se não existir, a alternativa é desabilitar linting flake8 da extensão e usar outro linter (ruff).
  "flake8.path": ["${workspaceFolder}/.venv/bin/flake8"],

  // Evite formatos customizados até estabilizar
  "flake8.args": []
}
```

> Observação técnica: a extensão `ms-python.flake8` mudou várias vezes as chaves (`flake8.path`, `python.linting.flake8Path`, etc.) conforme a geração do sistema de lint. Se o VS Code reclamar que a configuração é “unknown”, vá em:

- `Ctrl+Shift+P` → **Preferences: Open Settings (JSON)**
- procure por “flake8” no UI settings para achar o nome exato aceito pela sua versão.

### 1.3. (Opcional) Desabilitar o flake8 “bundled” e usar só o seu

Se a extensão permitir, prefira “usar flake8 do ambiente”. Se não houver toggle, a abordagem mais simples é **desinstalar** a extensão `ms-python.flake8` e usar **ruff** (ver seção 4).

---

## 2) Correção direta do erro atual: remover o format/--format customizado

O seu `format_name` no erro é:

`'%(row)d,%(col)d,%(code).1s,%(code)s:%(text)s'`

Isso parece uma string de template (estilo “pycodestyle format”), mas o Flake8 moderno normalmente espera `--format` com **nome de formatador** (ex.: `default`, `pylint`, `quiet-filename`, etc.) *ou* uma configuração que exista de fato. No bundle da extensão, o registro de reporters está quebrando, então qualquer customização tende a expor o bug.

### 2.1. Procure onde isso está definido

Cheque estas fontes (nessa ordem):

1. **Workspace**: `.vscode/settings.json`
2. **User settings**: `~/.config/Code/User/settings.json` (ou equivalente no seu sistema)
3. Config do flake8: `.flake8`, `setup.cfg`, `tox.ini`, `pyproject.toml`

Procure por:

- `format =`
- `--format`
- `flake8.args`
- `--output-file` (às vezes vem junto)
- `--format=%(row)d...`

### 2.2. Ajuste para algo “default” (ou simplesmente remova)

Em `.flake8` (exemplo), deixe assim:

```
[flake8]
# NÃO defina format por enquanto
max-line-length = 88
extend-ignore = E203,W503
```

Se você **precisa** de um formato parseável, use algo reconhecido. Exemplos possíveis (dependem da versão), mas em geral o mais seguro é **não setar** e deixar padrão.

---

## 3) Workaround específico para o VS Code: desabilitar apenas o linting do Flake8 (sem desinstalar)

Se o seu fluxo está travando toda hora, o workaround operacional:

No settings do VS Code, desabilite o flake8 como provider de lint. Dependendo da versão do seu stack Python no VS Code, pode ser algo como:

- desabilitar a extensão `ms-python.flake8`, ou
- setar algo como “linting enabled: false” para flake8.

Como a Microsoft vem migrando o linting para extensões separadas, a forma mais confiável é:

- **Extensions** → procure `Flake8` → **Disable (Workspace)**

Isso elimina o erro constante e te permite usar CLI (no terminal) enquanto corrige o setup.

---

## 4) Alternativa moderna (e melhor no VS Code hoje): trocar para Ruff

O Ruff substitui Flake8 + vários plugins com performance superior e integração muito boa no VS Code.

### 4.1. Instalar Ruff

```
python -m pip install -U ruff
ruff --version
```

### 4.2. Configurar pyproject.toml

```
[tool.ruff]
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "W", "I"]  # estilo flake8 básico
```

### 4.3. No VS Code

- Instale a extensão **Ruff** (oficial).
- Desabilite a extensão `ms-python.flake8` (para evitar conflito).

---

## 5) Diagnóstico rápido (para cravar a causa) via terminal

Execute estes comandos no terminal embutido do VS Code (no mesmo ambiente do editor):

```
which python
python -V
which flake8 || true
flake8 --version || true
python -c "import flake8; import flake8.plugins.reporter as r; print('flake8', flake8.__version__); print('reporter', r.__file__)"
```

Se o `reporter.py` apontar para o caminho da extensão: `.../.vscode/extensions/ms-python.flake8-.../bundled/libs/...` você confirmou que está usando o **bundle**.

---

## 6) O que eu preciso de você para fechar 100% a correção (sem adivinhação)

Cole aqui (pode mascarar paths sensíveis, mas preserve as chaves/valores):

1. Conteúdo de:
- `.vscode/settings.json` (do workspace)
- `~/.config/Code/User/settings.json` (somente as linhas relacionadas a python/flake8)
2. Se existir, conteúdo de um destes:
- `.flake8` **ou** `setup.cfg` **ou** `tox.ini` **ou** `pyproject.toml` (seção de flake8)
3. Saída de:

```
python -c "import sys; print(sys.executable)"
python -c "import flake8, flake8.plugins.reporter as r; print(flake8.__version__); print(r.__file__)"
```

Com isso eu te digo exatamente **qual configuração está injetando esse `format`**, e qual chave do VS Code você deve ajustar na sua versão.

---

### Resumo objetivo do fix

- **Remova qualquer `format` / `--format` customizado** que esteja igual ao template `'%(row)d,%(col)d,...'`.
- Preferencialmente, **use flake8 instalado no seu ambiente** e aponte o VS Code para ele.
- Se quiser eliminar a classe inteira de problemas: **migre para Ruff** e desabilite a extensão do Flake8.

```
"python-envs.pythonProjects": [
    {
        "path": ".",
        "envManager": "ms-python.python:venv",
        "packageManager": "ms-python.python:pip"
    }
],
```
como altero a configuração abaixo para usar o uv?

Para usar **uv** nesse bloco `python-envs.pythonProjects`, você precisa trocar o `packageManager` de `ms-python.python:pip` para o identificador do **uv** (e, opcionalmente, manter o `envManager` como `venv`, porque o uv pode tanto **criar venv** quanto **instalar pacotes** dentro dela).

A configuração fica assim:

```
"python-envs.pythonProjects": [
  {
    "path": ".",
    "envManager": "ms-python.python:venv",
    "packageManager": "astral-sh.uv:uv"
  }
]
```

## Observações importantes (para não quebrar)

1. O valor `"astral-sh.uv:uv"` **só funciona** se você tiver a extensão do uv instalada no VS Code (geralmente chamada **“uv”** e publicada pela Astral).
2. Se o VS Code não reconhecer esse `packageManager`, ele normalmente:
- ignora silenciosamente, ou
- marca como inválido, dependendo da versão.

## Como validar no seu ambiente (rápido, no Linux)

No terminal:

```
uv --version
which uv
```

Se não existir, instale (exemplos comuns):

```
# via script oficial (recomendado pela Astral)
curl -LsSf https://astral.sh/uv/install.sh | sh

# ou via pipx
pipx install uv
```

## Se você quer que o uv gerencie também o ambiente (não só pacotes)

Em alguns fluxos, você pode preferir que o uv seja responsável por criar/sincronizar o ambiente (em vez do `ms-python.python:venv`). Dependendo do que a extensão `python-envs` aceita na sua versão, pode existir um `envManager` para uv. Se existir, ficaria algo como:

```
{
  "path": ".",
  "envManager": "astral-sh.uv:uv",
  "packageManager": "astral-sh.uv:uv"
}
```

Mas isso **depende 100%** de a sua instalação do VS Code + extensões reconhecerem esse provider para `envManager`.

## Para eu te dar o valor exato (sem chute)

Me diga:

1. qual extensão você instalou para uv (nome exato / publisher) e
2. cole o trecho do `settings.json` onde aparece `python-envs` completo (ou um print).

Com isso eu confirmo se o provider correto é `astral-sh.uv:uv` mesmo, ou outro identificador (algumas versões usam IDs diferentes).

settings.json

Cole aqui o conteúdo do seu `settings.json` (pode ser o do **Workspace**: `.vscode/settings.json` e/ou o **User**). Sem ele não dá para eu dizer exatamente qual chave/ID o seu VS Code está aceitando para `python-envs.pythonProjects`.

Para ficar objetivo, cole **pelo menos** estas partes:

1. Todo bloco que começa com:
- `"python-envs.pythonProjects": ...`
2. Qualquer configuração relacionada a Python/venv/uv, por exemplo chaves que contenham:
- `python.`
- `venv`
- `pip`
- `uv`
- `flake8`
- `lint`

Se quiser pelo terminal (Linux/vi), pode fazer:

```
# workspace
sed -n '1,200p' .vscode/settings.json 2>/dev/null || true

# user (caminho típico do VS Code no Linux)
sed -n '1,260p' ~/.config/Code/User/settings.json 2>/dev/null || true
```

Depois que você colar, eu te devolvo:

- a edição exata do JSON para usar `uv`,
- e como validar que o provider foi realmente aplicado (log/saída/commands no VS Code).

```
{
    "files.associations": {
        "*.yaml": "yaml",
        "*.yml": "yaml",
        "mcp.json": "jsonc"
    },
    "yaml.schemas": {},
    "files.exclude": {
        "**/node_modules": true,
        "**/.git": true,
        "**/.mcp-status": true
    },
    "search.exclude": {
        "**/node_modules": true,
        "**/.git": true
    },
    "editor.rulers": [
        80,
        120
    ],
    "editor.tabSize": 2,
    "editor.insertSpaces": true,
    "files.trimTrailingWhitespace": true,
    "files.insertFinalNewline": true,
    "editor.formatOnSave": true,
    "aiAssistant.projectContext": ".vscode/mcp.json",
    "aiAssistant.followProjectConventions": true,
    "chat.promptFilesRecommendations": {
        "speckit.constitution": true,
        "speckit.specify": true,
        "speckit.clarify": true,
        "speckit.plan": true,
        "speckit.checklist": true,
        "speckit.tasks": true,
        "speckit.analyze": true,
        "speckit.implement": true
    },
    "chat.tools.terminal.autoApprove": {
        ".specify/scripts/bash/": true,
        ".specify/scripts/powershell/": true
    },
    "python-envs.pythonProjects": [
        {
            "path": ".",
            "envManager": "astral-sh.uv:uv",
            "packageManager": "astral-sh.uv:uv"
        }
    ],
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
    "flake8.path": [
        "${workspaceFolder}/.venv/bin/flake8"
    ],
    "flake8.args": []
}
```
esse é o settings.json completo.

A sua configuração **já está apontando para o uv** corretamente **dentro do schema do `python-envs`**:

```
"python-envs.pythonProjects": [
  {
    "path": ".",
    "envManager": "astral-sh.uv:uv",
    "packageManager": "astral-sh.uv:uv"
  }
]
```

Então a pergunta “como altero para usar uv?”: **você já alterou**.

O que normalmente falta (e é onde as pessoas travam) é: **isso não cria/atualiza a `.venv` automaticamente** a menos que:

1. a extensão/provider `astral-sh.uv` esteja instalada e ativa, e
2. você esteja usando os comandos corretos (ou tenha arquivo de projeto do uv para o provider saber o que fazer).

Abaixo está o checklist técnico para garantir que *de fato* está usando uv e não pip/venv “antigos”.

---

## 1) Verifique se o provider astral-sh.uv:uv existe mesmo no seu VS Code

Sem isso, o `python-envs` pode simplesmente ignorar o provider e cair em fallback.

### 1.1. Confirme extensão instalada

No VS Code:

- `Ctrl+Shift+X` → procure por **uv**
- você precisa de uma extensão cujo **publisher** seja **astral-sh** (ou Astral) e que exponha o provider `astral-sh.uv`.

### 1.2. Verifique no Output/Logs

- `Ctrl+Shift+U` → “Output”
- no dropdown, procure algo como:
	- **Python Environments**
		- **Python**
		- **uv**
- Recarregue a janela: `Ctrl+Shift+P` → **Developer: Reload Window**
- veja se aparece log dizendo que reconheceu `astral-sh.uv:uv`.

Se não aparece nada, suspeita forte: provider não está carregando, e o bloco fica “decorativo”.

---

## 2) Sua linha python.defaultInterpreterPath ainda força.venv/bin/python

Você setou:

```
"python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python"
```

Isso é OK, **desde que** a `.venv` seja realmente a do uv. Caso contrário, você pode acabar com:

- `python` apontando para uma venv antiga/criada manualmente
- `python-envs` tentando gerenciar outra coisa

Recomendação prática:

### Opção A (mais previsível): manter.venv e fazer uv gerenciá-la

Fica como está, mas você precisa garantir que a `.venv` foi criada pelo uv:

No terminal do projeto:

```
# 1) cria/garante a venv em .venv
uv venv .venv

# 2) instala dependências (ver seção 3)
```

### Opção B (mais “automática”): não fixar o interpreter path

Se você remover `python.defaultInterpreterPath`, o VS Code tende a selecionar a venv descoberta. Mas isso depende do seu setup/heurística, então para ambiente avançado eu geralmente prefiro a Opção A.

---

## 3) Para uv funcionar bem, você precisa de “fonte de dependências”

O uv trabalha muito bem com **`pyproject.toml`** (recomendado) e também pode sincronizar lock.

### 3.1. Setup típico com pyproject.toml

Exemplo mínimo:

```
[project]
name = "meu-projeto"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
  "flake8>=7.0.0",
]
```

E então:

```
uv venv .venv
uv pip install -r requirements.txt   # se você ainda usa requirements
# ou (preferível) se estiver usando pyproject:
uv sync                              # se você tiver lock/config do uv
# ou:
uv pip install -e .                  # instala o projeto e deps do pyproject (quando aplicável)
```

Sem `pyproject.toml` /requirements, o provider do editor pode não ter “o que instalar”.

---

## 4) Ajuste recomendado no seu settings.json (pequena melhoria)

Hoje você está assim:

```
"flake8.path": ["${workspaceFolder}/.venv/bin/flake8"]
```

Isso é bom, mas para evitar qualquer chance do VS Code cair no flake8 “bundled”, eu sugiro:

1. Garantir que o flake8 está na `.venv` gerenciada pelo uv:

```
uv pip install flake8
```

2. (Opcional) adicionar um `flake8.args` mínimo e não mexer com `--format`:

```
"flake8.args": [
  "--config",
  "${workspaceFolder}/.flake8"
]
```

E criar `.flake8` com configurações simples (sem `format=`).

---

## 5) Comandos de verificação (Linux) para confirmar que está tudo coerente

Rode dentro do workspace:

```
# Confirma uv disponível
command -v uv && uv --version

# Confirma python/flake8 dentro da .venv
ls -l .venv/bin/python .venv/bin/flake8 2>/dev/null || true

# Confirma versão de flake8 e de onde está sendo importado
. .venv/bin/activate
python -c "import sys; print(sys.executable)"
flake8 --version
python -c "import flake8, flake8.plugins.reporter as r; print(flake8.__version__); print(r.__file__)"
```

Se `r.__file__` apontar para `.venv/...` (e não para `.vscode/extensions/...`), você eliminou o bug do bundle.

---

## 6) Se ainda não estiver funcionando: o que eu preciso para fechar

Se, mesmo com isso, o VS Code continuar tentando usar pip/bundled flake8, me diga:

1. Qual é a extensão do uv instalada (nome/publisher/versão).
2. Saída do comando:

```
code --list-extensions --show-versions | grep -i uv
code --list-extensions --show-versions | grep -i python
```

Aí eu te digo exatamente se o `python-envs` que você está usando suporta `astral-sh.uv:uv` como `envManager` de verdade ou só como `packageManager`, e qual o fallback correto na sua versão.

code funciona muito bem. obrigado

De nada. Se voltar a aparecer aquele erro do Flake8 no VS Code, o caminho mais “à prova de bala” é exatamente o que você já fez: garantir que o editor use o `flake8` instalado na `.venv` (gerenciada pelo `uv`) e evitar `--format` customizado.

Se quiser, em outra mensagem você pode colar a saída de:

```
. .venv/bin/activate
python -c "import flake8, flake8.plugins.reporter as r; print(flake8.__version__); print(r.__file__)"
```

e eu confirmo se ele está 100% fora do bundle da extensão.
