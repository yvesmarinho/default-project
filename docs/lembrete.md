# Alterações necessárias

---
## Informações adquiridas para futuro debate

- Buscar melhores práticas em Engenharia de Especificação orientada a Engenharia de Software.
- 4 Camadas do desenvolvimento: Negócio -> Produto -> Arquitetura -> Implementação.
- Decisões de Arquitetura (ADRs)
- Requisitos Funcionais
- Critérios de Aceite

---

## Novas demandas para adicionar a lista de tarefas/issues/melhorias.

1. Criar um modelo ser utilizado no inicio do projeto [objetivo.yaml](../docs/modelo_docs/objetivo.yaml)
    - Esse modelo conterá informações e instruções que serão utilizados como base para o contrato/constitution.
    - Conterá informações iniciais para o debate entre os agents mencionados no documento.
    - O debate analisará o conteúdo fornecido pelo usuário para aprimorar as especificações ou indicar informações ausente, gerando um questionário.
    - Informações obtidas em um video do Youtube [Spec Driven Development é o Caminho?](https://www.youtube.com/watch?v=DJE0LL0CuUQ).
    - Fluxo de especificação:

2. Após a conclusão da analise e aprimoramento do "objetivo.yaml" atualizar o [mc-questions.yaml](../docs/modelo_docs/mcp-questions.yaml).

3. Incluir no workflow instruções para gerar arquivo com o resultado do chat [CHAT-YYYYMMDD-000000.md](../docs/modelo_docs/CHAT-20260401-000000.md).
    Toda resposta do Copilot no chat deve gerar um arquivo desse. Esse arquivo pode ser usado como memória.
    Aceito sugestão de um fluxo que atenda essa demanda para torná-la mais agil.
    Um posssíbilidade seria o Engram, que já temos como melhoria.
    Avalie as opções e informe uma boa opção para essa demanda


---

## ✅ Processado em 2026-04-03

Os itens abaixo foram analisados e convertidos em issues estruturadas no `docs/TODO.md`:

1. ✅ **[IMP-52]** Adicionar instruções para usar as ferramentas jsonschema e yamllint já disponíveis.
   - Tipo: Improvement (documentação)
   - Prioridade: P1
   - Adicionado em: docs/TODO.md (seção "Itens Recentes")
   - Estimativa: 2h

2. ✅ **[BUG-03]** Não foi gerado o .github/copilot-instructions.md com as instruções básicas existentes.
   - Tipo: Bug (geração de arquivo do scaffold)
   - Prioridade: P0
   - Adicionado em: docs/TODO.md (seção "Itens Recentes")
   - Requer investigação em: scripts/lib/templates.py, scripts/lib/flows/new_project.py

3. (vazio - descartado)

---

## 📚 Referência

Para entender como gerenciar bugs e features no projeto, consulte:
- **Guia completo**: [docs/ISSUE_MANAGEMENT_GUIDE.md](../docs/ISSUE_MANAGEMENT_GUIDE.md)
- **TODO principal**: [docs/TODO.md](../docs/TODO.md)
- **Templates de issues**: `.github/ISSUE_TEMPLATE/`

---

## 💡 Próximos Passos

1. **Investigar BUG-03** (P0):
   ```bash
   # Verificar se generate_copilot_instructions() é chamado
   grep -r "generate_copilot_instructions" scripts/lib/

   # Criar projeto teste e verificar
   python scripts/scaffold.py new --ci --name test-bug03 \
     --domain programming --language python --target-dir ./tmp

   ls -la ./tmp/test-bug03/.github/copilot-instructions.md
   ```

2. **Implementar IMP-52** (P1):
   - Adicionar seção no README.md sobre validação de YAML/JSON
   - Criar targets `make lint-yaml` e `make lint-json`
   - Documentar em docs/DEVELOPMENT_GUIDE.md (criar se necessário)

---

**Status**: Items triaged and documented ✅

