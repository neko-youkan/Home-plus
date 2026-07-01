import bcrypt

from services.db import get_connection


def create_users_table():
    """ユーザーテーブルを作成"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    conn.commit()
    conn.close()


def hash_password(password):
    """パスワードをハッシュ化"""

    password_bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    return hashed.decode("utf-8")


def check_password(password, password_hash):
    """パスワードを検証"""

    return bcrypt.checkpw(
        password.encode("utf-8"),
        password_hash.encode("utf-8"),
    )


def register_user(username, password):
    """ユーザー登録"""

    if not username or not password:
        return {
            "success": False,
            "message": "ユーザー名とパスワードを入力してください",
        }

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE username = ?",
        (username,),
    )

    if cursor.fetchone():
        conn.close()
        return {
            "success": False,
            "message": "このユーザー名は既に使われています",
        }

    password_hash = hash_password(password)

    cursor.execute(
        """
        INSERT INTO users (username, password_hash)
        VALUES (?, ?)
        """,
        (username, password_hash),
    )

    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": "ユーザー登録が完了しました",
    }


def login_user(username, password):
    """ログイン"""

    if not username or not password:
        return {
            "success": False,
            "message": "ユーザー名とパスワードを入力してください",
        }

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, username, password_hash
        FROM users
        WHERE username = ?
        """,
        (username,),
    )

    user = cursor.fetchone()

    conn.close()

    if user is None:
        return {
            "success": False,
            "message": "ユーザー名またはパスワードが違います",
        }

    user_id, username, password_hash = user

    if not check_password(password, password_hash):
        return {
            "success": False,
            "message": "ユーザー名またはパスワードが違います",
        }

    return {
        "success": True,
        "message": "ログインしました",
        "user_id": user_id,
        "username": username,
    }