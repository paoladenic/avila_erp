# Generated by Django 5.0 on 2024-05-16 19:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0022_rename_name_clientetrabajo_names'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trabajo',
            name='apellido',
        ),
        migrations.RemoveField(
            model_name='trabajo',
            name='nombre',
        ),
        migrations.RemoveField(
            model_name='trabajo',
            name='telefono',
        ),
        migrations.RemoveField(
            model_name='trabajo',
            name='vehiculo',
        ),
        migrations.AddField(
            model_name='trabajo',
            name='cliente',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='erp.clientetrabajo'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='trabajo',
            name='detalle',
            field=models.CharField(max_length=700, verbose_name='Detalle'),
        ),
    ]
