from pathlib import Path

import streamlit as st

from pages import home
from pages import reading
from pages import shopping
from pages import garbage
from services.db import create_tables

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
        "📚 読書記録",
        "🛒 買い物メモ",
        "🗑️ ゴミの日",
    ],
)

# -------------------------
# ページ切り替え
# -------------------------

if page == "🏠 Home":
    home.show()

elif page == "📚 読書記録":
    reading.show()

elif page == "🛒 買い物メモ":
    shopping.show()

elif page == "🗑️ ゴミの日":
    garbage.show()
