#!/usr/bin/env python3
"""
Teste de correção do bug de duplicação em mcp.json

Simula merge de arquivo mcp.json existente com template para verificar
se os argumentos não são duplicados.
"""

import sys
import json
from pathlib import Path

# Adicionar scripts ao path para importação de módulos
scripts_path = Path(__file__).parent.parent
sys.path.insert(0, str(scripts_path))

from lib.json_merge import VSCodeJSONMerger

def test_mcp_merge():
    """Testa merge sem duplicação de arrays."""

    # Template (base)
    template = {
        "servers": {
            "memory": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-memory"],
                "type": "stdio"
            },
            "sequential-thinking": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"],
                "type": "stdio"
            }
        }
    }

    # Arquivo existente (overlay/usuário) - mesmos valores
    overlay = {
        "servers": {
            "memory": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-memory"],
                "type": "stdio"
            },
            "sequential-thinking": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"],
                "type": "stdio"
            }
        }
    }

    # Executar merge
    merger = VSCodeJSONMerger()
    result = merger._merge_user_wins(template, overlay)

    # Verificar resultados
    print("=" * 70)
    print("TESTE: Merge de mcp.json (correção de duplicação)")
    print("=" * 70)
    print()

    print("Template (base):")
    print(json.dumps(template, indent=2))
    print()

    print("Overlay (usuário):")
    print(json.dumps(overlay, indent=2))
    print()

    print("Resultado do merge:")
    print(json.dumps(result, indent=2))
    print()

    # Validar que não houve duplicação
    memory_args = result["servers"]["memory"]["args"]
    expected_args = ["-y", "@modelcontextprotocol/server-memory"]

    if memory_args == expected_args:
        print("✅ SUCESSO: Args não duplicados!")
        print(f"   Esperado: {expected_args}")
        print(f"   Recebido: {memory_args}")
        return True
    else:
        print("❌ FALHA: Args duplicados!")
        print(f"   Esperado: {expected_args}")
        print(f"   Recebido: {memory_args}")
        return False

if __name__ == "__main__":
    success = test_mcp_merge()
    sys.exit(0 if success else 1)
