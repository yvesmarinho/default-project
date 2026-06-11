# RESUMO DE ACOES — SESSION START PROMPT

## Arquivo de origem
.github/prompts/session-start.prompt.md

## Objetivo
Definir o ritual recorrente de inicio de sessao, com recuperacao de contexto, checagens de seguranca e preparo para trabalho com rastreabilidade.

## Acoes principais
1. Pergunta o modo de execucao: quick ou completo.
2. Valida a configuracao dos MCPs obrigatorios, com foco em memory e sequential-thinking.
3. Recupera contexto recente lendo TODO, INDEX e os documentos da ultima sessao.
4. Carrega e reforca as regras centrais do projeto, incluindo `.copilot-rules.md` e `.github/copilot-instructions.md`.
5. Executa scan de seguranca para identificar arquivos sensiveis fora de `.secrets/`.
6. Verifica dependencias e interrompe a sessao se houver pacotes criticos de seguranca desatualizados.
7. No modo completo, checa o estado do Git, cria a documentacao de sessao e inicia o time tracking.
8. No modo completo, define o escopo do trabalho e carrega o perfil de dominio apropriado.
9. Fecha com um checklist de prontidao antes da implementacao.

## Diferenca entre modos
- Quick: executa apenas os passos essenciais para começar rapido com seguranca minima.
- Completo: executa governanca, documentacao, rastreabilidade e verificacoes adicionais.

## Resultado esperado
Sessao iniciada com contexto recuperado, regras aplicadas, riscos reduzidos e caminho pronto para execucao.
