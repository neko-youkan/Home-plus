import streamlit as st

from components.ui import show_title
from services.menu_service import (
    get_previous_menu_date,
    get_today_menu,
    save_today_menu,
)
from services.recipe_service import get_random_recipe


@st.dialog("🎲 今日のおすすめ")
def show_random_recipe_dialog():
    recipe = get_random_recipe()

    if recipe is None:
        st.info("献立テンプレートがまだありません")
        return

    st.write(f"### {recipe['name']}")

    st.write(f"🍚 **主食**　{recipe['staple'] or '未入力'}")
    st.write(f"🐟 **主菜**　{recipe['main_dish'] or '未入力'}")
    st.write(f"🥗 **副菜**　{recipe['side_dish'] or '未入力'}")
    st.write(f"🥣 **汁物**　{recipe['soup'] or '未入力'}")

    st.divider()

    if st.button("🔄 もう一度選ぶ", use_container_width=True):
        st.rerun()

    if st.button("✅ 今日の献立に採用", use_container_width=True):
        save_today_menu(
            recipe["staple"],
            recipe["main_dish"],
            recipe["side_dish"],
            recipe["soup"],
        )

        st.success(f"「{recipe['name']}」を今日の献立に設定しました")
        st.rerun()


def show_menu_card():
    menu = get_today_menu()

    menu_items = ["主食", "主菜", "副菜", "汁物"]

    key_map = {
        "主食": "staple",
        "主菜": "main_dish",
        "副菜": "side_dish",
        "汁物": "soup",
    }

    if "selected_menu" not in st.session_state:
        st.session_state.selected_menu = "主食"

    with st.container(border=True):
        show_title("meal", "🍽️", "今日の献立")

        selected = st.segmented_control(
            "項目を選ぶ",
            menu_items,
            default=st.session_state.selected_menu,
        )

        value = st.text_input(
            "記入欄：",
            value=menu[key_map[selected]],
            placeholder="例）ごはん、焼き魚、冷奴、味噌汁",
        )

        if st.button("💾 保存", use_container_width=True):
            updated_menu = menu.copy()
            updated_menu[key_map[selected]] = value.strip()

            result = save_today_menu(
                updated_menu["staple"],
                updated_menu["main_dish"],
                updated_menu["side_dish"],
                updated_menu["soup"],
            )

            if result["success"]:
                current_index = menu_items.index(selected)
                next_index = (current_index + 1) % len(menu_items)
                st.session_state.selected_menu = menu_items[next_index]

                st.success(result["message"])
                st.rerun()
            else:
                st.error(result["message"])

        if st.button("🎲 ランダム献立", use_container_width=True):
            show_random_recipe_dialog()

        st.divider()

        show_title("meal", "🍱", "今日のメニュー")

        items = [
            ("🍚", "主食", "staple"),
            ("🐟", "主菜", "main_dish"),
            ("🥗", "副菜", "side_dish"),
            ("🥣", "汁物", "soup"),
        ]

        for icon, label, key in items:
            value = menu[key]

            st.write(f"{icon} **{label}**　{value or '未入力'}")

            if value:
                previous = get_previous_menu_date(key, value)

                if previous:
                    st.caption(
                        f"前回：{previous['date']}（{previous['days']}日前）"
                    )