"""
MCP Host - Orquestrador que conecta com MCP Servers
"""
import os
import json
from dotenv import load_dotenv
from openai import AzureOpenAI
from tools_implementations import execute_tool

class MCPHost: 
    def __init__(self):
        self.client = None
        self.tools = []
        self.system_prompt = ""
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
        
        with open("tools_definitions.json", "r", encoding="utf8") as file:
            self.tools = json.load(file)
        
        # Carrega prompt do sistema
        with open("system.txt", "r", encoding="utf8") as file:
            self.system_prompt = file.read().strip()
        
        print(f"[*] MCP Host iniciado!")
        print(f"[*] Tools carregadas: {len(self.tools)}")
        print(f"[*] Domínios: agendamento, cancelamento, pagamento, exames")
        
    def process_message(self, user_input):
        self.conversation_history.append({"role": "user", "content": user_input})
        messages = [{"role": "system", "content": self.system_prompt}] + self.conversation_history
        
        completion = self.client.chat.completions.create(
            model=self.deployment,
            messages=messages,
            tools=self.tools,
            max_tokens=500,
            temperature=0.3
        )
        
        response = completion.choices[0].message
        
        if response.content:
            self.conversation_history.append({"role": "assistant", "content": response.content})
        
        return response
    
    def process_agent_message(self, agent_result, tool_name):
        # Verifica se o agente está fora do ar ou retornou erro
        if not agent_result or (isinstance(agent_result, dict) and not agent_result.get('success', True)):
            error_msg = agent_result.get('error', 'Agente não respondeu') if agent_result else 'Agente não respondeu'
            
            # Determina o domínio do agente para criar mensagem específica
            domain_names = {
                'scheduling_agent': 'agendamento',
                'cancellation_agent': 'cancelamento', 
                'payment_agent': 'pagamento',
                'exam_agent': 'busca de exames'
            }
            domain = domain_names.get(tool_name, tool_name)
            
            # Cria resposta de fallback informando que o serviço está temporariamente indisponível
            fallback_message = f"Desculpe, o serviço de {domain} está temporariamente indisponível. Tente novamente em alguns momentos ou entre em contato conosco pelo telefone (11) 1234-5678 para assistência imediata."
            
            self.conversation_history.append({"role": "assistant", "content": fallback_message})
            
            # Cria uma resposta mock para retornar
            class MockResponse:
                def __init__(self, content):
                    self.content = content
            
            return MockResponse(fallback_message)
        
        # Processa normalmente se o agente respondeu com sucesso
        result_str = json.dumps(agent_result, ensure_ascii=False, indent=2)
        self.conversation_history.append({"role": "assistant", "content": f"Resultado do {tool_name}: {result_str}"})
        messages = [{"role": "system", "content": self.system_prompt}] + self.conversation_history

        completion = self.client.chat.completions.create(
            model=self.deployment,
            messages=messages,
            tools=self.tools,
            max_tokens=500,
            temperature=0.3
        )
        response = completion.choices[0].message
        if response.content:
            self.conversation_history.append({"role": "assistant", "content": response.content})
        return response

    def execute_tool_call(self, tool_call):
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        
        print(f"🔧 Executando tool: {tool_name}")
        print(f"📤 Parâmetros: {arguments}")

        result = execute_tool(tool_name, arguments)
        
        print(f"📥 Resposta do Server:")
        print(result)
        
        # Se o resultado for None ou vazio, cria uma resposta de erro
        if result is None:
            result = {"success": False, "error": "Agente não respondeu (resultado None)"}
        
        return result
    
    def run(self):
        self.setup()
        print("\n[*] Digite suas mensagens ou 'sair' para encerrar.")
        
        while True:
            try:
                user_input = input("Você: ").strip()
                
                if user_input.lower() == 'sair':
                    print("[*] Encerrando MCP Host. Até logo!")
                    break
                
                if not user_input:
                    continue
                
                print("[*] Processando...")
                
                response = self.process_message(user_input)
                
                # Verifica se precisa executar tools
                if response.tool_calls:
                    for tool_call in response.tool_calls:
                        agent_result = self.execute_tool_call(tool_call)
                        # Processa resultado do agente e gera resposta final ao paciente
                        final_response = self.process_agent_message(agent_result, tool_call.function.name)
                        print(f"Assistente: {final_response.content}")
                else:
                    print(f"Assistente: {response.content}")
                
                print()
                
            except KeyboardInterrupt:
                print("\n[*] Encerrando MCP Host. Até logo!")
                break
            except Exception as e:
                print(f"[!] Erro: {e}")

if __name__ == "__main__":
    host = MCPHost()
    host.run()