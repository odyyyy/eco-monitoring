from http.client import HTTPResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from events.forms import EventForm
from events.models import Event


class EventCreateView(LoginRequiredMixin, CreateView):
    template_name = 'create_event.html'
    form_class = EventForm
    success_url = reverse_lazy('event-create-success')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


@login_required
def create_event_success_view(request):
    return render(request, 'create_event_successful.html')


@login_required
def delete_event_view(request):
    event_id = request.POST.get('event_id')
    event = get_object_or_404(Event, id=int(event_id))

    if event.created_by == request.user:
        event.delete()
        return redirect('user-events')
    else:
        return HTTPResponse('Вы не можете удалить это мероприятие', status=403)


class UserEventsListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'user_events.html'
    context_object_name = 'events'

    def get_queryset(self):
        return Event.objects.filter(created_by=self.request.user)
