from fastapi import APIRouter, Depends

from app.core.config import Settings, get_settings
from app.schemas.ai import AgentRunRequest, AgentRunResponse, ChatRequest, ChatResponse
from app.services.agents import AgentOrchestrator
from app.services.llm import LLMService

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, settings: Settings = Depends(get_settings)) -> ChatResponse:
    answer, provider = await LLMService(settings).chat(request.message, request.provider)
    return ChatResponse(
        conversation_id=request.conversation_id,
        answer=answer,
        provider=provider,
        tools_used=["langchain"],
    )


@router.post("/agents/run", response_model=AgentRunResponse)
async def run_agent(request: AgentRunRequest) -> AgentRunResponse:
    result = await AgentOrchestrator().run(request.objective, request.context)
    return AgentRunResponse(status="completed", result=result["result"], steps=result["steps"])
