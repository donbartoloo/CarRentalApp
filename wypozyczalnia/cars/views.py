from django.shortcuts import render, redirect, get_object_or_404
from .models import Car, CarType
from django.db.models import Q
from .forms import CarForm, CarTypeForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

# Create your views here.

def is_valid_filter(param):
    return param !='' and param is not None

def is_employee(user):
    return user.groups.filter(name='Employees').exists()

def cars(request):
    user_is_employee = request.user.groups.filter(name='Employees').exists()
    cars = Car.objects.all()
    car_types = CarType.objects.all()
    brand_or_model = request.GET.get('brand_or_model')
    car_type = request.GET.get('car_type')
    fuel_type = request.GET.get('fuel_type')
    transmission_type = request.GET.get('transmission_type')
    doors_quantity = request.GET.get('doors_quantity')
    air_conditioning = request.GET.get('air_conditioning')
    
    if is_valid_filter(brand_or_model):
        cars = cars.filter(Q(brand__icontains=brand_or_model) | Q(model__icontains=brand_or_model))
    
    if is_valid_filter(car_type) and car_type !="Wybierz...":
        cars = cars.filter(car_type__name=car_type)
    
    if is_valid_filter(fuel_type) and fuel_type !="Wybierz...":
        cars = cars.filter(fuel_type=fuel_type)
        
    if is_valid_filter(transmission_type) and transmission_type !="Wybierz...":
        cars = cars.filter(transmission_type=transmission_type)
    
    if is_valid_filter(doors_quantity) and doors_quantity !="Wybierz...":
        cars = cars.filter(doors_quantity=doors_quantity)
    
        
    if is_valid_filter(air_conditioning) and air_conditioning !="Wybierz...":
        cars = cars.filter(air_conditioning=air_conditioning)
 
 
        
    
    return render(request, 'cars/cars.html', {'cars': cars, 'car_types' : car_types, 'user_is_employee' : user_is_employee})



def car_details(request):
    user_is_employee = request.user.groups.filter(name='Employees').exists()
    car_id = request.GET.get('car')
    car = Car.objects.get(id=car_id)
    return render(request, 'cars/car_details.html', {'car' : car, 'user_is_employee' : user_is_employee} )

@user_passes_test(is_employee, login_url='home')
def employee_cars(request):
    user_is_employee = request.user.groups.filter(name='Employees').exists()
    cars = Car.objects.all()
    car_types = CarType.objects.all()
    brand_or_model = request.GET.get('brand_or_model')
    car_type = request.GET.get('car_type')
    fuel_type = request.GET.get('fuel_type')
    transmission_type = request.GET.get('transmission_type')
    doors_quantity = request.GET.get('doors_quantity')
    air_conditioning = request.GET.get('air_conditioning')
    
    if is_valid_filter(brand_or_model):
        cars = cars.filter(Q(brand__icontains=brand_or_model) | Q(model__icontains=brand_or_model))
    
    if is_valid_filter(car_type) and car_type !="Wybierz...":
        cars = cars.filter(car_type__name=car_type)
    
    if is_valid_filter(fuel_type) and fuel_type !="Wybierz...":
        cars = cars.filter(fuel_type=fuel_type)
        
    if is_valid_filter(transmission_type) and transmission_type !="Wybierz...":
        cars = cars.filter(transmission_type=transmission_type)
    
    if is_valid_filter(doors_quantity) and doors_quantity !="Wybierz...":
        cars = cars.filter(doors_quantity=doors_quantity)
    
        
    if is_valid_filter(air_conditioning) and air_conditioning !="Wybierz...":
        cars = cars.filter(air_conditioning=air_conditioning)
    return render(request, 'cars/employee_cars.html', {'cars' : cars, 'car_types' : car_types, 'user_is_employee' : user_is_employee})

@user_passes_test(is_employee, login_url='home')
def add_car(request):
    user_is_employee = request.user.groups.filter(name='Employees').exists()
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Samochód został dodany pomyślnie!')
            return redirect('employee_cars')
    else:
        form = CarForm()
    return render(request, 'cars/add_car.html', {'form': form, 'user_is_employee' : user_is_employee})

@user_passes_test(is_employee, login_url='home')
def edit_car(request, car_id):
    user_is_employee = request.user.groups.filter(name='Employees').exists()
    car = get_object_or_404(Car, pk=car_id)

    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            messages.success(request, 'Samochód został zedytowany pomyślnie!')
            return redirect('employee_cars')
    else:
        form = CarForm(instance=car)
    return render(request, 'cars/edit_car.html', {'form': form, 'car': car, 'user_is_employee' : user_is_employee})

@user_passes_test(is_employee, login_url='home')
def delete_car(request, car_id):
    user_is_employee = request.user.groups.filter(name='Employees').exists()
    car = get_object_or_404(Car, pk=car_id)
    
    if request.method == 'POST':
        car.delete()
        messages.success(request, 'Samochód został usunięty pomyślnie!')
        return redirect('employee_cars')

    return render(request, 'cars/delete_car.html', {'car': car, 'user_is_employee' : user_is_employee})

@user_passes_test(is_employee, login_url='home')
def employee_car_types(request):
    user_is_employee = request.user.groups.filter(name='Employees').exists()
    car_types = CarType.objects.all()
    return render(request, 'cars/employee_car_types.html', {'car_types' : car_types, 'user_is_employee' : user_is_employee})

@user_passes_test(is_employee, login_url='home')
def add_car_type(request):
    user_is_employee = request.user.groups.filter(name='Employees').exists()
    if request.method == 'POST':
        form = CarTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Typ samochodu został dodany pomyślnie!')
            return redirect('employee_car_types')
    else:
        form = CarTypeForm()
    return render(request, 'cars/add_car_type.html', {'form': form, 'user_is_employee' : user_is_employee})

@user_passes_test(is_employee, login_url='home')
def edit_car_type(request, car_type_id):
    user_is_employee = request.user.groups.filter(name='Employees').exists()
    car_type = get_object_or_404(CarType, pk=car_type_id)

    if request.method == 'POST':
        form = CarTypeForm(request.POST, instance=car_type)
        if form.is_valid():
            form.save()
            messages.success(request, 'Typ samochodu został zedytowany pomyślnie!')
            return redirect('employee_car_types')
    else:
        form = CarTypeForm(instance=car_type)
    return render(request, 'cars/edit_car_type.html', {'form': form, 'car_type': car_type, 'user_is_employee' : user_is_employee})

@user_passes_test(is_employee, login_url='home')
def delete_car_type(request, car_type_id):
    user_is_employee = request.user.groups.filter(name='Employees').exists()
    car_type = get_object_or_404(CarType, pk=car_type_id)
    
    if request.method == 'POST':
        car_type.delete()
        messages.success(request, 'Typ samochodu został usunięty pomyślnie!')
        return redirect('employee_car_types')

    return render(request, 'cars/delete_car_type.html', {'car_type': car_type, 'user_is_employee' : user_is_employee})
    