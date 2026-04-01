import json
import logging
from collections.abc import AsyncIterator

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from app.core.config import Settings, get_settings
from app.db import load_conversation, save_conversation
from app.providers.factory import get_provider
from app.schemas import ChatRequest, ChatResponse, ConversationResponse, Message, Role

router = APIRouter()
logger = logging.getLogger(__name__)


def dict_to_sse(data: dict) -> str:
    return f"data: {json.dumps(data)}\n\n"


async def stream_with_persistence(
    provider_stream: AsyncIterator[str],
    messages: list[Message],
    conversation_id: str | None,
) -> AsyncIterator[str]:
    text_content = ""
    diagram_code = None

    try:
        async for event_string in provider_stream:
            if event_string.startswith("data: "):
                event_data: dict[str, str] = json.loads(
                    event_string.removeprefix("data: ")
                )
                if event_data["type"] == "text_delta":
                    text_content += event_data["delta"]
                    yield event_string
                elif event_data["type"] == "diagram":
                    diagram_code = event_data["code"]
                    yield event_string
                # Skip the provider's done event — we emit our own after saving
    except Exception:
        logger.exception("Provider stream failed")
        error_message = "The AI service encountered an error. Please try again or switch to a different model if the issue persists."
        yield dict_to_sse({"type": "error", "message": error_message})
        yield dict_to_sse({"type": "done"})
        return

    assistant_message = Message(role=Role.assistant, content=text_content, diagram=diagram_code)
    saved_id = save_conversation(conversation_id, [*messages, assistant_message])

    yield dict_to_sse({"type": "conversation_id", "id": saved_id})
    yield dict_to_sse({"type": "done"})


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    settings: Settings = Depends(get_settings),
) -> ChatResponse:
    provider = get_provider(settings.model_provider, settings)

    try:
        return await provider.get_response(request.messages)
    except Exception as error:
        # 502 Bad Gateway: the provider (upstream service) failed, not this server
        raise HTTPException(status_code=502, detail=str(error)) from error


@router.post("/chat/stream")
async def stream_chat(
    request: ChatRequest,
    settings: Settings = Depends(get_settings),
) -> StreamingResponse:
    provider = get_provider(settings.model_provider, settings)

    return StreamingResponse(
        stream_with_persistence(
            provider.stream_response(request.messages),
            request.messages,
            request.conversation_id,
        ),
        media_type="text/event-stream",
    )


@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(conversation_id: str) -> ConversationResponse:
    messages = load_conversation(conversation_id)

    if messages is None:
        raise HTTPException(status_code=404, detail="Conversation not found")

    return ConversationResponse(conversation_id=conversation_id, messages=messages)
