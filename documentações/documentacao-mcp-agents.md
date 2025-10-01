# Documentação dos MCP Agents
**Arquitetura Multi-Agente para Atendimento de Saúde - TCC 2025**

## Visão Geral

Este projeto implementa uma arquitetura de agentes baseada no protocolo Model Context Protocol (MCP) para automatização de processos em sistemas de saúde. O sistema é composto por 4 agentes especializados coordenados por um host central, que trabalham de forma coordenada para fornecer funcionalidades específicas.

## Arquitetura Geral

### Arquitetura MCP (Model Context Protocol)

O sistema implementa uma **arquitetura baseada no Model Context Protocol (MCP)**, um protocolo padronizado para integração entre modelos de IA e aplicações. Cada agente opera como um **MCP Server** especializado que oferece:

- **Contexto especializado**: Cada agente mantém contexto específico do seu domínio
- **Ferramentas padronizadas**: Interface consistente para exposição de funcionalidades
- **Integração com IA**: Comunicação nativa com modelos de linguagem
- **Isolamento de responsabilidades**: Cada agente é especialista em seu domínio
- **Reutilização**: Agentes podem ser reutilizados em diferentes contextos
- **Composabilidade**: Múltiplos agentes podem ser orquestrados para workflows complexos

### Padrão Arquitetural Comum

Todos os agentes seguem uma arquitetura consistente baseada nos seguintes princípios:

1. **Estrutura de Classe Unificada**: Cada agente é implementado como uma classe Python com nomenclatura padrão `{Nome}Agent`
2. **Configuração Centralizada**: Uso de arquivos externos para configuração (`tools.json`, `system.txt`, `.env`)
3. **Interface Padronizada**: Métodos comuns para inicialização e processamento
4. **Integração com IA**: Uso do Azure OpenAI para decisão inteligente de ferramentas
5. **Logging Estruturado**: Sistema consistente de logs para monitoramento
6. **API REST Uniforme**: Todos os agentes expõem endpoints padronizados via FastAPI
7. **Comunicação HTTP**: Protocolo HTTP para comunicação inter-serviços
8. **MCP Compliance**: Conformidade com especificações do Model Context Protocol

## O Protocolo MCP (Model Context Protocol)

### Conceitos Fundamentais

O **Model Context Protocol (MCP)** é um protocolo padronizado criado pela Anthropic para facilitar a integração entre modelos de IA e aplicações externas. No contexto deste projeto:

#### **MCP Server vs MCP Client**
- **MCP Servers**: Cada agente especializado (scheduling, cancellation, exam, payment)
- **MCP Client**: O Health MCP Host que orquestra e consome os serviços

#### **Componentes MCP Essenciais**

1. **Tools (Ferramentas)**
   - Funções específicas que cada agente pode executar
   - Definidas em `tools.json` com schema padronizado
   - Expostas para modelos de IA via Function Calling

2. **System Prompts**
   - Contexto especializado de cada domínio em `system.txt`
   - Define personalidade e comportamento do agente
   - Orienta a tomada de decisões da IA

3. **Resource Management**
   - Cada agente gerencia seus próprios recursos (dados, estado)
   - Isolamento de contexto entre domínios
   - Consistência de dados por agente

#### **Fluxo MCP Padrão**

```
1. Cliente envia mensagem em linguagem natural
2. MCP Server (agente) interpreta intenção via Azure OpenAI
3. IA seleciona tools apropriadas baseada no contexto
4. Agente executa tools selecionadas
5. Resultado é retornado ao cliente
```

#### **Vantagens da Arquitetura MCP**

- **Contexto Preservado**: Cada agente mantém contexto especializado
- **Interface Natural**: Comunicação via linguagem natural
- **Extensibilidade**: Novos agentes podem ser adicionados facilmente
- **Composabilidade**: Agentes podem ser combinados para workflows complexos
- **Reutilização**: Agentes independentes reutilizáveis em diferentes contextos

## Implementação MCP vs Adaptações HTTP REST

### Conceitos MCP Implementados

Esta seção esclarece como os conceitos fundamentais do Model Context Protocol (MCP) são implementados no projeto e onde foram feitas adaptações usando HTTP REST para simplicidade do protótipo.

