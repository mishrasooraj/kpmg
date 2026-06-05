from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    user_id: str = Field(min_length=1)
    message: str = Field(min_length=1)
    conversation_id: str | None = None
    provider: str | None = Field(default=None, pattern="^(openai|anthropic)$")


class ChatResponse(BaseModel):
    conversation_id: str | None
    answer: str
    provider: str
    tools_used: list[str] = []


class AgentRunRequest(BaseModel):
    objective: str = Field(min_length=1)
    context: dict = Field(default_factory=dict)


class AgentRunResponse(BaseModel):
    status: str
    result: dict
    steps: list[str]
