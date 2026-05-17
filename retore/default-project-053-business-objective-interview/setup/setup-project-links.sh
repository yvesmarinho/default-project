#!/bin/bash
# Setup Project Links - Criar links simbólicos para configurações compartilhadas
# Uso: ./setup-project-links.sh [diretório-do-projeto]

set -e

# Cores
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Diretórios
PROJECT_DIR="${1:-.}"
SHARED_DIR="$HOME/Documentos/DevOps/.copilot-shared"

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Setup Project Links - Configurações Compartilhadas       ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Verificar se diretório do projeto existe
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${RED}❌ Erro: Diretório não encontrado: $PROJECT_DIR${NC}"
    exit 1
fi

# Verificar se diretório compartilhado existe
if [ ! -d "$SHARED_DIR" ]; then
    echo -e "${YELLOW}⚠️  Diretório compartilhado não encontrado: $SHARED_DIR${NC}"
    echo -e "${YELLOW}   Deseja criar? (s/n)${NC}"
    read -r response
    if [[ "$response" =~ ^[Ss]$ ]]; then
        echo -e "${BLUE}📁 Criando estrutura compartilhada...${NC}"
        mkdir -p "$SHARED_DIR"/{rules,scripts,templates,docs}
        echo -e "${GREEN}✅ Estrutura criada${NC}"
    else
        echo -e "${RED}❌ Operação cancelada${NC}"
        exit 1
    fi
fi

cd "$PROJECT_DIR"

echo -e "${BLUE}📂 Projeto: $(pwd)${NC}"
echo -e "${BLUE}🔗 Shared: $SHARED_DIR${NC}"
echo ""

# Arquivos para criar links
declare -A FILES=(
    [".copilot-strict-rules.md"]="rules/.copilot-strict-rules.md"
    [".copilot-strict-enforcement.md"]="rules/.copilot-strict-enforcement.md"
    [".copilot-git-rules.md"]="rules/.copilot-git-rules.md"
    [".copilot-rules.md"]="rules/.copilot-rules.md"
    [".copilot-file-rules.sh"]="scripts/.copilot-file-rules.sh"
)

echo -e "${BLUE}🔗 Criando links simbólicos...${NC}"
echo ""

for local_file in "${!FILES[@]}"; do
    shared_file="${FILES[$local_file]}"
    shared_path="$SHARED_DIR/$shared_file"

    # Verificar se arquivo compartilhado existe
    if [ ! -f "$shared_path" ]; then
        echo -e "${YELLOW}  ⚠️  $local_file → Arquivo não existe no compartilhado${NC}"

        # Se arquivo existe localmente, perguntar se quer mover
        if [ -f "$local_file" ] && [ ! -L "$local_file" ]; then
            echo -e "${YELLOW}     Arquivo existe localmente. Mover para compartilhado? (s/n)${NC}"
            read -r response
            if [[ "$response" =~ ^[Ss]$ ]]; then
                mkdir -p "$(dirname "$shared_path")"
                mv "$local_file" "$shared_path"
                echo -e "${GREEN}     ✅ Movido para compartilhado${NC}"
            else
                echo -e "${YELLOW}     ⏭️  Pulando este arquivo${NC}"
                continue
            fi
        else
            # Arquivo não existe em nenhum lugar - oferecer criar template
            echo -e "${YELLOW}     Arquivo não existe. Criar template? (s/n)${NC}"
            read -r response
            if [[ "$response" =~ ^[Ss]$ ]]; then
                mkdir -p "$(dirname "$shared_path")"
                # Criar arquivo template básico
                cat > "$shared_path" << 'EOF'
# Copilot Rules
# Add your project-specific Copilot rules here

## General Guidelines
- Follow project conventions
- Write clean, maintainable code
- Add comments for complex logic

## Code Style
- Use consistent formatting
- Follow naming conventions
- Keep functions small and focused
EOF
                echo -e "${GREEN}     ✅ Template criado em $shared_path${NC}"
            else
                echo -e "${YELLOW}     ⏭️  Pulando este arquivo${NC}"
                continue
            fi
        fi
    fi

    # Remover arquivo/link existente
    if [ -e "$local_file" ] || [ -L "$local_file" ]; then
        if [ -L "$local_file" ]; then
            echo -e "${YELLOW}  ♻️  $local_file → Já é um link, recriando...${NC}"
        else
            echo -e "${YELLOW}  ⚠️  $local_file → Existe como arquivo, fazendo backup...${NC}"
            mv "$local_file" "${local_file}.backup"
        fi
        rm -f "$local_file"
    fi

    # Criar link simbólico relativo
    relative_path=$(realpath --relative-to="$(pwd)" "$shared_path")
    ln -sf "$relative_path" "$local_file"

    echo -e "${GREEN}  ✅ $local_file → $relative_path${NC}"
done

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  ✅ Links criados com sucesso!                             ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}💡 Próximos passos:${NC}"
echo -e "   1. Verificar links: ${YELLOW}./check-project-links.sh${NC}"
echo -e "   2. Testar alterações no compartilhado${NC}"
echo -e "   3. Commitar mudanças no projeto${NC}"
echo ""
