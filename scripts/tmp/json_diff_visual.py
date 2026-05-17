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


def analyze_duplicates_in_file(file_path: Path, data: dict) -> dict:
    """
    Analisa duplicações em arrays do arquivo JSON.

    Returns:
        Dict com estatísticas de duplicação
    """
    stats = {
        "total_arrays": 0,
        "arrays_with_duplicates": 0,
        "duplicates": []
    }

    def analyze_value(value, path=""):
        """Analisa recursivamente valores buscando arrays."""
        if isinstance(value, list):
            stats["total_arrays"] += 1

            # Detectar duplicados
            duplicates = {}
            for item in value:
                if isinstance(item, (str, int, float, bool)):
                    count = value.count(item)
                    if count > 1:
                        duplicates[str(item)] = count

            if duplicates:
                stats["arrays_with_duplicates"] += 1
                stats["duplicates"].append({
                    "path": path,
                    "array_size": len(value),
                    "unique_items": len(set(str(x) for x in value if isinstance(x, (str, int, float, bool)))),
                    "duplicates": duplicates
                })

        elif isinstance(value, dict):
            for key, val in value.items():
                new_path = f"{path}.{key}" if path else key
                analyze_value(val, new_path)

    analyze_value(data)
    return stats


def print_duplicate_analysis(file_path: Path, stats: dict):
    """Imprime relatório de análise de duplicações."""
    print("=" * 80)
    print(f"🔍 ANÁLISE DE DUPLICAÇÕES - Arquivo de Origem")
    print(f"   Arquivo: {file_path}")
    print("=" * 80)
    print()

    print(f"📊 Estatísticas Gerais:")
    print(f"   Total de arrays: {stats['total_arrays']}")
    print(f"   Arrays com duplicações: {stats['arrays_with_duplicates']}")

    if stats['arrays_with_duplicates'] > 0:
        print(f"   Taxa de duplicação: {stats['arrays_with_duplicates'] / stats['total_arrays'] * 100:.1f}%")

    print()

    if stats['duplicates']:
        print("🔴 Duplicações Encontradas:")
        print()

        for idx, dup_info in enumerate(stats['duplicates'], 1):
            print(f"   [{idx}] Path: {dup_info['path']}")
            print(f"       Tamanho do array: {dup_info['array_size']}")
            print(f"       Itens únicos: {dup_info['unique_items']}")
            print(f"       Elementos duplicados:")

            for item, count in dup_info['duplicates'].items():
                print(f"         • '{item}': {count} ocorrências (duplicado {count - 1}x)")

            print()
    else:
        print("✅ Nenhuma duplicação encontrada!")
        print()

    print("=" * 80)
    print()


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

    # Análise de duplicações no arquivo de origem
    stats = analyze_duplicates_in_file(file1, data1)
    print_duplicate_analysis(file1, stats)

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
