import json
from collections.abc import AsyncIterator

import anthropic

from app.providers.base import BaseProvider
from app.schemas import ChatResponse, Message

_SYSTEM_PROMPT = """You are a helpful assistant that creates diagrams using Mermaid.js.

When the user asks you to create, generate, draw, build, or update a diagram, use the create_diagram tool to provide the Mermaid code.
For all other messages, respond conversationally."""

_CREATE_DIAGRAM_TOOL = {
    "name": "create_diagram",
    "description": "Create or update a Mermaid.js diagram based on the user's request.",
    "input_schema": {
        "type": "object",
        "properties": {
            "mermaid_code": {
                "type": "string",
                "description": "Valid Mermaid.js diagram code.",
            }
        },
        "required": ["mermaid_code"],
    },
}


class AnthropicProvider(BaseProvider):
    def __init__(self, api_key: str) -> None:
        self._client = anthropic.AsyncAnthropic(api_key=api_key)

    async def get_response(self, messages: list[Message]) -> ChatResponse:
        response = await self._client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1024,
            system=_SYSTEM_PROMPT,
            tools=[_CREATE_DIAGRAM_TOOL],
            messages=self._format_messages(messages),
        )

        text = ""
        diagram = None

        for block in response.content:
            is_diagram_tool = (
                block.type == "tool_use" and block.name == "create_diagram"
            )
            if block.type == "text":
                text = block.text
            elif is_diagram_tool:
                diagram = block.input.get("mermaid_code")

        return ChatResponse(
            message=text or "Here's your diagram.",
            diagram=diagram,
        )

    async def stream_response(self, messages: list[Message]) -> AsyncIterator[str]:
        async with self._client.messages.stream(
            model="claude-opus-4-6",
            max_tokens=1024,
            system=_SYSTEM_PROMPT,
            tools=[_CREATE_DIAGRAM_TOOL],
            messages=self._format_messages(messages),
        ) as stream:
            async for text_delta in stream.text_stream:
                yield f"data: {json.dumps({'type': 'text_delta', 'delta': text_delta})}\n\n"

            final_message = await stream.get_final_message()
            for content_block in final_message.content:
                is_diagram_tool = (
                    content_block.type == "tool_use"
                    and content_block.name == "create_diagram"
                )
                if is_diagram_tool:
                    diagram_code = content_block.input.get("mermaid_code", "")
                    if diagram_code != "":
                        yield f"data: {json.dumps({'type': 'diagram', 'code': diagram_code})}\n\n"

        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    def _format_messages(self, messages: list[Message]) -> list[dict[str, str]]:
        formatted = []
        for message in messages:
            content = message.content
            if message.diagram:
                diagram_context = (
                    "[Previously generated diagram]\n"
                    f"```mermaid\n{message.diagram}\n```"
                )
                content += f"\n\n{diagram_context}"
            formatted.append({"role": message.role.value, "content": content})
        return formatted
