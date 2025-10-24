# 🎭 Importador Automático de Workflow n8n com Puppeteer

## 🚀 O QUE É ISSO?

Este é um script **100% automatizado** que:
- ✅ Abre o navegador
- ✅ Faz login no n8n
- ✅ Navega até a área de workflows
- ✅ Importa automaticamente o arquivo JSON
- ✅ Confirma a importação
- ✅ Tira screenshots do processo

**Não precisa fazer NADA manualmente!** 🎉

---

## 📦 INSTALAÇÃO

### Passo 1: Instalar Node.js

Se não tiver Node.js instalado:

```bash
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verificar instalação
node --version
npm --version
```

### Passo 2: Instalar Dependências

```bash
cd Meu-fluxo-de-trabalho.json
npm install
```

Isso vai instalar:
- **Puppeteer**: Automação de navegador
- **dotenv**: Gerenciamento de variáveis de ambiente
- **chalk**: Cores no terminal

### Passo 3: Configurar Credenciais

```bash
npm run setup
```

Ou crie manualmente o arquivo `.env`:

```bash
cp .env.example .env
nano .env
```

Preencha:
```env
N8N_URL=http://162.240.164.165:5678
N8N_EMAIL=seu@email.com
N8N_PASSWORD=suasenha
HEADLESS=true
```

---

## 🎯 USO

### Modo Simples (Recomendado)

```bash
npm run import
```

### Modo Avançado

```bash
# Mostrar o navegador (para debug)
HEADLESS=false npm run import

# Usar URL diferente
N8N_URL=http://outro-server:5678 npm run import

# Executar diretamente
node import_with_puppeteer.js
```

---

## 📊 O QUE ACONTECE

```
═══════════════════════════════════════════════════════════════════
🎭 IMPORTADOR AUTOMÁTICO DE WORKFLOW N8N (PUPPETEER)
═══════════════════════════════════════════════════════════════════

📂 Verificando arquivo do workflow...
✅ Arquivo encontrado (101.23 KB)
   Nome: My workflow 2
   Nós: 132

🔐 Verificando credenciais...
✅ Credenciais encontradas

🌐 Iniciando navegador...
✅ Navegador iniciado

🌍 Acessando http://162.240.164.165:5678...
✅ Página carregada
   Screenshot salvo: screenshot-01-inicial.png

🔑 Fazendo login no n8n...
✅ Email digitado
✅ Senha digitada
✅ Login realizado com sucesso!
   Screenshot salvo: screenshot-02-depois-login.png

📤 Importando workflow...

1️⃣ Tentando método 1: Menu principal...

2️⃣ Tentando método 2: Upload direto...
✅ Encontrado 1 input(s) de arquivo
✅ Arquivo enviado!
✅ Importação confirmada!
   Screenshot salvo: screenshot-03-depois-import.png

═══════════════════════════════════════════════════════════════════
✅ WORKFLOW IMPORTADO COM SUCESSO!
═══════════════════════════════════════════════════════════════════

📋 Próximos passos:
   1. Acesse seu n8n e verifique o workflow
   2. Configure as credenciais necessárias
   3. Ative o workflow

🔒 Navegador fechado
```

---

## 🎨 SCREENSHOTS AUTOMÁTICOS

O script tira 3 screenshots automaticamente:

1. **`screenshot-01-inicial.png`**: Página inicial do n8n
2. **`screenshot-02-depois-login.png`**: Após fazer login
3. **`screenshot-03-depois-import.png`**: Após importar workflow

Use essas imagens para verificar o que aconteceu! 📸

---

## 🐛 DEBUG

### Ver o navegador em ação

```bash
HEADLESS=false npm run import
```

Isso mostra o navegador fazendo tudo automaticamente! 🎬

### Manter navegador aberto

```bash
HEADLESS=false npm run import
# O navegador fica aberto, pressione Ctrl+C para fechar
```

---

## 🔧 TROUBLESHOOTING

### Erro: "Arquivo não encontrado"

Certifique-se de que o arquivo existe:
```bash
ls -lh workflows/My\ workflow\ 2.json
```

### Erro: "Login falhou"

Verifique suas credenciais no arquivo `.env`:
```bash
cat .env
```

### Erro: "puppeteer não encontrado"

Instale as dependências:
```bash
npm install
```

### Erro: "Chromium não instalou"

Em algumas distros Linux, instale dependências:
```bash
sudo apt-get install -y \
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
  libasound2
```

### O script não encontra o botão de importar

