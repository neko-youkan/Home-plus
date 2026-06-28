import streamlit as st

from services.weather_service import get_weather
from services.menu_service import get_today_menu, save_today_menu
from services.shopping_service import get_shopping_list, save_shopping_list


def show():
    weather = get_weather()
    menu = get_today_menu()
    shopping = get_shopping_list()

    st.title("🏠 Home＋")

    st.subheader("🌤 天気")
    st.write(weather["location"])
    st.write(weather["weather"])
    st.write(weather["temperature"])

    st.divider()

    st.subheader("🍽 今日の献立")

    main = st.text_input("主菜", value=menu["main"])
    side = st.text_input("副菜", value=menu["side"])
    soup = st.text_input("汁物", value=menu["soup"])

    if st.button("💾 献立を保存"):
        result = save_today_menu(main, side, soup)

        if result["success"]:
            st.success(result["message"])
        else:
            st.error(result["message"])

    st.write("### 今日のメニュー")
    st.write(f"主菜：{main if main else '未入力'}")
    st.write(f"副菜：{side if side else '未入力'}")
    st.write(f"汁物：{soup if soup else '未入力'}")

    st.divider()

    st.subheader("🛒 買い物メモ")

    items = []

    for i, item in enumerate(shopping):
        items.append(
            st.text_input(
                f"項目 {i + 1}",
                value=item,
                key=f"shopping_{i}",
            )
        )

    if st.button("💾 買い物メモを保存"):
        result = save_shopping_list(items)

        if result["success"]:
            st.success(result["message"])
        else:
            st.error(result["message"])

    st.write("### 買い物リスト")

    if any(items):
        for item in items:
            if item:
                st.write(f"• {item}")
    else:
        st.write("未入力")