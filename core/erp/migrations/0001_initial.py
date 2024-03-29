# Generated by Django 5.0 on 2024-03-06 22:15

import datetime
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Nombre')),
                ('desc', models.CharField(blank=True, max_length=500, null=True, verbose_name='Descripción')),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('names', models.CharField(max_length=150, verbose_name='Nombres')),
                ('surnames', models.CharField(max_length=150, verbose_name='Apellidos')),
                ('dni', models.CharField(max_length=10, unique=True, verbose_name='Dni')),
                ('address', models.CharField(blank=True, max_length=150, null=True, verbose_name='Dirección')),
                ('phone', models.CharField(blank=True, max_length=15, null=True, verbose_name='Telefono')),
                ('email', models.CharField(blank=True, max_length=150, null=True, verbose_name='Email')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_cash', models.DateField(default=datetime.datetime.now)),
                ('date_joined', models.DateTimeField(default=datetime.datetime.now)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('iva', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
            ],
            options={
                'verbose_name': 'Ticket',
                'verbose_name_plural': 'Tickets',
                'ordering': ['-date_joined'],
            },
        ),
        migrations.CreateModel(
            name='TipoPago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'Método de Pago',
                'verbose_name_plural': 'Métodos de Pagos',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='AbrirCaja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_apertura', models.DateField(default=datetime.datetime.now)),
                ('hora_apertura', models.TimeField(default=django.utils.timezone.now)),
                ('monto_apertura', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CerrarCaja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_cierre', models.DateField(default=datetime.datetime.now)),
                ('hora_cierre', models.TimeField(default=django.utils.timezone.now)),
                ('monto_cierre', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BanqueadoCaja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_banqueado', models.DateField(default=datetime.datetime.now)),
                ('monto_caja', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('total_gastos', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('total_ventas_tarjeta', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('total_ventas_efectivo', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('diferencia_caja', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('monto_banqueado', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('cierre_caja', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.cerrarcaja')),
            ],
            options={
                'verbose_name': 'Banqueado',
                'verbose_name_plural': 'Banqueados',
                'ordering': ['-fecha_banqueado'],
            },
        ),
        migrations.CreateModel(
            name='GastoCaja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Descripción')),
                ('fecha_gasto', models.DateField(default=datetime.datetime.now)),
                ('monto_gasto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Gasto',
                'verbose_name_plural': 'Gastos',
                'ordering': ['-fecha_gasto'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Nombre')),
                ('sku', models.CharField(default='0000', max_length=13, unique=True, verbose_name='SKU')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Descripción')),
                ('image', models.ImageField(blank=True, null=True, upload_to='product/%Y/%m/%d', verbose_name='Imagen')),
                ('stock', models.IntegerField(default=0, verbose_name='Stock')),
                ('pc', models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='Precio de compra')),
                ('pvp', models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='Precio de venta')),
                ('cat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.category', verbose_name='Categoría')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
                'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField(default=datetime.datetime.now)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('iva', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('cli', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.client')),
                ('tipo_pago', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.tipopago', verbose_name='Método de Pago')),
            ],
            options={
                'verbose_name': 'Venta',
                'verbose_name_plural': 'Ventas',
                'ordering': ['-date_joined'],
            },
        ),
        migrations.CreateModel(
            name='DetSale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('cant', models.IntegerField(default=0)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('prod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.product')),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.sale')),
            ],
            options={
                'verbose_name': 'Detalle de Venta',
                'verbose_name_plural': 'Detalle de Ventas',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='DetTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('cant', models.IntegerField(default=0)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('prod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.product')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.ticket')),
            ],
            options={
                'verbose_name': 'Detalle de Ticket',
                'verbose_name_plural': 'Detalle de Tickets',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='ticket',
            name='tipo_pago',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.tipopago', verbose_name='Método de Pago'),
        ),
    ]
