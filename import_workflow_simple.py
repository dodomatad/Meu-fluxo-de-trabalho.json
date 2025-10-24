#!/usr/bin/env python3
"""
Script Simplificado para Importar Workflow n8n
Versão com múltiplas tentativas de endpoint
"""

import json
import requests
import sys
from pathlib import Path

# Configurações
N8N_URL = "http://162.240.164.165:5678"
WORKFLOW_FILE = "workflows/My workflow 2.json"

# Possíveis endpoints da API n8n (vamos tentar todos)
API_ENDPOINTS = [
    "/api/v1/workflows",      # n8n moderno
    "/rest/workflows",        # n8n com autenticação básica
    "/webhook-test/workflow", # webhook alternativo
]

def carregar_workflow():
    """Carrega o arquivo JSON do workflow"""
    print(f"📂 Carregando workflow de: {WORKFLOW_FILE}")
    try:
        with open(WORKFLOW_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)

        nome = data.get('name', 'Desconhecido')
        total_nos = len(data.get('nodes', []))

        print(f"✅ Workflow carregado:")
        print(f"   Nome: {nome}")
        print(f"   Total de nós: {total_nos}")
        print()
        return data
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {WORKFLOW_FILE}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Erro ao ler JSON: {e}")
        return None

def testar_conexao():
    """Testa se o n8n está acessível"""
    print(f"🔍 Testando conexão com {N8N_URL}...")

    endpoints_teste = ["/healthz", "/", "/rest/login", "/api/v1/workflows"]

    for endpoint in endpoints_teste:
        try:
            response = requests.get(f"{N8N_URL}{endpoint}", timeout=5)
            print(f"   {endpoint}: {response.status_code}")
            if response.status_code in [200, 401, 403]:  # Servidor respondeu
                print("✅ n8n está online e respondendo")
                print()
                return True
        except:
            continue

    print("❌ Não foi possível conectar ao n8n")
    return False

def importar_workflow(workflow_data):
    """Tenta importar o workflow testando diferentes endpoints"""

    # Prepara payload
    payload = {
        "name": workflow_data.get("name", "Workflow Importado"),
        "nodes": workflow_data.get("nodes", []),
        "connections": workflow_data.get("connections", {}),
        "settings": workflow_data.get("settings", {}),
        "active": False
    }

    if "tags" in workflow_data:
        payload["tags"] = workflow_data["tags"]

    print("🚀 Tentando importar workflow...")
    print()

    # Tenta cada endpoint
    for i, endpoint in enumerate(API_ENDPOINTS, 1):
        url = f"{N8N_URL}{endpoint}"
        print(f"Tentativa {i}/{len(API_ENDPOINTS)}: {endpoint}")

        try:
            # Sem autenticação primeiro
            response = requests.post(
                url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )

            if response.status_code in [200, 201]:
                resultado = response.json()
                workflow_id = resultado.get("id", resultado.get("data", {}).get("id", "?"))

                print()
                print("=" * 60)
                print("✅ SUCESSO! Workflow importado com sucesso!")
                print("=" * 60)
                print(f"ID do Workflow: {workflow_id}")
                print(f"Nome: {resultado.get('name', 'N/A')}")
                print(f"URL: {N8N_URL}/workflow/{workflow_id}")
                print(f"Editor: {N8N_URL}/workflows/{workflow_id}")
                print("=" * 60)
                return True

            elif response.status_code == 401:
                print(f"   ⚠️  Requer autenticação (401)")
                print(f"   💡 Você precisa de API Key ou login")

            elif response.status_code == 403:
                print(f"   ⚠️  Acesso negado (403)")

            elif response.status_code == 404:
                print(f"   ℹ️  Endpoint não existe (404)")

            else:
                print(f"   ❌ Erro {response.status_code}")
                print(f"   Resposta: {response.text[:200]}")

        except requests.exceptions.Timeout:
            print(f"   ⏱️  Timeout")
        except requests.exceptions.ConnectionError:
            print(f"   🔌 Erro de conexão")
        except Exception as e:
            print(f"   ❌ Erro: {str(e)[:100]}")

        print()

    # Nenhum endpoint funcionou
    print("=" * 60)
    print("❌ FALHA: Não foi possível importar o workflow")
    print("=" * 60)
    print()
    print("💡 Possíveis soluções:")
    print()
    print("1️⃣  Importação Manual:")
    print(f"   - Acesse: {N8N_URL}")
    print("   - Clique em 'Import from File'")
    print(f"   - Selecione: {WORKFLOW_FILE}")
    print()
    print("2️⃣  Configurar API Key:")
    print("   - Acesse Settings > API no n8n")
    print("   - Crie uma API Key")
    print("   - Execute: N8N_API_KEY='sua_key' python3 import_workflow_to_n8n.py")
    print()
    print("3️⃣  Usar curl diretamente:")
    print(f"   curl -X POST {N8N_URL}/api/v1/workflows \\")
    print(f"        -H 'Content-Type: application/json' \\")
    print(f"        -d @{WORKFLOW_FILE}")
    print()
    print("=" * 60)

    return False

def main():
    print()
    print("=" * 60)
    print("🤖 IMPORTADOR DE WORKFLOW N8N")
    print("=" * 60)
    print()

    # Passo 1: Testa conexão
    if not testar_conexao():
        print("💡 Verifique se:")
        print("   1. A VPS está online")
        print("   2. O n8n está rodando na porta 5678")
        print("   3. O firewall permite conexões")
        sys.exit(1)

    # Passo 2: Carrega workflow
    workflow = carregar_workflow()
    if not workflow:
        sys.exit(1)

    # Passo 3: Importa
    sucesso = importar_workflow(workflow)

    # Resultado final
    sys.exit(0 if sucesso else 1)

if __name__ == "__main__":
    main()
