import streamlit as st

from pages import home

st.set_page_config(
    page_title="Homeplus",
    page_icon="🏠",
    layout="wide",
)

home.show()