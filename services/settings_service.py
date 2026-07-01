from services.db import get_connection
from services.user_service import get_current_user_id


def save_setting(key, value):
    """設定を保存"""

    user_id = get_current_user_id()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO settings (
            user_id,
            key,
            value
        )
        VALUES (?, ?, ?)
        ON CONFLICT(user_id, key)
        DO UPDATE SET
            value = excluded.value
        """,
        (
            user_id,
            key,
            str(value),
        ),
    )

    conn.commit()
    conn.close()


def get_setting(key, default=None):
    """設定を取得"""

    user_id = get_current_user_id()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT value
        FROM settings
        WHERE user_id = ?
          AND key = ?
        """,
        (
            user_id,
            key,
        ),
    )

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return default

    return row["value"]