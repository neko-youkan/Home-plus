import json

import streamlit as st
from streamlit_js_eval import get_geolocation

from services.auth_service import change_password
from services.geocoding_service import search_location
from services.settings_service import get_setting, save_setting
from services.user_service import get_current_user_id, get_current_username


def load_favorite_locations():
    data = get_setting("weather_favorites", "[]")
    return json.loads(data)


def save_favorite_locations(favorites):
    save_setting(
        "weather_favorites",
        json.dumps(favorites, ensure_ascii=False),
    )


def save_weather_location(location_name, lat, lon):
    save_setting("weather_location", location_name)
    save_setting("weather_lat", lat)
    save_setting("weather_lon", lon)


def show_profile_settings():
    st.subheader("👤 プロフィール")

    current_display_name = get_setting(
        "display_name",
        get_current_username(),
    )

    display_name = st.text_input(
        "表示名",
        value=current_display_name,
        placeholder="例：ねこ羊羹",
    )

    if st.button("プロフィールを保存"):
        if not display_name.strip():
            st.warning("表示名を入力してください")
            return

        save_setting("display_name", display_name.strip())
        st.success("プロフィールを保存しました")
        st.rerun()


def show_password_settings():
    st.subheader("🔑 パスワード変更")

    with st.form("password_change_form"):
        current_password = st.text_input(
            "現在のパスワード",
            type="password",
        )

        new_password = st.text_input(
            "新しいパスワード",
            type="password",
        )

        new_password_confirm = st.text_input(
            "新しいパスワード（確認）",
            type="password",
        )

        submitted = st.form_submit_button("パスワードを変更")

        if submitted:
            if new_password != new_password_confirm:
                st.error("新しいパスワードが一致しません")
                return

            result = change_password(
                get_current_user_id(),
                current_password,
                new_password,
            )

            if result["success"]:
                st.success(result["message"])
            else:
                st.error(result["message"])


def show_account_info():
    st.subheader("ℹ️ アカウント情報")

    st.write(f"ユーザー名：**{get_current_username()}**")
    st.write(f"ユーザーID：`{get_current_user_id()}`")


def show_weather_settings():
    st.subheader("📍 天気の現在地")

    current_location = get_setting("weather_location", "未設定")
    current_lat = get_setting("weather_lat", "")
    current_lon = get_setting("weather_lon", "")

    st.write(f"現在の設定：**{current_location}**")

    st.markdown("### 住所から設定")

    address = st.text_input(
        "住所",
        value="" if current_location == "未設定" else current_location,
        placeholder="例：東京都千代田区千代田1-1",
    )

    display_name = st.text_input(
        "地点の表示名",
        value="" if current_location == "未設定" else current_location,
        placeholder="例：自宅 / 実家 / 職場",
    )

    if st.button("住所から検索して保存"):
        if not address:
            st.warning("住所を入力してください")
            return

        result = search_location(address)

        if result is None:
            st.error("場所が見つかりませんでした")
            return

        name = display_name if display_name else address

        save_weather_location(
            name,
            result["lat"],
            result["lon"],
        )

        st.success("現在地を保存しました")
        st.rerun()

    st.divider()

    st.markdown("### 📍 現在地から設定")

    location = get_geolocation()

    if location and "coords" in location:
        coords = location["coords"]

        gps_lat = coords["latitude"]
        gps_lon = coords["longitude"]

        gps_name = st.text_input(
            "現在地の表示名",
            value="現在地",
        )

        st.write(f"緯度：{gps_lat}")
        st.write(f"経度：{gps_lon}")

        if st.button("現在地を保存"):
            save_weather_location(
                gps_name,
                gps_lat,
                gps_lon,
            )

            st.success("現在地を保存しました")
            st.rerun()

    else:
        st.info("ブラウザで位置情報を許可してください。")

    st.divider()

    st.markdown("### ⭐ お気に入り地点")

    favorites = load_favorite_locations()

    if favorites:
        favorite_names = [
            item["name"]
            for item in favorites
        ]

        selected_name = st.selectbox(
            "お気に入り",
            favorite_names,
        )

        selected = next(
            item
            for item in favorites
            if item["name"] == selected_name
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("この地点に切り替え"):
                save_weather_location(
                    selected["name"],
                    selected["lat"],
                    selected["lon"],
                )

                st.success("切り替えました")
                st.rerun()

        with col2:
            if st.button("🗑️ 削除"):
                favorites.remove(selected)
                save_favorite_locations(favorites)

                st.success("削除しました")
                st.rerun()

        st.markdown("#### ✏️ 名前を変更")

        new_name = st.text_input(
            "新しい名前",
            value=selected["name"],
            key="favorite_edit_name",
        )

        if st.button("名前を変更"):
            if not new_name:
                st.warning("名前を入力してください")
                return

            if any(
                item["name"] == new_name and item != selected
                for item in favorites
            ):
                st.warning("同じ名前があります")
                return

            selected["name"] = new_name
            save_favorite_locations(favorites)

            if current_location == selected_name:
                save_weather_location(
                    new_name,
                    selected["lat"],
                    selected["lon"],
                )

            st.success("変更しました")
            st.rerun()

    else:
        st.info("お気に入りはまだありません。")

    st.markdown("#### 現在地をお気に入りに追加")

    favorite_name = st.text_input(
        "お気に入り名",
        value="" if current_location == "未設定" else current_location,
    )

    if st.button("お気に入りに追加"):
        if not current_lat or not current_lon:
            st.warning("先に現在地を設定してください")
            return

        if not favorite_name:
            st.warning("お気に入り名を入力してください")
            return

        if any(
            item["name"] == favorite_name
            for item in favorites
        ):
            st.warning("同じ名前のお気に入りがあります")
            return

        favorites.append(
            {
                "name": favorite_name,
                "lat": current_lat,
                "lon": current_lon,
            }
        )

        save_favorite_locations(favorites)

        st.success("お気に入りに追加しました")
        st.rerun()

    st.divider()

    st.markdown("### 手動で緯度・経度を設定")

    lat = st.text_input(
        "緯度",
        value=current_lat,
    )

    lon = st.text_input(
        "経度",
        value=current_lon,
    )

    location_name = st.text_input(
        "表示名",
        value="" if current_location == "未設定" else current_location,
        key="manual_location_name",
    )

    if st.button("手動で保存"):
        save_weather_location(
            location_name,
            lat,
            lon,
        )

        st.success("手動設定を保存しました")
        st.rerun()


def show():
    st.title("⚙️ 設定")

    selected = st.radio(
        "設定メニュー",
        [
            "👤 プロフィール",
            "📍 天気",
            "🔑 パスワード",
            "ℹ️ アカウント",
        ],
        horizontal=True,
    )

    st.divider()

    if selected == "👤 プロフィール":
        show_profile_settings()

    elif selected == "📍 天気":
        show_weather_settings()

    elif selected == "🔑 パスワード":
        show_password_settings()

    elif selected == "ℹ️ アカウント":
        show_account_info()