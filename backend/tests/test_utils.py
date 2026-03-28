from app.providers._utils import get_last_user_message
from app.schemas import Message, Role


def make_message(role: Role, content: str) -> Message:
    return Message(role=role, content=content)


class TestGetLastUserMessage:
    def test_returns_last_user_message(self) -> None:
        messages = [
            make_message(Role.user, "Hello"),
            make_message(Role.assistant, "Hi there"),
            make_message(Role.user, "Create a diagram"),
        ]
        result = get_last_user_message(messages)
        assert result.content == "Create a diagram"

    def test_returns_none_when_no_user_message(self) -> None:
        messages = [
            make_message(Role.assistant, "Hi there"),
        ]
        result = get_last_user_message(messages)
        assert result is None

    def test_returns_none_for_empty_list(self) -> None:
        result = get_last_user_message([])
        assert result is None

    def test_skips_trailing_assistant_message(self) -> None:
        messages = [
            make_message(Role.user, "First message"),
            make_message(Role.assistant, "Response"),
        ]
        result = get_last_user_message(messages)
        assert result is not None
        assert result.content == "First message"
