# ⚡ QUICK START - Importar Workflow em 3 Passos

## 🎭 Método Puppeteer (Automático - RECOMENDADO!)

### Instalação Única (3 minutos)

```bash
# 1. Entrar na pasta
cd Meu-fluxo-de-trabalho.json

# 2. Instalar dependências
npm install

# 3. Configurar credenciais
npm run setup
```

### Executar (30 segundos)

```bash
npm run import
```

**Pronto!** O navegador abre, faz login e importa tudo sozinho! 🎉

---

## 🐍 Método Python (Com API Key)

```bash
# 1. Criar API Key no n8n
# Acesse: http://162.240.164.165:5678 → Settings → API

# 2. Executar
N8N_API_KEY='sua_chave' python3 import_n8n.py
```

---

## 👆 Método Manual (Mais Simples)

1. Abra: http://162.240.164.165:5678
2. Clique: Workflows → "+" → ⋮ → "Import from File"
3. Selecione: `workflows/My workflow 2.json`

---

## 🗄️ Criar Tabela PostgreSQL (IMPORTANTE!)

Execute no seu banco:

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
```

---

## ⚙️ Configurar Credencial no n8n

1. Acesse: **Settings → Credentials**
2. Crie: **PostgreSQL**
3. Nome: `PostgreSQL Conversas`
4. Salve

---

## ✅ Checklist Final

- [ ] Workflow importado
- [ ] Tabela PostgreSQL criada
- [ ] Credencial PostgreSQL configurada
- [ ] Outras credenciais verificadas (OpenAI, Supabase, Redis)
- [ ] Workflow ativado

---

## 📚 Documentação Completa

- **README_PUPPETEER.md**: Tudo sobre automação com Puppeteer
- **GUIA_RAPIDO.md**: Instruções detalhadas todos os métodos
- **README_IMPORT.md**: Documentação técnica API Python

---

## 🆘 Problemas?

### Puppeteer não funciona
```bash
# Execute com navegador visível para debug
HEADLESS=false npm run import
```

### API Python retorna 403
Use o método Puppeteer ou importação manual

### Workflow importado mas não funciona
Verifique se todas as credenciais estão configuradas no n8n

---

**Escolha o método que preferir - todos funcionam!** 🚀
