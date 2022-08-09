from django.http import Http404
from django.shortcuts import render, redirect
from .forms import CustomAuthenticationForm, CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404


def loginpage_view(request):
    return render(request, 'user/login.html',
                  {'form': CustomAuthenticationForm()})


def registration_view(request):
    if request.method == 'GET':
        return render(request, 'user/registration.html',
                      {'form': CustomUserCreationForm()})
    else:
        form = CustomUserCreationForm(request.POST, auto_id='cre_f_%s')
        if form.is_valid():
            form.save()
            return redirect('user:after_registration_page')
        else:
            return render(request, 'user/registration.html',
                          {'form': CustomUserCreationForm(
                              request.POST,
                              auto_id='cre_f_%s'),
                           'errors': 'sometrubles'})


def thanks_view(request):
    return render(request, 'user/thanks.html')


def activation_view(request, hash1, hash2):
    if request.method == 'GET':
        user = get_object_or_404(
            get_user_model(),
            activation_link1=hash1,
            activation_link2=hash2)
        if user.is_active:
            raise Http404
        else:
            user.is_active = True
            user.save()

    return render(request, 'user/activation.html', {
        'messege': 'Account has been activated'
    })
