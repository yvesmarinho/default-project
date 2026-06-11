# RESUMO DE ACOES — SESSION END PROMPT

## Arquivo de origem
.github/prompts/session-end.prompt.md

## Objetivo
Definir o ritual de encerramento de sessao para consolidar o que foi feito, atualizar rastreabilidade e preparar o proximo retorno com seguranca.

## Acoes principais
1. Consolida as atividades do dia em `DAILY_ACTIVITIES_[YYYY-MM-DD].md`.
2. Atualiza `docs/TODO.md` com itens concluidos, pendencias novas e prioridades revisadas.
3. Cria `FINAL_STATUS_[YYYY-MM-DD].md` quando a sessao encerrar uma fase importante.
4. Executa verificacoes de qualidade do codigo quando a sessao for de desenvolvimento.
5. Executa validacoes de infraestrutura quando a sessao for focada em IaC ou operacao.
6. Faz revisão de seguranca nos documentos de sessao antes de qualquer commit.
7. Faz scan final de arquivos e staging para impedir vazamento de segredos ou logs indevidos.
8. Prepara a mensagem de commit em arquivo dedicado, seguindo a regra P0 de mensagens longas.
9. Realiza commit e push para deixar o estado da sessao sincronizado.

## Pontos de atencao
- A documentacao de sessao e incremental e deve preservar historico anterior.
- O scan de seguranca deve incluir arquivos de sessao e a area de staging.
- O commit nao deve ser feito com `-m`; a mensagem precisa vir de arquivo.

## Resultado esperado
Sessao encerrada com atividades registradas, TODO atualizado, seguranca revisada e repositorio sincronizado.
