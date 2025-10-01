# Documentação Detalhada - Server MCP Host

## 📋 Visão Geral

Este documento explica detalhadamente cada função e a organização do arquivo `server.ts` do projeto MCP Host. O servidor implementa uma arquitetura HTTP nativa minimalista para demonstrar o protocolo MCP em sistemas médicos.

## 🏗️ Estrutura do Arquivo server.ts

O arquivo está organizado em **5 seções principais**:

1. **Importações e Configuração** (linhas 1-3)
2. **Funções Utilitárias** (linhas 5-22)
3. **Handler Principal do Servidor** (linhas 24-102)
4. **Inicialização do Servidor** (linhas 104-114)
5. **Gerenciamento de Sinais** (linhas 116-130)

---

## 📦 1. Importações e Configuração

```typescript
import * as http from 'http';

const PORT = process.env.PORT || 3001;
```

### Análise:
- **`import * as http`**: Importa o módulo HTTP nativo do Node.js
- **`PORT`**: Configuração de porta flexível (variável de ambiente ou padrão 3001)

### Por que usar HTTP nativo?
- **Performance**: Sem overhead de frameworks
- **Simplicidade**: Código direto e transparente
- **Controle**: Controle total sobre requests/responses

---

## 🛠️ 2. Funções Utilitárias

### 2.1. parseBody() - Parsing de Requisições JSON

```typescript
const parseBody = async (req: http.IncomingMessage): Promise<any> => {
  return new Promise((resolve, reject) => {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      try {
        resolve(body ? JSON.parse(body) : {});
      } catch (error) {
        reject(new Error('Invalid JSON'));
      }
    });
  });
};
```

### Função: Converter stream de dados em objeto JavaScript

**Parâmetros:**
- `req`: Objeto de requisição HTTP

**Retorno:**
- `Promise<any>`: Dados parseados ou erro

**Fluxo de Execução:**
1. **Coleta de dados**: Escuta eventos `'data'` para concatenar chunks
2. **Finalização**: No evento `'end'`, processa o body completo
3. **Parse JSON**: Converte string para objeto JavaScript
4. **Tratamento de erro**: Captura erros de JSON inválido

**Por que usar Promises com eventos?**
- O Node.js streams são assíncronos por natureza
- Promise oferece interface mais limpa que callbacks
- Permite uso de `async/await` no handler principal

### 2.2. sendResponse() - Padronização de Respostas

```typescript
const sendResponse = (res: http.ServerResponse, statusCode: number, data: any) => {
  res.writeHead(statusCode, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify(data, null, 2));
};
```

### Função: Enviar resposta HTTP padronizada

**Parâmetros:**
- `res`: Objeto de resposta HTTP
- `statusCode`: Código de status HTTP (200, 404, 500, etc.)
- `data`: Dados para serialização JSON

**Características:**
- **Headers**: Define Content-Type como JSON
- **Formatação**: `JSON.stringify` com indentação (2 espaços)
- **Finalização**: `res.end()` fecha a conexão

**Vantagens da centralização:**
- Consistência em todas as respostas
- Headers padronizados automaticamente
- Fácil manutenção e modificação

---

## 🚀 3. Handler Principal do Servidor

```typescript
const server = http.createServer(async (req: http.IncomingMessage, res: http.ServerResponse) => {
  // Processamento das requisições
});
```

### 3.1. Extração de Informações da Requisição

```typescript
const url = new URL(req.url || '/', `http://localhost:${PORT}`);
const path = url.pathname;
const method = req.method;

console.log(`[${method}] ${path}`);
```

**Função:** Extrair e logar informações da requisição

- **URL parsing**: Converte string URL em objeto URL
- **Path extraction**: Obtém caminho sem query parameters
- **Method extraction**: GET, POST, etc.
- **Logging**: Log simples para debug

### 3.2. Roteamento GET /health

```typescript
if (method === 'GET' && path === '/health') {
  sendResponse(res, 200, { status: 'ok' });
  return;
}
```

**Função:** Endpoint de verificação de saúde

- **Condição**: Método GET + caminho `/health`
- **Resposta**: Status 200 com `{"status": "ok"}`
- **Return**: Sai da função para evitar processamento adicional

**Importância do Health Check:**
- Monitoramento de aplicação
- Load balancers verificam disponibilidade
- Debugging rápido

### 3.3. Roteamento POST - Domínios Médicos

```typescript
if (method === 'POST') {
  try {
    const body = await parseBody(req);
    
    switch (path) {
      case '/agendamento':
        // Processamento
      case '/cancelamento':
        // Processamento  
      case '/pagamento':
        // Processamento
      case '/exame':
        // Processamento
      default:
        // 404
    }
  } catch (error) {
    // Tratamento de erro
  }
}
```

**Estrutura de Controle:**
1. **Verificação de método**: Apenas POST
2. **Parse do body**: Converte JSON em objeto
3. **Switch/case**: Roteamento por path
4. **Try/catch**: Captura erros de parsing

### 3.4. Implementação dos Endpoints Médicos

Cada endpoint segue o mesmo padrão:

```typescript
case '/agendamento':
  console.log('[INFO] Processando agendamento...');
  sendResponse(res, 200, { 
    success: true, 
    message: 'Agendamento processado',
    data: body 
  });
  break;
