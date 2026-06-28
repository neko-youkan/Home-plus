"""
献立サービス
"""


def get_today_menu():
    """今日の献立の初期データを取得する"""

    return {
        "main": "",
        "side": "",
        "soup": "",
    }


def save_today_menu(main, side, soup):
    """今日の献立を保存する"""

    # SQLite / Googleスプレッドシート連携は今後実装予定
    return {
        "success": True,
        "message": "献立を保存しました（仮）",
        "data": {
            "main": main,
            "side": side,
            "soup": soup,
        },
    }