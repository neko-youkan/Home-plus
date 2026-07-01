from services.db import get_connection


def save_setting(key, value):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO settings (key, value)
        VALUES (?, ?)
        ON CONFLICT(key)
        DO UPDATE SET value = excluded.value
        """,
        (key, str(value)),
    )

    conn.commit()
    conn.close()


def get_setting(key, default=None):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT value FROM settings WHERE key = ?",
        (key,),
    )

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return default

    return row[0]