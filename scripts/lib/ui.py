"""
lib/ui.py — Interface com usuário: prompts Rich, menus e validação.

Parte do scripts/scaffold.py — Enterprise Default Project Template.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table
from rich.text import Text

from .config import (
    ALL_SELECTABLE_PROFILES,
    DOMAIN_DEFAULT_PROFILES,
    SCAFFOLD_VERSION,
    SPECKIT_TRANSVERSAL_PROFILES,
    VALID_DOMAINS,
    VALID_LANGUAGES,
    CreatedItem,
    LinkStatus,
    ProjectConfig,
    get_default_shared_dir,
    get_default_target_dir,
    load_user_config,
)

console = Console()

# Regex de validação do nome (kebab-case)
_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


# ---------------------------------------------------------------------------
# Utilitários internos
# ---------------------------------------------------------------------------

def _to_title(name: str) -> str:
    """Converte kebab-case para Title Case. Ex: my-api-v2 → My Api V2."""
    return " ".join(word.capitalize() for word in name.split("-"))


def _validate_name(name: str) -> bool:
    return bool(_NAME_RE.match(name))


def _validate_directory_conflict(project_name: str, target_dir: Path) -> tuple[bool, str]:
    """
    Valida se há potencial conflito entre nome do projeto e diretório alvo.
    Com a nova lógica de project_path (config.py), se target_dir.name == project_name,o scaffold usa target_dir diretamente (sem criar subdiretório duplicado).

    Esta validação agora apenas AVISA o usuário quando isso acontece,
    sem bloquear a operação.

    Returns:
        (is_valid, warning_message)
    """
    target_dir_resolved = target_dir.resolve()

    # Se nomes coincidem, scaffold criará arquivos diretamente em target_dir
    if target_dir_resolved.name == project_name:
        # Se diretório tem conteúdo, avisar usuário
        if target_dir_resolved.exists() and target_dir_resolved.is_dir():
            try:
                # Verifica se tem algum conteúdo
                has_content = any(target_dir_resolved.iterdir())
                if has_content:
                    # Retorna warning mas permite continuar (valid=True)
                    return True, (
                        f"⚠️  Aviso: o diretório '{target_dir}' já existe e tem conteúdo.\n"
                        f"   Como o nome coincide com o projeto '{project_name}', "
                        f"os arquivos serão criados diretamente neste diretório.\n"
                        f"   Arquivos existentes NÃO serão sobrescritos (serão pulados)."
                    )
            except OSError:
                pass  # Ignorar erros de permissão

    return True, ""


def _iso_now() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------------------
# Funções públicas
# ---------------------------------------------------------------------------

def show_banner() -> None:
    """Exibe banner Rich com nome do projeto e versão."""
    panel = Panel(
        Text(f"🚀  Enterprise Project Scaffold  v{SCAFFOLD_VERSION}", justify="center"),
        style="bold blue",
        border_style="blue",
    )
    console.print()
    console.print(panel)
    console.print()


def show_menu() -> str:
    """
    Exibe menu principal e retorna a opção escolhida ('1'–'4').
    Fica em loop até opção válida.
    """
    while True:
        console.print("  [bold cyan][1][/bold cyan]  Novo Projeto")
        console.print("  [bold cyan][2][/bold cyan]  Verificar Links (.copilot-*)")
        console.print("  [bold cyan][3][/bold cyan]  Gerar .copilot-rules-[projeto].md")
        console.print("  [bold cyan][5][/bold cyan]  Upgrade (re-aplicar template)")
        console.print("  [bold cyan][4][/bold cyan]  Sair")
        console.print()
        choice = Prompt.ask("  Escolha", choices=["1", "2", "3", "4", "5"], show_choices=False)
        return choice


def collect_project_info(ci_mode: bool = False, **overrides) -> ProjectConfig:
    """
    Coleta informações do projeto via prompts interativos ou via overrides (CI).

    Em modo interativo:
    - Valida formato do project_name (kebab-case)
    - Exibe padrão sugerido para cada campo opcional
    - Permite corrigir antes de confirmar

    Em modo CI (ci_mode=True):
    - Campos obrigatórios ausentes levantam ValueError
    - Campos opcionais usam defaults se ausentes
    """
    # Carregar defaults do JSON e mesclar com overrides
    user_config = load_user_config()
    json_defaults = user_config.get("defaults", {})

    # Mesclar: overrides (CLI) têm prioridade sobre JSON
    merged_defaults = {**json_defaults, **overrides}

    if ci_mode:
        return _collect_ci(merged_defaults)
    return _collect_interactive(merged_defaults)


def _collect_ci(overrides: dict) -> ProjectConfig:
    """Coleta dados no modo CI — sem prompts."""
    required = ("name", "domain", "language")
    missing = [f for f in required if not overrides.get(f)]
    if missing:
        raise ValueError(
            f"Campos obrigatórios ausentes no modo --ci: {', '.join(missing)}"
        )

    domain = overrides["domain"]
    language = overrides["language"]
    if domain not in VALID_DOMAINS:
        raise ValueError(f"--domain inválido: '{domain}'. Válidos: {VALID_DOMAINS}")
    if language not in VALID_LANGUAGES:
        raise ValueError(f"--language inválido: '{language}'. Válidos: {VALID_LANGUAGES}")

    name = overrides["name"]
    if not _validate_name(name):
        raise ValueError(
            f"--name inválido: '{name}'. Use apenas letras minúsculas, números e hífens."
        )

    # BUG-02 fix: resolve() garante caminho absoluto independente do CWD
    target_dir = Path(overrides["target_dir"]).expanduser().resolve() if overrides.get("target_dir") else get_default_target_dir().resolve()

    # Validar conflito de diretório (BUG-01)
    is_valid, error_msg = _validate_directory_conflict(name, target_dir)
    if not is_valid:
        raise ValueError(f"Conflito de diretório: {name} == {target_dir.name}. {error_msg}")

    return ProjectConfig(
        project_name=name,
        project_title=overrides.get("title") or _to_title(name),
        description=overrides.get("description") or "",
        domain=domain,
        language=language,
        github_repo=overrides.get("repo") or None,
        shared_dir=Path(overrides["shared_dir"]).expanduser().resolve() if overrides.get("shared_dir") else get_default_shared_dir().resolve(),
        target_dir=target_dir,
        created_at=_iso_now(),
        extra_profiles=_parse_extra_profiles(overrides.get("extra_profiles") or "domain-only", domain),
    )


def _collect_interactive(defaults: dict) -> ProjectConfig:
    """Coleta dados interativamente com Rich prompts."""
    console.print("[bold]Informações do Projeto[/bold]\n", style="blue")

    # project_name — obrigatório, validado
    while True:
        name = Prompt.ask(
            "  [cyan]Nome do projeto[/cyan] [dim](kebab-case, ex: my-api-v2)[/dim]",
            default=defaults.get("name") or "",
        ).strip()
        if not name:
            console.print("  [red]❌ Nome obrigatório.[/red]")
            continue
        if not _validate_name(name):
            console.print(
                "  [red]❌ Formato inválido. Use apenas letras minúsculas, números e hífens.[/red]"
            )
            continue
        break

    title = Prompt.ask(
        "  [cyan]Título legível[/cyan]",
        default=defaults.get("title") or _to_title(name),
    ).strip() or _to_title(name)

    description = Prompt.ask(
        "  [cyan]Descrição[/cyan] [dim](1 frase, opcional)[/dim]",
        default=defaults.get("description") or "",
    ).strip()

    # domain
    domain = Prompt.ask(
        "  [cyan]Domínio[/cyan]",
        choices=VALID_DOMAINS,
        default=defaults.get("domain") or "programming",
    )

    # language
    language = Prompt.ask(
        "  [cyan]Linguagem principal[/cyan]",
        choices=VALID_LANGUAGES,
        default=defaults.get("language") or "python",
    )

    github_repo = Prompt.ask(
        "  [cyan]Repositório GitHub[/cyan] [dim](URL ou Enter para pular)[/dim]",
        default=defaults.get("repo") or "",
    ).strip() or None

    shared_dir_str = Prompt.ask(
        "  [cyan]Diretório compartilhado[/cyan]",
        default=str(defaults.get("shared_dir") or get_default_shared_dir()),
    ).strip()

    target_dir_str = Prompt.ask(
        "  [cyan]Diretório alvo[/cyan] [dim](onde criar o projeto)[/dim]",
        default=str(defaults.get("target_dir") or get_default_target_dir()),
    ).strip()

    # BUG-02 fix: resolve() garante caminho absoluto independente do CWD
    target_dir = Path(target_dir_str).expanduser().resolve()

    # Validar conflito de diretório (BUG-01)
    is_valid, error_msg = _validate_directory_conflict(name, target_dir)
    if not is_valid:
        console.print(f"\n[bold red]{error_msg}[/bold red]\n")
        raise ValueError(f"Conflito de diretório: {name} == {target_dir.name}")

    return ProjectConfig(
        project_name=name,
        project_title=title,
        description=description,
        domain=domain,
        language=language,
        github_repo=github_repo,
        shared_dir=Path(shared_dir_str).expanduser().resolve(),
        target_dir=target_dir,
        created_at=_iso_now(),
        extra_profiles=_collect_extra_profiles(domain),
    )


def _collect_extra_profiles(domain: str) -> list[str]:
    """
    Pergunta [8]: quais perfis adicionais além do perfil do domínio principal.

    Opções:
      [1] Apenas meu domínio — só o perfil principal (default)
      [2] Todos disponíveis  — todos os perfis selecionáveis
      [3] Selecionar         — escolha individual por número

    devops-security é sempre incluído (D-20) e não aparece nesta escolha.
    """
    domain_profile = DOMAIN_DEFAULT_PROFILES.get(domain, f"devops-{domain}")
    # Perfis que podem ser selecionados extras (excluindo o do domínio atual)
    available_extras = [p for p in ALL_SELECTABLE_PROFILES if p != domain_profile]

    console.print(
        f"\n  [cyan][8] Perfis adicionais além de [bold]{domain_profile}[/bold]?[/cyan]"
    )
    console.print("      [dim]devops-security incluído sempre — não aparece aqui[/dim]")
    console.print(f"      [bold cyan][1][/bold cyan]  Apenas meu domínio ({domain_profile})  [dim](default)[/dim]")
    console.print("      [bold cyan][2][/bold cyan]  Todos disponíveis")
    console.print("      [bold cyan][3][/bold cyan]  Selecionar individualmente")
    console.print()

    mode = Prompt.ask("      Escolha", choices=["1", "2", "3"], default="1", show_choices=False)

    if mode == "1":
        return []

    if mode == "2":
        return list(available_extras)

    # mode == "3": seleção individual
    console.print("\n      Perfis disponíveis:")
    for idx, profile in enumerate(available_extras, start=1):
        console.print(f"        [bold cyan][{idx}][/bold cyan]  {profile}")
    console.print()

    selected: list[str] = []
    raw = Prompt.ask(
        "      Números separados por vírgula [dim](ex: 1,2)[/dim] ou Enter para nenhum",
        default="",
    ).strip()
    if raw:
        for part in raw.split(","):
            part = part.strip()
            if part.isdigit():
                idx = int(part) - 1
                if 0 <= idx < len(available_extras):
                    selected.append(available_extras[idx])
    return selected


def _parse_extra_profiles(value: str, domain: str) -> list[str]:
    """
    Interpreta o valor de --extra-profiles no modo CI.

    Aceita:
      "domain-only"  → [] (apenas domínio, default)
      "all"          → todos os perfis exceto o domínio
      "none"         → [] (equivalente a domain-only)
      "profile1,profile2" → lista explícita
    """
    domain_profile = DOMAIN_DEFAULT_PROFILES.get(domain, f"devops-{domain}")
    available_extras = [p for p in ALL_SELECTABLE_PROFILES if p != domain_profile]

    if value in ("domain-only", "none", ""):
        return []
    if value == "all":
        return list(available_extras)
    # lista explícita
    selected = []
    for name in value.split(","):
        name = name.strip()
        if name in available_extras:
            selected.append(name)
    return selected


def confirm_summary(config: ProjectConfig) -> bool:
    """Exibe tabela resumo da configuração e pede confirmação (s/n)."""
    console.print()
    table = Table(
        title="📋 Resumo do Projeto",
        box=box.ROUNDED,
        border_style="blue",
        show_header=False,
    )
    table.add_column("Campo", style="cyan", no_wrap=True)
    table.add_column("Valor", style="white")

    table.add_row("Nome", config.project_name)
    table.add_row("Título", config.project_title)
    table.add_row("Descrição", config.description or "[dim](vazia)[/dim]")
    table.add_row("Domínio", config.domain)
    table.add_row("Linguagem", config.language)
    table.add_row("Repositório", config.github_repo or "[dim](não informado)[/dim]")
    table.add_row("Shared dir", str(config.shared_dir))
    table.add_row("Target dir", str(config.target_dir))
    table.add_row("Project path", str(config.project_path))

    domain_profile = DOMAIN_DEFAULT_PROFILES.get(config.domain, f"devops-{config.domain}")
    extras = config.extra_profiles or []
    all_profiles = [domain_profile] + extras + SPECKIT_TRANSVERSAL_PROFILES
    table.add_row("Perfis SpecKit", ", ".join(all_profiles))

    console.print(table)
    console.print()
    return Confirm.ask("  Confirmar e criar projeto?", default=True)


def print_final_summary(items: list[CreatedItem | LinkStatus]) -> None:
    """Exibe tabela Rich com status de cada item operado."""
    console.print()
    table = Table(
        title="✅ Resultado da Operação",
        box=box.ROUNDED,
        border_style="green",
    )
    table.add_column("Tipo", style="dim", width=8)
    table.add_column("Caminho / Nome", style="cyan")
    table.add_column("Status", width=10)
    table.add_column("Mensagem", style="dim")

    status_styles = {
        "created": "[green]created[/green]",
        "skipped": "[yellow]skipped[/yellow]",
        "error":   "[red]error[/red]",
        "ok":      "[green]ok[/green]",
        "broken":  "[red]broken[/red]",
        "missing": "[yellow]missing[/yellow]",
    }

    for item in items:
        if isinstance(item, CreatedItem):
            table.add_row(
                item.kind,
                str(item.path),
                status_styles.get(item.status, item.status),
                item.message,
            )
        else:  # LinkStatus
            target_str = str(item.target) if item.target else ""
            table.add_row(
                "symlink",
                item.name,
                status_styles.get(item.status, item.status),
                target_str,
            )

    console.print(table)
    console.print()
