from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from app.core.config import Settings, get_settings
from app.providers.factory import get_provider
from app.schemas import ChatRequest, ChatResponse

router = APIRouter()


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

    try:
        return StreamingResponse(
            provider.stream_response(request.messages),
            media_type="text/event-stream",
        )
    except Exception as error:
        # 502 Bad Gateway: the provider (upstream service) failed, not this server
        raise HTTPException(status_code=502, detail=str(error)) from error
