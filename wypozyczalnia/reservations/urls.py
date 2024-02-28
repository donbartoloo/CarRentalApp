from django.urls import path
from . import views

urlpatterns = [
    path('reservation', views.reservation, name='reservation'),
    path('my_reservations', views.my_reservations, name='my_reservations'),
    path("reservation/create_reservation", views.create_reservation, name='create_reservation'),
    path('employee_reservations', views.employee_reservations, name='employee_reservations'),
    path('add_reservation', views.add_reservation, name='add_reservation'),
    path('edit_reservation/<int:reservation_id>', views.edit_reservation, name='edit_reservation'),
    path('delete_reservation/<int:reservation_id>/', views.delete_reservation, name='delete_reservation'),
    path('cancel_reservation/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation')
]