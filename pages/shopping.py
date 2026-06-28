import streamlit as st

from components.ui import show_title
from services.shopping_service import (
    add_shopping_item,
    delete_shopping_item,
    get_shopping_list,
    update_shopping_status,
)


def show():
    """買い物メモ画面"""

    show_title("shopping", "🛒", "買い物メモ")

    st.subheader("買うものを追加")

    with st.form("shopping_form"):
        item_name = st.text_input("商品名")

        submitted = st.form_submit_button("追加する")

        if submitted:
            if item_name.strip():
                add_shopping_item(item_name.strip())
                st.success("買い物メモを追加しました")
                st.rerun()
            else:
                st.warning("商品名を入力してください")

    st.divider()

    st.subheader("買い物メモ一覧")

    items = get_shopping_list()

    if not items:
        st.info("買い物メモはまだありません")

    else:
        for item in items:
            col1, col2 = st.columns([9, 1])

            with col1:
                checked = st.checkbox(
                    item["item_name"],
                    value=bool(item["is_checked"]),
                    key=f"shopping_{item['id']}",
                )

                if checked != bool(item["is_checked"]):
                    update_shopping_status(
                        item["id"],
                        int(checked),
                    )
                    st.rerun()

            with col2:
                if st.button("🗑️", key=f"delete_{item['id']}"):
                    delete_shopping_item(item["id"])
                    st.rerun()