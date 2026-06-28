import random

from services.db import get_connection


def add_recipe(name, staple="", main_dish="", side_dish="", soup=""):
    """献立テンプレートを追加する"""

    if not name.strip():
        return {"success": False, "message": "献立名を入力してね"}

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO recipes (name, staple, main_dish, side_dish, soup)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            name.strip(),
            staple.strip(),
            main_dish.strip(),
            side_dish.strip(),
            soup.strip(),
        ),
    )

    conn.commit()
    conn.close()

    return {"success": True, "message": "献立テンプレートを追加しました"}


def get_all_recipes():
    """献立テンプレートをすべて取得する"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, name, staple, main_dish, side_dish, soup
        FROM recipes
        ORDER BY created_at DESC
        """
    )

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": row[0],
            "name": row[1],
            "staple": row[2] or "",
            "main_dish": row[3] or "",
            "side_dish": row[4] or "",
            "soup": row[5] or "",
        }
        for row in rows
    ]


def get_random_recipe():
    """ランダムに献立テンプレートを1件取得する"""

    recipes = get_all_recipes()

    if not recipes:
        return None

    return random.choice(recipes)