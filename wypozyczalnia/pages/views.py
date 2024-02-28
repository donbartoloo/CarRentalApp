from django.shortcuts import render, redirect, get_object_or_404
from .models import News
from .forms import NewsForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

def is_employee(user):
    return user.groups.filter(name='Employees').exists()

def home(request):
    user_is_employee = request.user.groups.filter(name='Employees').exists()
    news = News.objects.all().order_by('-date_created')
    return render(request, 'pages/home.html', {'news': news, 'user_is_employee': user_is_employee})

def faq(request):
    user_is_employee = request.user.groups.filter(name='Employees').exists()
    return render(request, 'pages/faq.html', {'user_is_employee': user_is_employee})

def contact(request):
    user_is_employee = request.user.groups.filter(name='Employees').exists()
    return render(request, 'pages/contact.html',{'user_is_employee': user_is_employee})


@user_passes_test(is_employee, login_url='home')
def employee_news(request):
    user_is_employee = request.user.groups.filter(name='Employees').exists()
    news = News.objects.all()
    return render(request, 'pages/employee_news.html', {'news' : news, 'user_is_employee' : user_is_employee})

@user_passes_test(is_employee, login_url='home')
def add_news(request):
    user_is_employee = request.user.groups.filter(name='Employees').exists()
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aktualność została dodana pomyślnie!')
            return redirect('employee_news')
    else:
        form = NewsForm()
    return render(request, 'pages/add_news.html', {'form': form, 'user_is_employee' : user_is_employee})

@user_passes_test(is_employee, login_url='home')
def edit_news(request, news_id):
    user_is_employee = request.user.groups.filter(name='Employees').exists()
    news = get_object_or_404(News, pk=news_id)

    if request.method == 'POST':
        form = NewsForm(request.POST, request.FiLES, instance=news)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aktualność została zedytowana pomyślnie!')
            return redirect('employee_news')
    else:
        form = NewsForm(instance=news)
    return render(request, 'pages/edit_news.html', {'form': form, 'news' : news, 'user_is_employee' : user_is_employee})

@user_passes_test(is_employee, login_url='home')
def delete_news(request, news_id):
    user_is_employee = request.user.groups.filter(name='Employees').exists()
    news = get_object_or_404(News, pk=news_id)
    
    if request.method == 'POST':
        news.delete()
        messages.success(request, 'Aktualność została usunięta pomyślnie!')
        return redirect('employee_news')

    return render(request, 'pages/delete_news.html', {'news': news, 'user_is_employee' : user_is_employee})