from datetime import date, datetime

from services.db import get_connection
from services.user_service import get_current_user_id


def save_today_menu(staple="", main_dish="", side_dish="", soup=""):
    """今日の献立を保存・更新する"""

    user_id = get_current_user_id()
    today = date.today().isoformat()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO menu (
            user_id,
            date,
            staple,
            main_dish,
            side_dish,
            soup
        )
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(user_id, date) DO UPDATE SET
            staple = excluded.staple,
            main_dish = excluded.main_dish,
            side_dish = excluded.side_dish,
            soup = excluded.soup,
            updated_at = CURRENT_TIMESTAMP
        """,
        (
            user_id,
            today,
            staple,
            main_dish,
            side_dish,
            soup,
        ),
    )

    conn.commit()
    conn.close()

    return {"success": True, "message": "献立を保存しました"}


def get_today_menu():
    """今日の献立を取得する"""

    user_id = get_current_user_id()
    today = date.today().isoformat()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, date, staple, main_dish, side_dish, soup
        FROM menu
        WHERE user_id = ?
          AND date = ?
        """,
        (user_id, today),
    )

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return {
            "staple": "",
            "main_dish": "",
            "side_dish": "",
            "soup": "",
        }

    return {
        "id": row["id"],
        "date": row["date"],
        "staple": row["staple"] or "",
        "main_dish": row["main_dish"] or "",
        "side_dish": row["side_dish"] or "",
        "soup": row["soup"] or "",
    }


def get_previous_menu_date(item_type, value):
    """同じ献立を前回作った日を取得する"""

    allowed_columns = ["staple", "main_dish", "side_dish", "soup"]

    if item_type not in allowed_columns:
        return None

    if not value:
        return None

    user_id = get_current_user_id()
    today = date.today().isoformat()

    conn = get_connection()
    cursor = conn.cursor()

    query = f"""
        SELECT date
        FROM menu
        WHERE user_id = ?
          AND {item_type} = ?
          AND date < ?
        ORDER BY date DESC
        LIMIT 1
    """

    cursor.execute(query, (user_id, value, today))

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None

    previous_date = datetime.strptime(row["date"], "%Y-%m-%d").date()
    days = (date.today() - previous_date).days

    return {
        "date": previous_date.strftime("%Y-%m-%d"),
        "days": days,
    }