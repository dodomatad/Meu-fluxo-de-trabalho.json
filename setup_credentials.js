#!/usr/bin/env node
/**
 * Script de configuração inicial
 * Cria o arquivo .env com as credenciais do usuário
 */

const fs = require('fs');
const readline = require('readline');
const path = require('path');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  blue: '\x1b[34m',
  yellow: '\x1b[33m',
  bold: '\x1b[1m'
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

async function perguntar(pergunta) {
  return new Promise((resolve) => {
    rl.question(pergunta, (resposta) => {
      resolve(resposta.trim());
    });
  });
}

async function setup() {
  console.clear();
  log('═'.repeat(60), 'bold');
  log('🔧 CONFIGURAÇÃO DO IMPORTADOR N8N', 'bold');
  log('═'.repeat(60), 'bold');
  console.log();

  log('Vamos configurar suas credenciais para o n8n.\n', 'blue');

  // Coleta informações
  const url = await perguntar('URL do n8n (padrão: http://162.240.164.165:5678): ') || 'http://162.240.164.165:5678';
  const email = await perguntar('Email de login do n8n: ');
  const password = await perguntar('Senha do n8n: ');
  const headless = await perguntar('Executar em modo invisível? (s/n, padrão: s): ') || 's';

  // Cria conteúdo do .env
  const envContent = `# Configurações para importador automático n8n

# URL do seu n8n
N8N_URL=${url}

# Credenciais de login
N8N_EMAIL=${email}
N8N_PASSWORD=${password}

# Modo do navegador
HEADLESS=${headless.toLowerCase() === 's' ? 'true' : 'false'}
`;

  // Salva arquivo
  const envPath = path.join(__dirname, '.env');
  fs.writeFileSync(envPath, envContent);

  console.log();
  log('═'.repeat(60), 'bold');
  log('✅ Configuração salva com sucesso!', 'green');
  log('═'.repeat(60), 'bold');
  console.log();
  log('📋 Arquivo criado: .env', 'blue');
  console.log();
  log('🚀 Agora você pode executar:', 'blue');
  log('   npm run import', 'green');
  console.log();

  rl.close();
}

setup();
