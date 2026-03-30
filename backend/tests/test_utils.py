from app.providers._utils import get_last_user_message, is_diagram_request
from app.schemas import Role
from tests.utils import make_message


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


class TestIsDiagramRequest:
    def test_returns_true_when_last_message_contains_keyword(self) -> None:
        messages = [make_message(Role.user, "Create a flowchart")]
        assert is_diagram_request(messages) is True

    def test_returns_false_when_last_message_has_no_keyword(self) -> None:
        messages = [make_message(Role.user, "Hello there")]
        assert is_diagram_request(messages) is False

    def test_returns_false_for_empty_list(self) -> None:
        assert is_diagram_request([]) is False

    def test_uses_last_user_message_not_earlier_ones(self) -> None:
        messages = [
            make_message(Role.user, "Create a diagram"),
            make_message(Role.assistant, "Here's your diagram."),
            make_message(Role.user, "Thanks"),
        ]
        assert is_diagram_request(messages) is False

    def test_ignores_keywords_in_assistant_messages(self) -> None:
        messages = [
            make_message(Role.assistant, "I can create a diagram for you"),
            make_message(Role.user, "Hello"),
        ]
        assert is_diagram_request(messages) is False
