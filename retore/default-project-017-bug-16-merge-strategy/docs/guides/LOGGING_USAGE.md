# Logging de Operações do Scaffold

## Resumo

O sistema de scaffold agora possui logging automático de todas as operações, salvando registros detalhados em arquivos de log para auditoria e debug.

## Funcionalidades

### 1. Logging Automático (Padrão)

Por padrão, **todas** as operações do scaffold salvam logs automaticamente:

```bash
# Criar novo projeto - log salvo em <projeto>/logs/scaffold_YYYY-MM-DD_HH-MM-SS.log
./scripts/scaffold.py new --ci --name my-project --domain programming

# Fazer upgrade - log salvo em <projeto>/logs/scaffold_YYYY-MM-DD_HH-MM-SS.log
./scripts/scaffold.py upgrade

# Gerar infra - log salvo em <projeto>/logs/scaffold_YYYY-MM-DD_HH-MM-SS.log
./scripts/scaffold.py infra

# Gerar rules - log salvo em <projeto>/logs/scaffold_YYYY-MM-DD_HH-MM-SS.log
./scripts/scaffold.py rules
```

### 2. Desabilitar Logging

Use `--no-log` para desabilitar o salvamento de logs:

```bash
./scripts/scaffold.py new --ci --name my-project --domain programming --no-log
```

### 3. Diretório de Log Customizado

Use `--log-dir` para especificar um diretório alternativo:

```bash
# Logs salvos em /tmp/scaffold-logs/
./scripts/scaffold.py new --ci --name my-project --domain programming --log-dir /tmp/scaffold-logs

# Logs salvos em ~/project-logs/
./scripts/scaffold.py upgrade --log-dir ~/project-logs
```

## Formato do Log

Cada arquivo de log contém:

### Header
```
# SCAFFOLD Operation Log
# Timestamp: 2026-02-27_14-30-45
# Project: my-project
# Total items: 42
```

### Estatísticas
```
## Statistics
- created: 38
- skipped: 3
- error: 1
```

### Detalhes de Itens
```
## Detailed Items

[CREATED] file | /path/to/project/.gitignore | Template default
[CREATED] file | /path/to/project/README.md | Project documentation
[SKIPPED] file | /path/to/project/.vscode/settings.json | Already exists
[ERROR] file | /path/to/project/invalid.txt | Permission denied
[OK] symlink | .copilot-rules.md -> /shared/.copilot-rules.md
```

## Saída na Tela

A saída na tela foi melhorada para **agrupar arquivos por pasta**:

```
╭─────────────────────────────────────────────────────────────────────╮
│                       📊 RESUMO DA OPERAÇÃO                          │
╰─────────────────────────────────────────────────────────────────────╯

┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┓
┃ Tipo      ┃ Arquivo                     ┃ Status    ┃ Mensagem           ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━┩
│           │ 📁 (root) — 4 arquivo(s)    │           │                    │
├───────────┼─────────────────────────────┼───────────┼────────────────────┤
│ file      │ .gitignore                  │ created   │ Template default   │
│ file      │ README.md                   │ created   │ Project docs       │
│ file      │ Makefile                    │ created   │ Build automation   │
│ file      │ pyproject.toml              │ created   │ Python deps        │
├───────────┼─────────────────────────────┼───────────┼────────────────────┤
│           │ 📁 .vscode — 3 arquivo(s)   │           │                    │
├───────────┼─────────────────────────────┼───────────┼────────────────────┤
│ file      │ settings.json               │ created   │ Merged config      │
│ file      │ mcp.json                    │ created   │ MCP servers        │
│ file      │ extensions.json             │ skipped   │ Already exists     │
└───────────┴─────────────────────────────┴───────────┴────────────────────┘

  38 criado(s) | 3 pulado(s) | 1 erro(s)
  Log salvo em: logs/scaffold_2026-02-27_14-30-45.log
```

## Benefícios

1. **Auditoria**: Histórico completo de todas as operações
2. **Debug**: Informações detalhadas para troubleshooting
3. **Visibilidade**: Saída agrupada facilita leitura
4. **Flexibilidade**: Controle via `--no-log` e `--log-dir`
5. **Transparência**: Usuário vê exatamente onde o log foi salvo

## Estrutura de Pastas

```
my-project/
├── logs/
│   ├── scaffold_2026-02-27_14-30-45.log  # Criação inicial
│   ├── scaffold_2026-03-01_10-15-30.log  # Upgrade
│   └── scaffold_2026-03-05_16-45-22.log  # Infra generation
├── .gitignore  # logs/ já está no .gitignore
└── ...
```

## Integração com Flows

Todos os flows principais foram atualizados:

- ✅ `flow_new_project` - Novo projeto
- ✅ `flow_upgrade` - Re-aplicação de template
- ✅ `flow_generate_infra` - Geração de CI/Docker
- ✅ `flow_generate_rules` - Geração de regras Copilot
- ❌ `flow_check_links` - Apenas verificação, sem logging (proposital)

## Exemplo de Uso Avançado

```bash
# Projeto com logging em diretório compartilhado
./scripts/scaffold.py new \
  --ci \
  --name my-api \
  --domain programming \
  --language python \
  --with-code-profile python-fastapi \
  --log-dir /shared/scaffold-logs

# Upgrade sem logging (CI/CD clean)
./scripts/scaffold.py upgrade --no-log

# Debug mode com logs detalhados
./scripts/scaffold.py upgrade --log-dir ./debug-logs
```

## Notas

- Logs são salvos em UTC timezone
- Formato de timestamp: `YYYY-MM-DD_HH-MM-SS`
- Diretório `logs/` é criado automaticamente
- Falhas no logging **não** interrompem a operação principal
- Log file path é sempre mostrado na saída final (exceto com `--no-log`)
