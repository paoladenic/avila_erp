# Generated by Django 5.0 on 2024-06-26 21:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0034_sale_desc'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticket',
            options={'ordering': ['-id'], 'verbose_name': 'Ticket', 'verbose_name_plural': 'Tickets'},
        ),
    ]