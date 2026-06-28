"""
買い物メモサービス
"""

from services.db import get_connection


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