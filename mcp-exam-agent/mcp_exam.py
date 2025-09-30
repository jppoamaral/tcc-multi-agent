"""
ExamAgent - MCP Server para consulta de exames
Arquitetura Multi-Agente para Atendimento de Saúde - TCC 2025
"""

import os
import json
from dotenv import load_dotenv
from openai import AzureOpenAI

class ExamAgent:
    def __init__(self):
        self.client = None
        self.tools = []
        self.system_prompt = ""
        self.deployment = ""
        self.conversation_history = []

    def setup(self):
        """Inicializa conexões e carrega configurações"""
        # Procura .env na raiz do projeto primeiro, depois local
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
        
        print(f"[*] MCP Exam Agent iniciado!")
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
        # Executa as ferramentas chamadas pelo modelo
        results = []
        
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            
            if function_name == "get_exam_result":
                result = self.get_exam_result(**arguments)
            else:
                result = {"error": f"Função {function_name} não encontrada"}
            
            results.append(result)
        
        return results[0] if len(results) == 1 else results
    
    
    def get_exam_result(self, patientId, examId=None):
        """Simula busca de resultados de exame"""
        # Dados simulados
        sample_exams = {
            "12345": {
                "HEM-001": {
                    "examType": "hemograma-completo",
                    "result": "Hemoglobina: 14.5 g/dL, Leucócitos: 7200/μL",
                    "date": "2025-09-15T10:00:00"
                },
                "RX-002": {
                    "examType": "raio-x-torax", 
                    "result": "Campos pulmonares livres",
                    "date": "2025-09-14T15:30:00"
                }
            }
        }
        
        if patientId not in sample_exams:
            return {
                "success": False,
                "message": f"Nenhum exame encontrado para paciente {patientId}"
            }
        
        patient_exams = sample_exams[patientId]
        
        if examId:
            if examId in patient_exams:
                exam = patient_exams[examId]
                return {
                    "success": True,
                    "message": f"Exame {examId} encontrado",
                    "data": {
                        "examId": examId,
                        "patientId": patientId,
                        "examType": exam["examType"],
                        "result": exam["result"],
                        "date": exam["date"]
                    }
                }
            else:
                return {
                    "success": False,
                    "message": f"Exame {examId} não encontrado"
                }
        else:
            # Retorna todos os exames
            all_exams = []
            for eid, exam in patient_exams.items():
                all_exams.append({
                    "examId": eid,
                    "examType": exam["examType"],
                    "date": exam["date"]
                })
            
            return {
                "success": True,
                "message": f"Encontrados {len(all_exams)} exame(s)",
                "data": {
                    "patientId": patientId,
                    "exams": all_exams
                }
            }

    def execute_tool(self, tool_name, arguments):
        """Executa uma tool específica"""
        if tool_name == "get_exam_result":
            return self.get_exam_result(**arguments)
        else:
            return {
                "success": False,
                "error": f"Tool '{tool_name}' não encontrada",
                "code": "TOOL_NOT_FOUND"
            }

def main():
    """Inicialização básica do agente"""
    agent = ExamAgent()
    agent.setup()
    print("[*] Exam Agent pronto para uso!")

if __name__ == "__main__":
    main()