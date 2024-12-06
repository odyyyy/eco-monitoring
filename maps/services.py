import re

import requests
from bs4 import BeautifulSoup
from djeym.models import Polygon

from config.settings import NINJA_API_KEY, OPENWEATHER_API_KEY


def get_air_temperature_and_weather_description():
    moscow_id = 524894

    response = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?id={moscow_id}&appid={OPENWEATHER_API_KEY}&lang=ru&units=metric')

    if response.status_code != requests.codes.ok:
        return '-', '-'

    return round(response.json()['main']['temp']), response.json()['weather'][0]['description']


def get_average_aqi():
    response = requests.get(f"https://api.api-ninjas.com/v1/airquality?city=Moscow",
                            headers={'X-Api-Key': NINJA_API_KEY})

    if response.status_code != requests.codes.ok:
        return '-'
    air_quality_index = response.json()['overall_aqi']

    return air_quality_index


def get_quality_status_and_style(aqi):
    if aqi <= 50:
        return 'Хорошее', 'color: #57D956'
    elif aqi <= 100:
        return 'Среднее', 'color: #FFD700'
    else:
        return 'Плохое', 'color: #C70000'


def get_radiation_level():
    url = 'https://www.radon.ru/online-map/?city=6'
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != requests.codes.ok:
        return '-'

    try:
        soup = BeautifulSoup(response.text, 'lxml')

        div_from_page = soup.find_all('script', attrs={'type': "text/javascript"})

        raw_radiation_values = re.findall(r"var iconText = \[[\s\S]*\];\n\t", str(div_from_page[-1]))
        matches = re.findall(r'(\d+\.\d+)', raw_radiation_values[0])

        radiations_levels = [float(match) for match in matches]
        avg_radiation_level = round(sum(radiations_levels) / len(radiations_levels), 2)

        return avg_radiation_level
    except Exception as e:
        print(e)
        return ''


def get_radiation_status_and_status_by_level(radiation_level):
    if radiation_level <= 0.3:
        return 'Допустимый', 'color: #57D956'
    elif radiation_level <= 0.5:
        return 'Повышенный', 'color: #FFD700'
    else:
        return 'Опасный', 'color: #C70000'


def change_map_territories_color(air_quality_status):
    air_quality_color = {
        'Хорошее': '#57D956',
        'Среднее': '#FFD700',
        'Плохое': '#C70000'
    }

    if Polygon.objects.first().fill_color != air_quality_color[air_quality_status]:
        Polygon.objects.update(fill_color=air_quality_color[air_quality_status])


def get_weather_id_and_status_from_forecast():
    moscow_id = 524894

    response = requests.get(
        f'https://api.openweathermap.org/data/2.5/forecast?id={moscow_id}&appid={OPENWEATHER_API_KEY}&lang=ru&units=metric&cnt=1')

    if response.status_code != requests.codes.ok:
        return 0, '-'

    return response.json()['list'][0]['weather'][0]['id'], response.json()['list'][0]['weather'][0]['description']