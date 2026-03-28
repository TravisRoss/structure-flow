from app.providers._constants import DEFAULT_DIAGRAM, DIAGRAM_PATTERN
from app.providers._utils import get_last_user_message
from app.providers.base import BaseProvider
from app.schemas import ChatResponse, Message


class StubOpenAIProvider(BaseProvider):
    async def complete(self, messages: list[Message]) -> ChatResponse:
        last_message = get_last_user_message(messages)

        if last_message and DIAGRAM_PATTERN.search(last_message.content):
            return ChatResponse(
                message="Here's the diagram you requested.",
                diagram=DEFAULT_DIAGRAM,
            )

        return ChatResponse(
            message="Hello! I can help you create diagrams. Try asking me to create a flowchart.",
        )
