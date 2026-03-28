import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


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
