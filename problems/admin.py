from django.contrib import admin

from problems.models import EcoProblem


@admin.register(EcoProblem)
class EcoProblemReportAdmin(admin.ModelAdmin):
    pass