from django.shortcuts import render, redirect, get_object_or_404
from datetime import date
from .models import Reservation
from cars.models import Car
from django.db.models import Q
from django.contrib import messages
from .forms import ReservationForm
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone


# Create your views here.

def is_valid_filter(param):
    return param !='' and param is not None

def is_employee(user):
    return user.groups.filter(name='Employees').exists()

def my_reservations(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    user_is_employee = request.user.groups.filter(name='Employees').exists()
    reservations = Reservation.objects.filter(user=request.user).order_by('-reservation_date')
    return render(request, 'reservations/my_reservations.html', {'reservations': reservations, 'user_is_employee' : user_is_employee})


def reservation(request):
    user_is_employee = request.user.groups.filter(name='Employees').exists()
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        finish_date = request.POST.get('finish_date')
        try:
            start_date = date.fromisoformat(start_date)
            finish_date = date.fromisoformat(finish_date)
        except ValueError:
            start_date = finish_date = None

        if start_date and finish_date:
            available_cars = get_available_cars(start_date, finish_date)
        else:
            available_cars = None
        return render(request, 'reservations/reservation.html', {'available_cars': available_cars, 'start_date': start_date.isoformat(), 'finish_date': finish_date.isoformat(), 'user_is_employee' : user_is_employee})
    else:
        available_cars = "start"
    return render(request, 'reservations/reservation.html', {'available_cars': available_cars, 'user_is_employee' : user_is_employee})


def get_available_cars(start_date, finish_date):
    reservations = Reservation.objects.filter(
        start_date__lte = finish_date,
        finish_date__gte = start_date,
        reservation_status='active'
    )
    reserved_cars = reservations.values_list('car', flat=True)
    available_cars = Car.objects.exclude(id__in=reserved_cars)
    return available_cars



def create_reservation(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    user_is_employee = request.user.groups.filter(name='Employees').exists()
    if request.method == 'GET':
        start_date_str = request.GET.get('start')
        finish_date_str = request.GET.get('end')
        car_id = request.GET.get('car')

    if request.method == 'POST':
        start_date_str = request.POST.get('start')
        finish_date_str = request.POST.get('end')
        car_id = request.POST.get('car')

    try:
        start_date = date.fromisoformat(start_date_str)
        finish_date = date.fromisoformat(finish_date_str)
    except (ValueError, TypeError):
        start_date = finish_date = None

    car = Car.objects.get(id=car_id)

    
    colliding_reservations = Reservation.objects.filter(
            car=car,
            finish_date__gt=start_date,
            start_date__lt=finish_date,
            reservation_status='active'
        )
    if colliding_reservations.exists():
            messages.error(request, 'Samochód w kolidującym terminie został zarezerwowany. Wybierz inny termin lub samochód!')
            return redirect('reservation')


    if request.method == 'POST':
        reservation = Reservation.objects.create(
            user=request.user,
            car=car,
            start_date=start_date,
            finish_date=finish_date,
            reservation_status='active'
        )
        reservation.save()
        messages.success(request, 'Rezerwacja samochodu przebiegła pomyślnie!')
        return redirect('home')
    return render(request, 'reservations/create_reservation.html', {'car': car, 'start_date': start_date, 'finish_date': finish_date, 'user_is_employee' : user_is_employee})

def cancel_reservation(request, reservation_id):
    user_is_employee = request.user.groups.filter(name='Employees').exists()
    if not request.user.is_authenticated:
        return redirect('signin')
    try:
        reservation = Reservation.objects.get(id=reservation_id)
    except Reservation.DoesNotExist:
        return render(request, 'reservations/response_template.html', {'message' : 'Rezerwacja nie istnieje!', 'user_is_employee' : user_is_employee})

    if reservation.reservation_status != Reservation.ReservationStatus.ACTIVE:
        return render(request, 'reservations/response_template.html', {'message' : 'Rezerwacja nie jest aktywna!', 'user_is_employee' : user_is_employee})

    current_time = timezone.now()
    one_day_before_start = reservation.start_date - timezone.timedelta(days=1)


    if current_time.date() >= one_day_before_start:
        return render(request, 'reservations/response_template.html', {'message' : 'Jest zbyt późno na anulowanie tej rezerwacji!', 'user_is_employee' : user_is_employee})

    reservation.reservation_status = Reservation.ReservationStatus.CANCELED
    reservation.save()
    
    return render(request, 'reservations/response_template.html', {'message' : 'Rezerwacja została anulowana!', 'user_is_employee' : user_is_employee})
 

@user_passes_test(is_employee, login_url='home')
def employee_reservations(request):
    user_is_employee = request.user.groups.filter(name='Employees').exists()
    reservations = Reservation.objects.all().order_by('-reservation_date')
    email = request.GET.get('email')
    brand_or_model = request.GET.get('brand_or_model')
    
    if is_valid_filter(email):
        reservations = reservations.filter(Q(user__email__icontains=email))
    if is_valid_filter(brand_or_model):
        reservations = reservations.filter(Q(car__brand__icontains=brand_or_model) | Q(car__model__icontains=brand_or_model))
        
    return render(request, 'reservations/employee_reservations.html', {'reservations' : reservations, 'user_is_employee' : user_is_employee})

@user_passes_test(is_employee, login_url='home')
def add_reservation(request):
    user_is_employee = request.user.groups.filter(name='Employees').exists()
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rezerwacja została dodana pomyślnie!')
            return redirect('employee_reservations')
    else:
        form = ReservationForm()
    return render(request, 'reservations/add_reservation.html', {'form': form, 'user_is_employee' : user_is_employee})

@user_passes_test(is_employee, login_url='home')
def edit_reservation(request, reservation_id):
    user_is_employee = request.user.groups.filter(name='Employees').exists()
    reservation = get_object_or_404(Reservation, pk=reservation_id)

    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rezerwacja została zedytowana pomyślnie!')
            return redirect('employee_reservations')
    else:
        form = ReservationForm(instance=reservation)
    return render(request, 'reservations/edit_reservation.html', {'form': form, 'reservation': reservation, 'user_is_employee' : user_is_employee})

@user_passes_test(is_employee, login_url='home')
def delete_reservation(request, reservation_id):
    user_is_employee = request.user.groups.filter(name='Employees').exists()
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    
    if request.method == 'POST':
        reservation.delete()
        messages.success(request, 'Rezerwacja została usunięta pomyślnie!')
        return redirect('employee_reservations')

    return render(request, 'reservations/delete_reservation.html', {'reservation': reservation, 'user_is_employee' : user_is_employee})