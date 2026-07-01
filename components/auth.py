import streamlit as st

from services.auth_service import login_user, register_user


def show_auth_page():
    st.title("🏠 Home＋")
    st.write("ログインしてHome＋を利用しましょう。")

    login_tab, register_tab = st.tabs(
        ["🔑 ログイン", "📝 新規登録"]
    )

    with login_tab:
        with st.form("login_form"):
            username = st.text_input("ユーザー名")
            password = st.text_input(
                "パスワード",
                type="password",
            )

            submitted = st.form_submit_button(
                "ログイン",
                use_container_width=True,
            )

            if submitted:
                result = login_user(
                    username,
                    password,
                )

                if result["success"]:
                    st.session_state.user_id = result["user_id"]
                    st.session_state.username = result["username"]

                    st.success(result["message"])
                    st.rerun()

                st.error(result["message"])

    with register_tab:
        with st.form("register_form"):
            username = st.text_input(
                "ユーザー名",
                key="register_username",
            )

            password = st.text_input(
                "パスワード",
                type="password",
                key="register_password",
            )

            password2 = st.text_input(
                "パスワード（確認）",
                type="password",
                key="register_password2",
            )

            submitted = st.form_submit_button(
                "新規登録",
                use_container_width=True,
            )

            if submitted:
                if password != password2:
                    st.error("パスワードが一致しません")
                else:
                    result = register_user(
                        username,
                        password,
                    )

                    if result["success"]:
                        st.success(result["message"])
                    else:
                        st.error(result["message"])


def show_logout_button():
    st.sidebar.divider()
    st.sidebar.write(
        f"👤 {st.session_state.username}"
    )

    if st.sidebar.button(
        "ログアウト",
        use_container_width=True,
    ):
        st.session_state.clear()
        st.rerun()