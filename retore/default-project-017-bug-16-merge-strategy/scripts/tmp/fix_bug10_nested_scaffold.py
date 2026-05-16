"""
BUG-10: Correção de Projeto Scaffold Aninhado

Problema: /teste_projetos/ contém arquivos de scaffold + subpasta sistema-deploy-automatizado/
também com arquivos de scaffold, criando estrutura aninhada incorreta.

Solução: Remover arquivos de scaffold de /teste_projetos/ (raiz), mantendo apenas
os do projeto correto em /teste_projetos/sistema-deploy-automatizado/

Este script:
1. Identifica arquivos/pastas de scaffold na raiz (teste_projetos/)
2. Move arquivos úteis (mcp-questions.yaml, objetivo.yaml) para o projeto correto
3. Remove arquivos de scaffold duplicados da raiz
4. Mantém apenas o projeto sistema-deploy-automatizado/ intacto
"""

import shutil
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)

# Diretórios
root = Path("/home/yves_marinho/Documentos/DevOps/teste_projetos")
project = root / "sistema-deploy-automatizado"

# Arquivos/pastas de scaffold a remover da raiz
SCAFFOLD_ITEMS_TO_REMOVE = [
    ".scaffold-state.yaml",
    ".copilot-rules-sistema-deploy-automatizado.md",
    ".copilot-rules.md",  # se existir
    ".git-hooks",
    ".github",
    ".gitignore",  # será recriado se necessário
    ".secrets",
    ".specify",
    ".vscode",
    "Makefile",
    "README.md",  # remover apenas se duplicado
    "SECURITY.md",
    "docs",
    "scripts",
    "src",
    ".memory",
    ".session-index",
    ".session-time",
    "tmp",
    "sistema-deploy-automatizado.code-workspace",  # duplicado
]

# Arquivos úteis a mover (não remover)
FILES_TO_MOVE = [
    "mcp-questions.yaml",
    "objetivo.yaml",
    "pyproject.toml",  # se não existir no projeto
    "uv.lock",  # se não existir no projeto
]

# NÃO TOCAR
KEEP_IN_ROOT = [
    ".git",  # repositório git
    ".venv",  # ambiente virtual
]


def main():
    log.info("🔍 Analisando estrutura...")

    # Verificar se projeto existe
    if not project.exists():
        log.error(f"❌ Projeto não encontrado: {project}")
        return 1

    # Verificar se raiz tem .scaffold-state.yaml (confirma duplicação)
    root_state = root / ".scaffold-state.yaml"
    if not root_state.exists():
        log.info("✅ Raiz não tem .scaffold-state.yaml - nenhuma duplicação detectada")
        return 0

    log.warning(f"⚠️  DUPLICAÇÃO DETECTADA: {root_state} existe")

    # Listar itens a processar
    items_to_remove = []
    items_to_move = []

    for item_name in SCAFFOLD_ITEMS_TO_REMOVE:
        item = root / item_name
        if item.exists():
            items_to_remove.append(item)
            log.info(f"  🗑️  Para remover: {item.name}")

    for file_name in FILES_TO_MOVE:
        src_file = root / file_name
        dst_file = project / file_name

        if src_file.exists() and not dst_file.exists():
            items_to_move.append((src_file, dst_file))
            log.info(f"  📦 Para mover: {file_name} → projeto/")
        elif src_file.exists() and dst_file.exists():
            log.info(f"  ⏭️  Já existe no projeto: {file_name}")
        else:
            log.info(f"  ⏭️  Não encontrado: {file_name}")

    # Confirmar com usuário
    print("\n" + "=" * 70)
    print(f"📋 RESUMO DA OPERAÇÃO:")
    print(f"   Remover {len(items_to_remove)} itens de: {root}/")
    print(f"   Mover {len(items_to_move)} arquivos para: {project}/")
    print("=" * 70)

    if items_to_remove:
        print("\n🗑️  Itens a REMOVER:")
        for item in items_to_remove:
            print(f"   - {item.relative_to(root)}")

    if items_to_move:
        print("\n📦 Arquivos a MOVER:")
        for src, dst in items_to_move:
            print(f"   - {src.name} → {dst.relative_to(root)}")

    print("\n⚠️  ATENÇÃO: Esta operação irá DELETAR arquivos!")
    response = input("\nProsseguir? (y/N): ")

    if response.lower() != 'y':
        log.warning("❌ Operação cancelada pelo usuário")
        return 1

    # Executar: Mover arquivos primeiro
    errors = []
    for src, dst in items_to_move:
        try:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))
            log.info(f"✅ Movido: {src.name} → {dst.relative_to(root)}")
        except Exception as e:
            log.error(f"❌ Erro ao mover {src.name}: {e}")
            errors.append(str(src))

    # Executar: Remover itens de scaffold
    for item in items_to_remove:
        try:
            if item.is_dir():
                shutil.rmtree(item)
                log.info(f"✅ Removido diretório: {item.name}/")
            else:
                item.unlink()
                log.info(f"✅ Removido arquivo: {item.name}")
        except Exception as e:
            log.error(f"❌ Erro ao remover {item.name}: {e}")
            errors.append(str(item))

    if errors:
        log.error(f"\n❌ {len(errors)} erro(s) durante a operação:")
        for err in errors:
            log.error(f"   - {err}")
        return 1

    log.info("\n🟢 Limpeza concluída com sucesso!")
    log.info(f"   Projeto correto mantido em: {project}/")

    return 0


if __name__ == "__main__":
    exit(main())
