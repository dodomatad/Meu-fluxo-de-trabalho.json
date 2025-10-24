#!/bin/bash
##############################################################################
# 🚀 INSTALADOR UNIVERSAL - Importador de Workflow n8n
# Detecta ambiente e instala tudo automaticamente
##############################################################################

set -e  # Para em caso de erro

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m' # No Color

echo -e "${BOLD}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BOLD}🚀 INSTALADOR UNIVERSAL - Importador de Workflow n8n${NC}"
echo -e "${BOLD}═══════════════════════════════════════════════════════════════${NC}"
echo ""

# Função para verificar se comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Função para log
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

log_step() {
    echo ""
    echo -e "${BOLD}${BLUE}$1${NC}"
}

# Detecta sistema operacional
log_step "🔍 Detectando sistema operacional..."
OS="unknown"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    log_success "Linux detectado"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="mac"
    log_success "macOS detectado"
else
    log_warning "Sistema não identificado: $OSTYPE"
fi

# Verifica Python
log_step "🐍 Verificando Python..."
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    log_success "Python encontrado: $PYTHON_VERSION"
    HAS_PYTHON=true
else
    log_warning "Python3 não encontrado"
    HAS_PYTHON=false
fi

# Verifica Node.js
log_step "📦 Verificando Node.js..."
if command_exists node; then
    NODE_VERSION=$(node --version)
    log_success "Node.js encontrado: $NODE_VERSION"
    HAS_NODE=true
else
    log_warning "Node.js não encontrado"
    HAS_NODE=false
fi

# Verifica npm
if command_exists npm; then
    NPM_VERSION=$(npm --version)
    log_success "npm encontrado: $NPM_VERSION"
    HAS_NPM=true
else
    HAS_NPM=false
fi

# Verifica curl
if command_exists curl; then
    HAS_CURL=true
else
    HAS_CURL=false
fi

echo ""
echo -e "${BOLD}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BOLD}📊 DIAGNÓSTICO DO AMBIENTE${NC}"
echo -e "${BOLD}═══════════════════════════════════════════════════════════════${NC}"
echo -e "Sistema Operacional: ${BLUE}$OS${NC}"
echo -e "Python3:             ${HAS_PYTHON:+${GREEN}✅${NC}}${HAS_PYTHON:-${RED}❌${NC}}"
echo -e "Node.js:             ${HAS_NODE:+${GREEN}✅${NC}}${HAS_NODE:-${RED}❌${NC}}"
echo -e "npm:                 ${HAS_NPM:+${GREEN}✅${NC}}${HAS_NPM:-${RED}❌${NC}}"
echo -e "curl:                ${HAS_CURL:+${GREEN}✅${NC}}${HAS_CURL:-${RED}❌${NC}}"
echo -e "${BOLD}═══════════════════════════════════════════════════════════════${NC}"
echo ""

# Decide qual método instalar
log_step "🎯 Decidindo melhor método de instalação..."

INSTALL_METHOD="manual"

if [ "$HAS_NODE" = true ] && [ "$HAS_NPM" = true ]; then
    INSTALL_METHOD="puppeteer"
    log_info "Método escolhido: ${GREEN}${BOLD}PUPPETEER${NC} (Node.js disponível)"
elif [ "$HAS_PYTHON" = true ]; then
    INSTALL_METHOD="python"
    log_info "Método escolhido: ${GREEN}${BOLD}PYTHON${NC} (Python disponível)"
else
    INSTALL_METHOD="manual"
    log_warning "Nenhum ambiente detectado. Você precisará fazer importação manual."
fi

echo ""
read -p "Deseja continuar com o método $INSTALL_METHOD? (s/n): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[SsYy]$ ]]; then
    log_warning "Instalação cancelada pelo usuário"
    exit 0
fi

# Instalação baseada no método
if [ "$INSTALL_METHOD" = "puppeteer" ]; then
    log_step "🎭 Instalando dependências do Puppeteer..."

    # Instala dependências do sistema (Linux)
    if [ "$OS" = "linux" ] && command_exists apt-get; then
        log_info "Instalando dependências do sistema (pode pedir sudo)..."
        sudo apt-get update -qq
        sudo apt-get install -y -qq \
            libnss3 \
            libatk1.0-0 \
            libatk-bridge2.0-0 \
            libcups2 \
            libdrm2 \
            libxkbcommon0 \
            libxcomposite1 \
            libxdamage1 \
            libxfixes3 \
            libxrandr2 \
            libgbm1 \
            libasound2 2>/dev/null || log_warning "Algumas dependências não foram instaladas"
    fi

    # Instala pacotes NPM
    log_info "Instalando pacotes Node.js..."
    npm install --silent
    log_success "Dependências instaladas!"

    # Configuração interativa
    echo ""
    read -p "Deseja configurar credenciais agora? (s/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[SsYy]$ ]]; then
        npm run setup
    else
        log_info "Você pode configurar depois executando: npm run setup"
    fi

    echo ""
    log_success "✨ Instalação do Puppeteer concluída!"
    echo ""
    echo -e "${BOLD}Para importar o workflow, execute:${NC}"
    echo -e "${GREEN}npm run import${NC}"

elif [ "$INSTALL_METHOD" = "python" ]; then
    log_step "🐍 Verificando dependências Python..."

    # Verifica se requests está instalado
    if python3 -c "import requests" 2>/dev/null; then
        log_success "Biblioteca 'requests' já instalada"
    else
        log_info "Instalando biblioteca 'requests'..."
        pip3 install requests 2>/dev/null || \
        python3 -m pip install requests 2>/dev/null || \
        log_warning "Não foi possível instalar 'requests'. Instale manualmente: pip3 install requests"
    fi

    log_success "✨ Ambiente Python pronto!"
    echo ""
    echo -e "${BOLD}Para importar o workflow, execute:${NC}"
    echo -e "${GREEN}python3 import_n8n.py${NC}"
    echo ""
    echo -e "${YELLOW}Nota: A API do n8n requer autenticação.${NC}"
    echo -e "Configure a API Key ou use importação manual."

else
    log_warning "Instalação automática não disponível"
    echo ""
    echo -e "${BOLD}📋 Importação Manual:${NC}"
    echo ""
    echo "1. Acesse: ${BLUE}http://162.240.164.165:5678${NC}"
    echo "2. Clique: Workflows → + → ⋮ → Import from File"
    echo "3. Selecione: workflows/My workflow 2.json"
fi

# Instruções finais
echo ""
echo -e "${BOLD}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BOLD}📚 DOCUMENTAÇÃO${NC}"
echo -e "${BOLD}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "📖 ${BLUE}README.md${NC}             - Guia principal completo"
echo -e "⚡ ${BLUE}QUICK_START.md${NC}        - Início rápido"
echo -e "🎭 ${BLUE}README_PUPPETEER.md${NC}  - Guia Puppeteer detalhado"
echo -e "📘 ${BLUE}GUIA_RAPIDO.md${NC}        - Todos os métodos"
echo ""
echo -e "${BOLD}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}${BOLD}✨ Instalação concluída!${NC}"
echo -e "${BOLD}═══════════════════════════════════════════════════════════════${NC}"
echo ""
