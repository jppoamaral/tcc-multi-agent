import requests

# Mapeamento de servers por domínio
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

# Funções simplificadas para os novos nomes de tools
def scheduling_agent(message):
    return route_to_agent('scheduling', message)

def cancellation_agent(message):
    return route_to_agent('cancellation', message)

def payment_agent(message):
    return route_to_agent('payment', message)

def exam_agent(message):
    return route_to_agent('exam', message)

TOOL_FUNCTIONS = {
    "scheduling_agent": scheduling_agent,
    "cancellation_agent": cancellation_agent,
    "payment_agent": payment_agent,
    "exam_agent": exam_agent,
}

def execute_tool(tool_name, arguments):
    message = arguments.get("message", "")
    if tool_name in TOOL_FUNCTIONS:
        return TOOL_FUNCTIONS[tool_name](message)
    else:
        return {"success": False, "error": f"Tool não encontrada: {tool_name}"}
