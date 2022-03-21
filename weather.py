"""
Погода в игре
Интеграция с Яндекс.Погодой
"""
import requests


def weather():
    """
    В зависимости от реальной погоды в игре появляется
    или исчезает дождь
    :return:
    """
    # appid = "78832b61-868c-48a9-8f1b-f4911d715bc0"
    try:

        ya_key = "78832b61-868c-48a9-8f1b-f4911d715bc0"

        url = "https://api.weather.yandex.ru/v1/forecast"

        payload = {'lat': '55.75396', 'lon': '37.620393', 'extra': 'true'}

        r = requests.get(url, headers={'X-Yandex-API-Key': ya_key}, params=payload)
        data = r.json()
        feel = data['fact']['condition']
        # print(data['fact']['temp'], feel)
        rain = False
        if len(feel) >= 14:
            rain = True
        # print(rain)
        return rain

    except Exception as e:
        print("Exception (weather):", e)
        return False


if __name__ == '__main__':
    weather()
