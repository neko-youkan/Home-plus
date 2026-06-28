import streamlit as st

from components.ui import show_title
from services.recipe_service import add_recipe


def show_recipe_card():
    with st.container(border=True):
        show_title("recipe", "📖", "献立テンプレート")

        name = st.text_input("献立名", placeholder="例）ハンバーグ定食")
        staple = st.text_input("🍚 主食", placeholder="例）ごはん")
        main_dish = st.text_input("🐟 主菜", placeholder="例）ハンバーグ")
        side_dish = st.text_input("🥗 副菜", placeholder="例）サラダ")
        soup = st.text_input("🥣 汁物", placeholder="例）味噌汁")

        if st.button("📖 テンプレート追加", use_container_width=True):
            result = add_recipe(name, staple, main_dish, side_dish, soup)

            if result["success"]:
                st.success(result["message"])
                st.rerun()
            else:
                st.error(result["message"])