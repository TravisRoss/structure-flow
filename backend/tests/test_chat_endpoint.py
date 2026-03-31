import json
from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient

from app.api.routes.chat import stream_with_persistence
from app.core.config import Settings, get_settings
from app.main import app
from app.schemas import Message, Role


@pytest.fixture(autouse=True)
def override_settings() -> None:
    app.dependency_overrides[get_settings] = lambda: Settings(model_provider="stub_openai")
    yield
    app.dependency_overrides.clear()


@pytest.fixture
async def client() -> AsyncClient:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as async_client:
        yield async_client


class TestChatEndpoint:
    async def test_returns_diagram_for_keyword_message(self, client: AsyncClient) -> None:
        response = await client.post("/api/chat", json={
            "messages": [{"role": "user", "content": "Create a flowchart"}],
        })
        assert response.status_code == 200
        data = response.json()
        assert data["diagram"] is not None
        assert data["message"]

    async def test_returns_text_for_non_keyword_message(self, client: AsyncClient) -> None:
        response = await client.post("/api/chat", json={
            "messages": [{"role": "user", "content": "Hello"}],
        })
        assert response.status_code == 200
        data = response.json()
        assert data["diagram"] is None
        assert data["message"]

    async def test_rejects_empty_messages(self, client: AsyncClient) -> None:
        response = await client.post("/api/chat", json={"messages": []})
        assert response.status_code == 422

    async def test_rejects_invalid_role(self, client: AsyncClient) -> None:
        response = await client.post("/api/chat", json={
            "messages": [{"role": "admin", "content": "Hello"}],
        })
        assert response.status_code == 422

    async def test_rejects_conversation_not_ending_with_user(self, client: AsyncClient) -> None:
        response = await client.post("/api/chat", json={
            "messages": [
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "Hi there"},
            ],
        })
        assert response.status_code == 422


class TestStreamWithPersistence:
    async def test_yields_error_and_done_when_provider_raises(self) -> None:
        async def failing_stream() -> AsyncIterator[str]:
            yield 'data: {"type":"text_delta","delta":"Hello"}\n\n'
            raise Exception("Provider failed")

        messages = [Message(role=Role.user, content="test")]
        events = [
            json.loads(event_string.removeprefix("data: "))
            async for event_string in stream_with_persistence(failing_stream(), messages, None)
        ]

        assert events[0] == {"type": "text_delta", "delta": "Hello"}
        assert events[1]["type"] == "error"
        assert "message" in events[1]
        assert events[2] == {"type": "done"}
