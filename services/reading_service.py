from datetime import datetime

from services.db import get_connection
from services.user_service import get_current_user_id


def create_book(
    title,
    author,
    start_date,
    end_date,
    rating,
    status,
    memo,
    total_pages=0,
    current_page=0,
):
    """読書記録を登録する"""

    user_id = get_current_user_id()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO books (
            user_id,
            title,
            author,
            start_date,
            end_date,
            rating,
            status,
            memo,
            total_pages,
            current_page,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            title,
            author,
            start_date,
            end_date,
            rating,
            status,
            memo,
            total_pages,
            current_page,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ),
    )

    conn.commit()
    conn.close()

    return {"success": True, "message": "読書記録を保存しました"}


def get_reading_books():
    """読書中の本を取得する"""

    user_id = get_current_user_id()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM books
        WHERE user_id = ?
          AND status = 'reading'
        ORDER BY created_at DESC
        """,
        (user_id,),
    )

    books = cursor.fetchall()
    conn.close()

    return books


def get_finished_books(limit=3):
    """最近読了した本を取得する"""

    user_id = get_current_user_id()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM books
        WHERE user_id = ?
          AND status = 'finished'
        ORDER BY end_date DESC
        LIMIT ?
        """,
        (user_id, limit),
    )

    books = cursor.fetchall()
    conn.close()

    return books


def get_current_reading_book():
    """現在読書中の最新1冊を取得する"""

    user_id = get_current_user_id()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM books
        WHERE user_id = ?
          AND status = 'reading'
        ORDER BY created_at DESC
        LIMIT 1
        """,
        (user_id,),
    )

    book = cursor.fetchone()
    conn.close()

    return book


def update_book_progress(book_id, current_page, total_pages):
    """読書進捗を更新する"""

    user_id = get_current_user_id()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE books
        SET current_page = ?,
            total_pages = ?
        WHERE id = ?
          AND user_id = ?
        """,
        (current_page, total_pages, book_id, user_id),
    )

    conn.commit()
    conn.close()

    return {"success": True, "message": "読書進捗を更新しました"}


def finish_book(book_id, end_date, rating, memo):
    """読書を完了する"""

    user_id = get_current_user_id()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE books
        SET end_date = ?,
            rating = ?,
            memo = ?,
            status = 'finished'
        WHERE id = ?
          AND user_id = ?
        """,
        (end_date, rating, memo, book_id, user_id),
    )

    conn.commit()
    conn.close()

    return {"success": True, "message": "読了として保存しました"}


def delete_book(book_id):
    """読書記録を削除する"""

    user_id = get_current_user_id()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM books
        WHERE id = ?
          AND user_id = ?
        """,
        (book_id, user_id),
    )

    conn.commit()
    conn.close()

    return {"success": True, "message": "読書記録を削除しました"}


def rating_to_stars(rating):
    """数値評価を星表示に変換する"""

    if rating is None:
        return "未評価"

    rating = int(rating)
    return "★" * rating + "☆" * (5 - rating)


def progress_percent(current_page, total_pages):
    """読書進捗率を計算する"""

    if not total_pages:
        return 0

    return min(int(current_page / total_pages * 100), 100)