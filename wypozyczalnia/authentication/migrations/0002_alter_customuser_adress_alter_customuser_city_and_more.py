# Generated by Django 4.2.5 on 2023-11-15 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='adress',
            field=models.TextField(max_length=100),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='city',
            field=models.TextField(max_length=30),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.TextField(max_length=30),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.TextField(max_length=30),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='postal_code',
            field=models.TextField(max_length=20),
        ),
    ]
