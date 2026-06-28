import streamlit as st

from pages import home
from pages import reading
from pages import shopping
from services.db import create_tables
from pages import menu


st.set_page_config(
    page_title="Home＋",
    page_icon="🏠",
    layout="wide",
)

create_tables()

page = st.sidebar.radio(
    "ページ",
    [
        "🏠 Home",
        "🛒 買い物メモ",
        "🍽️ 献立管理",
        "📚 読書記録",
        
    ],
)

if page == "🏠 Home":
    home.show()

elif page == "🛒 買い物メモ":
    shopping.show()

elif page == "🍽️ 献立管理":
    menu.show()

elif page == "📚 読書記録":
    reading.show()

