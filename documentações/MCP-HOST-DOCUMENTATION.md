# MCP Host Documentation

## Overview

The MCP Host is a healthcare-focused orchestrator that implements the Model Communication Protocol (MCP) architecture. It serves as a central hub connecting Azure OpenAI with specialized healthcare services through a structured tool-based communication system.

## MCP Architecture

### Core Components

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Input    │───▶│    MCP Host     │───▶│  Azure OpenAI   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │ Tool Execution  │
                       └─────────────────┘
                                │
                ┌───────────────┼───────────────┐
                ▼               ▼               ▼
        ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
        │ Scheduling  │ │ Cancellation│ │  Payment    │
        │   Server    │ │   Server    │ │   Server    │
        └─────────────┘ └─────────────┘ └─────────────┘
```

## 1. MCP Host (mcp-host.py:7-121)

### Class Structure
```python
class MCPHost:
    def __init__(self):
        self.client = None              # Azure OpenAI client
        self.tools = []                 # Available tools from MCP servers
        self.system_prompt = ""         # System instructions
        self.conversation_history = []  # Maintains conversational context
```

### Key Methods

#### Setup (mcp-host.py:19-42)
- Loads environment configuration
- Establishes Azure OpenAI connection
- Discovers available tools from MCP servers
- Loads system prompt

#### Message Processing (mcp-host.py:43-65)
- Maintains conversation history for context
- Sends complete context to LLM
- Returns response with potential tool calls

#### Tool Execution (mcp-host.py:67-81)
- Routes tool calls to appropriate MCP servers
- Simulates HTTP communication (future implementation)
- Returns structured results

## 2. MCP Servers (tools_implementations.py:1-151)

### Scheduling Server (tools_implementations.py:11-31)
```python
def scheduling_create_appointment(patientId, dateTime, service):
    # Future: POST /mcp/scheduling
    # Creates new medical appointment
```

### Cancellation Server (tools_implementations.py:34-52)
```python
def cancellation_cancel_appointment(appointmentId, patientId, reason):
    # Future: POST /mcp/cancellation
    # Cancels existing appointment
```

### Payment Server (tools_implementations.py:55-75)
```python
def payment_process_payment(appointmentId, paymentMethod, amount):
    # Future: POST /mcp/payment
    # Processes payment transactions
```

### Exam Server (tools_implementations.py:78-105)
```python
def exam_get_results(patientId, examId=None):
    # Future: POST /mcp/exam
    # Retrieves exam results
```

### Tool Router (tools_implementations.py:108-151)
Central dispatcher that routes tool calls to appropriate server implementations.

## 3. Tool Definitions (tools_definitions.json:1-98)

Defines interface contracts using OpenAI Function Calling format:

```json
{
    "type": "function",
    "function": {
        "name": "scheduling_create_appointment",
        "description": "Agenda uma nova consulta médica",
        "parameters": {
            "type": "object",
            "properties": {
                "patientId": {"type": "string", "description": "ID do paciente"},
                "dateTime": {"type": "string", "description": "Data e hora no formato ISO"},
                "service": {"type": "string", "description": "Tipo de consulta"}
            },
            "required": ["patientId", "dateTime", "service"]
        }
    }
}
```

## Execution Flow

### 1. System Initialization
```
Load .env → Connect Azure OpenAI → Discover Tools → Load System Prompt
```

### 2. Request Processing
```
User Input → Add to History → Send to LLM → Tool Selection → Execute → Response
```

### 3. Example: Appointment Scheduling

**User Input:**
```
"Schedule a cardiology appointment for patient 12345 tomorrow at 2pm"
```

**Processing Flow:**
1. MCP Host adds to conversation history
2. Sends context to Azure OpenAI with available tools
3. LLM identifies need for `scheduling_create_appointment`
4. MCP Host executes call to Scheduling Server
5. Returns structured confirmation

**System Response:**
```json
{
    "success": true,
    "message": "Consulta agendada com sucesso!",
    "data": {
        "appointmentId": "APT-A1B2C3D4",
        "patientId": "12345",
        "dateTime": "2025-09-17T14:00:00",
        "service": "cardiologia",
        "status": "confirmed"
    }
}
```

## Configuration

### Environment Variables (.env)
```env
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
AZURE_OPENAI_KEY=your-api-key
AZURE_OPENAI_DEPLOYMENT=your-deployment-name
```

### System Prompt (system.txt:1-3)
```
você é um assistente de central de saúde para uma clínica.

quando algum paciente/usuário pedir para reagendar/remarcar uma consulta, você deve primeiro cancelar a consulta atual, e em seguida agendar uma nova.
```

## Usage

### Prerequisites
```bash
pip install openai python-dotenv
```

### Run the MCP Host
```bash
python mcp-host.py
```

## MCP Architecture Benefits

### 1. Modularity
- Each business domain is an independent MCP server
- Facilitates maintenance and scalability
- Enables parallel team development

### 2. Extensibility  
- New MCP servers can be added without modifying the host
- Standardized tool definitions ease integration
- Support for different communication protocols

### 3. Flexibility
- Local simulation for development
- Gradual migration to real HTTP
- Support for different LLM providers

### 4. Maintainability
- Clear separation of responsibilities
- Well-defined contracts
- Centralized logging and monitoring

## Future Evolution

### Migration to Real HTTP
```python
# Current (simulated)
result = execute_tool(tool_name, arguments)

# Future (real HTTP)
response = requests.post(f"{server_url}/mcp/{tool_name}", json=arguments)
result = response.json()
```

### Dynamic Server Discovery
```python
# MCP Server registry
servers = discover_mcp_servers()
for server in servers:
    tools.extend(server.get_available_tools())
```

### Monitoring and Observability
```python
# Structured metrics and logs
logger.info(f"Tool executed: {tool_name}", extra={
    "duration": execution_time,
    "server": server_id,
    "success": result.success
})
```

## Healthcare Domain Tools

### Available Operations
- **Scheduling**: Create appointments across medical specialties
- **Cancellation**: Cancel appointments with refund processing
- **Payment**: Process payments via multiple methods
- **Exams**: Retrieve medical exam results

### Business Logic
- Rescheduling requires cancellation followed by new appointment creation
- All operations return structured JSON responses
- Patient ID validation across all services
- Appointment status tracking throughout lifecycle

## Conclusion

This MCP Host implementation demonstrates a robust pattern for integrating LLMs with specialized business systems. The modular design enables efficient scaling while simulation facilitates local development before real HTTP implementation. This approach is particularly valuable in complex domains like healthcare where different specialties require dedicated systems but need coordinated operation through a unified conversational interface.