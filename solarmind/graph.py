from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_ollama import OllamaLLM
from langchain_community.tools import DuckDuckGoSearchRun
import sqlite3
from typing import List
import os

from .state import AgentState
from .rag import retrieve_context

# Open-source model components initialization
def get_llm():
    return OllamaLLM(model="llama3", base_url=os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434"))

search_tool = DuckDuckGoSearchRun()

def researcher_node(state: AgentState) -> dict:
    """Agent that performs specific topic lookup."""
    query = state.get("research_query", "")
    
    # Simple DuckDuckGo search for gathering info if LLM lacks exact
    try:
        search_res = search_tool.run(f"Latest on {query}")
    except Exception:
        search_res = "Search failed."

    prompt = (
        f"You are a researcher. Based on the topic: {query}, "
        f"summarize findings combining knowledge and the following search results: {search_res}."
    )
    # Using open-source free local LLM
    response = get_llm().invoke(prompt)

    # Note: State uses add_strings reducer for research_report
    return {"research_report": f"=== RESEARCH REPORT ({query}) ===\n{response}"}

def researcher_router(state: AgentState) -> List[Send]:
    """Spawns parallel researchers based on Send API"""
    query = state.get("research_query", "")
    
    # We create multiple paths using `Send(node_name, state_overrides)`
    # This acts like a fan-out parallel pipeline.
    parallel_requests = [
        Send("researcher", {"research_query": f"{query} market trends"}),
        Send("researcher", {"research_query": f"{query} tech PatchTST efficiency"}),
        Send("researcher", {"research_query": f"{query} policy subsidies and open source"})
    ]
    return parallel_requests

def technical_analyst_node(state: AgentState) -> dict:
    """Analyst retrieves specific solar/technical context via RAG/Chroma"""
    # Using the root query for technical context
    # Usually you would extract specifically the main query, wait:
    # State holds the last researcher's query? No, main flow preserves original state unless overridden!
    query = state.get('research_query', '')
    
    # RAG Retrieval
    context = retrieve_context(query)
    
    # CRAG fallback
    if not context.strip():
        try:
            search_results = search_tool.run(f"solar tech metrics {query}")
            context = f"(Fallback Web Results)\n{search_results}"
        except Exception:
            context = "(No specific technical data obtained)"

    prompt = (
        "Analyze solar metrics (e.g., efficiency, PatchTST baseline loss, hardware costs) "
        f"using the following context:\n{context}\n"
        "If context has limited info, extrapolate structurally."
    )
    
    tech_data = get_llm().invoke(prompt)
    return {"technical_data": f"=== TECHNICAL ANALYSIS ===\n{tech_data}"}

def critic_node(state: AgentState) -> dict:
    """Enforce loops with conditional edges if report needs expansion."""
    report = state.get('research_report', '')
    prompt = (
        f"Critique this compiled research report:\n{report}\n\n"
        "Does it have massive gaps, errors, or completely lack technical depth? "
        "Reply 'FAIL' explicitly if it needs heavy revision, otherwise 'PASS'."
    )
    critique = get_llm().invoke(prompt)
    critique_flag = "FAIL" in critique.upper()
    return {"critique_flag": critique_flag}

def pre_writer_node(state: AgentState) -> dict:
    """Human-in-the-loop anchor point before final compilation."""
    # Graph halts here because it will be added to interrupt_before
    return {"messages": [{"role": "human", "content": "Approve report? Provide feedback."}]}

def writer_node(state: AgentState) -> dict:
    """Consolidation step aggregating all parallel data"""
    report = state.get('research_report', '')
    tech_data = state.get('technical_data', '')
    
    prompt = (
        "You are the senior editor. Write the final comprehensive structured report "
        "combining the gathered research findings and technical/RAG analysis.\n\n"
        f"Research:\n{report}\n\nTechnical Data:\n{tech_data}"
    )
    
    final_report = get_llm().invoke(prompt)
    # Output replaces research report via our custom reducer approach
    # Since add_strings appends, we'll format it with clear headers
    return {"research_report": f"\n\n=== FINAL COMPREHENSIVE REPORT ===\n{final_report}"}

def build_graph() -> StateGraph:
    """Compile graph edges and configure states"""
    graph = StateGraph(AgentState)
    
    def router_dummy(state: AgentState):
        """Pass-through node to fan-out"""
        return state

    graph.add_node("router", router_dummy)
    graph.add_node("researcher", researcher_node)
    graph.add_node("technical_analyst", technical_analyst_node)
    graph.add_node("critic", critic_node)
    graph.add_node("human_review", pre_writer_node)
    graph.add_node("writer", writer_node)
    
    # Core flow:
    # 1. Parallel researchers phase
    graph.add_edge(START, "router")
    graph.add_conditional_edges("router", researcher_router, ["researcher"])
    
    # 2. Aggregating to Critic
    # All researchers converge to Critic naturally in LangGraph when Send is resolved
    graph.add_edge("researcher", "critic")
    
    def should_loop_eval(state: AgentState) -> str:
        """Critic loop evaluator"""
        if state.get('critique_flag'):
            return "router" # Kick back to parallel research
        return "technical_analyst"
        
    # 3. Validation / Iteration
    graph.add_conditional_edges("critic", should_loop_eval, ["router", "technical_analyst"])
    
    # 4. RAG Node -> UI interrupt -> Final Output
    graph.add_edge("technical_analyst", "human_review")
    graph.add_edge("human_review", "writer")
    graph.add_edge("writer", END)
    
    return graph

def get_compiled_graph(conn_string="checkpoints.sqlite"):
    """Prepare checkpointer persistence mechanisms natively using SqliteSaver"""
    graph = build_graph()
    os.makedirs(os.path.dirname(conn_string) if os.path.dirname(conn_string) else '.', exist_ok=True)
    # Allows checkpointer logic handling failures/rollbacks implicitly 
    conn = sqlite3.connect(conn_string, check_same_thread=False)
    memory = SqliteSaver(conn)
    app = graph.compile(checkpointer=memory, interrupt_before=["human_review"])
    return app
