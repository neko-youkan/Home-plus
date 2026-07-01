import streamlit as st


def get_current_user_id():
    """ログイン中のユーザーIDを取得する"""

    return st.session_state.user_id


def get_current_username():
    """ログイン中のユーザー名を取得する"""

    return st.session_state.username