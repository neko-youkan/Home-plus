import streamlit as st

from components.ui import show_title
from services.garbage_service import get_next_garbage_day


def show_garbage_card():
    """次のごみの日カード"""

    show_title("garbage", "🗑️", "次のごみの日")

    result = get_next_garbage_day()

    if result is None:
        st.info("ごみ収集ルールが登録されていません。")
        return

    target_date = result["date"]
    rules = result["rules"]

    weekday_names = ["月", "火", "水", "木", "金", "土", "日"]

    st.markdown(
        f"""
        <div class="garbage-date">
            {target_date.month}月{target_date.day}日（{weekday_names[target_date.weekday()]}）
        </div>
        """,
        unsafe_allow_html=True,
    )

    for rule in rules:
        _, garbage_name, icon, _, _, _ = rule

        st.markdown(
            f"""
            <div class="garbage-item">
                <span class="garbage-icon">{icon}</span>
                <span>{garbage_name}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )