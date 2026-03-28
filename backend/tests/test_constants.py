import pytest

from app.providers._constants import DIAGRAM_PATTERN


class TestDiagramPattern:
    @pytest.mark.parametrize("word", [
        "create",
        "generate",
        "make",
        "build",
        "draw",
        "show",
        "diagram",
        "flowchart",
        "chart",
        "flow",
    ])
    def test_matches_keyword(self, word: str) -> None:
        assert DIAGRAM_PATTERN.search(word) is not None

    @pytest.mark.parametrize("word", [
        "Create",
        "GENERATE",
        "Make",
        "FLOWCHART",
    ])
    def test_is_case_insensitive(self, word: str) -> None:
        assert DIAGRAM_PATTERN.search(word) is not None

    def test_matches_keyword_within_sentence(self) -> None:
        assert DIAGRAM_PATTERN.search("Can you create a login flow?") is not None

    def test_does_not_match_unrelated_input(self) -> None:
        assert DIAGRAM_PATTERN.search("Hello, how are you?") is None

    def test_does_not_match_empty_string(self) -> None:
        assert DIAGRAM_PATTERN.search("") is None
