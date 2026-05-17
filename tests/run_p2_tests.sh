#!/usr/bin/env bash
# /// script
# description = "Run GitHub Best Practices P2 test suite"
# ///
#
# tests/run_p2_tests.sh
#
# Executa bateria completa de testes para GitHub Best Practices P2
#
# Uso:
#   ./tests/run_p2_tests.sh              # Rodar todos testes P2
#   ./tests/run_p2_tests.sh --verbose    # Modo verbose
#   ./tests/run_p2_tests.sh --coverage   # Com coverage

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Parse argumentos
VERBOSE=false
COVERAGE=false
MARKERS=""

for arg in "$@"; do
    case $arg in
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --coverage|-c)
            COVERAGE=true
            shift
            ;;
        --markers=*)
            MARKERS="${arg#*=}"
            shift
            ;;
        *)
            ;;
    esac
done

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     GitHub Best Practices P2 - Test Suite                     ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

cd "$PROJECT_ROOT"

# Construir comando pytest
PYTEST_CMD="pytest tests/test_github_best_practices_p2.py"

if [ "$VERBOSE" = true ]; then
    PYTEST_CMD="$PYTEST_CMD -v"
fi

if [ "$COVERAGE" = true ]; then
    # Verificar se pytest-cov está instalado
    if python -c "import pytest_cov" 2>/dev/null; then
        PYTEST_CMD="$PYTEST_CMD --cov=scripts/lib/project.py --cov-report=term-missing --cov-report=html"
    else
        echo -e "${YELLOW}⚠️  pytest-cov não instalado. Rodando sem coverage.${NC}"
        echo -e "${YELLOW}   Instale com: pip install pytest-cov${NC}"
        echo ""
        COVERAGE=false
    fi
fi

if [ -n "$MARKERS" ]; then
    PYTEST_CMD="$PYTEST_CMD -m $MARKERS"
fi

echo -e "${YELLOW}Comando: $PYTEST_CMD${NC}"
echo ""

# Executar testes
if eval "$PYTEST_CMD"; then
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                    ✅ ALL TESTS PASSED                         ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"

    if [ "$COVERAGE" = true ]; then
        echo ""
        echo -e "${BLUE}📊 Coverage report: htmlcov/index.html${NC}"
    fi

    exit 0
else
    echo ""
    echo -e "${RED}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║                    ❌ TESTS FAILED                             ║${NC}"
    echo -e "${RED}╚════════════════════════════════════════════════════════════════╝${NC}"
    exit 1
fi
