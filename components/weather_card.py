import streamlit as st

from components.ui import show_title
from services.weather_service import get_weather


def show_weather_card():
    weather = get_weather()

    with st.container(border=True):
        show_title("weather", "🌤️", "今日の天気")

        col1, col2 = st.columns([3, 1])

        with col1:
            st.write(f"📍 {weather['location']}")
            st.write(weather["weather"])

        with col2:
            st.metric("気温", weather["temperature"])