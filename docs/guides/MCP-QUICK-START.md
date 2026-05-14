# 🚀 Como Ativar Servidores MCP (Primeira Vez)

**Problema**: Servidores MCP não iniciam automaticamente mesmo com `chat.mcp.autostart: true`
**Motivo**: VS Code precisa de confirmação de **trust** na primeira execução (segurança)
**Solução**: Seguir procedimento manual **uma única vez**

---

## 📋 Passo a Passo (5 minutos)

### 1️⃣ Abrir Command Palette

**Windows/Linux**: `Ctrl + Shift + P`
**macOS**: `Cmd + Shift + P`

### 2️⃣ Executar Comando MCP

Digite e selecione:

```
MCP: Refresh Servers
```

### 3️⃣ Conceder Trust aos Servidores

O VS Code exibirá uma janela de confirmação para **cada servidor**:

```
┌─────────────────────────────────────────────────────┐
│ Do you trust the MCP server "memory"?               │
│                                                     │
│ Command: npx                                        │
│ Args: -y @modelcontextprotocol/server-memory       │
│                                                     │
│ [Trust] [Cancel]                                    │
└─────────────────────────────────────────────────────┘
```

**Clique em "Trust"** para:
- ✅ memory
- ✅ sequential-thinking
- ✅ filesystem
- ✅ github

### 4️⃣ Verificar Status

Command Palette → `MCP: List Servers`

**Resultado esperado**:

```
✅ memory               [running]
✅ sequential-thinking  [running]
✅ filesystem          [running]
✅ github              [running]
```

### 5️⃣ Testar no Copilot Chat

Abra o Copilot Chat e pergunte:

```
Quais servidores MCP estão disponíveis?
```

**Resposta esperada**:

> Tenho acesso a 4 servidores MCP:
> 1. **memory** - Persistência de memória entre sessões
> 2. **sequential-thinking** - Raciocínio estruturado
> 3. **filesystem** - Leitura/escrita de arquivos locais
> 4. **github** - Issues, PRs, busca de código

---

## 🔧 Troubleshooting

### ❌ Servidores aparecem como [stopped]

**Causa**: Trust não concedido ou comando não encontrado

**Solução**:
1. Refaça o passo 2 (MCP: Refresh Servers)
2. Verifique se `npx` está instalado: `npx --version`
3. Verifique logs: Command Palette → "MCP: List Servers" → selecione servidor → "Show Output"

### ❌ Workspace não é trusted

**Causa**: VS Code não confia na pasta do projeto

**Solução**:
1. Command Palette → "Workspaces: Manage Workspace Trust"
2. Clique em "Trust" para o workspace atual

### ❌ Erro "command not found: npx"

**Causa**: Node.js não instalado ou não no PATH

**Solução**:
```bash
# Verificar instalação
node --version
npm --version
npx --version

# Instalar se necessário (Ubuntu/Debian)
sudo apt install nodejs npm

# Ou via nvm (recomendado)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install --lts
```

### ❌ Servidor github falha por falta de token

**Causa**: `GITHUB_PERSONAL_ACCESS_TOKEN` não configurado

**Solução**:
1. Crie token em: https://github.com/settings/tokens
2. Scopes necessários: `repo`, `read:org`
3. Configure no ambiente:

```bash
# Adicionar ao ~/.bashrc ou ~/.zshrc
export GITHUB_PERSONAL_ACCESS_TOKEN="ghp_seu_token_aqui"

# Ou criar .secrets/.env no projeto
echo "GITHUB_PERSONAL_ACCESS_TOKEN=ghp_seu_token_aqui" > .secrets/.env
```

**Nota**: O servidor github **tolera** falta de token (fails gracefully), os outros 3 servidores funcionarão normalmente.

---

## ✅ Após Primeira Configuração

Nas próximas vezes que abrir o workspace:

1. ✅ **Autostart funcionará automaticamente**
2. ✅ Não precisará conceder trust novamente
3. ✅ Servidores estarão disponíveis imediatamente

**Exceção**: Se modificar `.vscode/mcp.json` (adicionar/alterar servidor), precisará repetir o processo de trust apenas para os servidores modificados.

---

## 🛠️ Script Helper (Opcional)

Para validar configuração antes de abrir o VS Code:

```bash
./scripts/activate-mcp.sh
```

Modo automático (tenta abrir Command Palette):

```bash
./scripts/activate-mcp.sh --auto
```

**Nota**: Mesmo no modo `--auto`, você precisará conceder trust manualmente nas janelas de confirmação.

---

## 📚 Mais Informações

- [VS Code MCP Documentation](https://code.visualstudio.com/docs/copilot/customization/mcp-servers)
- [BUG-15: Limitação conhecida](../bugs/BUG-15-mcp-autostart-requires-manual-trust.md)
- [Referência completa de autostart](VS%20Code%20autostart%20MCP%20servers.md)
