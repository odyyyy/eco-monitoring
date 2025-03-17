from django.contrib import admin
from djeym.admin import PolygonAdmin
from djeym.models import Polygon


def update_fill_color(modeladmin, request, queryset):
    new_color = '#FFF'
    queryset.update(fill_color=new_color)


update_fill_color.short_description = "Обновить цвет заливки выбранных полигонов"

admin.site.unregister(Polygon)

@admin.register(Polygon)
class PolygonAdminV(PolygonAdmin):
    actions = [update_fill_color]
