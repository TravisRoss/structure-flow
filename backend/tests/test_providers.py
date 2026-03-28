import pytest

from app.providers._constants import DEFAULT_DIAGRAM
from app.providers.stub_anthropic import StubAnthropicProvider
from app.providers.stub_openai import StubOpenAIProvider
from app.schemas import Role
from tests.utils import make_message


class TestStubOpenAIProvider:
    async def test_returns_diagram_when_keyword_present(self) -> None:
        provider = StubOpenAIProvider()
        messages = [make_message(Role.user, "Create a login flowchart")] # keyword here is Create
        response = await provider.get_response(messages)
        assert response.diagram == DEFAULT_DIAGRAM
        assert response.message == "Here's the diagram you requested."

    async def test_returns_text_when_no_keyword(self) -> None:
        provider = StubOpenAIProvider()
        messages = [make_message(Role.user, "Hello there")]
        response = await provider.get_response(messages)
        assert response.diagram is None
        assert response.message == "Hello! I can help you create diagrams. Try asking me to create a flowchart."

    async def test_uses_last_user_message_for_keyword_detection(self) -> None:
        provider = StubOpenAIProvider()
        messages = [
            make_message(Role.user, "Create a diagram"),
            make_message(Role.assistant, "Here's your diagram."),
            make_message(Role.user, "Thanks"),
        ]
        response = await provider.get_response(messages)
        assert response.diagram is None


class TestStubAnthropicProvider:
    async def test_returns_diagram_when_keyword_present(self) -> None:
        provider = StubAnthropicProvider()
        messages = [make_message(Role.user, "Generate a flowchart")]
        response = await provider.get_response(messages)
        assert response.diagram == DEFAULT_DIAGRAM
        assert response.message == "I've generated a diagram based on your request."

    async def test_returns_text_when_no_keyword(self) -> None:
        provider = StubAnthropicProvider()
        messages = [make_message(Role.user, "Hello there")]
        response = await provider.get_response(messages)
        assert response.diagram is None
        assert response.message == "Hi! I can help you visualise processes as diagrams. What would you like to create?"

    async def test_uses_last_user_message_for_keyword_detection(self) -> None:
        provider = StubAnthropicProvider()
        messages = [
            make_message(Role.user, "Create a diagram"),
            make_message(Role.assistant, "Here's your diagram."),
            make_message(Role.user, "Thanks"),
        ]
        response = await provider.get_response(messages)
        assert response.diagram is None
