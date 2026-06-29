import streamlit as st

from components.ui import show_title
from services.garbage_service import (
    create_garbage_rule,
    delete_garbage_rule,
    get_all_garbage_rules,
)


def show():
    show_title(
    "garbage",
    "🗑️",
    "ゴミの日",
)

    st.subheader("収集ルールを追加")

    col1, col2 = st.columns(2)

    with col1:
        garbage_name = st.text_input(
            "ごみの種類",
            placeholder="燃えるごみ",
        )

        icon = st.text_input(
            "アイコン",
            value="🗑️",
        )

    with col2:
        weekday = st.selectbox(
            "曜日",
            [
                "月曜日",
                "火曜日",
                "水曜日",
                "木曜日",
                "金曜日",
                "土曜日",
                "日曜日",
            ],
        )

        repeat = st.selectbox(
            "収集日",
            [
                "毎週",
                "第1",
                "第2",
                "第3",
                "第4",
                "第5",
                "第1・第3",
                "第2・第4",
                "第1・第2・第3・第4",
            ],
        )

    if st.button("追加", use_container_width=True):

        week_numbers = {
            "毎週": "",
            "第1": "1",
            "第2": "2",
            "第3": "3",
            "第4": "4",
            "第5": "5",
            "第1・第3": "1,3",
            "第2・第4": "2,4",
            "第1・第2・第3・第4": "1,2,3,4",
        }[repeat]

        weekday_number = {
            "月曜日": 0,
            "火曜日": 1,
            "水曜日": 2,
            "木曜日": 3,
            "金曜日": 4,
            "土曜日": 5,
            "日曜日": 6,
        }[weekday]

        result = create_garbage_rule(
            garbage_name,
            icon,
            weekday_number,
            week_numbers,
        )

        st.success(result["message"])
        st.rerun()

    st.divider()

    st.subheader("登録済み")

    weekday_names = [
        "月",
        "火",
        "水",
        "木",
        "金",
        "土",
        "日",
    ]

    rules = get_all_garbage_rules()

    if not rules:
        st.info("まだ登録されていません。")

    for rule in rules:

        rule_id, name, icon, weekday, weeks, _ = rule

        repeat_text = "毎週" if weeks == "" else f"第{weeks}"

        col1, col2 = st.columns([6, 1])

        with col1:
            st.write(
                f"{icon} **{name}**　{repeat_text} {weekday_names[weekday]}曜日"
            )

        with col2:
            if st.button(
                "🗑️",
                key=f"delete_{rule_id}",
            ):
                delete_garbage_rule(rule_id)
                st.rerun()