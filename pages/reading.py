import streamlit as st

from components.ui import show_title
from services.reading_service import create_book


def show():
    show_title("book", "📚", "読書記録")

    with st.container(border=True):
        st.write("### 基本情報")

        title = st.text_input("タイトル")
        author = st.text_input("著者")

        col1, col2 = st.columns([1, 2])

        with col1:
            date_type = st.radio(
                "日付",
                ["読みはじめ", "読みおわり"],
                horizontal=True,
            )

        with col2:
            reading_date = st.date_input("日付を選択")

        st.divider()

        st.write("### 読書情報")

        col3, col4 = st.columns(2)

        with col3:
            total_pages = st.number_input(
                "総ページ数",
                min_value=0,
                step=1,
            )

        with col4:
            current_page = st.number_input(
                "現在ページ",
                min_value=0,
                step=1,
            )

        rating = st.slider("評価", 1, 5, 3)

        memo = st.text_area("感想", height=180)

        if st.button("💾 保存", use_container_width=True):
            if not title:
                st.error("タイトルを入力してください")
                return

            if current_page > total_pages and total_pages != 0:
                st.error("現在ページは総ページ数以下にしてください")
                return

            start_date = str(reading_date) if date_type == "読みはじめ" else ""
            end_date = str(reading_date) if date_type == "読みおわり" else ""

            status = "reading" if date_type == "読みはじめ" else "finished"

            result = create_book(
                title=title,
                author=author,
                start_date=start_date,
                end_date=end_date,
                rating=rating,
                status=status,
                memo=memo,
                total_pages=total_pages,
                current_page=current_page,
            )

            if result["success"]:
                st.success(result["message"])
            else:
                st.error(result["message"])