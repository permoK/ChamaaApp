# Generated by Django 5.1.4 on 2025-01-07 18:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RestApi', '0002_customuser_pin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='pin',
            field=models.CharField(max_length=4, validators=[django.core.validators.MinLengthValidator(4), django.core.validators.RegexValidator(message='PIN must be numeric and 4-6 digits long.', regex='^\\d{4,6}$')]),
        ),
    ]