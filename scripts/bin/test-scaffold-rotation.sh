#!/usr/bin/env bash
# Criado em: 24/06/2026 14:00
# Modificado em: 24/06/2026 15:30
#
# test-scaffold-rotation.sh — Executa scaffold new rotacionando entre combinações
# de opções a cada execução. Usa arquivo de estado para lembrar qual combinação
# foi usada por último.
#
# Uso:
#   ./scripts/bin/test-scaffold-rotation.sh          # próxima combinação
#   ./scripts/bin/test-scaffold-rotation.sh --reset  # reinicia do índice 0
#   ./scripts/bin/test-scaffold-rotation.sh --list   # lista todas as combinações
#   ./scripts/bin/test-scaffold-rotation.sh --dry-run # mostra o que seria executado
#
# Saída:
#   - Projeto criado em tmp/test-runs/<nome>/
#   - Log da execução em tmp/stdout.txt (sobrescreve para uso como contexto)

set -euo pipefail

# ---------------------------------------------------------------------------
# Configuração
# ---------------------------------------------------------------------------

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
SCAFFOLD_CMD="uv run scripts/scaffold.py"
TARGET_DIR="${PROJECT_ROOT}/tmp/test-runs"
STATE_FILE="${PROJECT_ROOT}/tmp/.test-scaffold-state"
STDOUT_FILE="${PROJECT_ROOT}/tmp/stdout.txt"

# ---------------------------------------------------------------------------
# Combinações de teste
# Formato: "nome_sufixo|domain|language|ai_assistant|code_profile"
# code_profile vazio = sem perfil de código
# ---------------------------------------------------------------------------

declare -a COMBINATIONS=(
    #  sufixo               domain          language    ai          code_profile
    "prog-py-claude        |programming    |python      |claude     |"
    "prog-py-both-fastapi  |programming    |python      |both       |python-fastapi"
    "prog-py-copilot-flask |programming    |python      |copilot    |python-flask"
    "prog-py-none          |programming    |python      |none       |"
    "prog-ts-claude        |programming    |typescript  |claude     |"
    "prog-go-claude        |programming    |go          |claude     |"
    "prog-other-both       |programming    |other       |both       |"
    "infra-py-claude       |infrastructure |python      |claude     |"
    "infra-py-both         |infrastructure |python      |both       |"
    "infra-py-none         |infrastructure |python      |none       |"
    "analysis-py-claude    |analysis       |python      |claude     |"
    "analysis-py-both      |analysis       |python      |both       |"
)

TOTAL=${#COMBINATIONS[@]}

# ---------------------------------------------------------------------------
# Funções auxiliares
# ---------------------------------------------------------------------------

_read_state() {
    if [[ -f "${STATE_FILE}" ]]; then
        cat "${STATE_FILE}"
    else
        echo "0"
    fi
}

_write_state() {
    echo "$1" > "${STATE_FILE}"
}

_parse_combo() {
    local entry="$1"
    # remove espaços extras ao redor dos campos
    SUFFIX=$(echo "${entry}" | cut -d'|' -f1 | tr -d ' ')
    DOMAIN=$(echo "${entry}" | cut -d'|' -f2 | tr -d ' ')
    LANGUAGE=$(echo "${entry}" | cut -d'|' -f3 | tr -d ' ')
    AI=$(echo "${entry}" | cut -d'|' -f4 | tr -d ' ')
    CODE_PROFILE=$(echo "${entry}" | cut -d'|' -f5 | tr -d ' ')
}

_list_combinations() {
    local current
    current=$(_read_state)
    echo ""
    echo "Combinações disponíveis (${TOTAL} total):"
    echo ""
    printf "  %-4s %-26s %-16s %-12s %-10s %s\n" "IDX" "SUFIXO" "DOMAIN" "LANGUAGE" "AI" "CODE_PROFILE"
    printf "  %-4s %-26s %-16s %-12s %-10s %s\n" "---" "------" "------" "--------" "--" "------------"
    for i in "${!COMBINATIONS[@]}"; do
        _parse_combo "${COMBINATIONS[$i]}"
        local marker=" "
        [[ "$i" == "$current" ]] && marker="▶"
        printf "  %s%-3s %-26s %-16s %-12s %-10s %s\n" \
            "$marker" "$i" "$SUFFIX" "$DOMAIN" "$LANGUAGE" "$AI" "${CODE_PROFILE:-(nenhum)}"
    done
    echo ""
    echo "  ▶ = próxima a ser executada"
    echo ""
}

_build_command() {
    local index="$1"
    _parse_combo "${COMBINATIONS[$index]}"

    local project_name
    project_name="test-$(printf '%03d' "$index")-${SUFFIX}"

    local cmd="${SCAFFOLD_CMD} new --ci"
    cmd+=" --name ${project_name}"
    cmd+=" --title 'Test ${index}: ${SUFFIX}'"
    cmd+=" --description 'Teste automatizado de rotação — combinação ${index}'"
    cmd+=" --domain ${DOMAIN}"
    cmd+=" --language ${LANGUAGE}"
    cmd+=" --ai-assistant ${AI}"
    cmd+=" --target-dir ${TARGET_DIR}"

    [[ -n "${CODE_PROFILE}" ]] && cmd+=" --with-code-profile ${CODE_PROFILE}"

    echo "${cmd}"
}

# ---------------------------------------------------------------------------
# Parse de argumentos
# ---------------------------------------------------------------------------

DRY_RUN=false
DO_RESET=false
DO_LIST=false

for arg in "$@"; do
    case "${arg}" in
        --dry-run) DRY_RUN=true ;;
        --reset)   DO_RESET=true ;;
        --list)    DO_LIST=true ;;
        --help|-h)
            echo "Uso: $0 [--reset] [--list] [--dry-run]"
            echo ""
            echo "  (sem args)  Executa a próxima combinação"
            echo "  --list      Lista todas as combinações e qual será a próxima"
            echo "  --reset     Reinicia o contador para o índice 0, apaga projetos e stdout.txt"
            echo "  --dry-run   Mostra o comando sem executar"
            exit 0
            ;;
        *)
            echo "Argumento desconhecido: ${arg}" >&2
            exit 1
            ;;
    esac
