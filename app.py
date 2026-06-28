import streamlit as st

from pages import home
from pages import reading
from services.db import create_tables

st.set_page_config(
    page_title="Home＋",
    page_icon="🏠",
    layout="wide",
)

create_tables()

page = st.sidebar.radio(
    "ページ",
    ["🏠 Home", "📚 読書記録"],
)

if page == "🏠 Home":
    home.show()
elif page == "📚 読書記録":
    reading.show()