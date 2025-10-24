#!/usr/bin/env node
/**
 * 🎭 Importador Automático de Workflow n8n com Puppeteer
 *
 * Este script usa automação de navegador para:
 * 1. Fazer login no n8n
 * 2. Navegar até a área de workflows
 * 3. Importar automaticamente o arquivo JSON
 * 4. Confirmar a importação
 */

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

// Configurações
const N8N_URL = process.env.N8N_URL || 'http://162.240.164.165:5678';
const N8N_EMAIL = process.env.N8N_EMAIL || '';
const N8N_PASSWORD = process.env.N8N_PASSWORD || '';
const WORKFLOW_FILE = path.join(__dirname, 'workflows/My workflow 2.json');
const HEADLESS = process.env.HEADLESS !== 'false'; // Mostra navegador se HEADLESS=false
const TIMEOUT = 30000; // 30 segundos

// Cores para console
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  bold: '\x1b[1m'
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

function logStep(step, message) {
  log(`\n${step} ${message}`, 'blue');
}

function logSuccess(message) {
  log(`✅ ${message}`, 'green');
}

function logError(message) {
  log(`❌ ${message}`, 'red');
}

function logWarning(message) {
  log(`⚠️  ${message}`, 'yellow');
}

async function verificarArquivo() {
  logStep('📂', 'Verificando arquivo do workflow...');

  if (!fs.existsSync(WORKFLOW_FILE)) {
    logError(`Arquivo não encontrado: ${WORKFLOW_FILE}`);
    return false;
  }

  const stats = fs.statSync(WORKFLOW_FILE);
  const sizeKB = (stats.size / 1024).toFixed(2);

  logSuccess(`Arquivo encontrado (${sizeKB} KB)`);

  try {
    const content = JSON.parse(fs.readFileSync(WORKFLOW_FILE, 'utf8'));
    const workflowName = content.name || 'Sem nome';
    const nodeCount = content.nodes?.length || 0;

    log(`   Nome: ${workflowName}`);
    log(`   Nós: ${nodeCount}`);

    return true;
  } catch (e) {
    logError('Erro ao ler JSON do workflow');
    return false;
  }
}

async function verificarCredenciais() {
  logStep('🔐', 'Verificando credenciais...');

  if (!N8N_EMAIL || !N8N_PASSWORD) {
    logWarning('Credenciais não configuradas');
    log('   Configure o arquivo .env ou variáveis de ambiente:');
    log('   N8N_EMAIL=seu@email.com');
    log('   N8N_PASSWORD=suasenha');
    return false;
  }

  logSuccess('Credenciais encontradas');
  return true;
}

async function fazerLogin(page) {
  logStep('🔑', 'Fazendo login no n8n...');

  try {
    // Aguarda a página carregar
    await page.goto(N8N_URL, { waitUntil: 'networkidle2', timeout: TIMEOUT });

    // Verifica se já está logado (procura por elementos da home)
    const jaLogado = await page.evaluate(() => {
      return document.querySelector('[data-test-id="menu-item-workflows"]') !== null ||
             document.querySelector('nav') !== null;
    });

    if (jaLogado) {
      logSuccess('Já está logado!');
      return true;
    }

    // Aguarda o formulário de login aparecer
    await page.waitForSelector('input[type="email"], input[name="email"]', { timeout: 10000 });

    // Digita email
    await page.type('input[type="email"], input[name="email"]', N8N_EMAIL, { delay: 50 });
    logSuccess('Email digitado');

    // Digita senha
    await page.type('input[type="password"], input[name="password"]', N8N_PASSWORD, { delay: 50 });
    logSuccess('Senha digitada');

    // Clica no botão de login
    await Promise.all([
      page.click('button[type="submit"]'),
      page.waitForNavigation({ waitUntil: 'networkidle2', timeout: TIMEOUT })
    ]);

    logSuccess('Login realizado com sucesso!');
    return true;

  } catch (error) {
    logError(`Erro no login: ${error.message}`);
    return false;
  }
}

