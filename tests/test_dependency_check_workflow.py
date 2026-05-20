"""
Testes para GitHub Actions dependency-check workflow e scripts auxiliares.

IMP-65 P1: GitHub Actions Dependency Check — CI/CD semanal para dependency checks

O workflow valida:
1. Executa semanalmente (segundas 9h UTC) e em PRs que modificam dependências
2. Verifica dependências desatualizadas (pip list --outdated)
3. Executa pip-audit para CVE scanning
4. Cria issues P0 automaticamente se vulnerabilidades encontradas
5. Upload de artifacts (outdated.json, audit.json)

Referência:
- .github/workflows/dependency-check.yml
- .github/scripts/process_outdated.py
- .github/scripts/process_audit.py
"""

import json
import subprocess
import tempfile
from pathlib import Path

import pytest
import yaml


def test_dependency_check_workflow_exists():
    """Verifica que o workflow dependency-check.yml existe."""
    workflow = Path(".github/workflows/dependency-check.yml")
    assert workflow.exists(), "Workflow dependency-check.yml não encontrado"


def test_dependency_check_workflow_valid_yaml():
    """Verifica que o workflow é um YAML válido."""
    workflow = Path(".github/workflows/dependency-check.yml")

    with open(workflow) as f:
        data = yaml.safe_load(f)

    assert data is not None, "Workflow YAML é vazio ou inválido"
    assert "name" in data, "Workflow não tem campo 'name'"
    assert data["name"] == "Dependency Check"


def test_dependency_check_workflow_has_schedule():
    """Verifica que o workflow tem schedule configurado."""
    workflow = Path(".github/workflows/dependency-check.yml")

    with open(workflow) as f:
        data = yaml.safe_load(f)

    # YAML parseia 'on' como boolean True, então acessamos por True
    triggers = data.get("on") or data.get(True)
    assert triggers is not None, "Workflow não tem triggers"
    assert "schedule" in triggers, "Workflow não tem schedule"

    schedule = triggers["schedule"]
    assert len(schedule) > 0, "Schedule está vazio"

    # Verificar cron (segundas 9h UTC)
    cron = schedule[0]["cron"]
    assert "0 9 * * MON" in cron, f"Schedule incorreto: {cron}"


def test_dependency_check_workflow_has_manual_trigger():
    """Verifica que o workflow permite trigger manual."""
    workflow = Path(".github/workflows/dependency-check.yml")

    with open(workflow) as f:
        data = yaml.safe_load(f)

    # YAML parseia 'on' como boolean True
    triggers = data.get("on") or data.get(True)
    assert triggers is not None, "Workflow não tem triggers"
    assert "workflow_dispatch" in triggers, "Workflow não tem workflow_dispatch"


def test_dependency_check_workflow_has_pr_trigger():
    """Verifica que o workflow roda em PRs que modificam dependências."""
    workflow = Path(".github/workflows/dependency-check.yml")

    with open(workflow) as f:
        data = yaml.safe_load(f)

    # YAML parseia 'on' como boolean True
    triggers = data.get("on") or data.get(True)
    assert triggers is not None, "Workflow não tem triggers"
    assert "pull_request" in triggers, "Workflow não tem trigger em PRs"

    pr_config = triggers["pull_request"]
    assert "paths" in pr_config, "PR trigger não tem filtro de paths"

    paths = pr_config["paths"]
    assert "pyproject.toml" in paths, "PR trigger não monitora pyproject.toml"
    assert any("requirements" in p for p in paths), "PR trigger não monitora requirements*.txt"


def test_dependency_check_workflow_has_permissions():
    """Verifica que o workflow tem permissões corretas."""
    workflow = Path(".github/workflows/dependency-check.yml")

    with open(workflow) as f:
        data = yaml.safe_load(f)

    assert "permissions" in data, "Workflow não tem permissões definidas"

    permissions = data["permissions"]
    assert permissions["contents"] == "read", "Permissão de contents incorreta"
    assert permissions["issues"] == "write", "Permissão de issues incorreta (necessário para criar issues)"


