import streamlit as st

from components.ui import show_title
from services.reading_service import (
    get_current_reading_book,
    get_finished_books,
    progress_percent,
    rating_to_stars,
)


def show_reading_card():
    book = get_current_reading_book()
    finished_books = get_finished_books()

    with st.container(border=True):
        show_title("book", "📚", "読書記録")

        st.divider()

        st.write("### 📖 読書中")

        if book:
            st.write(f"**{book['title']}**")

            if book["author"]:
                st.caption(book["author"])

            percent = progress_percent(
                book["current_page"] or 0,
                book["total_pages"] or 0,
            )

            st.progress(percent / 100)

            st.caption(
                f"{book['current_page'] or 0} / "
                f"{book['total_pages'] or 0} ページ ・ {percent}%"
            )

        else:
            st.caption("読書中の本はありません。")

        st.divider()

        st.write("### 📚 最近読了")

        if finished_books:
            for finished in finished_books:
                stars = rating_to_stars(finished["rating"])

                st.write(f"**{finished['title']}**　{stars}")

                if finished["author"]:
                    st.caption(finished["author"])

        else:
            st.caption("まだ読了した本はありません。")