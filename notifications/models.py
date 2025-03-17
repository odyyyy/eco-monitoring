from django.db import models
from django.contrib.auth import get_user_model

from notifications.forms import NOTIFICATION_TYPE_CHOICES


class NotificationOption(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='notification_options')
    notification_type = models.CharField(max_length=1, choices=NOTIFICATION_TYPE_CHOICES)

    class Meta:
        unique_together = ('user', 'notification_type')
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'

    def __str__(self):
        return f"{self.user.username} - {self.get_notification_type_display()}"