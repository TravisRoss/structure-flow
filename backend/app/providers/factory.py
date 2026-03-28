from app.providers.base import BaseProvider
from app.providers.stub_anthropic import StubAnthropicProvider
from app.providers.stub_openai import StubOpenAIProvider

# Maps the MODEL_PROVIDER env var value to its provider class.
# To add a new provider, add an entry here and create the corresponding class.
_REGISTRY: dict[str, type[BaseProvider]] = {
    "stub_openai": StubOpenAIProvider,
    "stub_anthropic": StubAnthropicProvider,
}


def get_provider(name: str) -> BaseProvider:
    cls = _REGISTRY.get(name)
    if cls is None:
        available = ", ".join(f'"{k}"' for k in _REGISTRY)
        raise ValueError(f'Unknown provider "{name}". Available: {available}')
    # Instantiate here so each request gets a fresh provider instance.
    return cls()
