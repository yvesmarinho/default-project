# Exemplos de Merge JSON por Tipo de Arquivo

Exemplos práticos de como a estratégia **user-wins sem array union** funciona para diferentes tipos de arquivos JSON do projeto.

**Documentação principal**: [json-merge-strategy.md](json-merge-strategy.md)

---

## 📚 Índice

1. [.vscode/extensions.json](#vscodeextensionsjson)
2. [.vscode/mcp.json](#vscodemcpjson)
3. [.vscode/settings.json](#vscodesettingsjson)
4. [package.json](#packagejson)
5. [tsconfig.json](#tsconfigjson)
6. [.eslintrc.json](#eslintrcjson)

---

## .vscode/extensions.json

**Tipo**: Recomendações de extensões do VS Code  
**Arrays**: `recommendations`, `unwantedRecommendations`  
**Comportamento**: User-wins (substituição completa)

### Exemplo

#### Template (base)
```json
{
  "recommendations": [
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode"
  ]
}
```

#### Usuário (overlay)
```json
{
  "recommendations": [
    "GitHub.copilot",
    "GitHub.copilot-chat"
  ]
}
```

#### Resultado do Merge
```json
{
  "recommendations": [
    "GitHub.copilot",
    "GitHub.copilot-chat"
  ]
}
```

**Explicação**: Arrays são **substituídos completamente**. Usuário escolhe quais extensões quer, template não força nada.

---

## .vscode/mcp.json

**Tipo**: Configuração de servidores MCP  
**Arrays**: `mcpServers[].args`, `mcpServers[].env`  
**Comportamento**: User-wins (substituição completa)

### Exemplo

#### Template (base)
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/tmp"
      ]
    }
  }
}
```

#### Usuário (overlay)
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/home/user/projects"
      ]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"]
    }
  }
}
```

#### Resultado do Merge
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/home/user/projects"
      ]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"]
    }
  }
}
```

**Explicação**:
- Array `args` do filesystem **substituído** (não duplica `-y`)
- Servidor `github` **adicionado** (nova chave)
- Objetos aninhados mergeados recursivamente

---

## .vscode/settings.json

**Tipo**: Configurações do VS Code  
**Arrays**: `editor.rulers`, `files.exclude`, etc.  
**Comportamento**: User-wins (substituição completa)

### Exemplo

#### Template (base)
```json
{
  "editor.formatOnSave": true,
  "editor.rulers": [80, 120],
  "files.exclude": {
    "**/.git": true,
    "**/node_modules": true
  }
}
```

#### Usuário (overlay)
```json
{
  "editor.rulers": [100],
  "files.exclude": {
    "**/.git": true,
    "**/__pycache__": true
  },
  "python.linting.enabled": true
}
```

#### Resultado do Merge
```json
{
  "editor.formatOnSave": true,
  "editor.rulers": [100],
  "files.exclude": {
    "**/.git": true,
    "**/__pycache__": true
  },
  "python.linting.enabled": true
}
```

**Explicação**:
- `editor.rulers`: **substituído** por `[100]` (não faz `[80, 120, 100]`)
- `files.exclude`: merge de objetos (`.git` mantido, `__pycache__` adicionado, `node_modules` removido)
- Configurações novas adicionadas (`python.linting.enabled`)

---

## package.json

**Tipo**: Manifesto de projeto Node.js  
**Arrays**: `scripts`, `dependencies`, `devDependencies`  
**Comportamento**: User-wins (substituição completa)

### Exemplo

#### Template (base)
```json
{
  "name": "template-project",
  "version": "1.0.0",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "test": "jest"
  },
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.0.0"
  }
}
```

#### Usuário (overlay)
```json
{
  "name": "my-project",
  "scripts": {
    "dev": "next dev --turbo",
    "lint": "eslint ."
  },
  "dependencies": {
    "next": "^14.1.0",
    "axios": "^1.6.0"
  }
}
```

#### Resultado do Merge
```json
{
  "name": "my-project",
  "version": "1.0.0",
  "scripts": {
    "dev": "next dev --turbo",
    "lint": "eslint .",
    "build": "next build",
    "test": "jest"
  },
  "dependencies": {
    "next": "^14.1.0",
    "axios": "^1.6.0",
    "react": "^18.0.0"
  }
}
```

**Explicação**:
- `name`: user wins (sobrescreve)
- `scripts`: merge de objetos (user sobrescreve `dev`, adiciona `lint`, template adiciona `build` e `test`)
- `dependencies`: merge de objetos (user controla versões, template adiciona deps faltantes)

---

## tsconfig.json

**Tipo**: Configuração TypeScript  
**Arrays**: `compilerOptions.paths`, `include`, `exclude`  
**Comportamento**: User-wins (substituição completa)

### Exemplo

#### Template (base)
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules"]
}
```

