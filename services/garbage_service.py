from services.db import get_connection
from datetime import date, timedelta

def get_week_number(target_date):
    """第何週かを返す"""

    return (target_date.day - 1) // 7 + 1

def get_all_garbage_rules():
    """ごみ収集ルール一覧を取得"""

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
        WHERE is_active = 1
        ORDER BY weekday, garbage_name
        """
    )

    rows = cursor.fetchall()
    conn.close()

    return rows

def is_match(rule, target_date):
    """ルールに一致するか"""

    (
        _,
        _,
        _,
        weekday,
        week_numbers,
        _,
    ) = rule

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

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO garbage_rules (
            garbage_name,
            icon,
            weekday,
            week_numbers
        )
        VALUES (?, ?, ?, ?)
        """,
        (
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

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM garbage_rules
        WHERE id = ?
        """,
        (rule_id,),
    )

    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": "削除しました",
    }