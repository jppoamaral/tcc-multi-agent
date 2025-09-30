from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os
from mcp_payment import PaymentAgent

app = FastAPI(title="MCP Payment Server")
agent = PaymentAgent()

class MessageRequest(BaseModel):
    message: str

@app.on_event("startup")
async def startup():
    agent.setup()

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "payment"}

@app.post("/mcp/process")
async def process_message(request: MessageRequest):
    """Recebe mensagem conversacional e deixa o agente decidir o que fazer"""
    try:
        print(f"PAYMENT: {request.message}")
        result = agent.process_message(request.message)
        print(f"PAYMENT: {result}")
        return {"success": True, "response": result}
    except Exception as e:
        print(f"PAYMENT ERRO: {str(e)}")
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3004, log_level="info")