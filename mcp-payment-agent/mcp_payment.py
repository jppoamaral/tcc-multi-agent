"""
PaymentAgent - MCP Server para processamento de pagamentos
Arquitetura Multi-Agente para Atendimento de Saúde - TCC 2025
"""
import json
import sys
import os
from dotenv import load_dotenv
from openai import AzureOpenAI

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared_db'))
import simple_db

class PaymentAgent:
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
        
        self.client = AzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            api_version="2024-02-01"
        )
        self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

        with open("tools.json", "r", encoding="utf8") as file:
            tools_data = json.load(file)
            self.tools = tools_data["tools"]
        
        with open("system.txt", "r", encoding="utf8") as file:
            self.system_prompt = file.read().strip()
        
        print(f"[*] MCP Payment Agent iniciado!")
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
        
        if response.tool_calls:
            result = self._execute_tools(response.tool_calls)
            # Adiciona resultado da tool ao histórico para que o LLM processe
            self.conversation_history.append({
                "role": "assistant",
                "content": f"Resultado das ferramentas: {json.dumps(result, ensure_ascii=False)}"
            })
            
            # Gera uma segunda resposta baseada nos resultados das tools
            messages = [{
                "role": "system", 
                "content": self.system_prompt + "\n\nCom base nos resultados das ferramentas, forneça uma resposta clara e conversacional ao paciente."
            }] + self.conversation_history
            
            final_response = self.client.chat.completions.create(
                model=self.deployment,
                messages=messages,
                max_tokens=300,
                temperature=0.7
            )
            
            final_content = final_response.choices[0].message.content
            self.conversation_history.append({"role": "assistant", "content": final_content})
            return final_content

        if response.content:
            self.conversation_history.append({"role": "assistant", "content": response.content})
        
        return response.content

    def _execute_tools(self, tool_calls):
        """Executa as ferramentas chamadas pelo LLM"""
        results = []
        
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            
            if function_name == "processar_pagamento":
                result = self.processar_pagamento(**arguments)
            elif function_name == "processar_reembolso":
                result = self.processar_reembolso(**arguments)
            else:
                result = {"error": f"Função {function_name} não encontrada"}
            
            results.append(result)
        
        return results
        
    def processar_pagamento(self, patient_name, document, date, specialty):
        result = simple_db.add_payment(patient_name, document, date, specialty)
        return result

    def processar_reembolso(self, document):
        result = simple_db.refund(document)
        return result


def main():
    agent = PaymentAgent()
    agent.setup()
    print("[*] Payment Agent pronto para uso!")

if __name__ == "__main__":
    main()