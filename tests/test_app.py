from fastapi.testclient import TestClient

from app.main import app


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
