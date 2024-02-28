from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('faq', views.faq, name='faq'),
    path('contact', views.contact, name='contact'),
    path('employee_news', views.employee_news, name='employee_news'),
    path('add_news', views.add_news, name='add_news'),
    path('edit_news/<int:news_id>', views.edit_news, name='edit_news'),
    path('delete_news/<int:news_id>/', views.delete_news, name='delete_news'),
]
