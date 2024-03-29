# Generated by Django 4.2.7 on 2024-01-31 09:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_remove_cart_session_key'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='Adress',
            new_name='adress',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='Name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='SurName',
            new_name='surname',
        ),
        migrations.RemoveField(
            model_name='order',
            name='PhoneNumber',
        ),
        migrations.AddField(
            model_name='order',
            name='phonenumber',
            field=models.CharField(default=' ', max_length=13, validators=[django.core.validators.RegexValidator(message='Номер телефону повинен бути валідним.', regex='^\\+38?\\d{10}$')]),
        ),
    ]
