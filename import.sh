#!/bin/bash
##############################################################################
# 🎯 IMPORTADOR INTELIGENTE - Detecta e usa o melhor método automaticamente
##############################################################################

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${BOLD}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BOLD}🎯 IMPORTADOR INTELIGENTE DE WORKFLOW${NC}"
echo -e "${BOLD}═══════════════════════════════════════════════════════════════${NC}"
echo ""

# Verifica se arquivo existe
if [ ! -f "workflows/My workflow 2.json" ]; then
    echo -e "${RED}❌ Erro: Arquivo não encontrado: workflows/My workflow 2.json${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Workflow encontrado${NC}"
echo ""

# Detecta métodos disponíveis
echo -e "${BLUE}🔍 Detectando métodos disponíveis...${NC}"
echo ""

HAS_NODE=false
HAS_PYTHON=false
HAS_CURL=false

if command -v node >/dev/null 2>&1 && [ -f "node_modules/.bin/puppeteer" ]; then
    HAS_NODE=true
    echo -e "${GREEN}✅ Puppeteer (Node.js)${NC}"
fi

if command -v python3 >/dev/null 2>&1; then
    HAS_PYTHON=true
    echo -e "${GREEN}✅ Python${NC}"
fi

if command -v curl >/dev/null 2>&1; then
    HAS_CURL=true
    echo -e "${GREEN}✅ curl${NC}"
fi

echo ""
echo -e "${BOLD}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BOLD}Escolha o método:${NC}"
echo ""
if [ "$HAS_NODE" = true ]; then
    echo -e "${GREEN}1)${NC} Puppeteer (automático, faz login e importa)"
fi
if [ "$HAS_PYTHON" = true ]; then
    echo -e "${GREEN}2)${NC} Python + API (rápido, requer API key)"
fi
echo -e "${GREEN}3)${NC} Instruções manuais"
echo -e "${GREEN}0)${NC} Sair"
echo ""
read -p "Digite o número: " choice

case $choice in
    1)
        if [ "$HAS_NODE" = true ]; then
            echo ""
            echo -e "${BLUE}🎭 Executando Puppeteer...${NC}"
            echo ""
            npm run import
        else
            echo -e "${RED}❌ Node.js não disponível. Execute: ./install.sh${NC}"
        fi
        ;;
    2)
        if [ "$HAS_PYTHON" = true ]; then
            echo ""
            echo -e "${BLUE}🐍 Executando Python...${NC}"
            echo ""
            if [ -n "$N8N_API_KEY" ]; then
                python3 import_n8n.py
            else
                echo -e "${YELLOW}⚠️  API Key não configurada${NC}"
                echo ""
                read -p "Digite sua N8N_API_KEY: " api_key
                N8N_API_KEY="$api_key" python3 import_n8n.py
            fi
        else
            echo -e "${RED}❌ Python não disponível${NC}"
        fi
        ;;
    3)
        echo ""
        echo -e "${BOLD}═══════════════════════════════════════════════════════════════${NC}"
        echo -e "${BOLD}📋 IMPORTAÇÃO MANUAL${NC}"
        echo -e "${BOLD}═══════════════════════════════════════════════════════════════${NC}"
        echo ""
        echo -e "${BOLD}1.${NC} Acesse: ${BLUE}http://162.240.164.165:5678${NC}"
        echo ""
        echo -e "${BOLD}2.${NC} No menu, clique em:"
        echo "   → Workflows"
        echo "   → Botão '+' (Novo Workflow)"
        echo "   → ⋮ (três pontos no canto)"
        echo "   → 'Import from File'"
        echo ""
        echo -e "${BOLD}3.${NC} Selecione o arquivo:"
        echo -e "   ${BLUE}$(pwd)/workflows/My workflow 2.json${NC}"
        echo ""
        echo -e "${BOLD}4.${NC} Configure a credencial PostgreSQL:"
        echo "   Settings → Credentials → Add Credential"
        echo "   Nome: PostgreSQL Conversas"
        echo ""
        echo -e "${BOLD}5.${NC} Execute o SQL para criar a tabela:"
        echo -e "   ${BLUE}cat << 'EOF' | psql${NC}"
        echo "   CREATE TABLE conversation_history ("
        echo "     id SERIAL PRIMARY KEY,"
        echo "     phone_number VARCHAR(255),"
        echo "     user_message TEXT,"
        echo "     bot_response TEXT,"
        echo "     message_type VARCHAR(50),"
        echo "     timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
        echo "     session_id VARCHAR(255)"
        echo "   );"
        echo "   EOF"
        echo ""
        echo -e "${BOLD}6.${NC} Ative o workflow!"
        echo ""
        echo -e "${BOLD}═══════════════════════════════════════════════════════════════${NC}"
        ;;
    0)
        echo "Até logo!"
        exit 0
        ;;
    *)
        echo -e "${RED}❌ Opção inválida${NC}"
        exit 1
        ;;
esac

echo ""
