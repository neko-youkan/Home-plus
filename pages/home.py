from datetime import date, datetime

import streamlit as st
from streamlit_js_eval import streamlit_js_eval

from components.weather_card import show_weather_card
from components.garbage_card import show_garbage_card
from components.menu_card import show_menu_card
from components.shopping_card import show_shopping_card
from components.reading_card import show_reading_card
from components.weekly_menu_card import show_weekly_menu_card
from components.recipe_card import show_recipe_card


def show():
    today = date.today()
    now = datetime.now()

    screen_width = streamlit_js_eval(
        js_expressions="window.innerWidth",
        key="screen_width",
    )

    is_mobile = screen_width is not None and screen_width <= 768

    st.write(f"画面幅: {screen_width}")
    st.write(f"スマホ判定: {is_mobile}")

    weekday_names = ["月", "火", "水", "木", "金", "土", "日"]

    if now.hour < 10:
        greeting = "おはようございます ☀️"
    elif now.hour < 18:
        greeting = "こんにちは 🌿"
    else:
        greeting = "こんばんは 🌙"

    st.markdown(
        f"""
        <div class="home-header">
            <div class="home-header-title">🏠 Home＋</div>
            <div class="home-header-info">
                <div>{today.year}/{today.month:02}/{today.day:02}（{weekday_names[today.weekday()]}）</div>
                <div>{greeting}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 天気
    show_weather_card()

    st.write("")

    # 次のごみの日
    show_garbage_card()

    st.divider()

    # 今日の献立・買い物メモ
    if is_mobile:
        show_menu_card()
        st.write("")
        show_shopping_card()
    else:
        col1, col2 = st.columns(2)

        with col1:
            show_menu_card()

        with col2:
            show_shopping_card()

    st.write("")

    # 今週の献立
    show_weekly_menu_card()

    st.write("")

    # 読書記録
    show_reading_card()