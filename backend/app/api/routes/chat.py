from fastapi import APIRouter, Depends, HTTPException

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
        raise HTTPException(status_code=502, detail=str(error)) from error
