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

    recipe_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": "献立テンプレートを追加しました",
        "recipe_id": recipe_id,
    }


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


def save_recipe_ingredients(recipe_id, ingredients):
    """レシピの材料を保存する"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM recipe_ingredients
        WHERE recipe_id = ?
        """,
        (recipe_id,),
    )

    for ingredient in ingredients:
        ingredient = ingredient.strip()

        if ingredient:
            cursor.execute(
                """
                INSERT INTO recipe_ingredients
                (recipe_id, ingredient_name)
                VALUES (?, ?)
                """,
                (recipe_id, ingredient),
            )

    conn.commit()
    conn.close()


def get_recipe_ingredients(recipe_id):
    """レシピの材料一覧を取得する"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT ingredient_name
        FROM recipe_ingredients
        WHERE recipe_id = ?
        ORDER BY id
        """,
        (recipe_id,),
    )

    rows = cursor.fetchall()
    conn.close()

    return [row[0] for row in rows]


def get_ingredients_from_recipe_ids(recipe_ids):
    """複数レシピの材料一覧を取得する"""

    if not recipe_ids:
        return []

    conn = get_connection()
    cursor = conn.cursor()

    placeholders = ",".join("?" * len(recipe_ids))

    cursor.execute(
        f"""
        SELECT DISTINCT ingredient_name
        FROM recipe_ingredients
        WHERE recipe_id IN ({placeholders})
        ORDER BY ingredient_name
        """,
        recipe_ids,
    )

    rows = cursor.fetchall()
    conn.close()

    return [row[0] for row in rows]