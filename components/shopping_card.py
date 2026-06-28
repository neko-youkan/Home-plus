import streamlit as st

from components.ui import show_title
from services.shopping_service import (
    get_unchecked_shopping_list,
    add_shopping_item,
    update_shopping_status,
)

def show_shopping_card():
    shopping = get_unchecked_shopping_list()

    with st.container(border=True):
        show_title("shopping", "🛒", "買い物メモ")

        new_item = st.text_input(
            "入力欄：",
            placeholder="例）卵",
        )

        if st.button("➕ 追加", use_container_width=True):
            if new_item:
                add_shopping_item(new_item)

                st.success("買い物メモを追加しました")

                st.rerun()

        st.divider()

        show_title("shopping", "🧺", "買い物リスト")

        items = shopping

        if items:
            for item in items:
                checked = st.checkbox(
                    item["item_name"],
                    value=bool(item["is_checked"]),
                    key=f"home_shopping_{item['id']}",
                )

                if checked != bool(item["is_checked"]):
                    update_shopping_status(item["id"], int(checked))
                    st.rerun()
        else:
            st.write("未入力")

        # リスト欄の高さ確保
        for _ in range(8):
            st.write("")