# Generated by Django 5.0 on 2024-06-14 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0033_ticket_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='desc',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
        ),
    ]
