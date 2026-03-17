from typing import TypedDict, List, Annotated
import operator

def add_strings(a: str, b: str) -> str:
    """Reducer function to concatenate string states, e.g. parallel researcher reports."""
    if not a:
        return b
    if not b:
        return a
    return f"{a}\n\n{b}"

class AgentState(TypedDict):
    """
    State object passed between LangGraph nodes.
    We use Annotated with operator.add and custom reducers 
    to support parallel scaling and multiple updates.
    """
    messages: Annotated[List[dict], operator.add]
    research_query: str
    research_report: Annotated[str, add_strings]
    critique_flag: bool
    technical_data: Annotated[str, add_strings]
