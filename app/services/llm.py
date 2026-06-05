from langchain_core.messages import HumanMessage, SystemMessage

from app.core.config import Settings


class LLMService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def _provider(self, requested: str | None) -> str:
        return requested or self.settings.default_llm_provider

    async def chat(self, message: str, provider: str | None = None) -> tuple[str, str]:
        selected = self._provider(provider)
        system = SystemMessage(
            content=(
                "You are a secure enterprise AI assistant. Prefer concise answers, "
                "call out uncertainty, and avoid exposing confidential information."
            )
        )
        human = HumanMessage(content=message)

        if selected == "anthropic" and self.settings.anthropic_api_key:
            from langchain_anthropic import ChatAnthropic

            model = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0)
            response = await model.ainvoke([system, human])
            return str(response.content), selected

        if selected == "openai" and self.settings.openai_api_key:
            from langchain_openai import ChatOpenAI

            model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
            response = await model.ainvoke([system, human])
            return str(response.content), selected

        return (
            "LLM provider is not configured. Set OPENAI_API_KEY or ANTHROPIC_API_KEY to enable live chat.",
            selected,
        )
