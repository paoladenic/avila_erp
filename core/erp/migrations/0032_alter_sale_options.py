# Generated by Django 5.0 on 2024-06-13 22:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0031_alter_gastocaja_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sale',
            options={'ordering': ['-id'], 'verbose_name': 'Venta', 'verbose_name_plural': 'Ventas'},
        ),
    ]
