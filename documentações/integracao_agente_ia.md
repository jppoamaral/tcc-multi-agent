# 🤖 Integração do Agente de IA - Azure OpenAI GPT-4o

## 📋 Estratégia de Implementação

### **Objetivo:** Adicionar camada de IA que processa linguagem natural e direciona para os domínios corretos.

**Fluxo desejado:**
```
Usuario: "Quero agendar consulta cardiologia quinta-feira 14h"
    ↓
Agente IA: Analisa e identifica
    ↓ 
Resultado: domain="agendamento", dados estruturados
    ↓
Server.ts: Processa no endpoint /agendamento
```

---

## 🎯 **COMANDO CLAUDE CODE:**

```bash
claude code "Adicione agente de IA ao MCP-Host usando Azure OpenAI:

ESTRUTURA ATUAL MANTIDA:
- Manter server.ts funcionando exatamente como está
- Adicionar nova camada de IA SEM quebrar código existente

IMPLEMENTAÇÃO:
1. CRIAR src/services/aiAgent.ts:
   - Classe AIAgent para Azure OpenAI GPT-4o
   - Método processNaturalLanguage(texto) → domínio + dados
   - Configuração via environment variables
   - HTTP nativo para chamadas API (sem bibliotecas extras)

2. ADICIONAR ENDPOINT /chat no server.ts:
   - POST /chat → recebe texto natural
   - Chama AIAgent.processNaturalLanguage()
   - Identifica domínio (agendamento/cancelamento/pagamento/exame)
   - Extrai dados estruturados
   - Retorna resposta + sugestão de ação

3. CONFIGURAÇÃO:
   - Adicionar ao package.json: dotenv
   - Criar .env para Azure OpenAI config
   - Variables: AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY, AZURE_OPENAI_DEPLOYMENT

4. PROMPTS ESPECIALIZADOS:
   - Sistema: Especialista em saúde que identifica intenções
   - Exemplos: 'agendar consulta' → agendamento
   - Output: JSON estruturado com domínio + dados

5. EXEMPLO DE USO:
   POST /chat
   {
     'message': 'Preciso cancelar minha consulta de amanhã'
   }
   
   Resposta:
   {
     'domain': 'cancelamento',
     'intent': 'cancel_appointment', 
     'data': {...},
     'natural_response': 'Vou processar seu cancelamento...'
   }

FOCO TCC: IA simples, direta, sem over-engineering, demonstrando MCP funcionando."
```

---

## 🔧 **Configurações Necessárias**

### **1. Environment Variables (.env):**
```env
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_KEY=your-api-key
AZURE_OPENAI_DEPLOYMENT=gpt-4o
AZURE_OPENAI_API_VERSION=2024-02-01
```

### **2. Instalar dependência mínima:**
```bash
npm install dotenv
```

---

## 🧠 **Prompts do Sistema**

### **System Prompt Especializado:**
```
Você é um assistente médico especializado em identificar intenções de pacientes.

DOMÍNIOS DISPONÍVEIS:
- agendamento: marcar, agendar, consulta, médico, especialista
- cancelamento: cancelar, desmarcar, não posso ir
- pagamento: pagar, cobrança, valor, cartão, boleto  
- exame: resultado, exame, laboratorio, sangue

RESPONDA SEMPRE EM JSON:
{
  "domain": "nome_do_dominio",
  "confidence": 0.95,
  "extracted_data": {...},
  "natural_response": "Resposta amigável"
}

EXEMPLOS:
Input: "Quero agendar cardiologia quinta"
Output: {"domain": "agendamento", "confidence": 0.9, "extracted_data": {"specialty": "cardiologia", "day": "quinta-feira"}, "natural_response": "Vou te ajudar a agendar uma consulta de cardiologia para quinta-feira."}
```

---

## 🚀 **Implementação Gradual**

### **Fase 1: Básico Funcionando**
- Endpoint `/chat` recebendo texto
- Chamada para Azure OpenAI
- Identificação de domínio simples
- Resposta JSON estruturada

### **Fase 2: Refinamento**
- Extração de dados mais precisa
- Prompts otimizados para saúde
- Tratamento de ambiguidade
- Logs detalhados

### **Fase 3: Integração**
- `/chat` chama automaticamente endpoint correto
- Fluxo completo: linguagem natural → processamento → resposta
- Exemplos de uso no TCC

---

## 📊 **Estrutura Final do Projeto**

```
mcp-host-azure/
├── src/
│   ├── server.ts               # Mantém como está
│   └── services/
│       └── aiAgent.ts          # NOVO - Agente IA
├── .env                        # NOVO - Config Azure OpenAI
├── README.md
└── package.json                # Adiciona dotenv
```

---

## 🧪 **Testes Planejados**

### **Teste 1: Agendamento**
```bash
curl -X POST http://localhost:3001/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Preciso marcar consulta cardiologia"}'
```

### **Teste 2: Cancelamento**
```bash
curl -X POST http://localhost:3001/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Não posso ir na consulta de amanhã"}'
```

### **Teste 3: Ambiguidade**
```bash
curl -X POST http://localhost:3001/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Queria falar sobre minha consulta"}'
```

---

## 🎯 **Benefícios para o TCC**

1. **Demonstra IA aplicada** - Uso prático de GPT-4o
2. **Arquitetura MCP clara** - IA identifica → MCP roteia
3. **Linguagem natural** - Interface mais humana
4. **Código simples** - Fácil de entender e explicar
5. **Integração real** - Azure OpenAI funcionando

---

## 💡 **Próximos Passos**

1. **Execute o comando Claude Code** acima
2. **Configure .env** com suas credenciais Azure
3. **Teste endpoint `/chat`**
4. **Refine prompts** conforme necessário
5. **Documente funcionamento** para TCC

**A base está sólida - agora vamos adicionar a IA! 🚀**
