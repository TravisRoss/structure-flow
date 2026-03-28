from enum import Enum

from pydantic import BaseModel, Field, field_validator


class Role(str, Enum):
    user = "user"
    assistant = "assistant"


class Message(BaseModel):
    role: Role
    content: str
    diagram: str | None = None


class ChatRequest(BaseModel):
    messages: list[Message] = Field(..., min_length=1)

    @field_validator("messages")
    @classmethod
    def last_message_must_be_from_user(cls, messages: list[Message]) -> list[Message]:
        if messages[-1].role != Role.user:
            raise ValueError("Last message must be from the user")
        return messages


class ChatResponse(BaseModel):
    message: str
    diagram: str | None = None
