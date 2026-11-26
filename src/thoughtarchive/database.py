import sqlite3
from contextlib import closing

from platformdirs import user_data_path

from thoughtarchive.parser import get_archive_datetime


DB_DIR = user_data_path("thoughtArchive", appauthor=False)
DB_PATH = DB_DIR / "thoughtarchive.db"


def get_connection() -> sqlite3.Connection:
    DB_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def initialise_database():
    with closing(get_connection()) as connection:
        with connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS thoughts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    thought_date TEXT NOT NULL,
                    thought_time TEXT,
                    created_at TEXT NOT NULL DEFAULT (
                        strftime('%Y-%m-%dT%H:%M:%fZ', 'now')
                    )
                )
            """)


def create_thoughts_table(connection: sqlite3.Connection):
    connection.execute("""
        CREATE TABLE IF NOT EXISTS thoughts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            thought_date TEXT NOT NULL,
            thought_time TEXT,
            created_at TEXT NOT NULL DEFAULT (
                strftime('%Y-%m-%dT%H:%M:%fZ', 'now')
            )
        )
    """)


def add_thought(
    content: str,
    thought_date: str,
    thought_time: str | None,
) -> None:
    with closing(get_connection()) as connection:
        with connection:
            connection.execute(
                """
                INSERT INTO thoughts (
                    content,
                    thought_date,
                    thought_time
                )
                VALUES (?, ?, ?)
                """,
                (content, thought_date, thought_time),
            )


def get_recent_thoughts(number) -> list[sqlite3.Row]:
    with closing(get_connection()) as connection:
        cursor = connection.execute(
            """
            SELECT *
            FROM (
                SELECT
                    id,
                    content,
                    thought_date AS date,
                    thought_time AS time
                FROM thoughts
                ORDER BY id DESC
                LIMIT ?
            )
            ORDER BY id ASC
            """,
            (number,)
        )
    
        return cursor.fetchall()


def get_todays_thoughts() -> list[sqlite3.Row]:
    today = get_archive_datetime()[0].isoformat()

    with closing(get_connection()) as connection:
        cursor = connection.execute(
            """
            SELECT
                id,
                content,
                thought_date AS date,
                thought_time AS time
            FROM thoughts
            WHERE thought_date = ?
            ORDER BY id ASC
            """,
            (today,)
        )
    
        return cursor.fetchall()
