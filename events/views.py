from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.shortcuts import render
from events.forms import EventForm
from events.models import Event
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


class EventCreateView(LoginRequiredMixin ,CreateView):
    template_name = 'create_event.html'
    form_class = EventForm
    success_url = reverse_lazy('event-create-success')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

@login_required
def create_event_success_view(request):
    return render(request, 'create_event_successful.html')

class UserEventsListView(LoginRequiredMixin ,ListView):
    model = Event
    template_name = 'user_events.html'
    context_object_name = 'events'

    def get_queryset(self):
        return Event.objects.filter(created_by=self.request.user)