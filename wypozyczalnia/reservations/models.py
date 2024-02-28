from django.db import models
from cars.models import Car
from authentication.models import CustomUser
from django.utils import timezone

# Create your models here.

class Reservation(models.Model):
    
    def __str__(self):
        return f'Rezerwacja - {self.car} {self.user}'
    
    user = models.ForeignKey(CustomUser,null=False, blank=True, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, null=False, blank=True, on_delete=models.CASCADE)
    reservation_date = models.DateField(timezone.now, default=timezone.now)
    start_date = models.DateField()
    finish_date = models.DateField()
    
    class ReservationStatus(models.TextChoices):
        ACTIVE = 'active', 'Aktywna'
        CANCELED = 'canceled', 'Anulowana'
        COMPLETED = 'completed', 'Zakończona'
    reservation_status = models.CharField(max_length=10, choices=ReservationStatus.choices, default=ReservationStatus.ACTIVE)
    