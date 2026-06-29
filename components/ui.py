import streamlit as st


def show_title(kind, icon, title, right_text=None):
    """カードタイトルを表示"""

    if right_text:
        html = f"""
<div class="home-title {kind}">
    <div class="home-title-row">
        <div class="home-title-left">
            <div class="home-title-main">
                <span class="icon">{icon}</span>
                <span>{title}</span>
            </div>
            <div class="home-title-line"></div>
        </div>
        <div class="home-title-right">
            {right_text}
        </div>
    </div>
</div>
"""
    else:
        html = f"""
<div class="home-title {kind}">
    <div class="home-title-left">
        <div class="home-title-main">
            <span class="icon">{icon}</span>
            <span>{title}</span>
        </div>
        <div class="home-title-line"></div>
    </div>
</div>
"""

    st.markdown(
        html,
        unsafe_allow_html=True,
    )