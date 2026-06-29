import streamlit as st

from components.ui import show_title
from services.weather_service import get_weather, weather_icon


def show_weather_card():
    weather = get_weather()

    icon = weather_icon(weather["weather"])

    with st.container(border=True):
        show_title(
            "weather",
            "🌤️",
            "今日の天気",
            right_text=f"📍 {weather['location']}",
        )

        left, right = st.columns([3, 2])

        with left:
            st.markdown(
                f"""
                <div class="weather-main">
                    <span class="weather-icon">{icon}</span>
                    <span class="weather-text">{weather["weather"]}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with right:
            st.markdown(
                f"""
                <div class="weather-right">
                    <div class="weather-temp">
                        {weather["temperature"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )