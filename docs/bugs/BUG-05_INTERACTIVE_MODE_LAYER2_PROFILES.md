# BUG-05: Modo Interativo Não Permite Seleção de Perfis Layer 2

**Status**: 🔴 ABERTO
**Prioridade**: P1 (High - impacta experiência do usuário novato)
**Descoberto**: 2026-04-23
**Reportado por**: Usuário em teste de usabilidade
**Afeta**: `scaffold.py new` (modo interativo)
**Branch**: 060-mini-engram-python

---

## 📋 Resumo Executivo

Usuários novatos que executam `scaffold.py new` no modo interativo **não conseguem selecionar perfis Layer 2** (como `python-fastapi`, `typescript-next`, etc.), apenas perfis Layer 1 (`devops-programming`, `devops-infrastructure`, `devops-analysis`).

Isso quebra a expectativa de criar um projeto completo em uma única execução interativa, forçando o usuário a executar um segundo comando (`compose`) que ele nem sabe que existe.

---

## 🐛 Descrição do Problema

### Comportamento Atual

Quando usuário executa `scaffold.py new` interativamente:

```bash
$ uv run scripts/scaffold.py new

Informações do Projeto

  Nome do projeto (kebab-case, ex: my-api-v2) (): tst-fast-api
  # ... outros campos ...

  [8] Perfis adicionais além de devops-programming?
      devops-security incluído sempre — não aparece aqui
      [1]  Apenas meu domínio (devops-programming)  (default)
      [2]  Todos disponíveis
      [3]  Selecionar individualmente

      Escolha (1): 3

      Perfis disponíveis:
        [1]  devops-infrastructure  ❌ Só Layer 1!
        [2]  devops-analysis        ❌ Só Layer 1!

      # python-fastapi NÃO aparece! ❌
```

**Resultado**: Usuário cria projeto sem código específico (FastAPI, Next.js, etc.), apenas estrutura base.

---

### Comportamento Esperado

Usuário deveria poder selecionar perfis Layer 2 relevantes para seu projeto:

```bash
  [8] Perfis adicionais além de devops-programming?
      devops-security incluído sempre — não aparece aqui
      [1]  Apenas meu domínio (devops-programming)  (default)
      [2]  Todos disponíveis (Layer 1 + Layer 2)
      [3]  Selecionar individualmente
      [4]  🆕 Adicionar perfil de código (python-fastapi, typescript-next, etc.)

      Escolha (1): 4

      Perfis de código disponíveis para Python:
        [1]  python-fastapi   (REST API com FastAPI)
        [2]  python-flask     (Web app com Flask)
        [3]  Nenhum          (apenas estrutura base)

      Escolha (3): 1

  ✅ Perfis selecionados:
     - devops-programming (base)
     - python-fastapi (código)
     - devops-security (transversal)
```

---

## 🎯 Impacto no Usuário

### Usuário Novato (Alta Severidade)

**Problema**: Não sabe que precisa executar 2 comandos
```bash
# O que faz (expectativa: projeto pronto)
$ scaffold.py new
# Resultado: projeto SEM código FastAPI 😞

# O que deveria fazer (não documentado claramente)
$ scaffold.py new
$ cd meu-projeto
$ scaffold.py compose python-fastapi  # ❓ Como descobrir isso?
```

**Impacto**:
- ❌ Frustração: "Por que não tem código FastAPI?"
- ❌ Confusão: "O que é compose? Quando usar?"
- ❌ Retrabalho: Precisa pesquisar documentação ou refazer

---

### Usuário Experiente (Média Severidade)

**Problema**: Fluxo menos eficiente
```bash
# Modo atual (2 comandos)
$ scaffold.py new
$ cd projeto
$ scaffold.py compose python-fastapi

# Modo ideal (1 comando - já possível via --ci, mas não interativo)
$ scaffold.py new --compose python-fastapi  # ❌ Não existe flag --compose em new
```

---

## 🔍 Análise Técnica

### Root Cause

**Arquivo**: `scripts/lib/ui.py`
**Função**: `_collect_extra_profiles()` (linha ~275)

```python
def _collect_extra_profiles(domain: str) -> list[str]:
    """
    Pergunta [8]: quais perfis adicionais além do perfil do domínio principal.
    """
    domain_profile = DOMAIN_DEFAULT_PROFILES.get(domain, f"devops-{domain}")

    # ❌ BUG: Só considera perfis Layer 1
    available_extras = [p for p in ALL_SELECTABLE_PROFILES if p != domain_profile]
    #                                 ^^^^^^^^^^^^^^^^^^^^^^^^
    #                                 Só tem Layer 1!
```

**Arquivo**: `scripts/lib/config.py`
**Constante**: `ALL_SELECTABLE_PROFILES` (linha 111)

```python
ALL_SELECTABLE_PROFILES: list[str] = [
    "devops-programming",      # Layer 1
    "devops-infrastructure",   # Layer 1
    "devops-analysis",         # Layer 1
]
# ❌ python-fastapi, typescript-next, etc. NÃO estão aqui
```

---

### Por Que Foi Projetado Assim?