def test_dependency_check_workflow_has_main_job():
    """Verifica que o workflow tem job principal."""
    workflow = Path(".github/workflows/dependency-check.yml")

    with open(workflow) as f:
        data = yaml.safe_load(f)

    assert "jobs" in data, "Workflow não tem jobs"
    assert "check-dependencies" in data["jobs"], "Job check-dependencies não encontrado"

    job = data["jobs"]["check-dependencies"]
    assert job["runs-on"] == "ubuntu-latest", "Job não usa ubuntu-latest"


def test_dependency_check_workflow_has_steps():
    """Verifica que o workflow tem steps corretos."""
    workflow = Path(".github/workflows/dependency-check.yml")

    with open(workflow) as f:
        data = yaml.safe_load(f)

    job = data["jobs"]["check-dependencies"]
    steps = job["steps"]

    # Verificar que tem pelo menos 6 steps
    assert len(steps) >= 6, f"Job tem apenas {len(steps)} steps (esperado >= 6)"

    # Verificar step names
    step_names = [step.get("name", "") for step in steps]

    assert any("Checkout" in name for name in step_names), "Sem step de checkout"
    assert any("Setup Python" in name or "Python" in name for name in step_names), "Sem step de setup Python"
    assert any("pip-audit" in name for name in step_names), "Sem step de pip-audit"
    assert any("desatualizadas" in name.lower() or "outdated" in name.lower() for name in step_names), "Sem step de dependências desatualizadas"
    assert any("artifact" in name.lower() for name in step_names), "Sem step de upload artifacts"
    assert any("issue" in name.lower() for name in step_names), "Sem step de criação de issues"


def test_process_outdated_script_exists():
    """Verifica que o script process_outdated.py existe."""
    script = Path(".github/scripts/process_outdated.py")
    assert script.exists(), "Script process_outdated.py não encontrado"


def test_process_outdated_script_executable():
    """Verifica que o script process_outdated.py tem shebang correto."""
    script = Path(".github/scripts/process_outdated.py")

    with open(script) as f:
        first_line = f.readline()

    assert first_line.startswith("#!"), "Script não tem shebang"
    assert "python" in first_line.lower(), "Shebang não referencia python"


