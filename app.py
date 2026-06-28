import streamlit as st

from pages import home

st.set_page_config(
    page_title="Home＋",
    page_icon="🏠",
    layout="wide",
)

home.show()