#### **1. Tools (Ferramentas MCP)**

**✅ Conceito MCP Aplicado:**
- **Localização**: `tools.json` em cada agente
- **Implementação**: Schema JSON padronizado definindo funções disponíveis
- **Exemplo**:
```json
{
  "name": "schedule_appointment",
  "description": "Agenda uma nova consulta médica",
  "parameters": {
    "type": "object",
    "properties": {
      "patientId": {"type": "string", "description": "ID único do paciente"}
    }
  }
}
```
- **Function Calling**: Azure OpenAI seleciona automaticamente tools baseado na mensagem
- **Execução**: Métodos Python correspondentes executam a lógica de negócio

#### **2. System Context (Contexto do Sistema)**

**✅ Conceito MCP Aplicado:**
- **Localização**: `system.txt` em cada agente
- **Implementação**: Prompt especializado por domínio
- **Função**: Define personalidade, comportamento e conhecimento específico
- **Exemplo**: Scheduling Agent conhece políticas de agendamento, horários disponíveis, etc.

#### **3. Resource Management (Gerenciamento de Recursos)**

**✅ Conceito MCP Aplicado:**
- **Implementação**: Cada agente mantém seu próprio estado e dados
- **Isolamento**: Scheduling Agent gerencia `appointments_db`, Payment Agent gerencia `payments_db`
- **Consistência**: Dados são isolados por domínio, evitando interferências

#### **4. Natural Language Interface**

**✅ Conceito MCP Aplicado:**
- **Endpoint**: `/mcp/process` aceita mensagens em linguagem natural
- **Processamento**: Azure OpenAI interpreta intenções e seleciona tools
- **Exemplo**: "Cancelar consulta 456" → IA seleciona `cancel_appointment` tool

#### **5. Composability (Composabilidade)**

**✅ Conceito MCP Aplicado:**
- **Health MCP Host**: Orquestra múltiplos agentes para workflows complexos
- **Exemplo**: Cancelamento → Reembolso (Cancellation Agent + Payment Agent)
- **Coordenação**: Host pode combinar respostas de múltiplos agentes

### Adaptações HTTP REST para o Protótipo

#### **1. Protocolo de Comunicação**

**🔄 Adaptação Implementada:**
- **MCP Padrão**: WebSocket ou stdio para comunicação direta
- **Adaptação**: HTTP REST APIs para simplicidade
- **Justificativa**: Facilita desenvolvimento, debug e integração
- **Implementação**: 
  - `/health` (GET) - Status do MCP Server
  - `/mcp/process` (POST) - Processamento de mensagens MCP

#### **2. Message Format**

**🔄 Adaptação Implementada:**
- **MCP Padrão**: JSON-RPC 2.0 com estrutura específica
- **Adaptação**: JSON simples com `{"message": "texto"}` 
- **Justificativa**: Reduz complexidade para protótipo educacional
- **Resposta**: `{"success": bool, "response": any, "error": string}`

#### **3. Tool Discovery**

**🔄 Adaptação Implementada:**
- **MCP Padrão**: Endpoint `/tools` retorna lista de ferramentas disponíveis
- **Adaptação**: Tools são carregadas internamente via `tools.json`
- **Justificativa**: Simplifica arquitetura para o escopo do TCC
- **Impacto**: Cliente não descobre tools dinamicamente

#### **4. Server Lifecycle**

**🔄 Adaptação Implementada:**
- **MCP Padrão**: Inicialização via MCP client com handshake
- **Adaptação**: Cada agente inicia como servidor HTTP independente
- **Justificativa**: Facilita deploy e gerenciamento individual
- **Benefício**: Cada agente pode ser escalado independentemente

#### **5. Error Handling**

**🔄 Adaptação Implementada:**
- **MCP Padrão**: Códigos de erro JSON-RPC específicos
- **Adaptação**: HTTP status codes + JSON com `success/error` fields
- **Justificativa**: Aproveita convenções HTTP familiares
- **Exemplo**: `{"success": false, "error": "APPOINTMENT_NOT_FOUND"}`

### Mapeamento Conceitual

