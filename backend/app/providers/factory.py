from app.core.config import Settings
from app.providers.anthropic import AnthropicProvider
from app.providers.base import BaseProvider
from app.providers.stub_anthropic import StubAnthropicProvider
from app.providers.stub_openai import StubOpenAIProvider


def get_provider(name: str, settings: Settings) -> BaseProvider:
    if name == "anthropic":
        if not settings.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY must be set when using the anthropic provider.")
        return AnthropicProvider(api_key=settings.anthropic_api_key)
    if name == "stub_openai":
        return StubOpenAIProvider()
    if name == "stub_anthropic":
        return StubAnthropicProvider()
    available = '"stub_openai", "stub_anthropic", "anthropic"'
    raise ValueError(f'Unknown provider "{name}". Available: {available}')
