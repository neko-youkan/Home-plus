import requests


LAT = 36.3910
LON = 140.4290
LOCATION_NAME = "水戸市石川1丁目"


WEATHER_CODE = {
    0: "晴れ",
    1: "ほぼ晴れ",
    2: "晴れ時々曇り",
    3: "曇り",
    45: "霧",
    48: "霧",
    51: "小雨",
    53: "小雨",
    55: "小雨",
    61: "雨",
    63: "雨",
    65: "強い雨",
    71: "雪",
    73: "雪",
    75: "大雪",
    80: "にわか雨",
    81: "にわか雨",
    82: "激しい雨",
    95: "雷",
}


def get_weather():
    """現在の天気情報を取得する"""

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={LAT}"
        f"&longitude={LON}"
        "&current=temperature_2m,weather_code"
    )

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        current = response.json()["current"]

        weather = WEATHER_CODE.get(
            current["weather_code"],
            "不明",
        )

        return {
            "location": LOCATION_NAME,
            "weather": weather,
            "temperature": f'{current["temperature_2m"]:.1f}℃',
        }

    except Exception as e:
        return {
            "location": LOCATION_NAME,
            "weather": f"取得失敗: {e}",
            "temperature": "--",
        }


def weather_icon(weather):
    """天気に応じたアイコンを返す"""

    weather = weather.strip()

    if "雷" in weather:
        return "⛈️"

    if "大雪" in weather:
        return "❄️"

    if "雪" in weather:
        if "曇" in weather:
            return "🌨️"
        return "❄️"

    if "激しい雨" in weather:
        return "⛈️"

    if "にわか雨" in weather:
        return "🌦️"

    if "小雨" in weather:
        return "🌦️"

    if "雨" in weather:
        if "晴" in weather:
            return "🌦️"
        return "🌧️"

    if "曇" in weather:
        if "晴" in weather:
            return "⛅"
        return "☁️"

    if "晴" in weather:
        if "ほぼ" in weather:
            return "🌤️"
        return "☀️"

    if "霧" in weather:
        return "🌫️"

    return "🌤️"