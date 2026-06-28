import streamlit as st

from components.ui import show_title
from services.garbage_service import get_next_garbage


def show_garbage_card():
    garbage = get_next_garbage()

    with st.container(border=True):

        show_title("garbage", "🗑️", "次のゴミの日")

        st.markdown("### " + garbage["icon"] + " " + garbage["type"])

        st.caption("📅 " + garbage["date"])