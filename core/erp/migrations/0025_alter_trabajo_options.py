# Generated by Django 5.0 on 2024-05-21 20:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0024_alter_trabajo_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='trabajo',
            options={'ordering': ['-id'], 'verbose_name': 'Trabajo', 'verbose_name_plural': 'Trabajos'},
        ),
    ]
