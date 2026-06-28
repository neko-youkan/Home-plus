from datetime import date, timedelta
import random

from services.db import get_connection
from services.recipe_service import get_all_recipes


def get_week_start():
    """今週の月曜日を取得"""
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    return monday.isoformat()


def save_weekly_menu(weekday, recipe_id):
    """週間献立を保存"""

    week_start = get_week_start()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO weekly_menu (week_start, weekday, recipe_id)
        VALUES (?, ?, ?)
        ON CONFLICT(week_start, weekday)
        DO UPDATE SET
            recipe_id = excluded.recipe_id,
            updated_at = CURRENT_TIMESTAMP
        """,
        (week_start, weekday, recipe_id),
    )

    conn.commit()
    conn.close()


def get_weekly_menu():
    """今週の献立を取得"""

    week_start = get_week_start()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            wm.weekday,
            wm.recipe_id,
            r.name,
            r.staple,
            r.main_dish,
            r.side_dish,
            r.soup
        FROM weekly_menu wm
        LEFT JOIN recipes r
            ON wm.recipe_id = r.id
        WHERE wm.week_start = ?
        ORDER BY wm.weekday
        """,
        (week_start,),
    )

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "weekday": row[0],
            "recipe_id": row[1],
            "name": row[2] or "",
            "staple": row[3] or "",
            "main_dish": row[4] or "",
            "side_dish": row[5] or "",
            "soup": row[6] or "",
        }
        for row in rows
    ]


def fill_empty_weekly_menu_random():
    """未定の曜日だけランダムで献立を埋める"""

    recipes = get_all_recipes()

    if not recipes:
        return {"success": False, "message": "献立テンプレートがまだありません"}

    current_week = get_weekly_menu()
    current_dict = {
        item["weekday"]: item["recipe_id"]
        for item in current_week
    }

    filled_count = 0

    for weekday in range(7):
        recipe_id = current_dict.get(weekday)

        if recipe_id is None:
            recipe = random.choice(recipes)
            save_weekly_menu(weekday, recipe["id"])
            filled_count += 1

    if filled_count == 0:
        return {"success": True, "message": "未定の曜日はありません"}

    return {
        "success": True,
        "message": f"未定の曜日を{filled_count}件ランダムで埋めました",
    }