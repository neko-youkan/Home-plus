import streamlit as st

from components.ui import show_title
from services.reading_service import (
    get_reading_books,
    get_finished_books,
    rating_to_stars,
)


def show_reading_card():
    reading_books = get_reading_books()
    finished_books = get_finished_books()

    with st.container(border=True):
        col1, col2 = st.columns([3, 1])

        with col1:
            show_title("book", "📚", "読書記録")

        with col2:
            st.button("＋ 読書を記録", use_container_width=True)

        st.divider()

        st.write("### 📖 読書中")

        if reading_books:
            for book in reading_books:
                st.write(f"**{book['title']}**")

                if book["author"]:
                    st.caption(f"著者：{book['author']}")

                if book["start_date"]:
                    st.caption(f"読みはじめ：{book['start_date']}")
        else:
            st.write("未入力")

        st.divider()

        st.write("### 📚 最近読了")

        if finished_books:
            for book in finished_books:
                stars = rating_to_stars(book["rating"])
                st.write(f"・{book['title']}　{stars}")
        else:
            st.write("未入力")