from app.providers._constants import DEFAULT_DIAGRAM, DIAGRAM_PATTERN
from app.providers._utils import get_last_user_message
from app.providers.base import BaseProvider
from app.schemas import ChatResponse, Message


class StubAnthropicProvider(BaseProvider):
    async def get_response(self, messages: list[Message]) -> ChatResponse:
        last_message = get_last_user_message(messages)

        if last_message and DIAGRAM_PATTERN.search(last_message.content):
            return ChatResponse(
                message="I've generated a diagram based on your request.",
                diagram=DEFAULT_DIAGRAM,
            )

        return ChatResponse(
            message="Hi! I can help you visualise processes as diagrams. What would you like to create?",
        )
