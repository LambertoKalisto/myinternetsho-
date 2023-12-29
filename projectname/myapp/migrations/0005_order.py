# Generated by Django 4.2.7 on 2023-12-28 13:30

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_remove_cart_user_cart_product_cart_quantity_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=50, verbose_name="Ім'я")),
                ('SurName', models.CharField(max_length=50, verbose_name='Прізвише')),
                ('Adress', models.CharField(max_length=250, verbose_name='Адресса відправки')),
                ('PhoneNumber', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Номер телефону')),
            ],
        ),
    ]
