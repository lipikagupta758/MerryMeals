# Generated by Django 5.1.2 on 2024-11-08 13:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0002_remove_cart_fooditem_remove_cart_quantity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='restaurant_cart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='marketplace.restaurant_cart'),
        ),
    ]
