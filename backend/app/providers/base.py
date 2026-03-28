from abc import ABC, abstractmethod
from app.schemas import ChatResponse, Message

class BaseProvider(ABC):
    @abstractmethod
    async def complete(self, messages: list[Message]) -> ChatResponse:
        """Send a conversation to the model and return its response."""
        ...
