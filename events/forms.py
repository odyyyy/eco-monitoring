from events.models import Event
from django import forms


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'datetime', 'address', 'latitude', 'longitude']
        widgets = {
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            'datetime': forms.TextInput(attrs={
                'id': 'id_date_time',
                'placeholder': 'Выберите дату и время',
            }),
        }