```

**Padrão comum:**
1. **Log informativo**: Indica processamento
2. **Resposta estruturada**:
   - `success: true` - Indicador de sucesso
   - `message` - Mensagem descritiva
   - `data` - Echo dos dados recebidos

**Domínios implementados:**
- **`/agendamento`**: Consultas médicas
- **`/cancelamento`**: Cancelamento de consultas
- **`/pagamento`**: Processamento de pagamentos
- **`/exame`**: Exames laboratoriais

### 3.5. Tratamento de Erros

```typescript
} catch (error) {
  console.error('[ERROR]', (error as Error).message);
  sendResponse(res, 500, {
    success: false,
    error: 'Erro interno do servidor'
  });
}
```

**Estratégia de erro:**
- **Log do erro**: Console.error para debug
- **Type casting**: `(error as Error)` para acessar `.message`
- **Resposta genérica**: Não expõe detalhes internos
- **Status 500**: Erro interno do servidor

### 3.6. Fallback 404

```typescript
sendResponse(res, 404, {
  success: false,
  error: `Rota ${method} ${path} não encontrada`
});
```

**Função:** Capturar requisições não atendidas
- **Informativo**: Inclui método e path na mensagem
- **Status 404**: Not Found
- **Formato consistente**: Mesmo padrão de resposta

---

## 🎛️ 4. Inicialização do Servidor

```typescript
server.listen(PORT, () => {
  console.log('\\n🚀 MCP Host - Servidor HTTP Simples');
  console.log(`📊 Rodando em: http://localhost:${PORT}`);
  console.log(`\\n🏥 Endpoints disponíveis:`);
  console.log(`   • GET  /health         - Status ok`);
  console.log(`   • POST /agendamento    - Agendamentos`);
  console.log(`   • POST /cancelamento   - Cancelamentos`);
  console.log(`   • POST /pagamento      - Pagamentos`);
  console.log(`   • POST /exame          - Exames`);
  console.log(`\\n✨ Servidor HTTP nativo funcionando!\\n`);
});
```

**Função:** Inicializar servidor na porta configurada

**Callback de inicialização:**
- **Banner informativo**: Identificação do servidor
- **URL de acesso**: Facilita testes
- **Lista de endpoints**: Documentação visual
- **Emojis**: Interface mais amigável

**Vantagens do banner:**
- Feedback visual imediato
- Documentação inline
- Facilita debugging

---

## ⚡ 5. Gerenciamento de Sinais

### 5.1. SIGTERM - Terminação Graceful

```typescript
process.on('SIGTERM', () => {
  console.log('\\n[INFO] Desligando servidor...');
  server.close(() => {
    console.log('[INFO] Servidor desligado');
    process.exit(0);
  });
});
```

### 5.2. SIGINT - Interrupção (Ctrl+C)

```typescript
process.on('SIGINT', () => {
  console.log('\\n[INFO] Desligando servidor...');
  server.close(() => {
    console.log('[INFO] Servidor desligado');
    process.exit(0);
  });
});
```

**Função:** Desligamento limpo do servidor

**Fluxo de shutdown:**
1. **Captura do sinal**: `process.on()`
2. **Log informativo**: Usuário sabe que está desligando
3. **Fechamento do servidor**: `server.close()` para finalizar conexões
4. **Exit graceful**: `process.exit(0)` com código de sucesso

**Importância:**
- Finaliza conexões ativas adequadamente
- Evita perda de dados
- Permite cleanup de recursos

---

## 🔄 Fluxo de Execução Completo

### Cenário: POST /agendamento com dados JSON

```
1. Cliente faz requisição POST para /agendamento
   ↓
2. server.createServer() recebe a requisição
   ↓
3. Handler extrai method=POST, path=/agendamento
   ↓
4. Log: "[POST] /agendamento"
   ↓
5. parseBody() converte stream em objeto JavaScript
   ↓
6. Switch case identifica '/agendamento'
   ↓
7. Log: "[INFO] Processando agendamento..."
   ↓
8. sendResponse() envia resposta JSON estruturada
   ↓
9. Cliente recebe: {"success": true, "message": "...", "data": {...}}
```

---

## 🎯 Padrões de Design Utilizados

### 1. **Factory Pattern**
- `http.createServer()` cria instância do servidor

### 2. **Strategy Pattern**  
- Switch/case para diferentes estratégias de roteamento

### 3. **Template Method**
- Padrão consistente para todos os endpoints médicos

### 4. **Error Handling Pattern**
- Try/catch centralizado com logging

### 5. **Callback Pattern**
- Event listeners para dados e finalização

---

## 📊 Métricas do Código

- **Total de linhas**: 130
- **Funções**: 3 (parseBody, sendResponse, handlers)
- **Endpoints**: 5 (health + 4 médicos)
- **Dependências externas**: 0 (apenas Node.js nativo)
- **Complexidade**: Baixa (roteamento linear)

---

## 🚀 Extensibilidade

### Adicionar novo endpoint:
1. Adicionar case no switch
2. Implementar lógica específica
3. Usar sendResponse() para resposta
4. Atualizar banner de inicialização

### Adicionar middleware:
1. Criar função antes do switch
2. Processar req/res conforme necessário
3. Chamar next() ou similar

### Adicionar autenticação:
1. Verificar headers na entrada
2. Validar token/credenciais
3. Retornar 401 se inválido

---

## 🎓 Conceitos Demonstrados

1. **HTTP nativo**: Como criar servidor sem frameworks
2. **Streams**: Processamento de dados de requisição
3. **Promises**: Conversão de callbacks para async/await
4. **Error handling**: Tratamento robusto de erros
5. **Signal handling**: Shutdown graceful
6. **JSON API**: Padronização de respostas
7. **Logging**: Debug e monitoramento básico

---

**Esta documentação demonstra como um servidor HTTP simples pode implementar uma arquitetura MCP completa para sistemas médicos, mantendo código limpo, legível e extensível.**