from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)
from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import UserLoginForm, UserRegisterForm

from django_email_verification import sendConfirm

# Create your views here.

def login_view(request):
    #currently disabled in favor of social authentication
    raise Http404
    title = "Login"
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(email=email, password=password)
        login(request, user)
        messages.success(request, "Welcome, %s, you are successfully logged in." % (user.email))
        if next: # if prompted to login, will redirect back to the intended page
            return redirect(next)
        return redirect("/")
    context = {
        "form": form,
        "title": title,
    }
    return render(request, "account_form.html", context)


def register_view(request):
    #currently disabled in favor of social authentication
    raise Http404
    title = "Register"
    next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        # login(request, new_user)
        sendConfirm(user)
        messages.success(request, "Your account is successfully registered. Welcome, %s. Please check your email account for a verification request." % (user.username))
        if next:
            return redirect(next)
        return redirect("/")

    context = {
        "form": form,
        "title": title
    }
    return render(request, "account_form.html", context)


def logout_view(request):
    logout(request)
    messages.success(request, "You are now logged out.")
    return redirect("/")


