# Generated by Django 4.2.7 on 2023-12-26 06:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_cart_cartitem_cart_products_cart_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='products',
        ),
    ]
