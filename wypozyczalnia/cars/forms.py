from django import forms
from .models import Car, CarType

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['photo', 'brand', 'model','air_conditioning', 'car_type', 'doors_quantity', 
                  'people_quantity', 'fuel_type', 'transmission_type', 'description', 'price']
    
class CarTypeForm(forms.ModelForm):
    class Meta:
        model = CarType
        fields = ['name', 'description']