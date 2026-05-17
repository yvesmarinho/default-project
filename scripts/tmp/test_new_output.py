#!/usr/bin/env python3
"""
Teste de demonstração da nova saída agrupada por pasta.

Executa um mock do print_final_summary para mostrar a saída melhorada.
"""

from pathlib import Path
import sys

# Adicionar path para importar módulos
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.lib.config import CreatedItem, LinkStatus
from scripts.lib.ui import print_final_summary

def main():
    """Demonstra a nova saída agrupada por pasta."""

    # Criar mock de itens criados/operados
    test_project = Path("/tmp/test-scaffold-demo")

    items = [
        # Root files (CreatedItem: path, kind, status, message)
        CreatedItem(test_project / ".gitignore", "file", "created", "Template default"),
        CreatedItem(test_project / "README.md", "file", "created", "Project documentation"),
        CreatedItem(test_project / "Makefile", "file", "created", "Build automation"),
        CreatedItem(test_project / "pyproject.toml", "file", "created", "Python dependencies"),

        # .vscode
        CreatedItem(test_project / ".vscode/settings.json", "file", "created", "Merged with user customizations"),
        CreatedItem(test_project / ".vscode/mcp.json", "file", "created", "MCP server configuration"),
        CreatedItem(test_project / ".vscode/extensions.json", "file", "skipped", "Already exists"),

        # docs
        CreatedItem(test_project / "docs/INDEX.md", "file", "created", "Documentation index"),
        CreatedItem(test_project / "docs/TODO.md", "file", "created", "Project TODO list"),
        CreatedItem(test_project / "docs/guides/UPGRADE_GUIDE.md", "file", "created", "Upgrade instructions"),

        # scripts
        CreatedItem(test_project / "scripts/scaffold.py", "file", "created", "Scaffold CLI"),
        CreatedItem(test_project / "scripts/lib/project.py", "file", "created", "Project utilities"),

        # Symlinks
        LinkStatus(".copilot-rules.md", Path("/shared/.copilot-rules.md"), "ok"),
        LinkStatus(".copilot-actions.md", Path("/shared/.copilot-actions.md"), "ok"),
    ]

    # Criar diretório de teste
    test_project.mkdir(exist_ok=True)

    print("\n" + "="*80)
    print("DEMONSTRAÇÃO 1: Nova Saída Agrupada por Pasta (log padrão)")
    print("="*80 + "\n")

    # Exibir com logging habilitado
    print_final_summary(items, project_path=test_project, save_log=True)

    print("\n" + "="*80)
    print("DEMONSTRAÇÃO 2: Saída com Log Customizado (--log-dir)")
    print("="*80 + "\n")

    # Criar diretório customizado
    custom_log_dir = Path("/tmp/custom-scaffold-logs")
    custom_log_dir.mkdir(exist_ok=True)

    # Exibir com diretório customizado
    print_final_summary(items, project_path=test_project, save_log=True, log_dir=custom_log_dir)

    print("\n" + "="*80)
    print("DEMONSTRAÇÃO 3: Saída Sem Logging (--no-log)")
    print("="*80 + "\n")

    # Exibir sem logging
    print_final_summary(items, project_path=test_project, save_log=False)

    print("\n" + "="*80)
    print("Logs salvos em:")
    print("  - Padrão: logs/scaffold_<timestamp>.log")
    print("  - Customizado: /tmp/custom-scaffold-logs/scaffold_<timestamp>.log")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
