import streamlit as st

from components.weather_card import show_weather_card
from components.menu_card import show_menu_card
from components.shopping_card import show_shopping_card
from components.reading_card import show_reading_card
from components.garbage_card import show_garbage_card
from components.recipe_card import show_recipe_card
from components.weekly_menu_card import show_weekly_menu_card


def show():
    st.title("🏠 Home＋")

    show_weather_card()

    st.write("")

    show_garbage_card()

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        show_menu_card()

    with col2:
        show_shopping_card()

    st.write("")

    show_weekly_menu_card()

    st.write("")

    show_reading_card()