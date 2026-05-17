#!/usr/bin/env python3
"""
Script para remover duplicações em arrays de arquivos JSON.

Uso:
    python scripts/tmp/fix-json-duplications.py <arquivo-ou-diretório>
    python scripts/tmp/fix-json-duplications.py .  # Todo o projeto
    python scripts/tmp/fix-json-duplications.py .vscode/extensions.json  # Arquivo específico
"""

import json
from pathlib import Path
from collections import Counter
import logging
import sys

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)


def remove_duplicates_from_arrays(data):
    """Remove duplicações em arrays, preservando ordem da primeira ocorrência."""
    if isinstance(data, dict):
        return {k: remove_duplicates_from_arrays(v) for k, v in data.items()}
    elif isinstance(data, list):
        # Preservar ordem: primeira ocorrência
        seen = set()
        unique = []
        for item in data:
            # Usar JSON string como chave (funciona para primitivos e objetos)
            key = json.dumps(item, sort_keys=True) if isinstance(item, (dict, list)) else item
            if key not in seen:
                seen.add(key)
                unique.append(remove_duplicates_from_arrays(item))
        return unique
    else:
        return data


def fix_json_file(file_path: Path) -> bool:
    """Remove duplicações de um arquivo JSON."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Backup
        backup = file_path.with_suffix(file_path.suffix + ".backup")
        with open(backup, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # Fix
        fixed = remove_duplicates_from_arrays(data)

        # Salvar se mudou
        if json.dumps(fixed, sort_keys=True) != json.dumps(data, sort_keys=True):
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(fixed, f, indent=2, ensure_ascii=False)
                f.write("\n")
            log.info(f"✅ Fixed: {file_path} (backup: {backup.name})")
            return True
        else:
            backup.unlink()  # Sem mudanças, remover backup
            log.info(f"✨ OK: {file_path} (sem duplicações)")
            return False

    except Exception as e:
        log.error(f"❌ Error in {file_path}: {e}")
        return False


if __name__ == "__main__":
    # Aceitar arquivo ou diretório
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")

    if target.is_file():
        files = [target]
    else:
        files = list(target.rglob("*.json"))
        # Filtrar arquivos ignorados
        files = [f for f in files if ".git" not in f.parts and "node_modules" not in f.parts]

    log.info(f"🔍 Scanning {len(files)} JSON files...")

    fixed_count = 0
    for file in sorted(files):
        if fix_json_file(file):
            fixed_count += 1

    log.info(f"✅ Completed: {fixed_count} files fixed, {len(files)-fixed_count} already clean")
