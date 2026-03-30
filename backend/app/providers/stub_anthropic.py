import json
from collections.abc import AsyncIterator

from app.providers._constants import DEFAULT_DIAGRAM, STUB_FALLBACK_MESSAGE
from app.providers._utils import is_diagram_request
from app.providers.base import BaseProvider
from app.schemas import ChatResponse, Message

_FALLBACK_MESSAGE = f"[stub_anthropic] {STUB_FALLBACK_MESSAGE}"


class StubAnthropicProvider(BaseProvider):
    async def get_response(self, messages: list[Message]) -> ChatResponse:
        if is_diagram_request(messages):
            return ChatResponse(
                message="I've generated a diagram based on your request.",
                diagram=DEFAULT_DIAGRAM,
            )

        return ChatResponse(message=_FALLBACK_MESSAGE)

    async def stream_response(self, messages: list[Message]) -> AsyncIterator[str]:
        if is_diagram_request(messages):
            diagram_message = "I've generated a diagram based on your request."
            event = json.dumps({"type": "text_delta", "delta": diagram_message})
            yield f"data: {event}\n\n"
            diagram_event = json.dumps({"type": "diagram", "code": DEFAULT_DIAGRAM})
            yield f"data: {diagram_event}\n\n"
        else:
            event = json.dumps({"type": "text_delta", "delta": _FALLBACK_MESSAGE})
            yield f"data: {event}\n\n"

        yield f"data: {json.dumps({'type': 'done'})}\n\n"
