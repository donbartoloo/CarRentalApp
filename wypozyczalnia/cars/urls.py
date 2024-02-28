from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('cars', views.cars, name='cars'),
    path('car_details', views.car_details, name='car_details'),
    path('employee_cars', views.employee_cars, name='employee_cars'),
    path('add_car', views.add_car, name='add_car'),
    path('edit_car/<int:car_id>', views.edit_car, name='edit_car'),
    path('delete_car/<int:car_id>/', views.delete_car, name='delete_car'),
    path('employee_car_types', views.employee_car_types, name='employee_car_types'),
    path('add_car_type', views.add_car_type, name='add_car_type'),
    path('edit_car_type/<int:car_type_id>', views.edit_car_type, name='edit_car_type'),
    path('delete_car_type/<int:car_type_id>/', views.delete_car_type, name='delete_car_type'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
