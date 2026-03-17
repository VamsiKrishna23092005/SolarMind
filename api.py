from fastapi import FastAPI
from pydantic import BaseModel
from solarmind.graph import get_compiled_graph

app = FastAPI(title="SolarMind LangGraph API", description="Production API endpoint for LangGraph DAG invocation")
graph_app = get_compiled_graph(conn_string="checkpoints.sqlite")

class InvokeRequest(BaseModel):
    research_query: str
    thread_id: str = "1"

@app.post("/invoke", tags=["Pipeline Execution"])
def invoke_graph(request: InvokeRequest):
    """Start workflow execution using persistent sqlite state matching the core structure."""
    config = {"configurable": {"thread_id": request.thread_id}}
    result = graph_app.invoke({"research_query": request.research_query}, config=config)
    
    # Format and unwrap return object to expose final strings instead of complex proxy objects
    return {
        "status": "success", 
        "final_report": result.get('research_report', ''),
        "technical_data": result.get('technical_data', '')
    }
