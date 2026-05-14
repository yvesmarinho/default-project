---
bug_id: BUG-15
title: "MCP Autostart requer trust manual na primeira execução"
status: "known_limitation"
severity: "low"
created: 2026-05-14
reporter: "yves_marinho"
---

# BUG-15: MCP Autostart Requer Trust Manual na Primeira Execução

## 📋 Descrição

Mesmo com `chat.mcp.autostart: true` configurado em `.vscode/settings.json`, os servidores MCP não iniciam automaticamente ao abrir o workspace pela primeira vez ou após adicionar/modificar servidores.

## 🔍 Causa Raiz

Segundo a documentação oficial do VS Code (v1.103+), o autostart de servidores MCP está condicionado a:

1. **Workspace Trust**: O workspace precisa estar marcado como "trusted"
2. **Server Trust**: Cada servidor MCP precisa ter trust concedido manualmente na primeira execução
3. **Configuração válida**: `.vscode/mcp.json` deve ter sintaxe JSONC válida

**O problema**: O VS Code **não concede trust automaticamente** aos servidores, mesmo com autostart habilitado. Isso é um comportamento de segurança intencional.

## 📊 Evidências

```bash
# Configuração presente e correta
$ grep "chat.mcp.autostart" .vscode/settings.json
  "chat.mcp.autostart": true

# Servidores configurados corretamente
$ python3 -c "..." .vscode/mcp.json
Servidores: ['memory', 'sequential-thinking', 'filesystem', 'github']

# Após reiniciar VS Code → servidores continuam parados
```

## 🛠️ Workaround

### Opção 1: Trust Manual via Command Palette (RECOMENDADO)

1. Abra o Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`)
2. Execute: **`MCP: Refresh Servers`**
3. VS Code solicitará confirmação de trust para cada servidor
4. Aceite o trust para todos os servidores
5. Após conceder trust, o autostart funcionará nas próximas sessões

### Opção 2: Script Helper

```bash
./scripts/activate-mcp.sh --auto
```

**Nota**: O script tenta abrir o Command Palette automaticamente, mas **ainda requer interação manual** para conceder trust.

### Opção 3: Verificar Trust Status

```bash
# Abrir Command Palette
Ctrl+Shift+P / Cmd+Shift+P

# Executar
MCP: List Servers

# Verificar status de cada servidor:
# - "running" → trust concedido, autostart funcionando
# - "stopped" → precisa conceder trust manualmente
```

## 🔧 Tentativas de Solução Automatizada

### Configurações testadas (sem sucesso):

```json
{
  "chat.mcp.autostart": true,  // ✓ Presente
  "github.copilot.chat.enableMcp": true  // ✓ Adicionado
}
```

### Limitação confirmada:

O VS Code **não oferece** configuração para:
- Auto-trust de servidores MCP
- Skip de confirmação de segurança
- Trust programático via settings.json

Isso é **intencional** por razões de segurança, pois servidores MCP podem executar código arbitrário.

## 📚 Referências

- [VS Code MCP Servers Documentation](https://code.visualstudio.com/docs/copilot/customization/mcp-servers)
- [VS Code 1.103 Release Notes](https://code.visualstudio.com/updates/v1_103)
- [Workspace Trust Documentation](https://code.visualstudio.com/docs/editing/workspaces/workspace-trust)
- [docs/guides/VS Code autostart MCP servers.md](../guides/VS%20Code%20autostart%20MCP%20servers.md)

## 🎯 Impacto

**Severidade**: Baixa  
**Frequência**: Apenas na primeira execução ou após modificar servidores  
**Afeta**: Experiência de desenvolvedor (DX)

### Cenários afetados:

1. ✅ **Projeto novo** via scaffold → precisa trust manual uma vez
2. ✅ **Clone de repositório** → precisa trust manual uma vez  
3. ✅ **Upgrade de template** → se servidores mudaram, precisa re-trust
4. ✅ **Desenvolvimento regular** → autostart funciona após trust concedido

## ✅ Status

**Classificação**: Limitação conhecida do VS Code  
**Solução**: Procedimento manual documentado (workarounds acima)  
**Próximos passos**:
- Adicionar instruções de trust em `README.md`
- Atualizar `session-start-first.prompt.md` com nota sobre trust
- Melhorar mensagens de `activate-mcp.sh` com passo-a-passo visual

## 🏷️ Tags

`mcp`, `vscode`, `autostart`, `trust`, `security`, `known-limitation`, `dx`