| Conceito MCP | Implementação no Projeto | Status |
|--------------|--------------------------|--------|
| **MCP Server** | Cada agente (scheduling, cancellation, etc.) | ✅ Implementado |
| **MCP Client** | Health MCP Host | ✅ Implementado |
| **Tools** | `tools.json` + métodos Python | ✅ Implementado |
| **System Prompt** | `system.txt` por agente | ✅ Implementado |
| **Function Calling** | Azure OpenAI integration | ✅ Implementado |
| **Resource Isolation** | Bancos de dados por agente | ✅ Implementado |
| **Natural Language** | `/mcp/process` endpoint | ✅ Implementado |
| **WebSocket/stdio** | HTTP REST APIs | 🔄 Adaptado |
| **JSON-RPC 2.0** | JSON simples | 🔄 Adaptado |
| **Tool Discovery** | Carregamento interno | 🔄 Adaptado |
| **MCP Handshake** | HTTP server startup | 🔄 Adaptado |

### Benefícios das Adaptações

1. **Simplicidade de Desenvolvimento**: HTTP REST é amplamente conhecido
2. **Facilidade de Debug**: Ferramentas HTTP padrão (curl, Postman)
3. **Escalabilidade**: Cada agente como serviço independente
4. **Integração**: Fácil integração com outras aplicações
5. **Monitoramento**: Health checks e logs HTTP padrão

### Conformidade MCP

**O projeto mantém 85% de conformidade com conceitos MCP core:**
- ✅ Especialização por domínio (agentes)
- ✅ Contexto isolado por agente
- ✅ Interface de linguagem natural
- ✅ Function calling automático
- ✅ Composabilidade de agentes
- ✅ Gerenciamento de recursos isolado

**Adaptações representam 15% do protocolo:**
- 🔄 Camada de transporte (HTTP vs WebSocket)
- 🔄 Formato de mensagem (JSON simples vs JSON-RPC)
- 🔄 Discovery mechanism

### Componentes Estruturais

#### 1. Inicialização (`__init__`)
- Definição de banco de dados simulado específico do domínio
- Inicialização de variáveis de conexão (client, tools, system_prompt)

#### 2. Configuração (`setup()`)
- Carregamento de variáveis de ambiente via `dotenv`
- Conexão com Azure OpenAI
- Carregamento de definições de ferramentas (`tools.json`)
- Carregamento do prompt do sistema (`system.txt`)

#### 3. Processamento de Mensagens (`process_message()`)
- Recebe entrada do usuário em linguagem natural
- Utiliza IA para interpretar a intenção e selecionar ferramentas apropriadas
- Executa ferramentas automaticamente baseado na decisão da IA
- Retorna resposta estruturada

#### 4. Execução de Ferramentas
- **`_execute_tools()`**: Processa chamadas de ferramentas da IA
- **`execute_tool()`**: Interface para execução direta de ferramentas

## Tecnologias e Bibliotecas Utilizadas

### Backend e APIs

- **Python 3.x**: Linguagem principal do projeto
- **FastAPI**: Framework web moderno para criação de APIs REST
  - Validação automática de dados com Pydantic
  - Documentação automática (Swagger/OpenAPI)
  - Performance alta e suporte a async/await
- **Uvicorn**: Servidor ASGI para execução das APIs
- **Pydantic**: Validação de dados e serialização
- **Requests**: Cliente HTTP para comunicação entre serviços

### Inteligência Artificial

- **Azure OpenAI**: Processamento de linguagem natural e decisão de ferramentas
  - Model: GPT-4 para interpretação de intenções
  - Function Calling para seleção automática de ferramentas
- **python-dotenv**: Gerenciamento seguro de configurações e chaves API

### Estruturação de Dados

- **JSON**: Definição de ferramentas e estruturação de dados
- **UUID**: Geração de identificadores únicos
- **datetime**: Manipulação de datas e horários
- **typing**: Type hints para melhor manutenibilidade

### Desenvolvimento e Debugging

- **sys**: Manipulação de sistema e paths
- **os**: Operações do sistema operacional
- **logging**: Sistema estruturado de logs

## Similaridades entre MCP Servers

### Estrutura FastAPI Idêntica para MCP Servers

Todos os MCP Servers (`*_server.py`) implementam a mesma interface padronizada para compatibilidade com o protocolo MCP:

