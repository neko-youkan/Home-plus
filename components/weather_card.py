import json

import streamlit as st

from components.ui import show_title
from services.settings_service import get_setting, save_setting
from services.weather_service import get_weather, weather_icon


def load_favorite_locations():
    data = get_setting("weather_favorites", "[]")
    return json.loads(data)


def save_weather_location(location_name, lat, lon):
    save_setting("weather_location", location_name)
    save_setting("weather_lat", lat)
    save_setting("weather_lon", lon)


def show_location_selector():
    favorites = load_favorite_locations()

    if not favorites:
        return

    current_location = get_setting("weather_location", "")

    favorite_names = [
        item["name"]
        for item in favorites
    ]

    if current_location in favorite_names:
        index = favorite_names.index(current_location)
    else:
        index = 0

    selected_name = st.selectbox(
        "天気の場所",
        favorite_names,
        index=index,
        label_visibility="collapsed",
        key="home_weather_location_selector",
    )

    selected = next(
        item
        for item in favorites
        if item["name"] == selected_name
    )

    if selected_name != current_location:
        save_weather_location(
            selected["name"],
            selected["lat"],
            selected["lon"],
        )
        st.rerun()


def show_weather_card():
    with st.container(border=True):
        show_location_selector()

        weather = get_weather()
        icon = weather_icon(weather["weather"])

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