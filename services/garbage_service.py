from datetime import date, timedelta

from services.db import get_connection
from services.user_service import get_current_user_id


def get_week_number(target_date):
    """第何週かを返す"""

    return (target_date.day - 1) // 7 + 1


def get_all_garbage_rules():
    """ごみ収集ルール一覧を取得"""

    user_id = get_current_user_id()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            garbage_name,
            icon,
            weekday,
            week_numbers,
            is_active
        FROM garbage_rules
        WHERE user_id = ?
          AND is_active = 1
        ORDER BY weekday, garbage_name
        """,
        (user_id,),
    )

    rows = cursor.fetchall()
    conn.close()

    return rows


def is_match(rule, target_date):
    """ルールに一致するか"""

    weekday = rule["weekday"]
    week_numbers = rule["week_numbers"]

    if target_date.weekday() != weekday:
        return False

    if week_numbers == "":
        return True

    week = get_week_number(target_date)

    return str(week) in week_numbers.split(",")


def get_next_garbage_day():
    """次のごみの日を取得"""

    rules = get_all_garbage_rules()

    today = date.today()

    for i in range(31):
        target_date = today + timedelta(days=i)

        matched_rules = []

        for rule in rules:
            if is_match(rule, target_date):
                matched_rules.append(rule)

        if matched_rules:
            return {
                "date": target_date,
                "rules": matched_rules,
            }

    return None


def create_garbage_rule(
    garbage_name,
    icon,
    weekday,
    week_numbers,
):
    """ごみ収集ルールを追加"""

    user_id = get_current_user_id()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO garbage_rules (
            user_id,
            garbage_name,
            icon,
            weekday,
            week_numbers
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            user_id,
            garbage_name,
            icon,
            weekday,
            week_numbers,
        ),
    )

    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": "追加しました",
    }


def delete_garbage_rule(rule_id):
    """ごみ収集ルールを削除"""

    user_id = get_current_user_id()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM garbage_rules
        WHERE id = ?
          AND user_id = ?
        """,
        (rule_id, user_id),
    )

    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": "削除しました",
    }