from operator import attrgetter
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate, logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import (
    RegistrationForm,
    AccountAuthenticationForm,
)
from .models import User
from .utils import account_activation_token

import sqlite3, os

# Create your views here.

User = get_user_model()


# Create your views here.

def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.registration_no = str(user.registration_no).upper()

            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Cast your vote for your CR.Let your voice be heard.'
            message = render_to_string('account/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            #print(message)
            return HttpResponse('Please confirm your email address to complete the registration')

        else:
            context['registration_form'] = form
    else:  # it means it is a GET request
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/register.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        print(e)
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('personal:home')
    else:
        return HttpResponse('Activation link is invalid!')


def logout_view(request):
    logout(request)
    return redirect('personal:home')


def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('personal:home')

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            registration_no = request.POST['registration_no']
            password = request.POST['password']
            print(registration_no,password)
            user = authenticate(registration_no=registration_no.upper(), password=password)

            if user:
                if not user.is_active: return HttpResponse('YOUR ACCOUNT IS NOT ACTIVE YET')
                login(request, user)
                return redirect('personal:home')
    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form
    return render(request, 'account/login.html', context)


def must_authenticate_view(request):
    return render(request, 'account/must_authenticate.html')