**Design Original**: Separação rígida entre layers
- `new` → estrutura base (SpecKit, agents, docs) + Layer 1
- `compose` → código específico + Layer 2

**Vantagem**: Separação de responsabilidades clara
**Desvantagem**: UX confusa para novatos

---

## 📊 Evidência do Bug

### Teste de Usabilidade (2026-04-23)

**Cenário**: Usuário quer criar projeto FastAPI

**Ações do Usuário**:
```bash
$ uv run scripts/scaffold.py new

  Nome do projeto: tst-fast-api
  Domínio: programming
  Linguagem: python

  [8] Perfis adicionais?
      Escolha (1): 3  # Selecionar individualmente

      Perfis disponíveis:
        [1]  devops-infrastructure
        [2]  devops-analysis

      # ❓ Onde está python-fastapi?
      Números: 1  # Seleciona infrastructure por confusão
```

**Resultado**: Projeto criado com perfis incorretos (programming + infrastructure)

**Expectativa do Usuário**: Ver `python-fastapi` na lista

**Comentário do Usuário**: *"no modo interativo não tem essa opção? estou testando como usuário novato."*

---

## ✅ Solução Proposta

### Opção 1: Adicionar Passo Extra no Modo Interativo (Recomendado)

**Modificar**: `_collect_extra_profiles()` em `scripts/lib/ui.py`

**Novo Fluxo**:
```python
def _collect_extra_profiles(domain: str, language: str) -> list[str]:
    """
    Pergunta [8]: perfis Layer 1 adicionais
    Pergunta [9]: perfis Layer 2 (código)
    """
    # Passo 1: Perfis Layer 1 (como antes)
    layer1_profiles = _select_layer1_profiles(domain)

    # Passo 2: Perfis Layer 2 (NOVO)
    layer2_profile = _select_layer2_profile(domain, language)

    return layer1_profiles + ([layer2_profile] if layer2_profile else [])


def _select_layer2_profile(domain: str, language: str) -> str | None:
    """
    Nova função: permite selecionar perfil de código (Layer 2).

    Mostra apenas perfis compatíveis com domain + language.
    """
    # Filtrar perfis Layer 2 por domain + language
    available = _get_compatible_layer2_profiles(domain, language)

    if not available:
        return None  # Sem perfis Layer 2 disponíveis

    console.print(f"\n  [cyan][9] Adicionar perfil de código específico?[/cyan]")
    console.print("      [bold cyan][1][/bold cyan]  Não, apenas estrutura base  [dim](default)[/dim]")

    for idx, profile in enumerate(available, start=2):
        desc = _get_profile_description(profile)
        console.print(f"      [bold cyan][{idx}][/bold cyan]  {profile}  [dim]({desc})[/dim]")

    console.print()

    choices = ["1"] + [str(i) for i in range(2, len(available) + 2)]
    choice = Prompt.ask("      Escolha", choices=choices, default="1", show_choices=False)

    if choice == "1":
        return None

    idx = int(choice) - 2
    return available[idx]


def _get_compatible_layer2_profiles(domain: str, language: str) -> list[str]:
    """
    Retorna perfis Layer 2 compatíveis com domain + language.

    Lê profile-descriptors/*.yaml e filtra por requires.
    """
    from pathlib import Path
    import yaml

    profiles = []
    descriptors_dir = Path(__file__).parent.parent.parent / "profile-descriptors"

    for yaml_file in sorted(descriptors_dir.glob("*.yaml")):
        if yaml_file.stem in ALL_SELECTABLE_PROFILES:
            continue  # Pular Layer 1

        try:
            with open(yaml_file, encoding="utf-8") as f:
                data = yaml.safe_load(f)

            requires = data.get("requires", [])

            # Checar compatibilidade
            domain_ok = any(f"domain == {domain}" in r for r in requires)
            language_ok = any(f"language == {language}" in r for r in requires)

            if domain_ok and language_ok:
                profiles.append(yaml_file.stem)
        except Exception:
            continue

    return profiles


def _get_profile_description(profile_name: str) -> str:
    """Retorna descrição curta do perfil."""
    descriptions = {
        "python-fastapi": "REST API com FastAPI",
        "python-flask": "Web app com Flask",
        "typescript-next": "Frontend com Next.js",
        "terraform-aws": "Infraestrutura AWS",
        "k8s-helm": "Deploy Kubernetes",
        # ... adicionar outros
    }
    return descriptions.get(profile_name, "")
```

**Benefícios**:
- ✅ UX intuitiva para novatos
- ✅ Projeto completo em uma execução
- ✅ Backward compatible (choice "1" = comportamento atual)
- ✅ Dinâmico (lê profile-descriptors, suporta novos perfis)

**Esforço**: 3-4 horas

---

### Opção 2: Adicionar Flag `--compose` ao Comando `new`

**Modificar**: `scripts/scaffold.py` argument parser

```python
new_group.add_argument(
    "--compose",
    metavar="PROFILE",
    help="Aplicar perfil Layer 2 após criar estrutura (ex: python-fastapi)"
)
```

