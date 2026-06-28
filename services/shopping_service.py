"""
買い物メモサービス
"""


def get_shopping_list():
    """買い物メモの初期データを取得する"""

    return [
        "",
        "",
        "",
        "",
        "",
    ]


def save_shopping_list(items):
    """買い物メモを保存する"""

    return {
        "success": True,
        "message": "買い物メモを保存しました（仮）",
        "items": items,
    }