def test_process_outdated_script_processes_json():
    """Verifica que process_outdated.py processa JSON corretamente."""
    script = Path(".github/scripts/process_outdated.py").absolute()

    # Criar JSON temporário
    test_data = [
        {"name": "package1", "version": "1.0.0", "latest_version": "2.0.0"},
        {"name": "package2", "version": "0.5.0", "latest_version": "0.9.0"}
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        json_file = tmpdir_path / "outdated.json"

        with open(json_file, "w") as f:
            json.dump(test_data, f)

        # Executar script
        result = subprocess.run(
            ["python3", str(script)],
            cwd=tmpdir_path,
            capture_output=True,
            text=True
        )

        # Verificar se houve erro
        if result.returncode != 0:
            pytest.fail(f"Script falhou: {result.stderr}")

        if not result.stdout.strip():
            pytest.fail(f"Script não retornou output. stderr: {result.stderr}")

        lines = result.stdout.strip().split("\n")

        # Primeira linha deve ser a contagem
        assert lines[0] == "2", f"Contagem incorreta: {lines[0]}"

        # Linhas seguintes devem ser tabela markdown
        assert "package1" in lines[1]
        assert "1.0.0" in lines[1]
        assert "2.0.0" in lines[1]


def test_process_audit_script_exists():
    """Verifica que o script process_audit.py existe."""
    script = Path(".github/scripts/process_audit.py")
    assert script.exists(), "Script process_audit.py não encontrado"


def test_process_audit_script_executable():
    """Verifica que o script process_audit.py tem shebang correto."""
    script = Path(".github/scripts/process_audit.py")

    with open(script) as f:
        first_line = f.readline()

    assert first_line.startswith("#!"), "Script não tem shebang"
    assert "python" in first_line.lower(), "Shebang não referencia python"


def test_process_audit_script_processes_json_no_vulns():
    """Verifica que process_audit.py processa JSON sem vulnerabilidades."""
    script = Path(".github/scripts/process_audit.py").absolute()

    # Criar JSON temporário sem vulnerabilidades
    test_data = {"vulnerabilities": []}

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        json_file = tmpdir / "audit.json"

        with open(json_file, "w") as f:
            json.dump(test_data, f)

        # Executar script
        result = subprocess.run(
            ["python3", str(script)],
            cwd=tmpdir,
            capture_output=True,
            text=True
        )

        # Deve retornar exit code 0 (sem vulnerabilidades)
        assert result.returncode == 0, "Script falhou sem vulnerabilidades"

        # Deve criar vuln_count.txt com 0
        vuln_count_file = tmpdir / "vuln_count.txt"
        assert vuln_count_file.exists(), "vuln_count.txt não criado"

        with open(vuln_count_file) as f:
            count = f.read().strip()

        assert count == "0", f"Contagem incorreta: {count}"


def test_process_audit_script_processes_json_with_vulns():
    """Verifica que process_audit.py processa JSON com vulnerabilidades."""
    script = Path(".github/scripts/process_audit.py").absolute()

    # Criar JSON temporário com vulnerabilidades
    test_data = {
        "vulnerabilities": [
            {
                "name": "vulnerable-package",
                "id": "CVE-2024-1234",
                "fix_versions": ["2.0.0"]
            },
            {
                "name": "another-package",
                "id": "CVE-2024-5678",
                "fix_versions": []
            }
        ]
    }

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        json_file = tmpdir / "audit.json"

        with open(json_file, "w") as f:
            json.dump(test_data, f)

        # Executar script
        result = subprocess.run(
            ["python3", str(script)],
            cwd=tmpdir,
            capture_output=True,
            text=True
        )

        # Deve retornar exit code 1 (vulnerabilidades encontradas)
        assert result.returncode == 1, "Script não falhou com vulnerabilidades"

        # Deve criar vuln_count.txt com contagem
        vuln_count_file = tmpdir / "vuln_count.txt"
        assert vuln_count_file.exists(), "vuln_count.txt não criado"

        with open(vuln_count_file) as f:
            count = f.read().strip()

        assert count == "2", f"Contagem incorreta: {count}"

        # Deve mencionar vulnerabilidades críticas
        assert "Vulnerabilidades Críticas" in result.stderr or "vulnerabilidade" in result.stderr.lower()


def test_dependency_check_workflow_creates_artifacts():
    """Verifica que o workflow cria artifacts."""
    workflow = Path(".github/workflows/dependency-check.yml")

    with open(workflow) as f:
        data = yaml.safe_load(f)

    job = data["jobs"]["check-dependencies"]
    steps = job["steps"]

    # Encontrar step de upload artifacts
    artifact_step = None
    for step in steps:
        if "upload-artifact" in step.get("uses", ""):
            artifact_step = step
            break

    assert artifact_step is not None, "Step de upload artifacts não encontrado"

    # Verificar configuração
    with_config = artifact_step["with"]
    assert with_config["name"] == "dependency-reports", "Nome do artifact incorreto"

    # Verificar que inclui outdated.json e audit.json
    path = with_config["path"]
    if isinstance(path, str):
        paths = [path]
    else:
        paths = path

    assert any("outdated.json" in p for p in paths), "outdated.json não incluído"
    assert any("audit.json" in p for p in paths), "audit.json não incluído"


def test_dependency_check_workflow_creates_issues():
    """Verifica que o workflow cria issues P0 para vulnerabilidades."""
    workflow = Path(".github/workflows/dependency-check.yml")

    with open(workflow) as f:
        content = f.read()

    # Verificar que usa github-script para criar issues
    assert "actions/github-script" in content, "Workflow não usa github-script para criar issues"

    # Verificar que cria issues com labels corretos
    assert "'security'" in content, "Issue não tem label 'security'"
    assert "'dependencies'" in content, "Issue não tem label 'dependencies'"
    assert "'P0'" in content, "Issue não tem label 'P0'"

    # Verificar que menciona vulnerabilidades
    assert "Vulnerabilidades" in content or "vulnerabilidade" in content.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
