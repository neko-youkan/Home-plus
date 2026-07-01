from pathlib import Path

import streamlit as st

from services.db import create_tables

create_tables()

from pages import home
from pages import menu
from pages import reading
from pages import shopping
from pages import garbage
from pages import settings

# -------------------------
# ページ設定
# -------------------------

st.set_page_config(
    page_title="Home＋",
    page_icon="🏠",
    layout="wide",
)

# -------------------------
# CSS読み込み
# -------------------------

css = Path("assets/style.css").read_text(encoding="utf-8")

st.markdown(
    f"<style>{css}</style>",
    unsafe_allow_html=True,
)

# -------------------------
# DB初期化
# -------------------------

create_tables()

# -------------------------
# サイドバー
# -------------------------

page = st.sidebar.radio(
    "ページ",
    [
        "🏠 Home",
        "🍽️ 献立",
        "🛒 買い物メモ",
        "🗑️ ゴミの日",
        "📚 読書記録",
        "⚙️ 設定",
    ],
)

# -------------------------
# ページ切り替え
# -------------------------

if page == "🏠 Home":
    home.show()

elif page == "🗑️ ゴミの日":
    garbage.show()

elif page == "🍽️ 献立":
    menu.show()

elif page == "🛒 買い物メモ":
    shopping.show()

elif page == "📚 読書記録":
    reading.show()

elif page == "⚙️ 設定":
    settings.show()