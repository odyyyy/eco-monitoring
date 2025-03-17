from django.core.exceptions import ValidationError
from django.db import models
from djeym.models import Placemark, Map, CategoryPlacemark, Status
from django.db import transaction
from django.contrib.auth import get_user_model


def validate_address(value):
    # if not re.match(r'[А-Яа-я]+,\s?(ул\.|улица)\s?[а-яА-Я]+,\s?(д\.|дом)\s?[0-9(А-Яа-я)?]+(\/[0-9]+)?,?(\s?(к\.|корпус)\s?[0-9а-яА-Я]*)?', value):
    #     raise ValidationError('Адрес должен быть в формате: Москва, ул. Тверская, д. 1В, корпус 3А')
    if 'Москва' not in value:
        raise ValidationError('Мероприятие должно проходить в Москве')


class Event(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    datetime = models.DateTimeField(verbose_name='Дата и время проведения')
    description = models.TextField(verbose_name='Описание')
    address = models.CharField(max_length=255, validators=[validate_address], verbose_name='Адрес')
    latitude = models.FloatField()
    longitude = models.FloatField()
    marker = models.OneToOneField(Placemark, null=True, on_delete=models.SET_NULL)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Создатель')

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'

    def __str__(self):
        return f'{self.title} - {self.datetime}'


def create_marker(sender, instance, created, **kwargs):
    """Сигнал, создающий маркер на карте и привязывающий его к мероприятию после создания объекта."""
    if created:
        try:
            with transaction.atomic():
                footer = (f'Адрес: <strong>{instance.address}</strong>'
                          f'<br><br> <strong>Время проведения: {instance.datetime.strftime("%d-%m-%Y %H:%M")}</strong>')

                # Создаем маркер
                marker = Placemark.objects.create(
                    ymap=Map.objects.get(slug='ekologicheskaia-karta'),
                    category=CategoryPlacemark.objects.first(),
                    header=instance.title,
                    body=instance.description,
                    footer=footer,
                    coordinates=f'[{instance.latitude},{instance.longitude}]',
                    icon_slug='garden',
                    status=Status.objects.first()
                )

                instance.marker = marker
                instance.save()
        except Exception as e:
            pass


def delete_market(sender, instance, **kwargs):
    if instance.marker:
        instance.marker.delete()

models.signals.post_save.connect(create_marker, sender=Event)
models.signals.pre_delete.connect(delete_market, sender=Event)
