# Generated by Django 4.2.5 on 2023-11-15 16:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='date_crated',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
