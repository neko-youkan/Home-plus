from services.db import get_connection


def create_announcement(title, message, created_by, is_pinned=0):
    """お知らせを作成"""

    if not title.strip() or not message.strip():
        return {
            "success": False,
            "message": "タイトルと本文を入力してください",
        }

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO announcements (
            title,
            message,
            created_by,
            is_pinned
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            title.strip(),
            message.strip(),
            created_by,
            is_pinned,
        ),
    )

    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": "お知らせを作成しました",
    }


def get_active_announcements():
    """公開中のお知らせを取得"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM announcements
        WHERE is_active = 1
        ORDER BY is_pinned DESC, created_at DESC
        """
    )

    rows = cursor.fetchall()
    conn.close()

    return rows


def get_all_announcements():
    """すべてのお知らせを取得"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM announcements
        ORDER BY created_at DESC
        """
    )

    rows = cursor.fetchall()
    conn.close()

    return rows


def update_announcement_status(announcement_id, is_active):
    """公開状態を変更"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE announcements
        SET is_active = ?
        WHERE id = ?
        """,
        (
            is_active,
            announcement_id,
        ),
    )

    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": "公開状態を変更しました",
    }


def update_announcement_pinned(announcement_id, is_pinned):
    """固定表示を変更"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE announcements
        SET is_pinned = ?
        WHERE id = ?
        """,
        (
            is_pinned,
            announcement_id,
        ),
    )

    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": "固定表示を変更しました",
    }


def delete_announcement(announcement_id):
    """お知らせを削除"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM announcements
        WHERE id = ?
        """,
        (announcement_id,),
    )

    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": "お知らせを削除しました",
    }