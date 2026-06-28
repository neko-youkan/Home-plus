"""
買い物メモサービス
"""

from services.db import get_connection
from services.recipe_service import get_ingredients_from_recipe_ids
from services.weekly_menu_service import get_weekly_menu


def get_shopping_list():
    """買い物メモ一覧を取得する"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM shopping_items
        ORDER BY created_at DESC
    """)

    items = cursor.fetchall()

    conn.close()

    return items


def add_shopping_item(item_name):
    """買い物メモを追加する"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO shopping_items (item_name)
        VALUES (?)
    """, (item_name,))

    conn.commit()
    conn.close()


def update_shopping_status(item_id, is_checked):
    """購入状態を更新する"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE shopping_items
        SET is_checked = ?
        WHERE id = ?
    """, (is_checked, item_id))

    conn.commit()
    conn.close()


def get_unchecked_shopping_list():
    """未購入の買い物メモだけ取得する"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM shopping_items
        WHERE is_checked = 0
        ORDER BY created_at DESC
    """)

    items = cursor.fetchall()

    conn.close()

    return items


def delete_shopping_item(item_id):
    """買い物メモを削除する"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM shopping_items
        WHERE id = ?
    """, (item_id,))

    conn.commit()
    conn.close()


def get_existing_unchecked_item_names():
    """未購入の買い物メモ名を取得する"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT item_name
        FROM shopping_items
        WHERE is_checked = 0
    """)

    rows = cursor.fetchall()

    conn.close()

    return [row[0] for row in rows]


def generate_shopping_from_weekly_menu():
    """今週の献立から買い物メモを生成する"""

    weekly_menu = get_weekly_menu()

    recipe_ids = [
        item["recipe_id"]
        for item in weekly_menu
        if item["recipe_id"] is not None
    ]

    if not recipe_ids:
        return {
            "success": False,
            "message": "今週の献立がまだ登録されていません",
            "added_items": [],
        }

    ingredients = get_ingredients_from_recipe_ids(recipe_ids)

    if not ingredients:
        return {
            "success": False,
            "message": "登録されている材料がありません",
            "added_items": [],
        }

    existing_items = get_existing_unchecked_item_names()
    existing_item_set = {
        item.strip()
        for item in existing_items
    }

    added_items = []

    conn = get_connection()
    cursor = conn.cursor()

    for ingredient in ingredients:
        ingredient = ingredient.strip()

        if not ingredient:
            continue

        if ingredient in existing_item_set:
            continue

        cursor.execute("""
            INSERT INTO shopping_items (item_name)
            VALUES (?)
        """, (ingredient,))

        added_items.append(ingredient)

    conn.commit()
    conn.close()

    if not added_items:
        return {
            "success": True,
            "message": "新しく追加する材料はありませんでした",
            "added_items": [],
        }

    return {
        "success": True,
        "message": f"{len(added_items)}件の材料を買い物メモに追加しました",
        "added_items": added_items,
    }