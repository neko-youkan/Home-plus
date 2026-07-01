import random

from services.db import get_connection
from services.user_service import get_current_user_id


def add_recipe(name, staple="", main_dish="", side_dish="", soup=""):
    """献立テンプレートを追加する"""

    if not name.strip():
        return {"success": False, "message": "献立名を入力してね"}

    user_id = get_current_user_id()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO recipes (
            user_id,
            name,
            staple,
            main_dish,
            side_dish,
            soup
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
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

    user_id = get_current_user_id()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, name, staple, main_dish, side_dish, soup
        FROM recipes
        WHERE user_id = ?
        ORDER BY created_at DESC
        """,
        (user_id,),
    )

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": row["id"],
            "name": row["name"],
            "staple": row["staple"] or "",
            "main_dish": row["main_dish"] or "",
            "side_dish": row["side_dish"] or "",
            "soup": row["soup"] or "",
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

    user_id = get_current_user_id()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM recipe_ingredients
        WHERE recipe_id = ?
          AND user_id = ?
        """,
        (recipe_id, user_id),
    )

    for ingredient in ingredients:
        ingredient = ingredient.strip()

        if ingredient:
            cursor.execute(
                """
                INSERT INTO recipe_ingredients (
                    user_id,
                    recipe_id,
                    ingredient_name
                )
                VALUES (?, ?, ?)
                """,
                (user_id, recipe_id, ingredient),
            )

    conn.commit()
    conn.close()


def get_recipe_ingredients(recipe_id):
    """レシピの材料一覧を取得する"""

    user_id = get_current_user_id()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT ingredient_name
        FROM recipe_ingredients
        WHERE recipe_id = ?
          AND user_id = ?
        ORDER BY id
        """,
        (recipe_id, user_id),
    )

    rows = cursor.fetchall()
    conn.close()

    return [row["ingredient_name"] for row in rows]


def get_ingredients_from_recipe_ids(recipe_ids):
    """複数レシピの材料一覧を取得する"""

    if not recipe_ids:
        return []

    user_id = get_current_user_id()

    conn = get_connection()
    cursor = conn.cursor()

    placeholders = ",".join("?" * len(recipe_ids))

    cursor.execute(
        f"""
        SELECT DISTINCT ingredient_name
        FROM recipe_ingredients
        WHERE user_id = ?
          AND recipe_id IN ({placeholders})
        ORDER BY ingredient_name
        """,
        [user_id, *recipe_ids],
    )

    rows = cursor.fetchall()
    conn.close()

    return [row["ingredient_name"] for row in rows]