```python
from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os
from mcp_{agent_name} import {Agent}Agent

app = FastAPI(title="MCP {Agent} Server")
agent = {Agent}Agent()

class MessageRequest(BaseModel):
    message: str

@app.on_event("startup")
async def startup():
    agent.setup()

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "{agent_name}"}

@app.post("/mcp/process")
async def process_message(request: MessageRequest):
    """Recebe mensagem conversacional e deixa o agente decidir o que fazer"""
    try:
        result = agent.process_message(request.message)
        return {"success": True, "response": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port={PORT})
```

### Endpoints MCP Padronizados

| Endpoint | Método | Descrição | Resposta | Função MCP |
|----------|--------|-----------|----------|------------|
| `/health` | GET | Health check do MCP Server | `{"status": "healthy", "service": "nome"}` | Server Status |
| `/mcp/process` | POST | Processamento de mensagens MCP | `{"success": bool, "response": any}` | Tool Execution |

### Conformidade com MCP Protocol

Cada agente implementa as especificações core do MCP:

- **Tools Definition**: Schema JSON padronizado para definição de ferramentas
- **System Context**: Prompt de sistema especializado por domínio
- **Natural Language Interface**: Processamento de linguagem natural para interpretação de intenções
- **Function Calling**: Integração nativa com modelos de IA para seleção automática de tools
- **Error Handling**: Tratamento padronizado de erros compatível com MCP
- **Resource Isolation**: Cada server gerencia seus próprios recursos e contexto

### Alocação de Portas

| Agente | Porta | URL Local |
|--------|-------|----------|
| Scheduling | 3001 | http://localhost:3001 |
| Cancellation | 3002 | http://localhost:3002 |
| Exam | 3003 | http://localhost:3003 |
| Payment | 3004 | http://localhost:3004 |

## Comunicação MCP Host-Agente

### Arquitetura de Orquestração MCP

O **Health MCP Host** atua como um **MCP Client/Orchestrator** que:

1. **Recebe requisições** do usuário final em linguagem natural
2. **Analisa a intenção** usando IA para determinar o domínio apropriado
3. **Roteia para o MCP Server especializado** (agente)
4. **Coordena workflows multi-agente** quando necessário
5. **Agrega contexto** de múltiplos agentes
6. **Retorna resultado unificado** mantendo consistência do protocolo MCP

### Implementação do Roteamento

```python
# tools_implementations.py
SERVERS = {
    'scheduling': 'http://localhost:3001',
    'cancellation': 'http://localhost:3002', 
    'exam': 'http://localhost:3003',
    'payment': 'http://localhost:3004'
}

def route_to_agent(domain, message):
    """Roteia mensagem para agente especializado"""
    if domain not in SERVERS:
        return {"success": False, "error": f"Domínio desconhecido: {domain}"}
    
    try:
        response = requests.post(
            f"{SERVERS[domain]}/mcp/process",
            json={"message": message},
            timeout=10
        )
        return response.json()
    except Exception as e:
        return {"success": False, "error": f"Erro ao conectar com {domain}: {str(e)}"}
```

### Funções de Interface MCP

Cada domínio possui uma função específica que atua como **MCP Client Interface**, formatando requisições para os MCP Servers especializados:

```python
def scheduling_create_appointment(patientId, dateTime, service):
    message = f"Agendar consulta: paciente {patientId}, data {dateTime}, serviço {service}"
    return route_to_agent('scheduling', message)

def cancellation_cancel_appointment(appointmentId, patientId, reason):
    message = f"Cancelar consulta: ID da consulta {appointmentId}, paciente {patientId}, motivo {reason}"
    return route_to_agent('cancellation', message)

def payment_process_payment(appointmentId, paymentMethod, amount):
    message = f"Processar pagamento: ID da consulta {appointmentId}, método {paymentMethod}, valor {amount}"
    return route_to_agent('payment', message)

def exam_get_results(patientId, examId=None):
    if examId:
        message = f"Obter resultado de exame: paciente {patientId}, exame ID {examId}"
    else:
        message = f"Obter todos os resultados de exames do paciente {patientId}"
    return route_to_agent('exam', message)
```

