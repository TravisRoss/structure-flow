import re

# Matches messages that are requesting a diagram to be created.
DIAGRAM_PATTERN = re.compile(
    r"\b(create|generate|make|build|draw|show|diagram|flowchart|chart|flow)\b",
    re.IGNORECASE,
)

STUB_FALLBACK_MESSAGE = (
    "Hi! I can help you visualise processes as diagrams. What would you like to create?"
)

DEFAULT_DIAGRAM = """flowchart TD
    Start([Start]) --> Input[Enter Credentials]
    Input --> Validate{Valid?}
    Validate -->|No| Input
    Validate -->|Yes| Dashboard[Dashboard]"""
