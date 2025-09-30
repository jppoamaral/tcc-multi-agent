from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os
from mcp_scheduling import SchedulingAgent

app = FastAPI(title="MCP Scheduling Server")
agent = SchedulingAgent()

class MessageRequest(BaseModel):
    message: str

@app.on_event("startup")
async def startup():
    agent.setup()

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "scheduling"}

@app.post("/mcp/process")
async def process_message(request: MessageRequest):
    try:
        print(f"SCHEDULING: {request.message}")
        result = agent.process_message(request.message)
        print(f"SCHEDULING: {result}")
        return {"success": True, "response": result}
    except Exception as e:
        print(f"SCHEDULING ERRO: {str(e)}")
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3001, log_level="info")