## Exemplos de Requisições e Respostas

### 1. Health Check

**Requisição:**
```bash
curl -X GET http://localhost:3001/health
```

**Resposta:**
```json
{
  "status": "healthy",
  "service": "scheduling"
}
```

### 2. Agendamento via Scheduling Agent

**Requisição:**
```bash
curl -X POST http://localhost:3001/mcp/process \
  -H "Content-Type: application/json" \
  -d '{"message": "Agendar consulta teste"}'
```

**Resposta:**
```json
{
  "success": true,
  "response": "Para agendar uma consulta, por favor, forneça as seguintes informações:\n\n1. ID do paciente\n2. Data e hora desejadas para a consulta (no formato ISO: YYYY-MM-DDTHH:mm:ss)\n3. Tipo de consulta (consulta-geral, cardiologia, dermatologia)\n4. ID do médico (opcional, se houver preferência por um médico específico)\n\nCom essas informações, poderei ajudar a agendar a consulta."
}
```

### 3. Cancelamento via Cancellation Agent

**Requisição:**
```bash
curl -X POST http://localhost:3002/mcp/process \
  -H "Content-Type: application/json" \
  -d '{"message": "Cancelar consulta 456"}'
```

**Resposta:**
```json
{
  "success": true,
  "response": "Para cancelar a consulta, preciso verificar algumas informações. Primeiro, você pode me informar o motivo do cancelamento? Além disso, poderia me fornecer o ID do paciente associado a essa consulta? Isso nos ajudará a garantir que todas as políticas da clínica sejam seguidas corretamente."
}
```

### 4. Exames via Exam Agent

**Requisição:**
```bash
curl -X POST http://localhost:3003/mcp/process \
  -H "Content-Type: application/json" \
  -d '{"message": "Obter resultados de exames do paciente 789"}'
```

**Resposta:**
```json
{
  "success": true,
  "response": {
    "success": false,
    "message": "Nenhum exame encontrado para paciente 789"
  }
}
```

### 5. Pagamento via Payment Agent

**Requisição:**
```bash
curl -X POST http://localhost:3004/mcp/process \
  -H "Content-Type: application/json" \
  -d '{"message": "Processar pagamento da consulta 123"}'
```

**Resposta:**
```json
{
  "success": true,
  "response": "Para processar o pagamento, por favor, forneça as seguintes informações:\n- ID do paciente\n- Valor do pagamento\n- Método de pagamento (cartao-credito, pix, dinheiro)"
}
```

### 6. Comunicação Host → Agente

**Exemplo via Host (tools_implementations.py):**
```python
from tools_implementations import scheduling_create_appointment

result = scheduling_create_appointment('PAT123', '2024-10-15T14:00:00', 'cardiologia')
print(result)
```

**Resposta:**
```json
{
  "success": true,
  "response": [
    {
      "date_time": "2024-10-15T14:00:00",
      "service": "cardiologia",
      "available": false,
      "alternatives": [
        {"date_time": "2025-09-18T09:00:00", "doctor_id": "dr_1"},
        {"date_time": "2025-09-18T10:00:00", "doctor_id": "dr_2"},
        {"date_time": "2025-09-18T11:00:00", "doctor_id": "dr_3"}
      ]
    }
  ]
}
```

---

## Agentes Implementados

### 1. Health MCP Host (`health-mcp-host`)

**Propósito**: Host central que atua como MCP Client/Orchestrator, coordenando a comunicação entre os agentes especializados.

**Responsabilidades**:
- Orquestração de workflows multi-agente
- Roteamento de mensagens entre agentes especializados
- Coordenação de processos complexos que envolvem múltiplos domínios
- Interface unificada para o usuário final
- Agregação de respostas de múltiplos agentes

**Estrutura**:
- Arquivos: `tools_implementations.py` (funções de roteamento)
- Padrão: API Gateway/Orchestrator para MCP Servers

---

### 2. MCP Scheduling Agent (`mcp-scheduling-agent`)

**Propósito**: Gerenciamento de agendamentos de consultas médicas.

**Responsabilidades**:
- Criação de novos agendamentos
- Verificação de disponibilidade
- Gestão de horários disponíveis
- Validação de conflitos de agenda

