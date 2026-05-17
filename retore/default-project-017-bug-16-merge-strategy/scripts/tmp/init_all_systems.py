"""
Inicializa TODOS os sistemas de rastreamento após scaffold upgrade.

Sistemas inicializados:
  1. Session Index (.session-index/index.db)
  2. Session Time Tracker (.session-time/history.csv)
  3. Memory System (.memory/memories/)

Uso:
    python scripts/tmp/init_all_systems.py

Referência:
    - BUG-11: Session systems não inicializados
    - BUG-12: Memory system não inicializado
    - Ritual: .github/prompts/session-start-first.prompt.md Passos 8.1-8.4
"""
import subprocess
import sys
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(message)s"
)
log = logging.getLogger(__name__)


def run_script(script_path: Path, args: list[str] = None) -> bool:
    """Executa um script Python e retorna True se sucesso."""
    cmd = [sys.executable, str(script_path)]
    if args:
        cmd.extend(args)

    result = subprocess.run(
        cmd,
        cwd=script_path.parent.parent,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        if result.stdout:
            print(result.stdout)
        return True
    else:
        log.error("Erro: %s", result.stderr)
        return False


def main():
    project_root = Path(__file__).resolve().parent.parent.parent
    scripts_dir = project_root / "scripts"

    log.info("🚀 Inicializando sistemas de rastreamento...")
    log.info("   Projeto: %s", project_root.name)

    # 1. Session Index
    log.info("\n1️⃣  Session Index...")
    script = scripts_dir / "session-index.py"
    if not script.exists():
        log.error("   ❌ Script não encontrado: %s", script)
        sys.exit(1)

    if run_script(script, ["--rebuild"]):
        db_file = project_root / ".session-index" / "index.db"
        if db_file.exists():
            size_kb = db_file.stat().st_size / 1024
            log.info("   ✅ Criado: %s (%.1f KB)", db_file.name, size_kb)
    else:
        log.error("   ❌ Falha na inicialização")
        sys.exit(1)

    # 2. Session Time Tracker
    log.info("\n2️⃣  Session Time Tracker...")
    script = scripts_dir / "session-time-tracker.py"
    if not script.exists():
        log.error("   ❌ Script não encontrado: %s", script)
        sys.exit(1)

    # Start
    log.info("   ▶️  Iniciando sessão...")
    if not run_script(script, ["start"]):
        log.error("   ❌ Falha no start")
        sys.exit(1)

    # Stop (criar histórico)
    log.info("   ⏹️  Parando sessão...")
    if run_script(script, ["stop"]):
        csv_file = project_root / ".session-time" / "history.csv"
        if csv_file.exists():
            log.info("   ✅ Criado: %s", csv_file.name)
    else:
        log.error("   ❌ Falha no stop")
        sys.exit(1)

    # 3. Memory System
    log.info("\n3️⃣  Memory System...")
    script = scripts_dir / "create_memory_structure.py"
    if not script.exists():
        log.error("   ❌ Script não encontrado: %s", script)
        sys.exit(1)

    if run_script(script):
        memory_dir = project_root / ".memory" / "memories"
        if memory_dir.exists():
            subdirs = [d.name for d in memory_dir.iterdir() if d.is_dir()]
            log.info("   ✅ Criadas %d pastas: %s",
                     len(subdirs), ", ".join(subdirs))
    else:
        log.error("   ❌ Falha na inicialização")
        sys.exit(1)

    # Resumo final
    log.info("\n" + "="*60)
    log.info("✅ TODOS OS SISTEMAS INICIALIZADOS COM SUCESSO!")
    log.info("="*60)
    log.info("\n📋 Próximos passos:")
    log.info("  1. Executar 'MCP: Refresh Servers' no VS Code")
    log.info("  2. Atualizar docs/TODO.md com objetivos do projeto")
    log.info("  3. Declarar domínio e carregar Domain Profile")
    log.info("  4. Verificar symlinks: uv run scripts/scaffold.py --check")


if __name__ == "__main__":
    main()