#### Usuário (overlay)
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "paths": {
      "@/*": ["./app/*"],
      "@components/*": ["./app/components/*"]
    }
  },
  "include": ["app/**/*", "types/**/*"]
}
```

#### Resultado do Merge
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "paths": {
      "@/*": ["./app/*"],
      "@components/*": ["./app/components/*"]
    }
  },
  "include": ["app/**/*", "types/**/*"],
  "exclude": ["node_modules"]
}
```

**Explicação**:
- `compilerOptions.target`: user wins
- `compilerOptions.paths`: **substituído completamente** (não duplica `@/*`)
- `include`: **substituído completamente** (user define estrutura)
- `exclude`: template adiciona (user não definiu)

---

## .eslintrc.json

**Tipo**: Configuração ESLint  
**Arrays**: `extends`, `plugins`, `rules`  
**Comportamento**: User-wins (substituição completa)

### Exemplo

#### Template (base)
```json
{
  "extends": ["next/core-web-vitals", "prettier"],
  "plugins": ["@typescript-eslint"],
  "rules": {
    "no-console": "warn"
  }
}
```

#### Usuário (overlay)
```json
{
  "extends": ["next/core-web-vitals"],
  "rules": {
    "no-console": "error",
    "no-unused-vars": "error"
  }
}
```

#### Resultado do Merge
```json
{
  "extends": ["next/core-web-vitals"],
  "plugins": ["@typescript-eslint"],
  "rules": {
    "no-console": "error",
    "no-unused-vars": "error"
  }
}
```

**Explicação**:
- `extends`: **substituído** (user não quer `prettier`, não duplica)
- `plugins`: template adiciona (user não definiu)
- `rules`: merge de objetos (user controla regras)

---

## 🎯 Princípios Gerais

### Arrays
- **SEMPRE substituídos completamente**
- Razão: Arrays em configs são escolhas intencionais do usuário
- Evita duplicações, ordem errada, conflitos

### Objetos
- **Merge recursivo**
- User wins para chaves conflitantes
- Template adiciona chaves faltantes

### Primitivos
- **User wins**
- Usuário controla valores (versões, nomes, flags)

---

## 🔧 Ferramentas

### Validar merge antes de aplicar
```bash
# Comparar base vs overlay
python scripts/tmp/json_diff_visual.py template.json user.json
```

### Detectar duplicações
```bash
# Scan do projeto
python scripts/detect-json-duplications.py .

# Scan de arquivo específico
python scripts/detect-json-duplications.py .vscode/extensions.json
```

### Corrigir duplicações
```bash
# Fix automático
python scripts/tmp/fix-json-duplications.py .
```

---

## 📚 Referências

- [Estratégia de Merge JSON](json-merge-strategy.md) - Documentação completa
- [Debate Técnico](../debates/2026-05-17-json-merge-duplication-bug.md) - Análise do problema
- [Plano de Ação](../planning/2026-05-17-json-merge-fix-action-plan-v2.md) - Implementação

---

**Última atualização**: 2026-05-17  
**Status**: ✅ Implementado e validado
