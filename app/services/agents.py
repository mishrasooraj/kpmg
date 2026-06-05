from app.agents.enterprise_graph import build_enterprise_agent_graph


class AgentOrchestrator:
    def __init__(self) -> None:
        self.graph = build_enterprise_agent_graph()

    async def run(self, objective: str, context: dict) -> dict:
        return await self.graph.ainvoke(
            {"objective": objective, "context": context, "steps": [], "result": {}}
        )
