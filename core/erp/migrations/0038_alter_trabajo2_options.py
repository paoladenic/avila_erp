# Generated by Django 5.0 on 2024-06-28 23:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0037_remove_trabajo_cliente_trabajo_apellido_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='trabajo2',
            options={'ordering': ['-id'], 'verbose_name': 'Trabajo2', 'verbose_name_plural': 'Trabajos2'},
        ),
    ]
