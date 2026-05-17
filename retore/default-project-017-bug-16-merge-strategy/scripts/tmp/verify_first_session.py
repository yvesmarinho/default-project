"""
Verifica conformidade do ritual Session Start (First Time).

Baseado no checklist de .github/prompts/session-start-first.prompt.md

Uso:
    python scripts/tmp/verify_first_session.py
"""
import sys
from pathlib import Path


def check_file_exists(path: Path, desc: str) -> bool:
    """Verifica se arquivo existe."""
    exists = path.exists()
    symbol = "✅" if exists else "❌"
    print(f"  {symbol} {desc}: {path.name}")
    return exists


def check_dir_exists(path: Path, desc: str) -> bool:
    """Verifica se diretório existe."""
    exists = path.is_dir()
    symbol = "✅" if exists else "❌"
    print(f"  {symbol} {desc}")
    return exists


def main():
    project_root = Path(__file__).resolve().parent.parent.parent
    print(f"📊 Verificando conformidade: {project_root.name}\n")

    score = 0
    total = 0

    # 1. Infraestrutura
    print("1️⃣  Infraestrutura")

    total += 1
    if check_file_exists(project_root / ".venv" / "pyvenv.cfg", "Ambiente virtual"):
        score += 1

    total += 1
    if check_file_exists(project_root / ".vscode" / "mcp.json", "MCP config"):
        score += 1

    total += 1
    if check_file_exists(project_root / ".gitignore", ".gitignore"):
        score += 1

    total += 1
    if check_file_exists(project_root / ".copilot-rules.md", ".copilot-rules.md"):
        score += 1

    # 2. Sistemas de Rastreamento
    print("\n2️⃣  Sistemas de Rastreamento")

    total += 1
    if check_file_exists(project_root / ".session-index" / "index.db", "Session Index DB"):
        score += 1

    total += 1
    if check_file_exists(project_root / ".session-time" / "history.csv", "Session Time CSV"):
        score += 1

    total += 1
    if check_dir_exists(project_root / ".memory" / "memories", "Memory System"):
        score += 1

    # 3. Scripts
    print("\n3️⃣  Scripts de Rastreamento")

    scripts = [
        "session-index.py",
        "session-time-tracker.py",
        "create_memory_structure.py",
    ]

    for script_name in scripts:
        total += 1
        if check_file_exists(project_root / "scripts" / script_name, f"Script: {script_name}"):
            score += 1

    # 4. Documentação
    print("\n4️⃣  Documentação de Sessão")

    from datetime import date
    today = date.today().strftime("%Y-%m-%d")
    session_dir = project_root / "docs" / "SESSIONS" / today

    total += 1
    if check_dir_exists(session_dir, f"docs/SESSIONS/{today}/"):
        score += 1

        total += 1
        if check_file_exists(session_dir / f"SESSION_RECOVERY_{today}.md", "SESSION_RECOVERY"):
            score += 1

        total += 1
        if check_file_exists(session_dir / f"DAILY_ACTIVITIES_{today}.md", "DAILY_ACTIVITIES"):
            score += 1
    else:
        total += 2  # conta SESSION_RECOVERY e DAILY_ACTIVITIES como falhas

    # 5. Segurança
    print("\n5️⃣  Segurança")

    total += 1
    if check_dir_exists(project_root / ".secrets", ".secrets/"):
        score += 1

    total += 1
    if check_file_exists(project_root / ".git-hooks" / "pre-commit.secrets", "Git hook de segurança"):
        score += 1

    # Resultado
    pct = (score / total) * 100
    print("\n" + "="*60)
    print(f"📊 Score: {score}/{total} ({pct:.0f}%)")
    print("="*60)

    if pct == 100:
        print("✅ CONFORMIDADE TOTAL — Session Start (First Time) completo!")
        return 0
    elif pct >= 80:
        print("🟡 PARCIALMENTE CONFORME — Alguns itens pendentes")
        return 1
    else:
        print("❌ NÃO CONFORME — Múltiplos itens críticos ausentes")
        return 2


if __name__ == "__main__":
    sys.exit(main())
