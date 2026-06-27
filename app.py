import streamlit as st

st.set_page_config(
    page_title="Home+",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Home+")

st.markdown("## 今日のダッシュボード")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📚 読書")
    st.info("現在読書中の本はありません")

    st.subheader("🛒 買い物")
    st.info("買い物リストはありません")

with col2:
    st.subheader("🍳 今日の献立")
    st.info("献立は登録されていません")

    st.subheader("🗑 ゴミの日")
    st.info("今日はゴミ収集はありません")

st.divider()

st.subheader("🌤 天気")
st.info("天気情報は準備中です。")