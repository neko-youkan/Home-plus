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
            is_admin INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cursor.execute("PRAGMA table_info(users)")
    columns = [row["name"] for row in cursor.fetchall()]

    if "is_admin" not in columns:
        cursor.execute(
            """
            ALTER TABLE users
            ADD COLUMN is_admin INTEGER DEFAULT 0
            """
        )

    cursor.execute(
        """
        UPDATE users
        SET is_admin = 1
        WHERE username = 'admin'
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


def record_login(user_id, username):
    """ログイン履歴を記録"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO login_logs (
            user_id,
            username
        )
        VALUES (?, ?)
        """,
        (
            user_id,
            username,
        ),
    )

    conn.commit()
    conn.close()


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

    user_id = user["id"]
    username = user["username"]
    password_hash = user["password_hash"]

    if not check_password(password, password_hash):
        return {
            "success": False,
            "message": "ユーザー名またはパスワードが違います",
        }

    record_login(user_id, username)

    return {
        "success": True,
        "message": "ログインしました",
        "user_id": user_id,
        "username": username,
    }


def change_password(user_id, current_password, new_password):
    """パスワードを変更"""

    if not current_password or not new_password:
        return {
            "success": False,
            "message": "現在のパスワードと新しいパスワードを入力してください",
        }

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT password_hash
        FROM users
        WHERE id = ?
        """,
        (user_id,),
    )

    user = cursor.fetchone()

    if user is None:
        conn.close()
        return {
            "success": False,
            "message": "ユーザーが見つかりません",
        }

    if not check_password(
        current_password,
        user["password_hash"],
    ):
        conn.close()
        return {
            "success": False,
            "message": "現在のパスワードが違います",
        }

    new_password_hash = hash_password(new_password)

    cursor.execute(
        """
        UPDATE users
        SET password_hash = ?
        WHERE id = ?
        """,
        (
            new_password_hash,
            user_id,
        ),
    )

    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": "パスワードを変更しました",
    }