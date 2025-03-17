from django import forms

NOTIFICATION_TYPE_CHOICES = (
    ("1", "Погода"),
    ("2", "Качество воздуха"),
    ("3", "Уровень радиации"),
)


class NotificationOptionsForm(forms.Form):
    notification_options = forms.MultipleChoiceField(
        choices=NOTIFICATION_TYPE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label="Выберите о чем вы хотите получать уведомления",
    )