import json

from app.providers._constants import DEFAULT_DIAGRAM
from app.providers.stub_anthropic import _FALLBACK_MESSAGE as ANTHROPIC_FALLBACK_MESSAGE
from app.providers.stub_anthropic import StubAnthropicProvider
from app.providers.stub_openai import _FALLBACK_MESSAGE as OPENAI_FALLBACK_MESSAGE
from app.providers.stub_openai import StubOpenAIProvider
from app.schemas import Role
from tests.utils import make_message


def parse_sse_chunk(chunk: str) -> dict:
    return json.loads(chunk.removeprefix("data: ").strip())


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
        assert response.message == OPENAI_FALLBACK_MESSAGE

    async def test_uses_last_user_message_for_keyword_detection(self) -> None:
        provider = StubOpenAIProvider()
        messages = [
            make_message(Role.user, "Create a diagram"),
            make_message(Role.assistant, "Here's your diagram."),
            make_message(Role.user, "Thanks"),
        ]
        response = await provider.get_response(messages)
        assert response.diagram is None

    async def test_stream_yields_text_delta_and_done_when_no_keyword(self) -> None:
        provider = StubOpenAIProvider()
        messages = [make_message(Role.user, "Hello there")]
        chunks = [chunk async for chunk in provider.stream_response(messages)]
        events = [parse_sse_chunk(chunk) for chunk in chunks]
        assert events[0]["type"] == "text_delta"
        assert events[0]["delta"] == OPENAI_FALLBACK_MESSAGE
        assert events[-1]["type"] == "done"

    async def test_stream_yields_diagram_when_keyword_present(self) -> None:
        provider = StubOpenAIProvider()
        messages = [make_message(Role.user, "Generate a flowchart")]
        chunks = [chunk async for chunk in provider.stream_response(messages)]
        events = [parse_sse_chunk(chunk) for chunk in chunks]
        event_types = [event["type"] for event in events]
        assert "text_delta" in event_types
        assert "diagram" in event_types
        assert events[-1]["type"] == "done"
        diagram_event = next(event for event in events if event["type"] == "diagram")
        assert diagram_event["code"] == DEFAULT_DIAGRAM

    async def test_stream_uses_last_user_message_for_keyword_detection(self) -> None:
        provider = StubOpenAIProvider()
        messages = [
            make_message(Role.user, "Create a diagram"),
            make_message(Role.assistant, "Here's your diagram."),
            make_message(Role.user, "Thanks"),
        ]
        chunks = [chunk async for chunk in provider.stream_response(messages)]
        events = [parse_sse_chunk(chunk) for chunk in chunks]
        event_types = [event["type"] for event in events]
        assert "diagram" not in event_types


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
        assert response.message == ANTHROPIC_FALLBACK_MESSAGE

    async def test_uses_last_user_message_for_keyword_detection(self) -> None:
        provider = StubAnthropicProvider()
        messages = [
            make_message(Role.user, "Create a diagram"),
            make_message(Role.assistant, "Here's your diagram."),
            make_message(Role.user, "Thanks"),
        ]
        response = await provider.get_response(messages)
        assert response.diagram is None

    async def test_stream_yields_text_delta_and_done_when_no_keyword(self) -> None:
        provider = StubAnthropicProvider()
        messages = [make_message(Role.user, "Hello there")]
        chunks = [chunk async for chunk in provider.stream_response(messages)]
        events = [parse_sse_chunk(chunk) for chunk in chunks]
        assert events[0]["type"] == "text_delta"
        assert events[0]["delta"] == ANTHROPIC_FALLBACK_MESSAGE
        assert events[-1]["type"] == "done"

    async def test_stream_yields_diagram_when_keyword_present(self) -> None:
        provider = StubAnthropicProvider()
        messages = [make_message(Role.user, "Generate a flowchart")]
        chunks = [chunk async for chunk in provider.stream_response(messages)]
        events = [parse_sse_chunk(chunk) for chunk in chunks]
        event_types = [event["type"] for event in events]
        assert "text_delta" in event_types
        assert "diagram" in event_types
        assert events[-1]["type"] == "done"
        diagram_event = next(event for event in events if event["type"] == "diagram")
        assert diagram_event["code"] == DEFAULT_DIAGRAM

    async def test_stream_uses_last_user_message_for_keyword_detection(self) -> None:
        provider = StubAnthropicProvider()
        messages = [
            make_message(Role.user, "Create a diagram"),
            make_message(Role.assistant, "Here's your diagram."),
            make_message(Role.user, "Thanks"),
        ]
        chunks = [chunk async for chunk in provider.stream_response(messages)]
        events = [parse_sse_chunk(chunk) for chunk in chunks]
        event_types = [event["type"] for event in events]
        assert "diagram" not in event_types
