import streamlit as st

from components.ui import show_title
from services.shopping_service import (
    get_shopping_list,
    save_shopping_list,
)


def show_shopping_card():
    shopping = get_shopping_list()

    with st.container(border=True):
        show_title("shopping", "🛒", "買い物メモ")

        new_item = st.text_input(
            "入力欄：",
            placeholder="例）卵",
        )

        if st.button("➕ 追加", use_container_width=True):
            if new_item:
                shopping.append(new_item)

                result = save_shopping_list(shopping)

                if result["success"]:
                    st.success(result["message"])

                st.rerun()

        st.divider()

        show_title("shopping", "🧺", "買い物リスト")

        items = [item for item in shopping if item]

        if items:
            for item in items:
                st.write(f"□ {item}")
        else:
            st.write("未入力")

        # リスト欄の高さ確保
        for _ in range(8):
            st.write("")