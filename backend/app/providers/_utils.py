from app.providers._constants import DIAGRAM_PATTERN
from app.schemas import Message, Role


def get_last_user_message(messages: list[Message]) -> Message | None:
    """Return the most recent user message from a conversation, or None if not found."""
    return next(
        (message for message in reversed(messages) if message.role == Role.user),
        None,
    )


def is_diagram_request(messages: list[Message]) -> bool:
    """Return True if the last user message is asking for a diagram."""
    last_message = get_last_user_message(messages)
    return (
        last_message is not None and DIAGRAM_PATTERN.search(last_message.content) is not None
    )
