from app.schemas import Message, Role


def make_message(role: Role, content: str) -> Message:
    return Message(role=role, content=content)
