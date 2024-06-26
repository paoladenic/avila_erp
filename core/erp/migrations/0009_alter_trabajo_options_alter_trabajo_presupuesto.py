# Generated by Django 5.0 on 2024-03-27 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0008_alter_trabajo_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='trabajo',
            options={'ordering': ['numero'], 'verbose_name': 'Trabajo', 'verbose_name_plural': 'Trabajos'},
        ),
        migrations.AlterField(
            model_name='trabajo',
            name='presupuesto',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10),
        ),
    ]
