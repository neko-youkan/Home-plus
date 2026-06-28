from datetime import datetime

from services.db import get_connection


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

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO books (
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
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
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

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM books
        WHERE status = 'reading'
        ORDER BY created_at DESC
        """
    )

    books = cursor.fetchall()
    conn.close()

    return books


def get_finished_books(limit=3):
    """最近読了した本を取得する"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM books
        WHERE status = 'finished'
        ORDER BY end_date DESC
        LIMIT ?
        """,
        (limit,),
    )

    books = cursor.fetchall()
    conn.close()

    return books


def get_current_reading_book():
    """現在読書中の最新1冊を取得する"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM books
        WHERE status = 'reading'
        ORDER BY created_at DESC
        LIMIT 1
        """
    )

    book = cursor.fetchone()

    conn.close()

    return book


def update_book_progress(book_id, current_page, total_pages):
    """読書進捗を更新する"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE books
        SET current_page = ?,
            total_pages = ?
        WHERE id = ?
        """,
        (current_page, total_pages, book_id),
    )

    conn.commit()
    conn.close()

    return {"success": True, "message": "読書進捗を更新しました"}


def finish_book(book_id, end_date, rating, memo):
    """読書を完了する"""

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
        """,
        (end_date, rating, memo, book_id),
    )

    conn.commit()
    conn.close()

    return {"success": True, "message": "読了として保存しました"}


def delete_book(book_id):
    """読書記録を削除する"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM books
        WHERE id = ?
        """,
        (book_id,),
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