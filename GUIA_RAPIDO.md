# 🚀 GUIA RÁPIDO - Importar Workflow para n8n

## ⚡ Importação Manual (Mais Fácil!)

### 1. Acesse seu n8n
```
http://162.240.164.165:5678
```

### 2. Importe o arquivo
1. Clique em **Workflows** (menu lateral)
2. Clique no botão **"+"** (Novo Workflow)
3. Clique nos **3 pontos** (⋮) no canto superior direito
4. Selecione **"Import from File"**
5. Escolha: `workflows/My workflow 2.json`

### 3. Configure a credencial PostgreSQL
1. Vá em **Settings → Credentials**
2. Clique em **"+ Add Credential"**
3. Procure por **PostgreSQL**
4. Preencha:
   - **Name**: `PostgreSQL Conversas`
   - **Host**: seu_host_postgres
   - **Database**: seu_database
   - **User**: seu_usuario
   - **Password**: sua_senha
   - **Port**: `5432`
5. Clique em **Save**

### 4. Crie a tabela no PostgreSQL
Execute este SQL no seu banco:

```sql
CREATE TABLE conversation_history (
  id SERIAL PRIMARY KEY,
  phone_number VARCHAR(255),
  user_message TEXT,
  bot_response TEXT,
  message_type VARCHAR(50),
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  session_id VARCHAR(255)
);

CREATE INDEX idx_phone_number ON conversation_history(phone_number);
CREATE INDEX idx_session_id ON conversation_history(session_id);
CREATE INDEX idx_timestamp ON conversation_history(timestamp);
```

### 5. Ative o workflow
1. No editor do workflow, clique no botão **"Active"** (canto superior direito)
2. Pronto! ✅

---

## 🤖 Importação Automática (Requer API Key)

### Método 1: Com API Key

#### Obter API Key do n8n
1. Acesse: `http://162.240.164.165:5678`
2. Vá em **Settings → API**
3. Clique em **"Create API Key"**
4. Copie a chave gerada

#### Executar script
```bash
cd Meu-fluxo-de-trabalho.json
N8N_API_KEY='sua_chave_aqui' python3 import_n8n.py
```

### Método 2: Com usuário e senha

```bash
cd Meu-fluxo-de-trabalho.json
N8N_USERNAME='seu_usuario' N8N_PASSWORD='sua_senha' python3 import_n8n.py
```

### Método 3: Script simples

```bash
cd Meu-fluxo-de-trabalho.json
python3 import_n8n.py
```

---

## 📊 Verificar se o n8n está online

```bash
curl http://162.240.164.165:5678
```

Se retornar código **200** ou **403**, está online! ✅

---

## ✨ O que foi alterado no workflow?

### 1. Modelos OpenAI atualizados
- ✅ `gpt-4o-mini` → `gpt-4o` (análise de imagens)
- ✅ `gpt-4o-mini` → `gpt-4o` (agente de treinamento)

### 2. Novo nó de logging PostgreSQL
- ✅ Salva automaticamente todas as conversas
- ✅ Registra: telefone, mensagem, resposta, tipo, timestamp
- ✅ Conectado ao fluxo do agente principal

---

## 🔧 Troubleshooting

### Erro 403 ao importar automaticamente
**Solução**: Use importação manual (mais fácil!) ou configure API Key

### Workflow importado mas não funciona
**Solução**: Verifique se todas as credenciais estão configuradas:
- OpenAI API Key
- PostgreSQL (novo!)
- Supabase
- Redis
- Evolution API

### Tabela PostgreSQL não existe
**Solução**: Execute o SQL da seção 4

### Nó PostgreSQL com erro
**Solução**:
1. Verifique a credencial PostgreSQL
2. Confirme que a tabela `conversation_history` existe
3. Teste a conexão

---

## 📞 Scripts disponíveis

| Script | Descrição |
|--------|-----------|
| `import_n8n.py` | Script completo com múltiplos métodos de autenticação |
| `import_workflow_simple.py` | Script simples que tenta vários endpoints |
| `import_workflow_to_n8n.py` | Script original com documentação detalhada |

**Recomendado**: Use `import_n8n.py` - é o mais completo!

---

## 🎯 Checklist de ativação

- [ ] Workflow importado no n8n
- [ ] Tabela PostgreSQL criada
- [ ] Credencial PostgreSQL configurada
- [ ] Demais credenciais verificadas
- [ ] Workflow ativado
- [ ] Teste realizado com mensagem WhatsApp

---

## 📚 Arquivos importantes

```
Meu-fluxo-de-trabalho.json/
├── workflows/
│   └── My workflow 2.json          # Workflow atualizado
├── import_n8n.py                   # ⭐ Script recomendado
├── import_workflow_simple.py       # Script alternativo
├── import_workflow_to_n8n.py       # Script original
├── README_IMPORT.md                # Documentação completa
└── GUIA_RAPIDO.md                  # Este arquivo
```

---

## ✅ Resumo das alterações

### Modelos OpenAI
- 2 nós atualizados de `gpt-4o-mini` para `gpt-4o`
- Melhor qualidade nas respostas

### Novo nó PostgreSQL
- Salva 100% das conversas
- Histórico completo para análise
- Backup de todas as interações

### Scripts Python
- 3 scripts diferentes disponíveis
- Suporte a API Key, Basic Auth e manual
- Instruções detalhadas para cada caso

---

**Dica**: Se tiver dúvidas, comece pela **importação manual** - é mais rápido e simples! 🚀
