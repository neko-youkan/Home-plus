import streamlit as st

from components.ui import show_title
from services.menu_service import get_today_menu, save_today_menu


def show_menu_card():
    menu = get_today_menu()

    with st.container(border=True):
        show_title("menu", "🍽️", "今日の献立")

        selected = st.segmented_control(
            "項目を選ぶ",
            ["主食", "主菜", "副菜", "汁物"],
            default="主食",
        )

        value = st.text_input(
            "記入欄：",
            placeholder="例）ごはん、焼き魚、冷奴、味噌汁",
        )

        if st.button("💾 保存", use_container_width=True):
            result = save_today_menu(selected, value)

            if result["success"]:
                st.success(result["message"])
            else:
                st.error(result["message"])

        st.divider()

        show_title("menu", "🍽️", "今日のメニュー")

        st.write(f"🍚 **主食**　{menu.get('主食', '未入力')}")
        st.write(f"🐟 **主菜**　{menu.get('主菜', '未入力')}")
        st.write(f"🥗 **副菜**　{menu.get('副菜', '未入力')}")
        st.write(f"🥣 **汁物**　{menu.get('汁物', '未入力')}")