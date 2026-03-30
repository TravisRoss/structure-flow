from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from app.schemas import ChatResponse, Message


class BaseProvider(ABC):
    @abstractmethod
    async def get_response(self, messages: list[Message]) -> ChatResponse:
        """Send a conversation to the model and return its response."""
        ...

    @abstractmethod
    async def stream_response(self, messages: list[Message]) -> AsyncIterator[str]:
        """Stream a conversation response as SSE-formatted strings."""
        ...
