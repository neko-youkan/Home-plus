from datetime import date, datetime

from services.db import get_connection


def save_today_menu(staple="", main_dish="", side_dish="", soup=""):
    """今日の献立を保存・更新する"""

    today = date.today().isoformat()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO menu (date, staple, main_dish, side_dish, soup)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(date) DO UPDATE SET
            staple = excluded.staple,
            main_dish = excluded.main_dish,
            side_dish = excluded.side_dish,
            soup = excluded.soup,
            updated_at = CURRENT_TIMESTAMP
        """,
        (today, staple, main_dish, side_dish, soup),
    )

    conn.commit()
    conn.close()

    return {"success": True, "message": "献立を保存しました"}


def get_today_menu():
    """今日の献立を取得する"""

    today = date.today().isoformat()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, date, staple, main_dish, side_dish, soup
        FROM menu
        WHERE date = ?
        """,
        (today,),
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
        "id": row[0],
        "date": row[1],
        "staple": row[2] or "",
        "main_dish": row[3] or "",
        "side_dish": row[4] or "",
        "soup": row[5] or "",
    }


def get_previous_menu_date(item_type, value):
    """同じ献立を前回作った日を取得する"""

    allowed_columns = ["staple", "main_dish", "side_dish", "soup"]

    if item_type not in allowed_columns:
        return None

    if not value:
        return None

    today = date.today().isoformat()

    conn = get_connection()
    cursor = conn.cursor()

    query = f"""
        SELECT date
        FROM menu
        WHERE {item_type} = ?
          AND date < ?
        ORDER BY date DESC
        LIMIT 1
    """

    cursor.execute(query, (value, today))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None

    previous_date = datetime.strptime(row[0], "%Y-%m-%d").date()
    days = (date.today() - previous_date).days

    return {
        "date": previous_date.strftime("%Y-%m-%d"),
        "days": days,
    }