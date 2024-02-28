from hashlib import sha256
import django.core.mail
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from authentication.models import CustomUser
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.contrib.auth.decorators import user_passes_test
from reservations.models import Reservation
from cars.models import Car, CarType
from pages.models import News
from django.db import transaction

# Create your views here.


def create_user_activation_token(user):
    string = f"{user.email};wypozyczalnia2024"
    encoded = string.encode()
    return sha256(encoded).hexdigest()


def send_email_confirmation_mail(request, user):
    confirm_url = request.build_absolute_uri(reverse("activate", kwargs=dict(userid=user.pk, token=create_user_activation_token(user))))
    print(confirm_url)
    message = f"<html><body><h1>Witaj, {user.first_name}!</h1>\nAktywuj swoje konto klikając w link.<br><a href='{confirm_url}'>{confirm_url}</a></body></html>"
    django.core.mail.send_mail(
        "Potwierdź swój adres email", message, from_email=None, recipient_list=[user.email], html_message=message
    )


@transaction.atomic
def activate(request, userid, token):
    user = get_object_or_404(CustomUser, pk=userid)
    if token == create_user_activation_token(user):
        user.is_active = True
        user.save()
        messages.success(request, 'Aktywacja konta przebiegła pomyślnie. Możesz się teraz zalogować.')
        return redirect('home')
    else:
        raise forms.ValidationError("Nieprawidłowy token.")


@transaction.atomic
def signup(request):
    if request.method == 'POST': 
        email = request.POST.get('email')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        postal_code=request.POST.get('postal_code')
        adress = request.POST.get('adress')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        
        if CustomUser.objects.filter(email=email):
            messages.error(request, "Ten adres e-mail jest już zajęty.")
            raise forms.ValidationError("Ten adres e-mail jest już zajęty.")

            
        if password1 != password2:
            messages.error(request, "Hasła nie zgadzają się ze sobą.")
            raise forms.ValidationError("Hasła nie zgadzają się ze sobą.")
        
        if len(password1) < 8:
            messages.error(request, "Twoje hasło musi mieć minimum 8 znaków.")
            raise forms.ValidationError("Twoje hasło musi mieć minimum 8 znaków.")

        user = CustomUser.objects.create_user(email, password1)
        user.first_name = firstname
        user.last_name = lastname
        user.phone = phone
        user.city = city
        user.adress = adress
        user.postal_code = postal_code
        user.is_active = False
        user.save()
        send_email_confirmation_mail(request, user)
        messages.success(request, "Rejestracja przebiegła pomyślnie! Na twój adres e-mail został wysłany link do aktywacji twojego konta.")
        return redirect('home') 
        
    return render(request, 'authentication/signup.html')

def is_employee(user):
    return user.groups.filter(name='Employees').exists()

@user_passes_test(is_employee)
def dashboard(request):
    user_is_employee = request.user.groups.filter(name='Employees').exists()
    cars_count = Car.objects.count()
    reservations_count = Reservation.objects.count()
    news_count = News.objects.count()
    car_type_count = CarType.objects.count()
    return render(request, 'authentication/dashboard.html', {'cars_count': cars_count, 'reservations_count' : reservations_count, 'news_count' : news_count, 'car_type_count': car_type_count, 'user_is_employee' : user_is_employee})


def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        user = authenticate(email=email, password = password1)
        if user is not None:
            login(request, user)
            if user.groups.filter(name='Employees').exists():
                return redirect('dashboard')
            firstname = user.first_name
            return redirect('home')
        else:
            messages.error(request, "Niepoprawne dane logowania!")
            return redirect('signin')
    return render(request, 'authentication/signin.html')

def signout(request):
    logout(request)
    messages.success(request, "Pomyślnie wylogowano cię z konta!")
    return redirect('home')
        
def profile(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    return render(request, 'authentication/profile.html') 

