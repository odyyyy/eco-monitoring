import collections

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Exists, OuterRef

from maps.services import get_quality_status_and_style, get_average_aqi, get_radiation_status_and_status_by_level, \
    get_radiation_level, get_weather_id_and_status_from_forecast
from notifications.models import NotificationOption

DANGEROUS_WEATHER_CODE_GROUPS = (
    2, 3, 5, 6,
)


@shared_task(bind=True, max_retries=3)
def send_notification_if_danger_level(self):
    air_quality = get_average_aqi()
    air_quality_status, _ = get_quality_status_and_style(air_quality)

    radiation_level = get_radiation_level()
    radiation_status, _ = get_radiation_status_and_status_by_level(radiation_level)

    weather_id, weather_status = get_weather_id_and_status_from_forecast()

    EcologyInfo = collections.namedtuple('EcologyInfo',['value', 'status'])
    notification_about = get_notify_about_params(EcologyInfo(weather_id, weather_status),
                                                 EcologyInfo(air_quality, air_quality_status),
                                                 EcologyInfo(radiation_level, radiation_status))
    if not notification_about.values(): return False

    users = get_user_model().objects.filter(
        Exists(NotificationOption.objects.filter(user=OuterRef('pk')))
    ).only('email')

    for user in users:
        user_notifications_subscribed = NotificationOption.objects.filter(user=user).values_list('notification_type',
                                                                                                 flat=True)
        messages_to_send = [notification_about[nt] for nt in user_notifications_subscribed if nt in notification_about]

        if messages_to_send:
            try:
                send_mail(subject='Рассылка об экологической обстановке в Москве',
                          message=f'Предупреждение!!!\n{"\n".join(messages_to_send)}',
                          from_email=settings.EMAIL_HOST_USER,
                          recipient_list=[user.email])
                # self.retry(countdown=60 * 60)
                return True
            except Exception as e:
                raise self.retry(exc=e, countdown=60)


def get_notify_about_params(weather_info, air_quality_info, radiation_info):
    """ Возвращает словарь параметров о которых нужно отправлять уведомление """
    notification_about = {}

    if weather_info.value // 100 in DANGEROUS_WEATHER_CODE_GROUPS:
        notification_about['1'] = f'Погода: В ближайшие 3 часа ожидается {weather_info.status}.'

    if air_quality_info.value > 50:
        notification_about['2'] = f'Качество воздуха: Сейчас в городе {air_quality_info.status} качество воздуха ' \
                                  f'({air_quality_info.value} AQI).'

    if radiation_info.value > 0.3:
        notification_about['3'] = f'Радиация: Зафиксирован {radiation_info.status} уровень радиации' \
                                  f' ({radiation_info.value} мкЗв/ч).'

    return notification_about
