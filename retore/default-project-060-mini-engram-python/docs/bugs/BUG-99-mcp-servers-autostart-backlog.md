---
bug_id: BUG-99
title: "MCP Servers não inicializam automaticamente - backlog"
status: "backlog"
severity: "none"
priority: "backlog"
created: 2026-05-14
reporter: "yves_marinho"
related: ["BUG-15"]
---

# BUG-99: MCP Servers Não Inicializam Automaticamente (Backlog)

## 📋 Descrição

Issue de backlog para rastreamento futuro de automação completa da inicialização de servidores MCP, caso o VS Code introduza novas APIs ou configurações que permitam trust programático.

## 🔗 Relacionamento

Este bug é uma **continuação de baixa prioridade** do [BUG-15](BUG-15-mcp-autostart-requires-manual-trust.md).

## 🎯 Objetivo de Longo Prazo

Eliminar completamente a necessidade de interação manual para ativar servidores MCP em novos projetos ou após scaffold upgrade.

## 🔍 Contexto Atual

**Situação em 2026-05-14**:
- ✅ `chat.mcp.autostart: true` configurado
- ✅ `github.copilot.chat.enableMcp: true` configurado
- ✅ Documentação completa criada (MCP-QUICK-START.md)
- ❌ VS Code ainda requer trust manual por razões de segurança
- ❌ Não existe API ou configuração para auto-trust programático

## 💡 Possíveis Soluções Futuras

### 1. API de Trust Programático (VS Code)

**Se** o VS Code introduzir API futura:
- Arquivo de configuração `.vscode/mcp-trust.json` com lista de servidores confiáveis
- Comando CLI `code --trust-mcp-servers`
- Variável de ambiente `VSCODE_MCP_AUTO_TRUST=true`

**Estimativa**: Depende do VS Code Team (fora do nosso controle)

### 2. Script de Automação via UI (Hacky)

**Possível abordagem**:
- Usar `xdotool` (Linux) / `AppleScript` (macOS) / `AutoHotkey` (Windows)
- Automatizar cliques nos diálogos de trust
- **CONTRA**: Frágil, depende de UI, não portável

**Estimativa**: 2-3 dias (não recomendado)

### 3. Container/Dev Container Pré-Configurado

**Possível abordagem**:
- Distribuir Dev Container com servidores MCP pré-trusted
- Usar volume persistente para configurações do VS Code
- **CONTRA**: Overhead de container para projetos simples

**Estimativa**: 1 semana

### 4. Monitorar Roadmap do VS Code

**Ação recomendada**:
- Acompanhar [VS Code GitHub Discussions](https://github.com/microsoft/vscode/discussions)
- Verificar changelog de releases mensais
- Abrir feature request se houver demanda da comunidade

## 📊 Critérios de Ativação

Este bug deve ser **promovido de backlog para ativo** se:

1. ✅ VS Code introduzir nova API de trust programático
2. ✅ Comunidade criar solução confiável e mantida
3. ✅ Usuários reportarem frustração significativa (> 5 relatos)
4. ✅ Alternativa técnica viável surgir

**Até lá**: Manter no backlog, sem prioridade.

## 🛠️ Workaround Atual

Documentado em:
- [BUG-15: MCP Autostart requires manual trust](BUG-15-mcp-autostart-requires-manual-trust.md)
- [docs/guides/MCP-QUICK-START.md](../guides/MCP-QUICK-START.md)

**Tempo necessário**: 2-5 minutos (one-time setup)

## 📚 Referências

- [BUG-15: Limitação conhecida](BUG-15-mcp-autostart-requires-manual-trust.md)
- [VS Code MCP Documentation](https://code.visualstudio.com/docs/copilot/customization/mcp-servers)
- [VS Code Workspace Trust](https://code.visualstudio.com/docs/editing/workspaces/workspace-trust)

## 🏷️ Tags

`backlog`, `mcp`, `vscode`, `automation`, `trust`, `future-enhancement`, `low-priority`

---

**Status**: BACKLOG (sem prioridade até surgir solução viável)  
**Next Review**: 2026-11-14 (6 meses)
