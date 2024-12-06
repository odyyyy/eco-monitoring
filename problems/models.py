from django.db import models
from djeym.models import Placemark, Map, CategoryPlacemark, Status
from django.contrib.auth import get_user_model
from django.db import transaction
from events.models import validate_address


class EcoProblem(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    address = models.CharField(max_length=255, validators=[validate_address], verbose_name='Адрес')
    latitude = models.FloatField()
    longitude = models.FloatField()
    marker = models.OneToOneField(Placemark, null=True, on_delete=models.SET_NULL)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Создатель')

    class Meta:
        verbose_name = 'Сообщение о проблеме'
        verbose_name_plural = 'Сообщения о проблемах'

    def __str__(self):
        return self.title


def create_marker(sender, instance, created, **kwargs):
    """Сигнал, создающий маркер на карте и привязывающий его к мероприятию после создания объекта."""
    if created:
        try:
            with transaction.atomic():
                footer = f'Адрес: <strong>{instance.address}</strong>'

                # Создаем маркер
                marker = Placemark.objects.create(
                    ymap=Map.objects.get(slug='ekologicheskaia-karta'),
                    category=CategoryPlacemark.objects.first(),
                    header=instance.title,
                    body=instance.description,
                    footer=footer,
                    coordinates=f'[{instance.latitude},{instance.longitude}]',
                    icon_slug='waste',
                    status=Status.objects.first()
                )

                instance.marker = marker
                instance.save()
        except Exception as e:
            pass


def delete_market(sender, instance, **kwargs):
    if instance.marker:
        instance.marker.delete()


models.signals.post_save.connect(create_marker, sender=EcoProblem)
models.signals.pre_delete.connect(delete_market, sender=EcoProblem)
