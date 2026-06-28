"""
献立サービス
"""


def get_today_menu():
    """今日の献立を取得する"""

    return {
        "主食": "ごはん",
        "主菜": "焼き魚",
        "副菜": "冷奴",
        "汁物": "味噌汁",
    }


def save_today_menu(item, value):
    """今日の献立を保存する"""

    # SQLite / Googleスプレッドシート連携は今後実装予定
    return {
        "success": True,
        "message": f"{item} を保存しました（仮）",
        "data": {
            "item": item,
            "value": value,
        },
    }