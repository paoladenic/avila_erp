# Generated by Django 5.0 on 2024-06-13 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0032_alter_sale_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='desc',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
        ),
    ]
