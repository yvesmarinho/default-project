#!/bin/bash
# Check Project Links - Verificar links simbólicos do projeto
# Uso: ./check-project-links.sh [diretório-do-projeto]

set -e

# Cores
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

PROJECT_DIR="${1:-.}"

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Check Project Links - Verificação de Links               ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${RED}❌ Erro: Diretório não encontrado: $PROJECT_DIR${NC}"
    exit 1
fi

cd "$PROJECT_DIR"

echo -e "${BLUE}📂 Projeto: $(pwd)${NC}"
echo ""

# Arquivos para verificar
FILES=(
    ".copilot-strict-rules.md"
    ".copilot-strict-enforcement.md"
    ".copilot-git-rules.md"
    ".copilot-rules.md"
    ".copilot-file-rules.sh"
)

echo -e "${BLUE}🔍 Verificando arquivos de configuração...${NC}"
echo ""

total=0
links=0
files=0
missing=0

for file in "${FILES[@]}"; do
    total=$((total + 1))

    if [ -L "$file" ]; then
        # É um link simbólico
        target=$(readlink -f "$file")
        if [ -f "$target" ]; then
            echo -e "${GREEN}  ✅ $file${NC}"
            echo -e "     ${BLUE}→ $(readlink "$file")${NC}"
            links=$((links + 1))
        else
            echo -e "${RED}  ❌ $file (link quebrado)${NC}"
            echo -e "     ${RED}→ $(readlink "$file") (não existe)${NC}"
            missing=$((missing + 1))
        fi
    elif [ -f "$file" ]; then
        # É um arquivo regular
        echo -e "${YELLOW}  📄 $file (arquivo local)${NC}"
        files=$((files + 1))
    else
        # Não existe
        echo -e "${RED}  ❌ $file (não encontrado)${NC}"
        missing=$((missing + 1))
    fi
done

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Resumo da Verificação                                     ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}  Total de arquivos:     ${NC}$total"
echo -e "${GREEN}  Links simbólicos:      ${NC}$links"
echo -e "${YELLOW}  Arquivos locais:       ${NC}$files"
echo -e "${RED}  Faltando/Quebrados:    ${NC}$missing"
echo ""

if [ $missing -gt 0 ]; then
    echo -e "${YELLOW}💡 Sugestão: Execute ${BLUE}./setup-project-links.sh${YELLOW} para corrigir${NC}"
    echo ""
    exit 1
elif [ $files -gt 0 ]; then
    echo -e "${YELLOW}💡 Arquivos locais detectados. Considere converter para links.${NC}"
    echo ""
    exit 0
else
    echo -e "${GREEN}✅ Todos os arquivos estão corretamente linkados!${NC}"
    echo ""
    exit 0
fi
