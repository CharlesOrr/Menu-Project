# Generated by Django 3.0.7 on 2020-06-24 20:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0003_item_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='add_date',
        ),
    ]
