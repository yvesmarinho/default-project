"""
JSON and Workspace Merge System

Sistema de merge inteligente para arquivos JSON e .code-workspace.
Implementa estratégia user-wins com deep merge de estruturas aninhadas.

Bug fix: BUG-16 (P1 - JSON/workspace não mergeados, customizações perdidas)
Implementação: Sprint 2026-W21 (Fase 1 e 2)
"""

from pathlib import Path
from typing import Any, Dict, List
import json
import logging

from .config import CreatedItem

log = logging.getLogger(__name__)


# =============================================================================
# JSON Deep Merge Utilities
# =============================================================================

def deep_merge_json(base: Dict[str, Any], overlay: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deep merge com estratégia user-wins SEM union de arrays.

    Mudança arquitetural (v2.0): JSON é padrão de configuração no projeto.
    Todos os JSONs devem usar user-wins sem duplicação de arrays.

    Estratégia:
    - Overlay (usuário) sobrescreve base (template)
    - Arrays substituídos completamente (NÃO faz union)
    - Objetos aninhados mergeados recursivamente
    - Chaves novas do template são adicionadas

    Histórico:
    - v1.0: Usava always_merger.merge() (union de arrays) ❌ BUG
    - v2.0: Implementa user-wins sem union ✅ FIX ARQUITETURAL

    Args:
        base: Template (upstream)
        overlay: Usuário (customizações)

    Returns:
        Dicionário mergeado com estratégia user-wins

    Exemplos:
        >>> base = {"a": 1, "b": {"c": 2}}
        >>> overlay = {"b": {"d": 3}, "e": 4}
        >>> deep_merge_json(base, overlay)
        {'a': 1, 'b': {'c': 2, 'd': 3}, 'e': 4}

        >>> base = {"list": [1, 2]}
        >>> overlay = {"list": [3, 4]}
        >>> deep_merge_json(base, overlay)
        {'list': [3, 4]}  # User array wins, NÃO faz union
    """
    return _merge_user_wins_recursive(base, overlay)


def _merge_user_wins_recursive(base: Dict, overlay: Dict) -> Dict:
    """
    Implementação do merge user-wins recursivo.

    Algoritmo:
    1. Copiar todos valores do overlay (user wins)
    2. Para objetos aninhados: merge recursivo
    3. Adicionar chaves novas do base que não existem no overlay

    Comportamento por tipo:
    - Primitivos: overlay wins
    - Arrays: overlay wins (NÃO faz union)
    - Objects: merge recursivo

    Args:
        base: Template
        overlay: Usuário

    Returns:
        Dicionário mergeado
    """
    merged = {}

    # Passo 1: User wins - copiar tudo do overlay
    for key, overlay_value in overlay.items():
        base_value = base.get(key)

        # Se ambos são dicts, merge recursivo
        if isinstance(overlay_value, dict) and isinstance(base_value, dict):
            merged[key] = _merge_user_wins_recursive(base_value, overlay_value)
        else:
            # Primitivos e arrays: user wins completamente
            merged[key] = overlay_value

    # Passo 2: Adicionar chaves novas do template
    for key, base_value in base.items():
        if key not in merged:
            merged[key] = base_value

    return merged


def load_json_safe(file_path: Path) -> Dict[str, Any]:
    """
    Carrega arquivo JSON com tratamento de erros.

    Args:
        file_path: Caminho do arquivo JSON

    Returns:
        Dict parsed ou {} se erro

    Raises:
        ValueError: Se JSON inválido
    """
    try:
        content = file_path.read_text(encoding="utf-8")
        return json.loads(content)
    except json.JSONDecodeError as e:
        log.error(f"❌ JSON inválido em {file_path.name}: {e}")
        raise ValueError(f"JSON inválido: {e}") from e
    except Exception as e:
        log.error(f"❌ Erro ao ler {file_path.name}: {e}")
        raise


def save_json_formatted(file_path: Path, data: Dict[str, Any]) -> None:
    """
    Salva JSON com formatação consistente.

    Args:
        file_path: Caminho do arquivo JSON
        data: Dados a serem salvos
    """
    content = json.dumps(data, indent=2, ensure_ascii=False, sort_keys=False)
    file_path.write_text(content + "\n", encoding="utf-8")


# =============================================================================
# JSONMerger - Merge genérico para arquivos .json
# =============================================================================

class JSONMerger:
    """
    Merger genérico para arquivos JSON.

    Aplica-se a:
    - .vscode/settings.json
    - .vscode/mcp.json
    - .vscode/extensions.json
    - package.json
    - tsconfig.json
    - Qualquer outro .json

    Estratégia:
    - Deep merge com user-wins
    - Backup automático antes de merge
    - Validação de sintaxe JSON
    """

    def can_merge(self, file_path: Path) -> bool:
        """Verifica se é arquivo .json (exceto .code-workspace que tem merger próprio)."""
        return (
            file_path.suffix == ".json" and
            not file_path.name.endswith(".code-workspace")
        )

    def merge(
        self,
        existing_path: Path,
        template_content: str,
        interactive: bool = True
    ) -> CreatedItem:
        """
        Faz deep merge de arquivo JSON existente com template.

        Args:
            existing_path: Arquivo JSON existente
            template_content: Conteúdo do template (string JSON)
            interactive: Não usado (merge sempre automático)

        Returns:
            CreatedItem com status="created" se merge bem-sucedido
        """
        try:
            # Backup do arquivo original
            backup_path = existing_path.with_suffix(existing_path.suffix + ".backup")
            existing_path.rename(backup_path)
            log.info(f"📦 Backup: {existing_path.name} → {backup_path.name}")

            # Carregar dados
            base_data = json.loads(template_content)
            overlay_data = load_json_safe(backup_path)

            # Deep merge (overlay sobrescreve base = user-wins)
            merged_data = deep_merge_json(base_data, overlay_data)

            # Salvar resultado
            save_json_formatted(existing_path, merged_data)

            log.info(f"🔄 Merged: {existing_path.name} (template + customizações)")

            return CreatedItem(
                path=existing_path,
                kind="file",
                status="created",
                message=f"Merged with user customizations (backup: {backup_path.name})"
            )

        except ValueError as e:
            # JSON inválido - restaurar backup
            log.error(f"❌ Merge falhou: {e}")
            if backup_path.exists():
                backup_path.rename(existing_path)
                log.info(f"♻️  Restaurado backup: {backup_path.name}")

            return CreatedItem(
                path=existing_path,
                kind="file",
                status="error",
                message=f"Invalid JSON, restored backup: {e}"
            )

        except Exception as e:
            log.error(f"❌ Erro inesperado no merge de {existing_path.name}: {e}")
            return CreatedItem(
                path=existing_path,
                kind="file",
                status="error",
                message=str(e)
            )


# =============================================================================
# WorkspaceMerger - Merge especializado para .code-workspace
# =============================================================================

class WorkspaceMerger:
    """
    Merger especializado para arquivos .code-workspace.

    Lógica específica:
    - folders: União de paths (sem duplicatas, preservar ordem overlay → base)
    - settings: Deep merge (user-wins)
    - extensions.recommendations: União de IDs (sem duplicatas)

    Exemplo:
        Base:
        {
          "folders": [{"path": "."}],
          "settings": {"editor.rulers": [80]},
          "extensions": {"recommendations": ["ms-python.python"]}
        }

        Overlay:
        {
          "folders": [{"path": "."}, {"path": "../libs"}],
          "settings": {"editor.rulers": [120], "python.linting.enabled": true},
          "extensions": {"recommendations": ["dbaeumer.vscode-eslint"]}
        }

        Resultado:
        {
          "folders": [{"path": "."}, {"path": "../libs"}],
          "settings": {
            "editor.rulers": [120],
            "python.linting.enabled": true
          },
          "extensions": {
            "recommendations": [
              "ms-python.python",
              "dbaeumer.vscode-eslint"
            ]
          }
        }
    """

    def can_merge(self, file_path: Path) -> bool:
        """Verifica se é arquivo .code-workspace."""
        return file_path.suffix == ".code-workspace" or file_path.name.endswith(".code-workspace")

    def merge(
        self,
        existing_path: Path,
        template_content: str,
        interactive: bool = True
    ) -> CreatedItem:
        """
        Merge especializado de .code-workspace.

        Args:
            existing_path: Arquivo .code-workspace existente
            template_content: Conteúdo do template
            interactive: Não usado

        Returns:
            CreatedItem com resultado do merge
        """
        try:
            # Backup
            backup_path = existing_path.with_suffix(".code-workspace.backup")
            existing_path.rename(backup_path)
            log.info(f"📦 Backup: {existing_path.name} → {backup_path.name}")

            # Carregar dados
            base_data = json.loads(template_content)
            overlay_data = load_json_safe(backup_path)

            # Merge especializado
            merged_data = self._merge_workspace_data(base_data, overlay_data)

            # Salvar
            save_json_formatted(existing_path, merged_data)

            log.info(f"🔄 Merged workspace: {existing_path.name}")

            return CreatedItem(
                path=existing_path,
                kind="file",
                status="created",
                message=f"Merged workspace (backup: {backup_path.name})"
            )

        except Exception as e:
            log.error(f"❌ Erro no merge de workspace: {e}")
            if backup_path.exists():
                backup_path.rename(existing_path)
                log.info(f"♻️  Restaurado backup")

            return CreatedItem(
                path=existing_path,
                kind="file",
                status="error",
                message=str(e)
            )

    def _merge_workspace_data(
        self,
        base: Dict[str, Any],
        overlay: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Merge de dados de workspace com lógica específica.

        Args:
            base: Dados do template
            overlay: Dados do usuário

        Returns:
            Dados mergeados
        """
        merged = {}

        # 1. Merge folders (união, sem duplicatas)
        base_folders = base.get("folders", [])
        overlay_folders = overlay.get("folders", [])

        # Usar set de paths para detectar duplicatas
        folders_set = set()
        merged_folders = []

        # Priorizar overlay (customizações do usuário primeiro)
        for folder in overlay_folders + base_folders:
            path = folder.get("path")
            if path and path not in folders_set:
                folders_set.add(path)
                merged_folders.append(folder)

        if merged_folders:
            merged["folders"] = merged_folders

        # 2. Merge settings (deep merge, user-wins)
        base_settings = base.get("settings", {})
        overlay_settings = overlay.get("settings", {})

        if base_settings or overlay_settings:
            merged["settings"] = deep_merge_json(base_settings, overlay_settings)

        # 3. Merge extensions.recommendations (união)
        base_ext = base.get("extensions", {}).get("recommendations", [])
        overlay_ext = overlay.get("extensions", {}).get("recommendations", [])

        if base_ext or overlay_ext:
            # União sem duplicatas, preservando ordem
            all_extensions = overlay_ext + base_ext
            unique_extensions = []
            seen = set()

            for ext_id in all_extensions:
                if ext_id not in seen:
                    seen.add(ext_id)
                    unique_extensions.append(ext_id)

            merged["extensions"] = {"recommendations": unique_extensions}

        # 4. Preservar outros campos do overlay (se houver)
        for key in overlay:
            if key not in ["folders", "settings", "extensions"]:
                merged[key] = overlay[key]

        return merged
