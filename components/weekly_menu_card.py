import streamlit as st

from components.ui import show_title
from services.weekly_menu_service import get_weekly_menu


def show_weekly_menu_card():
    with st.container(border=True):
        show_title("weekly_menu", "📅", "今週の献立")

        week = get_weekly_menu()

        weekdays = {
            0: "月",
            1: "火",
            2: "水",
            3: "木",
            4: "金",
            5: "土",
            6: "日",
        }

        week_dict = {item["weekday"]: item for item in week}

        for day in range(7):
            if day in week_dict:
                recipe = week_dict[day]
                st.write(
                    f"**{weekdays[day]}**　{recipe['name'] or '未定'}"
                )
            else:
                st.write(f"**{weekdays[day]}**　未定")