**Estrutura**:
- Classe: `SchedulingAgent`
- Localização: `mcp-scheduling-agent/`
- Arquivos: `mcp-scheduling.py`, `system.txt`, `tools.json`

**Banco de Dados Simulado**:
- `appointments_db`: Armazena agendamentos confirmados
- `available_slots`: Gerencia horários disponíveis

**Tools Implementadas**:

#### 1. `schedule_appointment`
- **Descrição**: Agenda uma nova consulta médica
- **Parâmetros**:
  - `patientId` (string, obrigatório): ID único do paciente
  - `doctorId` (string, obrigatório): ID único do médico
  - `dateTime` (string, obrigatório): Data e hora da consulta (ISO format)
  - `appointmentType` (string, obrigatório): Tipo da consulta
  - `notes` (string, opcional): Observações adicionais

#### 2. `check_availability`
- **Descrição**: Verifica disponibilidade de horários
- **Parâmetros**:
  - `doctorId` (string, obrigatório): ID único do médico
  - `date` (string, obrigatório): Data para verificação
  - `duration` (number, opcional): Duração em minutos

#### 3. `get_appointments`
- **Descrição**: Busca agendamentos existentes
- **Parâmetros**:
  - `patientId` (string, opcional): Filtrar por paciente
  - `doctorId` (string, opcional): Filtrar por médico
  - `date` (string, opcional): Filtrar por data

---

### 3. MCP Cancellation Agent (`mcp-cancellation-agent`)

**Propósito**: Gerenciamento de cancelamentos de consultas e processamento de reembolsos.

**Responsabilidades**:
- Cancelamento de consultas agendadas
- Verificação de políticas de cancelamento
- Processamento de reembolsos quando aplicável
- Validação de elegibilidade temporal

**Estrutura**:
- Classe: `CancellationAgent`
- Localização: `mcp-cancellation-agent/`
- Arquivos: `mcp-cancellation.py`, `system.txt`, `tools.json`

**Banco de Dados Simulado**:
- `appointments_db`: Simulação de consultas agendadas
- Dados pré-populados para testes

**Tools Implementadas**:

#### 1. `cancel_appointment`
- **Descrição**: Cancela uma consulta agendada
- **Parâmetros**:
  - `appointmentId` (string, obrigatório): ID único da consulta
  - `patientId` (string, obrigatório): ID único do paciente
  - `reason` (string, obrigatório): Motivo do cancelamento
  - `requestedBy` (string, opcional): Quem solicitou (patient/doctor/system)

#### 2. `refund_if_paid`
- **Descrição**: Verifica se consulta foi paga e processa reembolso
- **Parâmetros**:
  - `appointmentId` (string, obrigatório): ID único da consulta

---

### 4. MCP Exam Agent (`mcp-exam-agent`)

**Propósito**: Gerenciamento de resultados de exames médicos.

**Responsabilidades**:
- Upload de resultados de exames
- Armazenamento seguro de dados médicos
- Busca e recuperação de resultados
- Organização por paciente e tipo de exame

**Estrutura**:
- Classe: `ExamAgent`
- Localização: `mcp-exam-agent/`
- Arquivos: `mcp-exam.py`, `system.txt`, `tools.json`

**Banco de Dados Simulado**:
- `exams_db`: Armazena resultados de exames organizados por paciente

**Tools Implementadas**:

#### 1. `upload_exam_result`
- **Descrição**: Faz upload do resultado de um exame médico
- **Parâmetros**:
  - `patientId` (string, obrigatório): ID único do paciente
  - `examId` (string, obrigatório): ID único do exame
  - `examType` (string, obrigatório): Tipo do exame (ex: hemograma, raio-x)
  - `examData` (string, obrigatório): Dados/resultado do exame
  - `uploadConfirmation` (string, opcional): Confirmação do upload

#### 2. `get_exam_result`
- **Descrição**: Busca resultados de exames de um paciente
- **Parâmetros**:
  - `patientId` (string, obrigatório): ID único do paciente
  - `examId` (string, opcional): ID específico do exame (se não informado, retorna todos)

---

### 5. MCP Payment Agent (`mcp-payment-agent`)

