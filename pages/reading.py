import streamlit as st

from components.ui import show_title

from services.reading_service import (
    create_book,
    get_reading_books,
    update_book_progress,
)


def show():
    show_title("book", "📚", "読書記録")

    st.write("### 操作")

    mode = st.radio(
        "",
        (
            "📖 新しい本を登録",
            "📚 読書中の本を更新",
        ),
        horizontal=True,
    )

    st.divider()

    if mode == "📖 新しい本を登録":
        with st.container(border=True):
            st.write("### 基本情報")

            title = st.text_input("タイトル")
            author = st.text_input("著者")
            start_date = st.date_input("読みはじめ")

            st.divider()

            st.write("### 読書情報")

            col1, col2 = st.columns(2)

            with col1:
                total_pages = st.number_input(
                    "総ページ数",
                    min_value=0,
                    step=1,
                    key="new_total_pages",
                )

            with col2:
                current_page = st.number_input(
                    "現在ページ",
                    min_value=0,
                    step=1,
                    key="new_current_page",
                )

            if st.button("💾 登録", use_container_width=True):
                if not title:
                    st.error("タイトルを入力してください")
                    return

                if total_pages != 0 and current_page > total_pages:
                    st.error("現在ページは総ページ数以下にしてください")
                    return

                result = create_book(
                    title=title,
                    author=author,
                    start_date=str(start_date),
                    end_date="",
                    rating=None,
                    status="reading",
                    memo="",
                    total_pages=total_pages,
                    current_page=current_page,
                )

                if result["success"]:
                    st.success(result["message"])
                else:
                    st.error(result["message"])

    elif mode == "📚 読書中の本を更新":
        with st.container(border=True):
            st.write("### 読書中の本を更新")

            books = get_reading_books()

            if not books:
                st.info("読書中の本はありません。")
                return

            book_options = {
                f"{book['title']} / {book['author'] or '著者未入力'}": book
                for book in books
            }

            selected_label = st.selectbox(
                "本を選択",
                list(book_options.keys()),
            )

            selected_book = book_options[selected_label]

            st.divider()

            st.write(f"### 📖 {selected_book['title']}")

            if selected_book["author"]:
                st.caption(f"著者：{selected_book['author']}")

            if selected_book["start_date"]:
                st.caption(f"読みはじめ：{selected_book['start_date']}")

            st.divider()

            st.write("### 進捗")

            col1, col2 = st.columns(2)

            with col1:
                current_page = st.number_input(
                    "現在ページ",
                    min_value=0,
                    value=selected_book["current_page"] or 0,
                    step=1,
                    key=f"current_page_{selected_book['id']}",
                )

            with col2:
                total_pages = st.number_input(
                    "総ページ数",
                    min_value=0,
                    value=selected_book["total_pages"] or 0,
                    step=1,
                    key=f"total_pages_{selected_book['id']}",
                )

            if total_pages != 0 and current_page > total_pages:
                st.error("現在ページは総ページ数以下にしてください")
                return

            progress = 0
            if total_pages > 0:
                progress = current_page / total_pages

            st.progress(progress)
            st.caption(f"{current_page} / {total_pages} ページ")

            if st.button("💾 進捗を更新", use_container_width=True):
                result = update_book_progress(
                    selected_book["id"],
                    current_page,
                    total_pages,
                )

                if result["success"]:
                    st.success(result["message"])
                    st.rerun()
                else:
                    st.error(result["message"])

            st.divider()

            finished = st.checkbox("この本を読了した")

            if finished:
                end_date = st.date_input("読み終わり")
                rating = st.slider("評価", 1, 5, 5)
                memo = st.text_area("感想", height=150)