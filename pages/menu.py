import streamlit as st

from components.recipe_card import show_recipe_card
from components.recipe_detail_card import show_recipe_detail_card
from components.ui import show_title
from services.recipe_service import get_all_recipes
from services.shopping_service import generate_shopping_from_weekly_menu
from services.weekly_menu_service import (
    fill_empty_weekly_menu_random,
    get_weekly_menu,
    save_weekly_menu,
)


def show():
    st.title("🍽 献立管理")

    recipes = get_all_recipes()

    with st.container(border=True):
        show_title("weekly_menu_setting", "📅", "今週の献立設定")

        if not recipes:
            st.write("先に献立テンプレートを登録してね")
        else:
            current_week = get_weekly_menu()
            current_dict = {
                item["weekday"]: item["recipe_id"]
                for item in current_week
            }

            weekdays = ["月", "火", "水", "木", "金", "土", "日"]

            options = [{"id": None, "name": "未定"}] + recipes
            selected_recipe_ids = {}

            for weekday_index, weekday_name in enumerate(weekdays):
                current_recipe_id = current_dict.get(weekday_index)

                default_index = 0
                for i, option in enumerate(options):
                    if option["id"] == current_recipe_id:
                        default_index = i
                        break

                selected_option = st.selectbox(
                    f"{weekday_name}曜日",
                    options,
                    index=default_index,
                    format_func=lambda option: option["name"],
                    key=f"weekly_menu_{weekday_index}",
                )

                selected_recipe_ids[weekday_index] = selected_option["id"]

            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("💾 保存", use_container_width=True):
                    for weekday_index, recipe_id in selected_recipe_ids.items():
                        save_weekly_menu(weekday_index, recipe_id)

                    st.success("今週の献立を保存しました")
                    st.rerun()

            with col2:
                if st.button("🎲 空欄だけ埋める", use_container_width=True):
                    result = fill_empty_weekly_menu_random()

                    if result["success"]:
                        st.success(result["message"])
                        st.rerun()
                    else:
                        st.error(result["message"])

            with col3:
                if st.button("🛒 買い物メモ生成", use_container_width=True):
                    result = generate_shopping_from_weekly_menu()

                    if result["success"]:
                        st.success(result["message"])

                        if result["added_items"]:
                            with st.expander("追加した材料"):
                                for item in result["added_items"]:
                                    st.write(f"✅ {item}")

                        # st.rerun()
                    else:
                        st.error(result["message"])

    st.write("")

    show_recipe_card()

    st.write("")

    show_recipe_detail_card()