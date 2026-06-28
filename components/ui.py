import streamlit as st

COLORS = {
    "weather": "#64B5F6",
    "garbage": "#C97A40",
    "menu": "#8BC34A",
    "shopping": "#FFA726",
    "book": "#9575CD",
}


def show_title(kind, icon, title):
    color = COLORS.get(kind, "#FFFFFF")

    st.markdown(
        f"""
        <h2 style="margin-bottom:0.8rem;font-weight:700;">
            {icon}
            <span style="color:{color};">
                {title}
            </span>
        </h2>
        """,
        unsafe_allow_html=True,
    )