from django.db import models

class CarType(models.Model):
    name = models.TextField(default='Kategoria')
    description = models.TextField(default='Opis')
    
    def __str__(self):
        return self.name

class Car(models.Model):
    
    def __str__(self):
        return f'{self.brand} {self.model}'
     
    
    photo = models.ImageField(default='cars_default.jpg', upload_to='car_images/')
    brand = models.TextField(default='Marka')
    model = models.TextField(default='Model')
    
    class AirConditioning(models.TextChoices):
        YES ='YES', 'Tak'
        NO = 'NO', 'Nie'
    air_conditioning = models.CharField(max_length=3, choices=AirConditioning.choices, default=AirConditioning.YES)
    
    car_type = models.ForeignKey(CarType, null=False, blank=True, on_delete=models.CASCADE)

    class DoorsQuantity(models.TextChoices):
        TWO_DOOR = 'TWO', '2'
        THREE_DOOR = 'THR', '3'
        FOUR_DOOR = 'FOU', '4'
        FIVE_DOOR = 'FIV', '5'
    doors_quantity = models.CharField(max_length=3, choices=DoorsQuantity.choices, default=DoorsQuantity.FIVE_DOOR)
    people_quantity = models.IntegerField()
    
    class FuelType(models.TextChoices):
        GASOLINE ='GAS', 'Benzyna'
        DIESEL = 'DIE', 'Diesel'
        LPG = 'LPG', 'LPG'
        ELECTRIC = 'ELE', 'Elektryczny'
    fuel_type = models.CharField(max_length=3, choices=FuelType.choices, default=FuelType.GASOLINE)
  
    class TransmissionType(models.TextChoices):
        AUTOMATIC = 'A', 'Automatyczna'
        MANUAL = 'M', 'Manualna'
    transmission_type = models.CharField(max_length=3, choices=TransmissionType.choices, default=TransmissionType.MANUAL)
    
    description = models.TextField(default='Description')
    price = models.DecimalField(decimal_places=2, max_digits=10)
    
    
    
    
