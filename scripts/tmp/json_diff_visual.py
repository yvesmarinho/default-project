#!/usr/bin/env python3
"""
Diff visual de arquivos JSON mostrando duplicações em arrays.

Uso:
    json_diff_visual.py <arquivo1> <arquivo2>

Exemplos:
    json_diff_visual.py /tmp/mcp-clean.json tmp/evidencia/mcp.json
    json_diff_visual.py config.json config.json.backup
"""

import json
import sys
from pathlib import Path


def show_usage():
    """Mostra mensagem de uso."""
    print("Uso: json_diff_visual.py <arquivo1> <arquivo2>", file=sys.stderr)
    print("", file=sys.stderr)
    print("Compara dois arquivos JSON e mostra diferenças em arrays.", file=sys.stderr)
    print("", file=sys.stderr)
    print("Exemplos:", file=sys.stderr)
    print("  json_diff_visual.py config.json config.json.backup", file=sys.stderr)
    print("  json_diff_visual.py /tmp/original.json /tmp/modified.json", file=sys.stderr)
    sys.exit(1)


def compare_json_arrays(file1: Path, file2: Path):
    """Compara arrays em dois arquivos JSON e mostra diferenças."""
    
    try:
        data1 = json.loads(file1.read_text())
        data2 = json.loads(file2.read_text())
    except json.JSONDecodeError as e:
        print(f"❌ Erro ao parsear JSON: {e}", file=sys.stderr)
        sys.exit(2)
    except FileNotFoundError as e:
        print(f"❌ Arquivo não encontrado: {e}", file=sys.stderr)
        sys.exit(2)

    print("=" * 80)
    print(f"📊 DIFF VISUAL - Comparação de Arrays JSON")
    print(f"   Arquivo 1: {file1}")
    print(f"   Arquivo 2: {file2}")
    print("=" * 80)
    print()

    # Detectar estrutura (mcp.json vs genérico)
    if "servers" in data1 and "servers" in data2:
        compare_mcp_servers(data1, data2)
    else:
        compare_generic_json(data1, data2)


def compare_mcp_servers(data1: dict, data2: dict):
    """Compara servidores MCP especificamente."""
    for server_name in data1.get("servers", {}):
        if server_name not in data2.get("servers", {}):
            print(f"🔹 Servidor: {server_name}")
            print(f"   ⚠️  Ausente no arquivo 2")
            print()
            continue
        
        args1 = data1["servers"][server_name].get("args", [])
        args2 = data2["servers"][server_name].get("args", [])

        print(f"🔹 Servidor: {server_name}")
        print(f"   Arquivo 1: {args1}")
        print(f"   Arquivo 2: {args2}")

        if args1 != args2:
            print(f"   ⚠️  DIFERENÇA: {len(args2) - len(args1)} elementos extras")

            # Mostrar elementos duplicados
            extras = []
            for item in args2:
                if args2.count(item) > args1.count(item):
                    extras.append(item)

            if extras:
                print(f"   🔴 Duplicados: {set(extras)}")
        else:
            print(f"   ✅ IGUAIS")

        print()


def compare_generic_json(data1: dict, data2: dict):
    """Compara JSON genérico."""
    print("Arquivo 1:")
    print(json.dumps(data1, indent=2))
    print()
    print("Arquivo 2:")
    print(json.dumps(data2, indent=2))
    print()
    
    if data1 == data2:
        print("✅ Arquivos são IDÊNTICOS")
    else:
        print("⚠️  Arquivos são DIFERENTES")
        
        # Mostrar chaves diferentes
        keys1 = set(data1.keys())
        keys2 = set(data2.keys())
        
        only_in_1 = keys1 - keys2
        only_in_2 = keys2 - keys1
        
        if only_in_1:
            print(f"   Chaves apenas no arquivo 1: {only_in_1}")
        if only_in_2:
            print(f"   Chaves apenas no arquivo 2: {only_in_2}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        show_usage()
    
    file1 = Path(sys.argv[1])
    file2 = Path(sys.argv[2])
    
    if not file1.exists():
        print(f"❌ Arquivo não existe: {file1}", file=sys.stderr)
        sys.exit(2)
    
    if not file2.exists():
        print(f"❌ Arquivo não existe: {file2}", file=sys.stderr)
        sys.exit(2)

    compare_json_arrays(file1, file2)
