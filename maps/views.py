from django.shortcuts import render
from django.views.decorators.cache import cache_page

from maps.services import get_quality_status_and_style, get_radiation_status_and_status_by_level, \
    get_air_temperature_and_weather_description, get_average_aqi, get_radiation_level


def index(request):
    return render(request, 'index.html')

def maps_view(request):
    air_temperature, weather_description = get_air_temperature_and_weather_description()

    average_aqi = get_average_aqi()
    if isinstance(average_aqi, int):
        air_quality_status, style = get_quality_status_and_style(average_aqi)
    else:
        air_quality_status, style = '-', ''

    average_radiation = get_radiation_level()
    if isinstance(average_radiation, float):
        radiation_status, radiation_style = get_radiation_status_and_status_by_level(average_radiation)
    else:
        radiation_status, radiation_style = '-', ''

    context = {
        'air_temperature': air_temperature,
        'weather_description': weather_description,

        'average_aqi': average_aqi,
        'quality_status': air_quality_status,
        'air_style': style,

        'average_radiation': average_radiation,
        'radiation_status': radiation_status,
        'radiation_style': radiation_style,
    }

    return render(request, 'maps.html', context=context)
