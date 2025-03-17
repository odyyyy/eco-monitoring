from django.http import JsonResponse
from django.shortcuts import render

from maps.services import get_quality_status_and_style, get_radiation_status_and_status_by_level, \
    get_air_temperature_and_weather_description, get_average_aqi, get_radiation_level
from django.views.decorators.cache import cache_page

def index(request):
    return render(request, 'index.html')


def maps_view(request):
    return render(request, 'maps.html')

@cache_page(60 * 15, cache='pages_cache')
def get_radiation_view(request):
    average_radiation = get_radiation_level()
    if isinstance(average_radiation, float):
        radiation_status, radiation_style = get_radiation_status_and_status_by_level(average_radiation)
    else:
        radiation_status, radiation_style = '-', ''

    return JsonResponse({
        'average_radiation': average_radiation,
        'radiation_status': radiation_status,
        'radiation_style': radiation_style,
    })

@cache_page(60 * 15, cache='pages_cache')
def get_aqi_view(request):
    average_aqi = get_average_aqi()
    if isinstance(average_aqi, int):
        air_quality_status, style = get_quality_status_and_style(average_aqi)
    else:
        air_quality_status, style = '-', ''

    return JsonResponse({

        'average_aqi': average_aqi,
        'quality_status': air_quality_status,
        'air_style': style,
    })

@cache_page(60 * 15, cache='pages_cache')
def get_weather_view(request):
    air_temperature, weather_description = get_air_temperature_and_weather_description()

    return JsonResponse(
        {
            'air_temperature': air_temperature,
            'weather_description': weather_description,
        }
    )
