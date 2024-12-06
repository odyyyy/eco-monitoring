from django.urls import path

from events.views import EventCreateView,create_event_success_view,UserEventsListView

urlpatterns = [
    path('create/', EventCreateView.as_view(), name='create_event'),
    path('success/', create_event_success_view, name='event-create-success'),
    path('my/', UserEventsListView.as_view(), name='user-events'),
]