async function importarWorkflow(page) {
  logStep('📤', 'Importando workflow...');

  try {
    // Método 1: Tenta pelo menu principal
    logStep('1️⃣', 'Tentando método 1: Menu principal...');

    // Clica em Workflows no menu
    const workflowsMenu = await page.$('[data-test-id="menu-item-workflows"], a[href*="/workflows"]');
    if (workflowsMenu) {
      await workflowsMenu.click();
      await page.waitForTimeout(1000);
    }

    // Procura botão de adicionar workflow
    const addButton = await page.$(
      '[data-test-id="resources-list-add"], ' +
      'button[aria-label*="Add"], ' +
      'button:has-text("Add workflow"), ' +
      '.add-workflow-button'
    );

    if (addButton) {
      await addButton.click();
      await page.waitForTimeout(1000);

      // Procura opção de import
      const importOption = await page.$(
        '[data-test-id="import-workflow"], ' +
        'button:has-text("Import"), ' +
        'a:has-text("Import")'
      );

      if (importOption) {
        await importOption.click();
        await page.waitForTimeout(1000);
      }
    }

    // Método 2: Usar input file diretamente (mais confiável)
    logStep('2️⃣', 'Tentando método 2: Upload direto...');

    // Procura por input de arquivo (pode estar oculto)
    const fileInputs = await page.$$('input[type="file"]');

    if (fileInputs.length > 0) {
      logSuccess(`Encontrado ${fileInputs.length} input(s) de arquivo`);

      // Usa o primeiro input encontrado
      const fileInput = fileInputs[0];
      await fileInput.uploadFile(WORKFLOW_FILE);

      logSuccess('Arquivo enviado!');

      // Aguarda processamento
      await page.waitForTimeout(2000);

      // Procura e clica no botão de confirmar/importar
      const confirmSelectors = [
        'button:has-text("Import")',
        'button:has-text("Confirm")',
        'button[type="submit"]',
        '[data-test-id="confirm-import"]'
      ];

      for (const selector of confirmSelectors) {
        try {
          const button = await page.$(selector);
          if (button) {
            await button.click();
            logSuccess('Importação confirmada!');
            await page.waitForTimeout(2000);
            break;
          }
        } catch (e) {
          // Continua tentando
        }
      }

      return true;
    }

    // Método 3: Via URL direta de criação
    logStep('3️⃣', 'Tentando método 3: URL de criação...');

    await page.goto(`${N8N_URL}/workflow/new`, { waitUntil: 'networkidle2' });
    await page.waitForTimeout(2000);

    // Tenta novamente encontrar input de arquivo
    const fileInput2 = await page.$('input[type="file"]');
    if (fileInput2) {
      await fileInput2.uploadFile(WORKFLOW_FILE);
      logSuccess('Arquivo enviado via método 3!');
      return true;
    }

    logWarning('Nenhum método de importação funcionou automaticamente');
    return false;

  } catch (error) {
    logError(`Erro na importação: ${error.message}`);
    return false;
  }
}

async function capturarScreenshot(page, filename) {
  try {
    const screenshotPath = path.join(__dirname, filename);
    await page.screenshot({ path: screenshotPath, fullPage: true });
    log(`   Screenshot salvo: ${filename}`, 'blue');
  } catch (e) {
    // Ignora erros de screenshot
  }
}

async function main() {
  console.clear();
  log('═'.repeat(70), 'bold');
  log('🎭 IMPORTADOR AUTOMÁTICO DE WORKFLOW N8N (PUPPETEER)', 'bold');
  log('═'.repeat(70), 'bold');

  // Verificações iniciais
  if (!await verificarArquivo()) {
    process.exit(1);
  }

  const temCredenciais = await verificarCredenciais();

  let browser;

  try {
    // Inicia o navegador
    logStep('🌐', 'Iniciando navegador...');

    browser = await puppeteer.launch({
      headless: HEADLESS,
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--disable-accelerated-2d-canvas',
        '--disable-gpu'
      ]
    });

    const page = await browser.newPage();

    // Configurações da página
    await page.setViewport({ width: 1366, height: 768 });
    await page.setUserAgent('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');

    logSuccess('Navegador iniciado');

    // Acessa o n8n
    logStep('🌍', `Acessando ${N8N_URL}...`);
    await page.goto(N8N_URL, { waitUntil: 'networkidle2', timeout: TIMEOUT });
    logSuccess('Página carregada');

    // Captura screenshot inicial
    await capturarScreenshot(page, 'screenshot-01-inicial.png');

    // Faz login se necessário
    if (temCredenciais) {
      const loginOk = await fazerLogin(page);
      if (!loginOk) {
        logWarning('Login falhou, tentando continuar...');
      }
      await capturarScreenshot(page, 'screenshot-02-depois-login.png');
    }

    // Importa o workflow
    const importOk = await importarWorkflow(page);
    await capturarScreenshot(page, 'screenshot-03-depois-import.png');

    // Aguarda um pouco para ver o resultado
    await page.waitForTimeout(3000);

    // Resultado final
    log('\n' + '═'.repeat(70), 'bold');
    if (importOk) {
      logSuccess('WORKFLOW IMPORTADO COM SUCESSO!');
      log('═'.repeat(70), 'bold');
      log('\n📋 Próximos passos:');
      log('   1. Acesse seu n8n e verifique o workflow');
      log('   2. Configure as credenciais necessárias');
      log('   3. Ative o workflow\n');
    } else {
      logWarning('IMPORTAÇÃO AUTOMÁTICA NÃO CONCLUÍDA');
      log('═'.repeat(70), 'bold');
      log('\n💡 Alternativas:');
      log('   1. Verifique os screenshots gerados');
      log('   2. Execute com HEADLESS=false para ver o navegador');
      log('   3. Use importação manual no n8n\n');
    }

    if (!HEADLESS) {
      log('ℹ️  Navegador permanece aberto. Pressione Ctrl+C para fechar.\n', 'yellow');
      await new Promise(() => {}); // Mantém aberto indefinidamente
    }

  } catch (error) {
    logError(`\nErro fatal: ${error.message}`);
    console.error(error);
    process.exit(1);

  } finally {
    if (browser && HEADLESS) {
      await browser.close();
      log('\n🔒 Navegador fechado\n');
    }
  }
}

// Executa
main().catch(console.error);
