from django.contrib import admin
from .models import Reservation

# Register your models here.

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("car", "user", "start_date","finish_date","reservation_status")
    list_filter=("user", "reservation_status", "car")