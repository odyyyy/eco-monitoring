from notifications.models import NotificationOption
from django.contrib import admin

class NotificationOptionAdmin(admin.ModelAdmin):
    pass


admin.site.register(NotificationOption, NotificationOptionAdmin)