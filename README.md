# Sistema de Saúde MCP - TCC

Sistema de agendamento médico utilizando Model Context Protocol (MCP) para integração com IA.

## Arquitetura

O projeto implementa uma arquitetura MCP com três componentes principais:

- **MCP Host** (`health-mcp-host/`): Orquestrador que conecta com Azure OpenAI
- **MCP Servers** (`mcp-*-agent/`): APIs FastAPI especializadas por domínio 
- **MCP Clients**: Agentes especializados em cada domínio

## Componentes

### Agentes Especializados
- `mcp-scheduling-agent/`: Agendamento de consultas
- `mcp-payment-agent/`: Processamento de pagamentos
- `mcp-exam-agent/`: Busca e gerenciamento de exames
- `mcp-cancellation-agent/`: Cancelamento de consultas

### MCP Host
- `health-mcp-host/`: Orquestrador principal com integração Azure OpenAI

## Configuração

1. Clone o repositório:
```bash
git clone <repository-url>
cd tcc
```

2. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o .env com suas credenciais do Azure OpenAI
```

3. Instale as dependências Python:
```bash
pip install -r requirements.txt
```

4. Execute os servidores MCP (em terminais separados):
```bash
# Terminal 1 - Agendamento
cd mcp-scheduling-agent
python scheduling_server.py

# Terminal 2 - Pagamento  
cd mcp-payment-agent
python payment_server.py

# Terminal 3 - Exames
cd mcp-exam-agent
python exam_server.py

# Terminal 4 - Cancelamento
cd mcp-cancellation-agent
python cancellation_server.py
```

5. Execute o MCP Host:
```bash
cd health-mcp-host
python mcp_host.py
```

## Variáveis de Ambiente

Copie `.env.example` para `.env` e configure:

- `AZURE_OPENAI_ENDPOINT`: Endpoint do Azure OpenAI
- `AZURE_OPENAI_DEPLOYMENT`: Nome do deployment
- `AZURE_OPENAI_KEY`: Chave de API do Azure OpenAI

## Estrutura do Projeto

```
tcc/
├── health-mcp-host/           # MCP Host (orquestrador)
├── mcp-scheduling-agent/      # Agente de agendamento
├── mcp-payment-agent/         # Agente de pagamento
├── mcp-exam-agent/           # Agente de exames
├── mcp-cancellation-agent/   # Agente de cancelamento
├── documentações/            # Documentação técnica
├── shared_db/               # Banco de dados compartilhado
└── .env.example             # Template de configuração
```

## Uso

Após iniciar todos os serviços, interaja com o sistema através do MCP Host. O sistema pode processar solicitações como:

- "Quero agendar uma consulta com cardiologista"
- "Preciso cancelar minha consulta"
- "Quais exames estão disponíveis?"
- "Como faço o pagamento da consulta?"

## Tecnologias

- **Python**: Linguagem principal
- **FastAPI**: Framework para APIs dos servidores MCP
- **Azure OpenAI**: Modelo de linguagem
- **MCP**: Model Context Protocol para integração IA
- **SQLite**: Banco de dados (shared_db/)

## Licença

Este projeto foi desenvolvido como Trabalho de Conclusão de Curso (TCC).