# Generated by Django 5.0 on 2024-04-07 20:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0015_alter_trabajo_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='trabajo',
            options={'ordering': ['-fecha_trabajo', '-id'], 'verbose_name': 'Trabajo', 'verbose_name_plural': 'Trabajos'},
        ),
    ]
