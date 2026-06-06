from fastapi.testclient import TestClient
import pytest

from app.core.config import Settings, get_settings
from app.main import app
from app.services.llm import LLMService


client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_agent_run() -> None:
    response = client.post(
        "/api/v1/ai/agents/run",
        json={"objective": "Assess an AI data architecture", "context": {"risk": "medium"}},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "completed"
    assert body["steps"]


def test_pipeline_dry_run() -> None:
    response = client.post(
        "/api/v1/data/pipelines/run",
        json={
            "pipeline_name": "demo",
            "source_uri": "sftp://source",
            "target_uri": "az://landing",
            "parameters": {},
        },
    )
    assert response.status_code == 200
    assert response.json()["status"] in {"dry_run", "queued"}


def test_chat_accepts_google_provider() -> None:
    app.dependency_overrides[get_settings] = lambda: Settings(
        google_api_key=None,
        default_llm_provider="google",
    )
    response = client.post(
        "/api/v1/ai/chat",
        json={
            "user_id": "sooraj",
            "message": "Explain RAG in simple words",
            "provider": "google",
        },
    )
    app.dependency_overrides.clear()
    assert response.status_code == 200
    assert response.json()["provider"] == "google"


@pytest.mark.asyncio
async def test_google_quota_error_returns_clean_message(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeGemini:
        def __init__(self, **_: object) -> None:
            pass

        async def ainvoke(self, _: object) -> object:
            raise RuntimeError("429 RESOURCE_EXHAUSTED")

    import langchain_google_genai

    monkeypatch.setattr(langchain_google_genai, "ChatGoogleGenerativeAI", FakeGemini)
    answer, provider = await LLMService(
        Settings(google_api_key="test-key", google_model="gemini-2.0-flash")
    ).chat("hello", "google")

    assert provider == "google"
    assert "quota is exhausted" in answer
