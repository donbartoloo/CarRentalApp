# Generated by Django 4.2.5 on 2023-12-08 20:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0002_reservation_car_reservation_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='reservation_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