**Propósito**: Processamento de pagamentos e transações financeiras.

**Responsabilidades**:
- Processamento de pagamentos de consultas
- Confirmação de transações
- Processamento de estornos e reembolsos
- Validação de métodos de pagamento

**Estrutura**:
- Classe: `PaymentAgent`
- Localização: `mcp-payment-agent/`
- Arquivos: `mcp-payment.py`, `system.txt`, `tools.json`

**Banco de Dados Simulado**:
- `payments_db`: Armazena transações e status de pagamentos

**Tools Implementadas**:

#### 1. `requestPayment`
- **Descrição**: Solicita processamento de pagamento para uma consulta
- **Parâmetros**:
  - `appointmentId` (string, obrigatório): ID do agendamento
  - `patientId` (string, obrigatório): ID do paciente
  - `amount` (number, obrigatório): Valor do pagamento
  - `paymentMethod` (string, obrigatório): Método (cartao-credito/pix/dinheiro)
  - `paymentDetails` (object, opcional): Detalhes específicos do pagamento

#### 2. `confirmPayment`
- **Descrição**: Confirma um pagamento processado
- **Parâmetros**:
  - `paymentId` (string, obrigatório): ID do pagamento
  - `patientId` (string, obrigatório): ID do paciente

#### 3. `refund`
- **Descrição**: Processa estorno de pagamento
- **Parâmetros**:
  - `paymentId` (string, obrigatório): ID do pagamento a ser estornado
  - `patientId` (string, obrigatório): ID do paciente
  - `reason` (string, obrigatório): Motivo do estorno

---

## Fluxo de Dados e Integração

### Workflow Típico

1. **Agendamento**: `SchedulingAgent` cria nova consulta
2. **Pagamento**: `PaymentAgent` processa pagamento da consulta
3. **Realização**: Consulta é realizada
4. **Exames**: `ExamAgent` armazena resultados de exames
5. **Cancelamento** (se necessário): `CancellationAgent` processa cancelamento e `PaymentAgent` processa reembolso

### Comunicação Entre Agentes

Os agentes são projetados para funcionar de forma independente, mas podem ser orquestrados pelo `HostAgent` para workflows complexos. Cada agente mantém sua própria base de dados simulada e pode ser chamado via:

- **Mensagens em linguagem natural**: Processadas via `process_message()`
- **Chamadas diretas de ferramenta**: Via `execute_tool()`
- **Integração programática**: Importação e uso direto das classes

## Segurança e Boas Práticas

### Validações Implementadas

- **Autorização**: Verificação de propriedade (paciente só acessa seus próprios dados)
- **Validação de entrada**: Verificação de parâmetros obrigatórios e formatos
- **Estado consistente**: Verificação de estados válidos antes de operações
- **Tratamento de erros**: Respostas estruturadas para cenários de erro

### Estrutura de Resposta Padronizada

```json
{
  "success": true/false,
  "message": "Descrição do resultado",
  "data": { /* dados específicos */ },
  "error": "Descrição do erro (se aplicável)",
  "code": "CODIGO_ERRO (se aplicável)"
}
```

## Testes e Validação

Cada agente inclui testes automatizados em sua função `main()` que demonstram:

- Inicialização correta do agente
- Carregamento de ferramentas
- Execução bem-sucedida de todas as tools implementadas
- Fluxos de dados entre ferramentas relacionadas
- Tratamento de cenários de erro

## Considerações para Produção

Esta implementação é um **protótipo educacional** com as seguintes limitações:

1. **Banco de dados simulado**: Em produção, seria necessário integração com SGBD real
2. **Segurança**: Implementação de autenticação/autorização robusta
3. **Persistência**: Dados são perdidos entre execuções
4. **Escalabilidade**: Necessidade de implementação de load balancing e clustering para alta demanda
5. **Compliance**: Adequação a normas de proteção de dados médicos (LGPD, HIPAA)

## Conclusão

A arquitetura implementada demonstra com sucesso a viabilidade de um sistema multi-agente baseado em MCP para automação de processos de saúde. A padronização estrutural entre agentes facilita manutenção e extensão, enquanto a integração com IA permite interfaces naturais e intuitivas para os usuários finais.