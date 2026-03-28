from app.schemas import Message, Role


def get_last_user_message(messages: list[Message]) -> Message | None:
    """Return the most recent user message from a conversation, or None if not found."""
    return next(
        (message for message in reversed(messages) if message.role == Role.user),
        None,
    )
