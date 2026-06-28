from services.db import get_connection


def add_ingredient(recipe_id, ingredient_name):
    """食材を追加する"""

    if not ingredient_name.strip():
        return {
            "success": False,
            "message": "食材名を入力してください",
        }

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO recipe_ingredients (
            recipe_id,
            ingredient_name
        )
        VALUES (?, ?)
        """,
        (
            recipe_id,
            ingredient_name.strip(),
        ),
    )

    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": "食材を追加しました",
    }


def get_ingredients_by_recipe(recipe_id):
    """献立の食材一覧を取得する"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            ingredient_name
        FROM recipe_ingredients
        WHERE recipe_id = ?
        ORDER BY ingredient_name
        """,
        (recipe_id,),
    )

    rows = cursor.fetchall()

    conn.close()

    return [
        {
            "id": row[0],
            "ingredient_name": row[1],
        }
        for row in rows
    ]


def delete_ingredient(ingredient_id):
    """食材を削除する"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM recipe_ingredients
        WHERE id = ?
        """,
        (ingredient_id,),
    )

    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": "食材を削除しました",
    }


def delete_all_ingredients_by_recipe(recipe_id):
    """献立に登録されている食材を全削除する"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM recipe_ingredients
        WHERE recipe_id = ?
        """,
        (recipe_id,),
    )

    conn.commit()
    conn.close()