1. Execute com `HEADLESS=false` para ver o que acontece
2. Verifique os screenshots gerados
3. O n8n pode ter mudado a interface - ajuste os seletores no código

---

## 📚 ESTRUTURA DOS ARQUIVOS

```
Meu-fluxo-de-trabalho.json/
├── package.json                   # Dependências Node.js
├── import_with_puppeteer.js       # 🎭 Script principal
├── setup_credentials.js           # Script de configuração
├── .env.example                   # Exemplo de configuração
├── .env                           # Suas credenciais (CRIAR)
├── workflows/
│   └── My workflow 2.json         # Workflow a ser importado
└── screenshot-*.png               # Screenshots gerados
```

---

## ⚙️ VARIÁVEIS DE AMBIENTE

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `N8N_URL` | URL do n8n | `http://162.240.164.165:5678` |
| `N8N_EMAIL` | Email de login | - |
| `N8N_PASSWORD` | Senha | - |
| `HEADLESS` | Executar sem mostrar navegador | `true` |

---

## 🎯 COMPARAÇÃO DE MÉTODOS

| Método | Dificuldade | Velocidade | Requer Config |
|--------|-------------|------------|---------------|
| **Puppeteer** (este!) | ⭐ Fácil | 🚀 Rápido | Sim (uma vez) |
| Python + API | ⭐⭐ Média | ⚡ Muito rápido | Sim (API Key) |
| Manual | ⭐ Muito fácil | 🐢 Lento | Não |

---

## 🎓 COMO FUNCIONA

### 1. Inicia o navegador Chrome headless
```javascript
const browser = await puppeteer.launch({ headless: true });
```

### 2. Acessa o n8n
```javascript
await page.goto('http://162.240.164.165:5678');
```

### 3. Faz login automaticamente
```javascript
await page.type('input[type="email"]', email);
await page.type('input[type="password"]', password);
await page.click('button[type="submit"]');
```

### 4. Procura o input de arquivo
```javascript
const fileInput = await page.$('input[type="file"]');
await fileInput.uploadFile('./workflows/My workflow 2.json');
```

### 5. Confirma a importação
```javascript
await page.click('button:has-text("Import")');
```

---

## 🚀 SCRIPTS NPM

```bash
npm run import       # Importa o workflow
npm run setup        # Configuração interativa
npm run install-deps # Instala dependências
```

---

## 💡 DICAS PRO

### 1. Execute uma vez para configurar
```bash
npm run setup
npm run import
```

### 2. Para importar múltiplos workflows

Modifique a variável `WORKFLOW_FILE` no script ou crie um loop:

```javascript
const workflows = ['workflow1.json', 'workflow2.json'];
for (const wf of workflows) {
  // ... importar cada um
}
```

### 3. Integre com CI/CD

Adicione ao seu GitHub Actions ou GitLab CI:

```yaml
- name: Import workflow to n8n
  env:
    N8N_EMAIL: ${{ secrets.N8N_EMAIL }}
    N8N_PASSWORD: ${{ secrets.N8N_PASSWORD }}
  run: |
    npm install
    npm run import
```

---

## 🔐 SEGURANÇA

⚠️ **IMPORTANTE**: Nunca commite o arquivo `.env` com suas credenciais!

O arquivo `.gitignore` já está configurado para ignorar:
- `.env`
- `node_modules/`
- `*.png` (screenshots)

---

## 📦 DEPENDÊNCIAS

- **puppeteer** (^21.5.0): Automação de navegador Chromium
- **dotenv** (^16.3.1): Gerenciamento de variáveis de ambiente
- **chalk** (^4.1.2): Cores no terminal

---

## 🎉 RESULTADO FINAL

Após executar com sucesso:

1. ✅ Workflow importado no n8n
2. ✅ Screenshots salvos para auditoria
3. ✅ Pronto para configurar credenciais e ativar

---

## 🆚 QUANDO USAR CADA MÉTODO?

### Use Puppeteer se:
- ✅ Você tem credenciais de login
- ✅ A API não está habilitada
- ✅ Quer automatizar sem configurar API Key
- ✅ Precisa de screenshots do processo

### Use API Python se:
- ✅ API está habilitada e configurada
- ✅ Quer máxima velocidade
- ✅ Vai integrar com outros scripts Python

### Use Manual se:
- ✅ É sua primeira vez
- ✅ Quer entender o processo
- ✅ Não quer instalar dependências

---

**Desenvolvido com ❤️ por Claude Code**

*Este script foi criado para facilitar o deployment de workflows n8n em ambientes automatizados!*