done

# ---------------------------------------------------------------------------
# Ações
# ---------------------------------------------------------------------------

if [[ "${DO_RESET}" == true ]]; then
    _write_state 0

    # Apaga projetos de teste
    if [[ -d "${TARGET_DIR}" ]]; then
        echo "Removendo projetos em ${TARGET_DIR}..."
        rm -rf "${TARGET_DIR:?}"/*
        echo "  ✅ Projetos removidos."
    fi

    # Apaga stdout.txt
    if [[ -f "${STDOUT_FILE}" ]]; then
        rm -f "${STDOUT_FILE}"
        echo "  ✅ ${STDOUT_FILE} removido."
    fi

    # Apaga logs de scaffold em logs/scaffold*.log
    logs_dir="${PROJECT_ROOT}/logs"
    if ls "${logs_dir}"/scaffold*.log 2>/dev/null | grep -q .; then
        rm -f "${logs_dir}"/scaffold*.log
        echo "  ✅ Logs de scaffold removidos de ${logs_dir}/."
    fi

    echo ""
    echo "Estado reiniciado. Próxima execução usará o índice 0."
    _list_combinations
    exit 0
fi

if [[ "${DO_LIST}" == true ]]; then
    _list_combinations
    exit 0
fi

# ---------------------------------------------------------------------------
# Execução principal
# ---------------------------------------------------------------------------

mkdir -p "${TARGET_DIR}"

current=$(_read_state)
next=$(( (current + 1) % TOTAL ))

_parse_combo "${COMBINATIONS[$current]}"
project_name="test-$(printf '%03d' "$current")-${SUFFIX}"

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
printf "║  Combinação %-3s/%-3s: %-40s║\n" "$((current + 1))" "$TOTAL" "${SUFFIX}"
echo "╠══════════════════════════════════════════════════════════════╣"
printf "║  domain  : %-50s║\n" "${DOMAIN}"
printf "║  language: %-50s║\n" "${LANGUAGE}"
printf "║  ai      : %-50s║\n" "${AI}"
printf "║  profile : %-50s║\n" "${CODE_PROFILE:-(nenhum)}"
printf "║  projeto : %-50s║\n" "${project_name}"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

CMD=$(_build_command "$current")

if [[ "${DRY_RUN}" == true ]]; then
    echo "[DRY-RUN] Comando que seria executado:"
    echo ""
    echo "  cd ${PROJECT_ROOT}"
    echo "  ${CMD} 2>&1 | tee ${STDOUT_FILE}"
    echo ""
    echo "Próximo índice seria: ${next} (combinação: $(echo "${COMBINATIONS[$next]}" | cut -d'|' -f1 | tr -d ' '))"
    exit 0
fi

# Executa o scaffold e salva saída em tmp/stdout.txt
cd "${PROJECT_ROOT}"
echo "Executando... (saída também em ${STDOUT_FILE})"
echo ""

if eval "${CMD}" 2>&1 | tee "${STDOUT_FILE}"; then
    STATUS="✅ SUCESSO"
else
    STATUS="❌ FALHA (código: ${PIPESTATUS[0]})"
fi

# Avança o contador apenas se a execução não travou no meio
_write_state "${next}"

echo ""
echo "══════════════════════════════════════════════════════════════"
echo "  ${STATUS}"
echo "  Log: ${STDOUT_FILE}"
echo "  Próxima execução: índice ${next} — $(echo "${COMBINATIONS[$next]}" | cut -d'|' -f1 | tr -d ' ')"
echo "══════════════════════════════════════════════════════════════"
echo ""
