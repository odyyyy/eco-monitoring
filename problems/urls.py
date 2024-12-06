from django.urls import path

from problems.views import ReportCreateView, report_problem_success_view

urlpatterns = [
    path('report/', ReportCreateView.as_view(), name='report_problem'),
    path('success/', report_problem_success_view, name='report_problem_success'),
]