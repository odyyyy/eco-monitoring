from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from notifications.forms import NotificationOptionsForm
from notifications.models import NotificationOption
from .forms import UserSignUpForm


def sign_up_view(request):
    if request.method == 'POST':
        user_form = UserSignUpForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return redirect('login')
    else:
        user_form = UserSignUpForm()
    return render(request, 'signup.html', {'form': user_form})


@login_required(login_url='login')
def profile_user_view(request):
    if request.method == 'POST' and 'notification_options' in request.POST:
        form = NotificationOptionsForm(request.POST)
        if form.is_valid():
            for notification_option in form.cleaned_data['notification_options']:
                NotificationOption.objects.update_or_create(user=request.user,
                                                            notification_type=notification_option)
            return redirect('profile')
    elif request.method == 'POST' and 'delete_notification_option' in request.POST:
        NotificationOption.objects.filter(user=request.user).delete()
        return redirect('profile')

    form = NotificationOptionsForm()
    context = {
        'form': form
    }
    return render(request, 'profile.html', context)
