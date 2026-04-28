"""flow_objetivo_init — inicializa arquivo objetivo.yaml via wizard ou template."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ..objetivo_wizard import ObjetivoWizard, WizardAnswers
from ..ui import console


def flow_objetivo_init(args: argparse.Namespace) -> int:
    """Inicializa arquivo objetivo.yaml.

    Modos:
    - Interactive (default): Run wizard interativo
    - Non-interactive (--from-file): Read answers from JSON
    - Template copy (--template-only): Copy template sem perguntas

    Args:
        args: Namespace with:
            - interactive: Interactive wizard mode (default True)
            - from_file: Path to JSON with answers (non-interactive mode)
            - template_only: Just copy template without wizard
            - output: Output path (default: objetivo.yaml)

    Returns:
        Exit code: 0 se sucesso, 1 se erro
    """
    output_path = Path(getattr(args, "output", None) or "objetivo.yaml")

    # Check if file already exists
    if output_path.exists():
        response = input(f"\n⚠️  {output_path} já existe. Sobrescrever? [y/N]: ").strip().lower()
        if response not in ['y', 'yes', 's', 'sim']:
            console.print("\n  [yellow]Cancelado.[/yellow]\n")
            return 1

    # Mode 1: Non-interactive from JSON file
    from_file = getattr(args, "from_file", None)
    if from_file:
        try:
            with open(from_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            answers = WizardAnswers.from_dict(data)
            wizard = ObjetivoWizard()
            return wizard.run_non_interactive(answers, output_path)

        except FileNotFoundError:
            console.print(f"\n  [bold red]❌ Erro:[/bold red] Arquivo não encontrado: {from_file}\n")
            return 1
        except json.JSONDecodeError as e:
            console.print(f"\n  [bold red]❌ Erro JSON:[/bold red] {e}\n")
            return 1
        except Exception as e:
            console.print(f"\n  [bold red]❌ Erro:[/bold red] {e}\n")
            return 1

    # Mode 2: Template-only (copy without wizard)
    template_only = getattr(args, "template_only", False)
    if template_only:
        try:
            wizard = ObjetivoWizard()
            if not wizard.template_path.exists():
                console.print(f"\n  [bold red]❌ Erro:[/bold red] Template não encontrado: {wizard.template_path}\n")
                return 1

            import shutil
            shutil.copy2(wizard.template_path, output_path)

            console.print(f"\n  [green]✅ Template copiado:[/green] {output_path}")
            console.print("  [dim]Edite o arquivo e preencha os campos manualmente.[/dim]\n")
            return 0

        except Exception as e:
            console.print(f"\n  [bold red]❌ Erro:[/bold red] {e}\n")
            return 1

    # Mode 3: Interactive wizard (default)
    wizard = ObjetivoWizard()
    return wizard.run(output_path)
