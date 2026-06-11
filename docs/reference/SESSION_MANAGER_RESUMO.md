# RESUMO DE ACOES — SESSION MANAGER

## Arquivo de origem
.github/agents/session-manager.agent.md

## Objetivo
Definir o agente responsavel por iniciar, organizar, pausar, retomar e encerrar sessoes de trabalho com foco em contexto, seguranca e documentacao.

## Acoes principais
1. Identifica quando o agente deve ser usado em inicio de sessao, setup inicial, retomada, pausa ou encerramento.
2. Valida MCPs e reforca o uso de ferramentas adequadas para contexto, analise e organizacao.
3. Recupera contexto anterior lendo README, INDEX, TODO e documentos de sessao.
4. Carrega regras do projeto e garante que restricoes de seguranca sejam seguidas.
5. Faz scan de arquivos sensiveis e confirma que `.secrets/` e a protecao padrao.
6. Organiza a estrutura do projeto, mantendo documentacao incremental e nomes consistentes.
7. Controla o time tracking da sessao, incluindo inicio, pausa, retomada e parada.
8. Em setup inicial, cria estrutura base, documentos de sessao e prepara o branch de trabalho.
9. No encerramento, atualiza documentos, consolida resultados e prepara o repositorio para o proximo ciclo.

## Comportamentos importantes
- Prioriza ferramentas nativas do VS Code e MCPs para leitura, busca e automacao.
- Evita terminal para operacoes de arquivo e segue as regras P0 do projeto.
- Mantem documentos de sessao de forma incremental, sem sobrescrever historico sem necessidade.

## Resultado esperado
Sessoes iniciadas e encerradas com contexto consistente, estrutura organizada, seguranca validada e rastreabilidade preservada.
