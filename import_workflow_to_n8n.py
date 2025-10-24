#!/usr/bin/env python3
"""
Script para importar workflow do n8n automaticamente via API
Lê o arquivo workflows/My workflow 2.json e envia para a instância n8n na VPS
"""

import json
import requests
import os
from pathlib import Path

# Configurações da API n8n
N8N_URL = "http://162.240.164.165:5678"
N8N_API_KEY = os.getenv("N8N_API_KEY", "")  # Defina a variável de ambiente N8N_API_KEY

# Caminho do arquivo workflow
WORKFLOW_FILE = "workflows/My workflow 2.json"


def load_workflow(file_path):
    """
    Carrega o workflow do arquivo JSON

    Args:
        file_path (str): Caminho para o arquivo do workflow

    Returns:
        dict: Dados do workflow
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            workflow_data = json.load(f)
        print(f"✅ Workflow carregado com sucesso: {file_path}")
        return workflow_data
    except FileNotFoundError:
        print(f"❌ Erro: Arquivo não encontrado: {file_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Erro ao decodificar JSON: {e}")
        return None


def import_workflow_to_n8n(workflow_data, n8n_url, api_key):
    """
    Importa o workflow para o n8n via API

    Args:
        workflow_data (dict): Dados do workflow
        n8n_url (str): URL da instância n8n
        api_key (str): Chave da API do n8n

    Returns:
        bool: True se importado com sucesso, False caso contrário
    """
    endpoint = f"{n8n_url}/api/v1/workflows"

    headers = {
        "Content-Type": "application/json",
    }

    # Adiciona API key se fornecida
    if api_key:
        headers["X-N8N-API-KEY"] = api_key

    try:
        # Remove campos que não devem ser enviados na criação
        workflow_payload = {
            "name": workflow_data.get("name", "Imported Workflow"),
            "nodes": workflow_data.get("nodes", []),
            "connections": workflow_data.get("connections", {}),
            "settings": workflow_data.get("settings", {}),
            "active": False  # Não ativa automaticamente
        }

        # Adiciona tags se existirem
        if "tags" in workflow_data:
            workflow_payload["tags"] = workflow_data["tags"]

        print(f"📤 Enviando workflow para {n8n_url}...")
        response = requests.post(endpoint, json=workflow_payload, headers=headers, timeout=30)

        if response.status_code in [200, 201]:
            result = response.json()
            workflow_id = result.get("id", "unknown")
            print(f"✅ Workflow importado com sucesso!")
            print(f"   ID: {workflow_id}")
            print(f"   Nome: {result.get('name', 'N/A')}")
            print(f"   URL: {n8n_url}/workflow/{workflow_id}")
            return True
        else:
            print(f"❌ Erro ao importar workflow")
            print(f"   Status Code: {response.status_code}")
            print(f"   Resposta: {response.text}")
            return False

    except requests.exceptions.ConnectionError:
        print(f"❌ Erro de conexão: Não foi possível conectar ao n8n em {n8n_url}")
        print("   Verifique se:")
        print("   1. A VPS está acessível")
        print("   2. O n8n está rodando na porta 5678")
        print("   3. O firewall permite conexões")
        return False
    except requests.exceptions.Timeout:
        print(f"❌ Timeout: A requisição demorou muito para responder")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False


def check_n8n_connection(n8n_url):
    """
    Verifica se o n8n está acessível

    Args:
        n8n_url (str): URL da instância n8n

    Returns:
        bool: True se acessível, False caso contrário
    """
    try:
        print(f"🔍 Verificando conexão com {n8n_url}...")
        response = requests.get(f"{n8n_url}/healthz", timeout=10)
        if response.status_code == 200:
            print("✅ n8n está acessível e respondendo")
            return True
        else:
            print(f"⚠️  n8n respondeu com status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Não foi possível conectar ao n8n")
        return False
    except Exception as e:
        print(f"❌ Erro ao verificar conexão: {e}")
        return False


def main():
    """
    Função principal
    """
    print("=" * 60)
    print("🤖 Importador de Workflow n8n")
    print("=" * 60)
    print()

    # Verifica se a API key está configurada
    if not N8N_API_KEY:
        print("⚠️  Aviso: N8N_API_KEY não está configurada")
        print("   Defina a variável de ambiente antes de executar:")
        print("   export N8N_API_KEY='sua_chave_aqui'")
        print()
        print("   Tentando continuar sem autenticação...")
        print()

    # Verifica conexão com n8n
    if not check_n8n_connection(N8N_URL):
        print()
        print("💡 Dica: Se você está usando autenticação básica, a API pode estar em:")
        print(f"   {N8N_URL}/rest/workflows")
        return

    print()

    # Carrega o workflow
    workflow_data = load_workflow(WORKFLOW_FILE)
    if not workflow_data:
        return

    print()
    print(f"📊 Informações do workflow:")
    print(f"   Nome: {workflow_data.get('name', 'N/A')}")
    print(f"   Nós: {len(workflow_data.get('nodes', []))}")
    print(f"   Ativo: {workflow_data.get('active', False)}")
    print()

    # Importa o workflow
    success = import_workflow_to_n8n(workflow_data, N8N_URL, N8N_API_KEY)

    print()
    print("=" * 60)
    if success:
        print("🎉 Processo concluído com sucesso!")
    else:
        print("⚠️  Processo concluído com erros")
    print("=" * 60)


if __name__ == "__main__":
    main()
