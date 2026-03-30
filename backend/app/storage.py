import json
import sqlite3
import uuid
from pathlib import Path

from app.schemas import Message

_DB_PATH = Path(__file__).parent.parent / "conversations.db"


def init_db() -> None:
    with sqlite3.connect(_DB_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                messages TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


def save_conversation(conversation_id: str | None, messages: list[Message]) -> str:
    if conversation_id is None:
        conversation_id = str(uuid.uuid4())

    messages_json = json.dumps([message.model_dump(mode="json") for message in messages])

    with sqlite3.connect(_DB_PATH) as connection:
        connection.execute(
            """
            INSERT INTO conversations (id, messages)
            VALUES (?, ?)
            ON CONFLICT(id) DO UPDATE SET
                messages = excluded.messages,
                updated_at = CURRENT_TIMESTAMP
            """,
            (conversation_id, messages_json),
        )

    return conversation_id


def load_conversation(conversation_id: str) -> list[Message] | None:
    with sqlite3.connect(_DB_PATH) as connection:
        row = connection.execute(
            "SELECT messages FROM conversations WHERE id = ?",
            (conversation_id,),
        ).fetchone()

    if row is None:
        return None

    messages_data = json.loads(row[0])
    return [Message(**message) for message in messages_data]
