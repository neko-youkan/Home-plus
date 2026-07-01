import streamlit as st

from services.admin_service import (
    delete_user,
    get_app_stats,
    get_user_stats,
    get_users,
    is_admin_user,
    remove_admin,
    set_admin,
)
from services.announcement_service import (
    create_announcement,
    delete_announcement,
    get_all_announcements,
    update_announcement_pinned,
    update_announcement_status,
)
from services.user_service import get_current_user_id


def show_stats():
    """アプリ全体の統計を表示"""

    stats = get_app_stats()

    st.subheader("📊 アプリ統計")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("登録ユーザー", stats["users"])
        st.metric("管理者", stats["admins"])

    with col2:
        st.metric("今日のログイン", stats["today_logins"])
        st.metric("総ログイン", stats["total_logins"])

    with col3:
        st.metric("レシピ", stats["recipes"])
        st.metric("読書記録", stats["books"])


def show_user_card(user, current_user_id):
    """ユーザーカードを表示"""

    user_id = user["id"]
    username = user["username"]
    is_admin = user["is_admin"] == 1

    role = "👑 管理者" if is_admin else "👤 一般"
    user_stats = get_user_stats(user_id)

    with st.container(border=True):
        col1, col2 = st.columns([4, 2])

        with col1:
            st.write(f"### {username}")
            st.write(role)
            st.caption(f"ID：{user_id}")
            st.caption(f"登録日：{user['created_at']}")
            st.caption(f"最終ログイン：{user_stats['last_login']}")
            st.caption(f"ログイン回数：{user_stats['login_count']}回")

            with st.expander("📊 利用状況"):
                st.write(f"🍽 レシピ：{user_stats['recipes']}件")
                st.write(f"🛒 買い物メモ：{user_stats['shopping_items']}件")
                st.write(f"📚 読書記録：{user_stats['books']}件")
                st.write(f"🗑 ゴミの日：{user_stats['garbage_rules']}件")
                st.write(f"📅 週間献立：{user_stats['weekly_menu']}件")
                st.write(f"🍚 今日の献立：{user_stats['menu']}件")

        with col2:
            if user_id == current_user_id:
                st.info("自分のアカウント")
                return

            if is_admin:
                if st.button(
                    "👤 一般にする",
                    key=f"remove_admin_{user_id}",
                    use_container_width=True,
                ):
                    result = remove_admin(user_id)

                    if result["success"]:
                        st.success(result["message"])
                        st.rerun()
                    else:
                        st.error(result["message"])
            else:
                if st.button(
                    "👑 管理者にする",
                    key=f"set_admin_{user_id}",
                    use_container_width=True,
                ):
                    result = set_admin(user_id)

                    if result["success"]:
                        st.success(result["message"])
                        st.rerun()
                    else:
                        st.error(result["message"])

            st.divider()

            confirm_delete = st.checkbox(
                "削除を確認",
                key=f"confirm_delete_{user_id}",
            )

            if st.button(
                "🗑 ユーザー削除",
                key=f"delete_user_{user_id}",
                use_container_width=True,
                disabled=not confirm_delete,
            ):
                result = delete_user(user_id)

                if result["success"]:
                    st.success(result["message"])
                    st.rerun()
                else:
                    st.error(result["message"])


def show_user_management():
    """ユーザー管理を表示"""

    st.subheader("👥 ユーザー管理")

    keyword = st.text_input(
        "🔍 ユーザー検索",
        placeholder="ユーザー名で検索",
    )

    users = get_users(keyword)

    if not users:
        st.info("該当するユーザーがいません")
        return

    st.caption("管理者を上に表示しています。")

    current_user_id = get_current_user_id()

    for user in users:
        show_user_card(user, current_user_id)


def show_announcement_management():
    """お知らせ管理"""

    st.subheader("📢 お知らせ管理")

    with st.form("announcement_form"):
        title = st.text_input("タイトル")

        message = st.text_area(
            "本文",
            height=150,
        )

        pinned = st.checkbox("📌 固定表示")

        submitted = st.form_submit_button("📢 お知らせを投稿")

        if submitted:
            result = create_announcement(
                title,
                message,
                get_current_user_id(),
                int(pinned),
            )

            if result["success"]:
                st.success(result["message"])
                st.rerun()
            else:
                st.error(result["message"])

    st.divider()

    st.subheader("📋 投稿済みのお知らせ")

    announcements = get_all_announcements()

    if not announcements:
        st.info("まだお知らせはありません。")
        return

    for notice in announcements:
        with st.container(border=True):
            status = "公開中" if notice["is_active"] else "非公開"
            pinned = "📌 固定" if notice["is_pinned"] else ""

            st.write(f"### {notice['title']}")
            st.caption(f"{status} {pinned} / 投稿日：{notice['created_at']}")
            st.write(notice["message"])

            col1, col2, col3 = st.columns(3)

            with col1:
                active = notice["is_active"] == 1

                if st.button(
                    "非公開にする" if active else "公開する",
                    key=f"active_{notice['id']}",
                    use_container_width=True,
                ):
                    update_announcement_status(
                        notice["id"],
                        0 if active else 1,
                    )
                    st.rerun()

            with col2:
                is_pinned = notice["is_pinned"] == 1

                if st.button(
                    "📌 固定解除" if is_pinned else "📌 固定",
                    key=f"pin_{notice['id']}",
                    use_container_width=True,
                ):
                    update_announcement_pinned(
                        notice["id"],
                        0 if is_pinned else 1,
                    )
                    st.rerun()

            with col3:
                if st.button(
                    "🗑 削除",
                    key=f"delete_notice_{notice['id']}",
                    use_container_width=True,
                ):
                    delete_announcement(notice["id"])
                    st.rerun()


def show():
    st.title("🛠️ 管理者画面")

    current_user_id = get_current_user_id()

    if not is_admin_user(current_user_id):
        st.error("このページを表示する権限がありません")
        return

    tab_dashboard, tab_users, tab_notice = st.tabs(
        [
            "📊 ダッシュボード",
            "👥 ユーザー",
            "📢 お知らせ",
        ]
    )

    with tab_dashboard:
        show_stats()

    with tab_users:
        show_user_management()

    with tab_notice:
        show_announcement_management()