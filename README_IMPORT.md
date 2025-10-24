# 📤 Como Importar o Workflow para o n8n

## Pré-requisitos

1. **Python 3.6+** instalado
2. **Biblioteca requests**:
   ```bash
   pip install requests
   ```

3. **Acesso à API do n8n**

## Configuração da API Key

### Método 1: Obter API Key no n8n

1. Acesse seu n8n: `http://162.240.164.165:5678`
2. Vá em **Settings** → **API**
3. Clique em **Create API Key**
4. Copie a chave gerada

### Método 2: Configurar Variável de Ambiente

```bash
export N8N_API_KEY='sua_chave_api_aqui'
```

Para tornar permanente, adicione ao `~/.bashrc` ou `~/.zshrc`:

```bash
echo 'export N8N_API_KEY="sua_chave_api_aqui"' >> ~/.bashrc
source ~/.bashrc
```

## Uso do Script

### Execução Simples

```bash
python3 import_workflow_to_n8n.py
```

Ou, se o script for executável:

```bash
./import_workflow_to_n8n.py
```

### Com API Key Inline

```bash
N8N_API_KEY='sua_chave' python3 import_workflow_to_n8n.py
```

## O que o Script Faz

1. ✅ Verifica conexão com o n8n
2. ✅ Lê o arquivo `workflows/My workflow 2.json`
3. ✅ Envia o workflow via API REST do n8n
4. ✅ Retorna confirmação com ID e URL do workflow

## Exemplo de Saída

```
============================================================
🤖 Importador de Workflow n8n
============================================================

🔍 Verificando conexão com http://162.240.164.165:5678...
✅ n8n está acessível e respondendo

✅ Workflow carregado com sucesso: workflows/My workflow 2.json

📊 Informações do workflow:
   Nome: My workflow 2
   Nós: 127
   Ativo: False

📤 Enviando workflow para http://162.240.164.165:5678...
✅ Workflow importado com sucesso!
   ID: xEOkeKozNeC4Jw6V
   Nome: My workflow 2
   URL: http://162.240.164.165:5678/workflow/xEOkeKozNeC4Jw6V

============================================================
🎉 Processo concluído com sucesso!
============================================================
```

## Resolução de Problemas

### Erro de Conexão

Se receber erro de conexão:

1. Verifique se o n8n está rodando:
   ```bash
   curl http://162.240.164.165:5678/healthz
   ```

2. Verifique o firewall:
   ```bash
   sudo ufw status
   ```

3. Teste a conexão SSH:
   ```bash
   ping 162.240.164.165
   ```

### Erro 401 (Não Autorizado)

- Verifique se a API Key está correta
- Confirme que a autenticação está habilitada no n8n

### Erro 404 (Not Found)

O endpoint pode ser diferente. Tente:

- `/api/v1/workflows`
- `/rest/workflows`

Edite a variável `endpoint` no script conforme necessário.

## Configurações do n8n

### Habilitar API

Certifique-se de que a API está habilitada no n8n:

```bash
# No arquivo .env do n8n
N8N_API_ENABLED=true
```

### Sem Autenticação (Desenvolvimento)

Se estiver em ambiente de desenvolvimento sem autenticação:

```bash
# Deixe N8N_API_KEY vazio
unset N8N_API_KEY
```

## Estrutura da Tabela PostgreSQL

Antes de ativar o workflow, crie a tabela de conversas:

```sql
CREATE TABLE conversation_history (
  id SERIAL PRIMARY KEY,
  phone_number VARCHAR(255),
  user_message TEXT,
  bot_response TEXT,
  message_type VARCHAR(50),
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  session_id VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para melhor performance
CREATE INDEX idx_phone_number ON conversation_history(phone_number);
CREATE INDEX idx_session_id ON conversation_history(session_id);
CREATE INDEX idx_timestamp ON conversation_history(timestamp);
```

## Alterações Realizadas no Workflow

### ✅ 1. Modelo OpenAI Atualizado

- **OpenAI1** (análise de imagens): `gpt-4o-mini` → `gpt-4o`
- **OpenAI Model** (treinamento): `gpt-4o-mini` → `gpt-4o`

### ✅ 2. Novo Nó PostgreSQL

- **Nome**: "Salvar Conversa PostgreSQL"
- **Tipo**: Insert automático
- **Tabela**: `conversation_history`
- **Campos salvos**:
  - Telefone do cliente
  - Mensagem do usuário
  - Resposta da IA
  - Tipo de mensagem
  - Timestamp
  - Session ID

## Próximos Passos

1. Execute o script de importação
2. Acesse o n8n e configure as credenciais PostgreSQL
3. Ative o workflow
4. Teste enviando uma mensagem WhatsApp

## Suporte

Para problemas ou dúvidas, consulte:
- [Documentação n8n API](https://docs.n8n.io/api/)
- [n8n Community](https://community.n8n.io/)
