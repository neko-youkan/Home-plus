from services.db import get_connection


def get_users(keyword=""):
    """ユーザー一覧を取得"""

    conn = get_connection()
    cursor = conn.cursor()

    if keyword:
        cursor.execute(
            """
            SELECT
                id,
                username,
                is_admin,
                created_at
            FROM users
            WHERE username LIKE ?
            ORDER BY is_admin DESC, id
            """,
            (f"%{keyword}%",),
        )
    else:
        cursor.execute(
            """
            SELECT
                id,
                username,
                is_admin,
                created_at
            FROM users
            ORDER BY is_admin DESC, id
            """
        )

    users = cursor.fetchall()
    conn.close()

    return users


def get_user_count():
    """登録ユーザー数を取得"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) AS count FROM users")

    row = cursor.fetchone()
    conn.close()

    return row["count"]


def get_admin_count():
    """管理者数を取得"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*) AS count
        FROM users
        WHERE is_admin = 1
        """
    )

    row = cursor.fetchone()
    conn.close()

    return row["count"]


def get_today_login_count():
    """今日のログイン回数を取得"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*) AS count
        FROM login_logs
        WHERE date(login_at) = date('now', 'localtime')
        """
    )

    row = cursor.fetchone()
    conn.close()

    return row["count"]


def get_total_login_count():
    """総ログイン回数を取得"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*) AS count
        FROM login_logs
        """
    )

    row = cursor.fetchone()
    conn.close()

    return row["count"]


def get_last_login(user_id):
    """最終ログイン日時を取得"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT login_at
        FROM login_logs
        WHERE user_id = ?
        ORDER BY login_at DESC
        LIMIT 1
        """,
        (user_id,),
    )

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return "未ログイン"

    return row["login_at"]


def get_user_login_count(user_id):
    """ユーザーごとのログイン回数を取得"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*) AS count
        FROM login_logs
        WHERE user_id = ?
        """,
        (user_id,),
    )

    row = cursor.fetchone()
    conn.close()

    return row["count"]


def get_table_count(table_name):
    """指定テーブルの件数を取得"""

    allowed_tables = [
        "recipes",
        "shopping_items",
        "books",
        "garbage_rules",
        "weekly_menu",
        "menu",
    ]

    if table_name not in allowed_tables:
        return 0

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"SELECT COUNT(*) AS count FROM {table_name}")

    row = cursor.fetchone()
    conn.close()

    return row["count"]


def get_user_table_count(table_name, user_id):
    """ユーザーごとの指定テーブル件数を取得"""

    allowed_tables = [
        "recipes",
        "shopping_items",
        "books",
        "garbage_rules",
        "weekly_menu",
        "menu",
    ]

    if table_name not in allowed_tables:
        return 0

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        f"""
        SELECT COUNT(*) AS count
        FROM {table_name}
        WHERE user_id = ?
        """,
        (user_id,),
    )

    row = cursor.fetchone()
    conn.close()

    return row["count"]


def get_user_stats(user_id):
    """ユーザーごとの利用状況を取得"""

    return {
        "recipes": get_user_table_count("recipes", user_id),
        "shopping_items": get_user_table_count("shopping_items", user_id),
        "books": get_user_table_count("books", user_id),
        "garbage_rules": get_user_table_count("garbage_rules", user_id),
        "weekly_menu": get_user_table_count("weekly_menu", user_id),
        "menu": get_user_table_count("menu", user_id),
        "last_login": get_last_login(user_id),
        "login_count": get_user_login_count(user_id),
    }


def get_app_stats():
    """アプリ全体の統計を取得"""

    return {
        "users": get_user_count(),
        "admins": get_admin_count(),
        "today_logins": get_today_login_count(),
        "total_logins": get_total_login_count(),
        "recipes": get_table_count("recipes"),
        "shopping_items": get_table_count("shopping_items"),
        "books": get_table_count("books"),
        "garbage_rules": get_table_count("garbage_rules"),
        "weekly_menu": get_table_count("weekly_menu"),
        "menu": get_table_count("menu"),
    }


def is_admin_user(user_id):
    """管理者かどうか判定"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT is_admin
        FROM users
        WHERE id = ?
        """,
        (user_id,),
    )

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return False

    return row["is_admin"] == 1


def set_admin(user_id):
    """管理者にする"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users
        SET is_admin = 1
        WHERE id = ?
        """,
        (user_id,),
    )

    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": "管理者に変更しました",
    }


def remove_admin(user_id):
    """一般ユーザーに戻す"""

    if get_admin_count() <= 1:
        return {
            "success": False,
            "message": "最後の管理者は一般ユーザーに変更できません",
        }

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users
        SET is_admin = 0
        WHERE id = ?
        """,
        (user_id,),
    )

    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": "一般ユーザーに変更しました",
    }


def delete_user(user_id):
    """ユーザーを削除"""

    conn = get_connection()
    cursor = conn.cursor()

    tables = [
        "recipes",
        "shopping_items",
        "books",
        "garbage_rules",
        "weekly_menu",
        "menu",
        "settings",
        "recipe_ingredients",
        "login_logs",
    ]

    for table in tables:
        cursor.execute(
            f"""
            DELETE FROM {table}
            WHERE user_id = ?
            """,
            (user_id,),
        )

    cursor.execute(
        """
        DELETE FROM users
        WHERE id = ?
        """,
        (user_id,),
    )

    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": "ユーザーを削除しました",
    }