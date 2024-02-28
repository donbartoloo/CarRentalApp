from django.contrib import admin

# Register your models here.

from .models import Car, CarType



@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("brand", "model", "car_type")
    list_filter=("car_type", "brand")

@admin.register(CarType)
class CarTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description")

