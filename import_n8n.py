#!/usr/bin/env python3
"""
🤖 Importador de Workflow n8n - Versão Completa
Suporta API Key, Basic Auth e importação manual
"""

import json
import requests
import sys
import os
from pathlib import Path

# Configurações
N8N_URL = "http://162.240.164.165:5678"
WORKFLOW_FILE = "workflows/My workflow 2.json"

# Credenciais (configure via variáveis de ambiente)
API_KEY = os.getenv("N8N_API_KEY", "")
USERNAME = os.getenv("N8N_USERNAME", "")
PASSWORD = os.getenv("N8N_PASSWORD", "")

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header():
    print()
    print("=" * 70)
    print(f"{Colors.BOLD}🤖 IMPORTADOR DE WORKFLOW N8N{Colors.END}")
    print("=" * 70)
    print()

def carregar_workflow():
    """Carrega o workflow do arquivo JSON"""
    print(f"📂 Carregando: {Colors.BLUE}{WORKFLOW_FILE}{Colors.END}")

    if not Path(WORKFLOW_FILE).exists():
        print(f"{Colors.RED}❌ Arquivo não encontrado!{Colors.END}")
        return None

    try:
        with open(WORKFLOW_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)

        print(f"{Colors.GREEN}✅ Workflow carregado com sucesso{Colors.END}")
        print(f"   Nome: {data.get('name', 'N/A')}")
        print(f"   Nós: {len(data.get('nodes', []))}")
        print()
        return data
    except Exception as e:
        print(f"{Colors.RED}❌ Erro: {e}{Colors.END}")
        return None

def tentar_importar(workflow_data, metodo, headers, auth=None):
    """Tenta importar com um método específico de autenticação"""

    payload = {
        "name": workflow_data.get("name"),
        "nodes": workflow_data.get("nodes", []),
        "connections": workflow_data.get("connections", {}),
        "settings": workflow_data.get("settings", {}),
        "active": False
    }

    if "tags" in workflow_data:
        payload["tags"] = workflow_data["tags"]

    endpoints = ["/api/v1/workflows", "/rest/workflows"]

    for endpoint in endpoints:
        url = f"{N8N_URL}{endpoint}"
        print(f"   Testando: {endpoint} com {metodo}...")

        try:
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                auth=auth,
                timeout=30
            )

            if response.status_code in [200, 201]:
                result = response.json()
                workflow_id = result.get("id") or result.get("data", {}).get("id")

                print()
                print("=" * 70)
                print(f"{Colors.GREEN}{Colors.BOLD}✅ SUCESSO! Workflow importado!{Colors.END}")
                print("=" * 70)
                print(f"📋 ID: {workflow_id}")
                print(f"📝 Nome: {result.get('name')}")
                print(f"🔗 Acesse: {N8N_URL}/workflow/{workflow_id}")
                print("=" * 70)
                print()
                return True

            elif response.status_code == 401:
                print(f"      {Colors.YELLOW}401 - Não autorizado{Colors.END}")
            elif response.status_code == 403:
                print(f"      {Colors.YELLOW}403 - Acesso negado{Colors.END}")
            else:
                print(f"      {Colors.RED}{response.status_code}{Colors.END}")

        except Exception as e:
            print(f"      {Colors.RED}Erro: {str(e)[:50]}{Colors.END}")

    return False

def importar_com_autenticacao(workflow_data):
    """Tenta importar usando diferentes métodos de autenticação"""

    print("🔐 Tentando métodos de autenticação...")
    print()

    # Método 1: API Key
    if API_KEY:
        print(f"{Colors.BOLD}1️⃣  Tentando com API Key...{Colors.END}")
        headers = {
            "Content-Type": "application/json",
            "X-N8N-API-KEY": API_KEY
        }
        if tentar_importar(workflow_data, "API Key", headers):
            return True
        print()

    # Método 2: Basic Auth
    if USERNAME and PASSWORD:
        print(f"{Colors.BOLD}2️⃣  Tentando com Basic Auth...{Colors.END}")
        headers = {"Content-Type": "application/json"}
        auth = (USERNAME, PASSWORD)
        if tentar_importar(workflow_data, "Basic Auth", headers, auth):
            return True
        print()

    # Método 3: Sem autenticação
    print(f"{Colors.BOLD}3️⃣  Tentando sem autenticação...{Colors.END}")
    headers = {"Content-Type": "application/json"}
    if tentar_importar(workflow_data, "Sem Auth", headers):
        return True
    print()

    return False

def mostrar_instrucoes_manuais():
    """Mostra instruções para importação manual"""
    print("=" * 70)
    print(f"{Colors.YELLOW}⚠️  IMPORTAÇÃO AUTOMÁTICA NÃO DISPONÍVEL{Colors.END}")
    print("=" * 70)
    print()
    print(f"{Colors.BOLD}📋 INSTRUÇÕES PARA IMPORTAÇÃO MANUAL:{Colors.END}")
    print()
    print("1️⃣  Abra seu n8n:")
    print(f"   {Colors.BLUE}http://162.240.164.165:5678{Colors.END}")
    print()
    print("2️⃣  No menu principal, clique em:")
    print("   → Workflows")
    print("   → Botão '+' (Novo Workflow)")
    print("   → ⋮ (três pontos)")
    print("   → 'Import from File'")
    print()
    print("3️⃣  Selecione o arquivo:")
    print(f"   {Colors.BLUE}workflows/My workflow 2.json{Colors.END}")
    print()
    print("4️⃣  Configure as credenciais:")
    print("   - PostgreSQL Conversas (para o novo nó)")
    print("   - Outras credenciais existentes")
    print()
    print("5️⃣  Ative o workflow!")
    print()
    print("=" * 70)
    print()
    print(f"{Colors.BOLD}💡 PARA HABILITAR IMPORTAÇÃO AUTOMÁTICA:{Colors.END}")
    print()
    print("Opção A - Usar API Key:")
    print("   1. No n8n: Settings → API → Create API Key")
    print("   2. Copie a chave")
    print("   3. Execute:")
    print(f"      {Colors.BLUE}N8N_API_KEY='sua_chave' python3 import_n8n.py{Colors.END}")
    print()
    print("Opção B - Usar Basic Auth:")
    print("   1. Execute:")
    print(f"      {Colors.BLUE}N8N_USERNAME='user' N8N_PASSWORD='pass' python3 import_n8n.py{Colors.END}")
    print()
    print("=" * 70)

def main():
    print_header()

    # Carrega workflow
    workflow = carregar_workflow()
    if not workflow:
        sys.exit(1)

    # Tenta importar
    print(f"🚀 Conectando ao n8n: {Colors.BLUE}{N8N_URL}{Colors.END}")
    print()

    sucesso = importar_com_autenticacao(workflow)

    if not sucesso:
        mostrar_instrucoes_manuais()
        sys.exit(1)

    print(f"{Colors.GREEN}✨ Processo concluído com sucesso!{Colors.END}")
    print()

if __name__ == "__main__":
    main()
