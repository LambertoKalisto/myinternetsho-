# Generated by Django 4.2.7 on 2024-01-05 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_cart_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='session_key',
            field=models.CharField(default=0, max_length=32),
            preserve_default=False,
        ),
    ]