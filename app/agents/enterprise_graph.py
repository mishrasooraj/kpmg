from typing import TypedDict

from langgraph.graph import END, StateGraph


class AgentState(TypedDict):
    objective: str
    context: dict
    steps: list[str]
    result: dict


def _plan(state: AgentState) -> AgentState:
    return {**state, "steps": [*state["steps"], "planned architecture and controls"]}


def _execute(state: AgentState) -> AgentState:
    result = {
        "architecture": "FastAPI + LangGraph agents + PostgreSQL/pgvector + Azure data workflows",
        "controls": ["audit logging", "provider key isolation", "async API boundaries"],
        "objective": state["objective"],
    }
    return {**state, "steps": [*state["steps"], "executed agent workflow"], "result": result}


def build_enterprise_agent_graph():
    graph = StateGraph(AgentState)
    graph.add_node("plan", _plan)
    graph.add_node("execute", _execute)
    graph.set_entry_point("plan")
    graph.add_edge("plan", "execute")
    graph.add_edge("execute", END)
    return graph.compile()