**Fluxo**:
```python
def flow_new_project(args):
    # Criar estrutura base
    cfg = collect_project_info(...)
    results = create_project(cfg)

    # Se --compose fornecido, aplicar perfil Layer 2
    if args.compose:
        from .flows import compose
        args_compose = argparse.Namespace(
            compose=args.compose,
            ci=True,
            # ... outros args
        )
        compose.flow_compose_profiles(args_compose)
```

**Benefícios**:
- ✅ Comando único para usuários CLI
- ✅ Documentação mais simples
- ✅ Menos código que Opção 1

**Desvantagens**:
- ❌ Não resolve modo interativo (foco deste bug)
- ❌ Requer documentação de flag extra

**Esforço**: 2 horas

---

### Opção 3: Unificar Layer 1 + Layer 2 em `ALL_SELECTABLE_PROFILES`

**Modificar**: `scripts/lib/config.py`

```python
ALL_SELECTABLE_PROFILES: list[str] = [
    # Layer 1
    "devops-programming",
    "devops-infrastructure",
    "devops-analysis",
    # Layer 2
    "python-fastapi",
    "python-flask",
    "typescript-next",
    "terraform-aws",
    "k8s-helm",
    # ... todos
]
```

**Benefícios**:
- ✅ Solução mais simples

**Desvantagens**:
- ❌ Lista gigante (20+ perfis)
- ❌ Confuso (mistura conceitos Layer 1 + Layer 2)
- ❌ Mostra perfis incompatíveis (typescript-next para Python)
- ❌ Não escala (cada novo perfil polui lista)

**Esforço**: 1 hora, mas **NÃO RECOMENDADO**

---

## 🎯 Recomendação

**Implementar Opção 1**: Adicionar passo extra no modo interativo

**Justificativa**:
1. ✅ Resolve o problema raiz (UX confusa para novatos)
2. ✅ Mantém separação Layer 1/Layer 2 conceitualmente clara
3. ✅ Filtragem inteligente por domain + language
4. ✅ Dinâmico (lê profile-descriptors automaticamente)
5. ✅ Backward compatible

**Adicionalmente**: Implementar Opção 2 (flag `--compose`) para usuários CLI

---

## 📝 Checklist de Implementação

### Fase 1: Core (Opção 1)
- [ ] Criar `_select_layer2_profile()` em `ui.py`
- [ ] Criar `_get_compatible_layer2_profiles()` em `ui.py`
- [ ] Criar `_get_profile_description()` em `ui.py`
- [ ] Modificar `_collect_extra_profiles()` para incluir Layer 2
- [ ] Modificar `_collect_interactive()` para passar `language` param
- [ ] Testar com `python-fastapi`, `typescript-next`, `terraform-aws`

### Fase 2: Enhancement (Opção 2)
- [ ] Adicionar flag `--compose` ao argument parser
- [ ] Modificar `flow_new_project()` para chamar compose após new
- [ ] Atualizar `--help` com exemplo
- [ ] Testar `scaffold.py new --compose python-fastapi --ci`

### Fase 3: Documentação
- [ ] Atualizar `docs/NEW_PROJECT_COMMAND.md` com novo fluxo
- [ ] Adicionar exemplos no `README.md`
- [ ] Criar screencast/GIF do fluxo interativo
- [ ] Atualizar `CHANGELOG.md`

### Fase 4: Testes
- [ ] Criar teste unitário para `_get_compatible_layer2_profiles()`
- [ ] Teste de integração: modo interativo completo
- [ ] Teste de regressão: modo CI ainda funciona
- [ ] Validação com usuário novato

---

## 📊 Estimativa

| Fase | Esforço | Prioridade |
|------|---------|------------|
| Fase 1 (Core) | 3-4 horas | P1 |
| Fase 2 (Enhancement) | 2 horas | P2 |
| Fase 3 (Documentação) | 2 horas | P1 |
| Fase 4 (Testes) | 2-3 horas | P1 |
| **Total** | **9-11 horas** | - |

---

## 🔗 Relacionados

- **BUG-02**: Compose from subdirectory (FIXED - b5fab59)
- **BUG-03**: Template bases saving (FIXED - 697d141)
- **BUG-04**: Breaking changes validation (OPEN - P1)
- **IMP-65**: Template synchronization (IN PROGRESS - scenarios 2-5 done)

---

## 💬 Comentários

**2026-04-23** (Descoberta):
> Usuário novato tentou criar projeto FastAPI via modo interativo, não encontrou `python-fastapi` na lista de perfis. Comentário: *"no modo interativo não tem essa opção?"*

**Ação Imediata**: Documentar workaround em `docs/QUICKSTART.md`

**Workaround Atual**:
```bash
# Passo 1: Criar estrutura base
$ scaffold.py new

# Passo 2: Adicionar código FastAPI
$ cd meu-projeto
$ scaffold.py compose python-fastapi --ci
```

---

## 🏷️ Labels

- `bug` - comportamento inesperado
- `ux` - experiência do usuário
- `P1` - alta prioridade
- `good-first-issue` - boa para contribuidores novos (Fase 2)
- `enhancement` - melhoria de feature existente

---

**Criado**: 2026-04-23
**Última atualização**: 2026-04-23
**Assignee**: TBD
**Milestone**: v1.1.0
