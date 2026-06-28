import sqlite3
from pathlib import Path

DB_PATH = Path("data/homeplus.db")


def get_connection():
    """SQLiteデータベースへ接続する"""

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def add_column_if_not_exists(cursor, table_name, column_name, column_type):
    """カラムが存在しなければ追加する"""

    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [row["name"] for row in cursor.fetchall()]

    if column_name not in columns:
        cursor.execute(
            f"ALTER TABLE {table_name} "
            f"ADD COLUMN {column_name} {column_type}"
        )


def create_tables():
    """必要なテーブルを作成する"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS menu (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL UNIQUE,
        staple TEXT,
        main_dish TEXT,
        side_dish TEXT,
        soup TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        staple TEXT,
        main_dish TEXT,
        side_dish TEXT,
        soup TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weekly_menu (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        week_start TEXT NOT NULL,
        weekday INTEGER NOT NULL,
        recipe_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(week_start, weekday),
        FOREIGN KEY (recipe_id) REFERENCES recipes(id)
    )
    """)

    cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS recipe_ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_id INTEGER NOT NULL,
        ingredient_name TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (recipe_id) REFERENCES recipes(id)
    )
    """)
    

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS shopping_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT NOT NULL,
        is_checked INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT,
        start_date TEXT,
        end_date TEXT,
        rating INTEGER,
        status TEXT,
        memo TEXT,
        created_at TEXT
    )
    """)


    # ===== 新しいカラムはここで追加 =====
    add_column_if_not_exists(cursor, "books", "total_pages", "INTEGER")
    add_column_if_not_exists(cursor, "books", "current_page", "INTEGER")

    conn.commit()
    conn.close()