from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from problems.forms import EcoProblemReportForm


class ReportCreateView(LoginRequiredMixin, CreateView):
    template_name = 'report_problem.html'
    form_class = EcoProblemReportForm
    success_url = reverse_lazy('report_problem_success')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


def report_problem_success_view(request):
    return render(request, 'report_problem_successful.html')
