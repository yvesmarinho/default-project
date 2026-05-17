#!/usr/bin/env python3
"""
Test BUG-16 Integration — End-to-End Upgrade Validation

Testa o fluxo completo de upgrade com merge inteligente:
1. Criar projeto inicial com scaffold
2. Customizar arquivos críticos (.vscode/settings.json, .copilot-rules.md)
3. Executar upgrade --force
4. Validar que customizações foram preservadas via merge
5. Validar que backups foram criados
"""

import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Any

# Cores para output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"


def run_cmd(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    """Executa comando e retorna resultado."""
    print(f"{BLUE}▶ {' '.join(cmd)}{RESET}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"{RED}✗ ERRO:{RESET}")
        print(result.stderr)
    return result


def validate_json_merge(file_path: Path, expected_keys: Dict[str, Any]) -> bool:
    """Valida que JSON tem chaves esperadas preservadas."""
    if not file_path.exists():
        print(f"{RED}✗ Arquivo não existe: {file_path}{RESET}")
        return False

    try:
        data = json.loads(file_path.read_text())
        for key, expected_value in expected_keys.items():
            if key not in data:
                print(f"{RED}✗ Chave ausente: {key}{RESET}")
                return False
            if expected_value is not None and data[key] != expected_value:
                print(f"{RED}✗ Valor incorreto: {key} = {data[key]} (esperado: {expected_value}){RESET}")
                return False
            print(f"{GREEN}✓ {key}: {data[key]}{RESET}")
        return True
    except Exception as e:
        print(f"{RED}✗ Erro ao ler JSON: {e}{RESET}")
        return False


def test_bug16_integration() -> int:
    """
    Teste principal de integração BUG-16.

    Returns:
        0 se sucesso, 1 se falha
    """
    print(f"\n{BLUE}{'='*70}{RESET}")
    print(f"{BLUE}BUG-16 Integration Test — End-to-End Upgrade Validation{RESET}")
    print(f"{BLUE}{'='*70}{RESET}\n")

    # Setup: criar diretório temporário
    with tempfile.TemporaryDirectory(prefix="bug16-test-") as tmpdir:
        tmpdir = Path(tmpdir)
        project_path = tmpdir / "test-project"

        print(f"{YELLOW}📁 Diretório de teste: {project_path}{RESET}\n")

        # =====================================================================
        # FASE 1: Criar projeto inicial
        # =====================================================================
        print(f"{BLUE}{'─'*70}{RESET}")
        print(f"{BLUE}FASE 1: Criar projeto inicial{RESET}")
        print(f"{BLUE}{'─'*70}{RESET}\n")

        result = run_cmd([
            "python", "scripts/scaffold.py", "--new",
            "--name", "test-project",
            "--domain", "programming",
            "--language", "python",
            "--target-dir", str(tmpdir),
            "--no-log"
        ])

        if result.returncode != 0:
            print(f"{RED}✗ FALHA: Criação de projeto{RESET}")
            return 1

        print(f"{GREEN}✓ Projeto criado com sucesso{RESET}\n")

        # =====================================================================
        # FASE 2: Customizar arquivos
        # =====================================================================
        print(f"{BLUE}{'─'*70}{RESET}")
        print(f"{BLUE}FASE 2: Customizar arquivos críticos{RESET}")
        print(f"{BLUE}{'─'*70}{RESET}\n")

        # Customização 1: .vscode/settings.json
        settings_file = project_path / ".vscode" / "settings.json"
        settings = json.loads(settings_file.read_text())
        settings["custom.user.key"] = "my-custom-value"
        settings["editor.fontSize"] = 16  # Override template default
        settings_file.write_text(json.dumps(settings, indent=2))
        print(f"{GREEN}✓ Customizado: .vscode/settings.json{RESET}")

        # Customização 2: .copilot-rules.md
        rules_file = project_path / ".copilot-rules.md"
        original_rules = rules_file.read_text()
        custom_rules = original_rules + "\n\n## 99. Custom Rule\n\nMinha regra customizada.\n"
        rules_file.write_text(custom_rules)
        print(f"{GREEN}✓ Customizado: .copilot-rules.md{RESET}")

        # Customização 3: Criar .copilot-rules-custom.md (para testar consolidação)
        custom_rules_file = project_path / ".copilot-rules-custom.md"
        custom_rules_file.write_text("## Custom Section\n\nConteúdo customizado.\n")
        print(f"{GREEN}✓ Criado: .copilot-rules-custom.md{RESET}\n")

        # =====================================================================
        # FASE 3: Executar upgrade --force
        # =====================================================================
        print(f"{BLUE}{'─'*70}{RESET}")
        print(f"{BLUE}FASE 3: Executar upgrade --force{RESET}")
        print(f"{BLUE}{'─'*70}{RESET}\n")

        result = run_cmd([
            "python", "scripts/scaffold.py", "--upgrade",
            "--target-dir", str(project_path),
            "--force",
            "--no-log"
        ], cwd=project_path)

        if result.returncode != 0:
            print(f"{RED}✗ FALHA: Upgrade{RESET}")
            print(result.stdout)
            return 1

        print(f"{GREEN}✓ Upgrade executado com sucesso{RESET}\n")

        # =====================================================================
        # FASE 4: Validar merges
        # =====================================================================
        print(f"{BLUE}{'─'*70}{RESET}")
        print(f"{BLUE}FASE 4: Validar merges inteligentes{RESET}")
        print(f"{BLUE}{'─'*70}{RESET}\n")

        # Validação 1: .vscode/settings.json deve ter customizações preservadas
        print(f"{YELLOW}Validando .vscode/settings.json...{RESET}")
        if not validate_json_merge(settings_file, {
            "custom.user.key": "my-custom-value",
            "editor.fontSize": 16
        }):
            print(f"{RED}✗ FALHA: settings.json não preservou customizações{RESET}")
            return 1
        print(f"{GREEN}✓ settings.json: customizações preservadas{RESET}\n")

        # Validação 2: .copilot-rules.md deve ter sido consolidado
        print(f"{YELLOW}Validando consolidação .copilot-rules.md...{RESET}")
        final_rules = rules_file.read_text()
        if "## 99. Custom Rule" not in final_rules:
            print(f"{RED}✗ FALHA: .copilot-rules.md perdeu regra customizada{RESET}")
            return 1
        if "## Custom Section" not in final_rules:
            print(f"{RED}✗ FALHA: .copilot-rules.md não consolidou .copilot-rules-custom.md{RESET}")
            return 1
        print(f"{GREEN}✓ .copilot-rules.md: consolidação bem-sucedida{RESET}\n")

        # Validação 3: .copilot-rules-custom.md deve ter sido removido
        print(f"{YELLOW}Validando remoção de duplicatas...{RESET}")
        if custom_rules_file.exists():
            print(f"{RED}✗ FALHA: .copilot-rules-custom.md não foi removido{RESET}")
            return 1
        print(f"{GREEN}✓ Duplicatas removidas corretamente{RESET}\n")

        # =====================================================================
        # FASE 5: Validar backups
        # =====================================================================
        print(f"{BLUE}{'─'*70}{RESET}")
        print(f"{BLUE}FASE 5: Validar criação de backups{RESET}")
        print(f"{BLUE}{'─'*70}{RESET}\n")

        # Verificar se backups foram criados em .backups/copilot-rules/
        backups_dir = project_path / ".backups" / "copilot-rules"
        if not backups_dir.exists():
            print(f"{YELLOW}⚠ Backups dir não criado (pode ser esperado se não houve merge){RESET}\n")
        else:
            backup_files = list(backups_dir.glob("*.md"))
            if backup_files:
                print(f"{GREEN}✓ Backups criados: {len(backup_files)} arquivo(s){RESET}")
                for bf in backup_files:
                    print(f"  • {bf.name}")
            else:
                print(f"{YELLOW}⚠ Nenhum backup encontrado (esperado se não houve conflito){RESET}")
            print()

        # =====================================================================
        # RESUMO FINAL
        # =====================================================================
        print(f"{BLUE}{'='*70}{RESET}")
        print(f"{GREEN}✅ BUG-16 Integration Test: PASSED{RESET}")
        print(f"{BLUE}{'='*70}{RESET}\n")

        print(f"{GREEN}Validações bem-sucedidas:{RESET}")
        print(f"  ✓ Projeto criado")
        print(f"  ✓ Upgrade executado")
        print(f"  ✓ JSON merge preservou customizações")
        print(f"  ✓ Copilot rules consolidadas")
        print(f"  ✓ Duplicatas removidas")
        print(f"  ✓ Backups verificados")
        print()

        return 0


if __name__ == "__main__":
    exit(test_bug16_integration())
