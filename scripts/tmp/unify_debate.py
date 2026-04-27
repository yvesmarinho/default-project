#!/usr/bin/env python3
"""
Unifica os 2 arquivos do debate objetivo.yaml em um único documento.

Uso:
    python scripts/tmp/unify_debate.py
"""

from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)

# Caminhos
project_root = Path(__file__).resolve().parent.parent.parent
parte1 = project_root / "docs/debates/DEBATE-OBJETIVO-YAML-HUMAN-READABLE.md"
parte2 = project_root / "docs/debates/DEBATE-OBJETIVO-YAML-HUMAN-READABLE-PARTE2.md"
unified = project_root / "docs/debates/DEBATE-OBJETIVO-YAML-HUMAN-READABLE-COMPLETO.md"

def unify():
    """Unifica as 2 partes do debate em um único arquivo."""

    if not parte1.exists():
        log.error(f"Parte 1 não encontrada: {parte1}")
        return False

    if not parte2.exists():
        log.error(f"Parte 2 não encontrada: {parte2}")
        return False

    log.info(f"Lendo Parte 1: {parte1}")
    content_p1 = parte1.read_text(encoding="utf-8")

    log.info(f"Lendo Parte 2: {parte2}")
    content_p2 = parte2.read_text(encoding="utf-8")

    # Remove header da Parte 2 (primeira linha que referencia Parte 1)
    lines_p2 = content_p2.split("\n")

    # Encontra primeira linha que não é header/metadata
    start_idx = 0
    for i, line in enumerate(lines_p2):
        if line.startswith("## 2.4") or line.startswith("## 3.") or line.startswith("## 4."):
            start_idx = i
            break

    content_p2_clean = "\n".join(lines_p2[start_idx:])

    # Unifica
    unified_content = f"""{content_p1}

---

{content_p2_clean}
"""

    # Salva arquivo unificado
    unified.write_text(unified_content, encoding="utf-8")
    log.info(f"✅ Arquivo unificado criado: {unified}")
    log.info(f"   Tamanho: {len(unified_content)} caracteres")
    log.info(f"   Linhas: {len(unified_content.splitlines())} linhas")

    return True

if __name__ == "__main__":
    success = unify()
    exit(0 if success else 1)
