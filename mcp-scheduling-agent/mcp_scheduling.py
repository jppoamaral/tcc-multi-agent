"""
MCP Scheduling Agent - Agente MCP para Agendamento de Consultas
Sistema Multi-Agente para Atendimento de Saúde - TCC 2025
"""
import json
import os
import sys
from dotenv import load_dotenv
from openai import AzureOpenAI

# Adiciona o caminho do módulo compartilhado
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared_db'))
import simple_db

class SchedulingAgent:
    def __init__(self):
        self.client = None
        self.tools = []
        self.system_prompt = ""
        self.deployment = ""
        self.conversation_history = []

    def setup(self):
        root_env = os.path.join(os.path.dirname(__file__), '..', '.env')
        if os.path.exists(root_env):
            load_dotenv(root_env)
        else:
            load_dotenv()
        
        # Conecta Azure OpenAI
        self.client = AzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            api_version="2024-02-01"
        )
        self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

        # Carrega definições de tools
        with open("tools.json", "r", encoding="utf8") as file:
            tools_data = json.load(file)
            self.tools = tools_data["tools"]
        
        # Carrega prompt do sistema
        with open("system.txt", "r", encoding="utf8") as file:
            self.system_prompt = file.read().strip()
        
        print(f"[*] MCP Scheduling Agent iniciado!")
        print(f"[*] Tools carregadas: {len(self.tools)}")

    def process_message(self, agent_input):
        self.conversation_history.append({"role": "user", "content": agent_input})
        messages = [{"role": "system", "content": self.system_prompt}] + self.conversation_history
        
        completion = self.client.chat.completions.create(
            model=self.deployment,
            messages=messages,
            tools=self.tools,
            max_tokens=500,
            temperature=0.7
        )
        
        response = completion.choices[0].message
        
        # Se há tool calls, executar
        if response.tool_calls:
            result = self._execute_tools(response.tool_calls)
            # Adiciona resposta do agente ao histórico
            self.conversation_history.append({
                "role": "assistant", 
                "content": f"Executei as seguintes ações: {result}"
            })
            return result
        
        # Adiciona resposta ao histórico se houver conteúdo
        if response.content:
            self.conversation_history.append({"role": "assistant", "content": response.content})
        
        return response.content

    def _execute_tools(self, tool_calls):
        results = []
        
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            
            if function_name == "consultar_slots":  
                result = simple_db.consultar_slots()
            elif function_name == "agendar_slot":
                slot_id = arguments["slot_id"]
                patient_cpf = arguments["patient_cpf"]
                result = simple_db.agendar_slot(slot_id, patient_cpf)
            else:
                result = {"error": f"Função {function_name} não encontrada"}
            
            results.append(result)
        
        return results

def main():
    agent = SchedulingAgent()
    agent.setup()
    print("[*] Scheduling Agent pronto para uso!")

if __name__ == "__main__":
    main()