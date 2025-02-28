from django.db import models
from django.forms import model_to_dict

from config.settings import MEDIA_URL, STATIC_URL
from core.models import BaseModel

from django.utils import timezone
from django.utils.timezone import make_aware, now
from datetime import datetime

import pytz

from core.user.models import User
from django.contrib.auth import get_user_model


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['id']

class TipoPago(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Método de Pago'
        verbose_name_plural = 'Métodos de Pagos'
        ordering = ['id']


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nombre')
    cat = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoría')
    sku = models.CharField(max_length=30, verbose_name='SKU', unique=True, default='0000')
    description = models.TextField(verbose_name='Descripción', blank=True, null=True)
    image = models.ImageField(upload_to='product/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    stock = models.IntegerField(default=0, verbose_name='Stock')
    pc = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio de compra')
    pvp = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio de venta')
    proveedor = models.CharField(max_length=150, verbose_name='Proveedor')
    skuprove = models.CharField(max_length=30, verbose_name='SKU Proveedor', default='0000')

    def __str__(self):
        return self.name

    def get_image_url(self, image_field):
        if image_field:
            return '{}{}'.format(MEDIA_URL, image_field)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = '{} / {}'.format(self.name, self.cat.name)
        item['cat'] = self.cat.name
        item['image'] = self.get_image_url(self.image)
        item['pc'] = format(self.pc, '.2f')
        item['pvp'] = format(self.pvp, '.2f')
        return item

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-name']


class Client(models.Model):
    names = models.CharField(max_length=150, verbose_name='Nombres')
    surnames = models.CharField(max_length=150, verbose_name='Apellidos')
    dni = models.CharField(max_length=10, unique=True, verbose_name='Dni')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    phone = models.CharField(max_length=15, null=True, blank=True, verbose_name='Telefono')
    email = models.CharField(max_length=150, null=True, blank=True, verbose_name='Email')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '{} {} / {}'.format(self.names, self.surnames, self.dni)

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = self.get_full_name()
        return item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']


class Sale(models.Model):
    cli = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    tipo_pago = models.ForeignKey(TipoPago, on_delete=models.CASCADE, verbose_name='Método de Pago')
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    desc = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cash = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    card = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.cli.names

    def toJSON(self):
        item = model_to_dict(self)
        item['cli'] = self.cli.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['desc'] = format(self.desc, '.2f')
        item['total'] = format(self.total, '.2f')
        item['cash'] = format(self.cash, '.2f')
        item['card'] = format(self.card, '.2f')
        item['tipo_pago'] = self.tipo_pago.name
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.detsale_set.all()]
        return item

    def delete(self, using=None, keep_parents=False):
        for det in self.detsale_set.all():
            det.prod.stock += det.cant
            det.prod.save()
        super(Sale, self).delete()

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['-id']


class DetSale(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.prod.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['prod'] = self.prod.toJSON()
        item['price'] = format(self.price, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
        ordering = ['id']

class Ticket(models.Model):
    date_cash = models.DateField(default=timezone.now)
    date_joined = models.DateTimeField(default=timezone.now)
    tipo_pago = models.ForeignKey(TipoPago, on_delete=models.CASCADE, verbose_name='Método de Pago')
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    desc = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cash = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    card = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def save(self, *args, **kwargs):
        local_timezone = pytz.timezone('Europe/Madrid')
        now_local = timezone.localtime(timezone.now(), local_timezone)
        print(f"Pre-save date_joined (local): {now_local}")
        self.date_joined = now_local
        self.date_cash = now_local.date()
        super(Ticket, self).save(*args, **kwargs)
        print(f"Post-save date_joined (stored): {self.date_joined}")

    def __str__(self):
        return f'Ticket # {self.id}'

    def toJSON(self):
        item = model_to_dict(self)
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['desc'] = format(self.desc, '.2f')
        item['total'] = format(self.total, '.2f')
        item['cash'] = format(self.cash, '.2f')
        item['card'] = format(self.card, '.2f')
        item['tipo_pago'] = self.tipo_pago.name

        local_timezone = pytz.timezone('Europe/Madrid')
        date_joined_local = self.date_joined.astimezone(local_timezone)
        item['date_joined'] = date_joined_local.strftime('%Y-%m-%d %H:%M:%S')
        item['date_cash'] = self.date_cash.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.detticket_set.all()]
        return item

    def delete(self, using=None, keep_parents=False):
        for det in self.detticket_set.all():
            det.prod.stock += det.cant
            det.prod.save()
        super(Ticket, self).delete()

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'
        ordering = ['-id']


class DetTicket(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.prod.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['ticket'])
        item['prod'] = self.prod.toJSON()
        item['price'] = format(self.price, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Ticket'
        verbose_name_plural = 'Detalle de Tickets'
        ordering = ['id']

class AbrirCaja(models.Model):
    usuario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    fecha_apertura = models.DateField(default=timezone.now)
    hora_apertura = models.TimeField(default=timezone.now)
    monto_apertura = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def save(self, *args, **kwargs):
        local_timezone = pytz.timezone('Europe/Madrid')
        self.fecha_apertura = timezone.localtime(timezone.now(), local_timezone).date()
        self.hora_apertura = timezone.localtime(timezone.now(), local_timezone).time()
        super(AbrirCaja, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.usuario.username} - {self.fecha_apertura} - {self.hora_apertura}"

class CerrarCaja(models.Model):
    usuario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    fecha_cierre = models.DateField(default=timezone.now)
    hora_cierre = models.TimeField(default=timezone.now)
    monto_cierre = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def save(self, *args, **kwargs):
        local_timezone = pytz.timezone('Europe/Madrid')
        self.fecha_cierre = timezone.localtime(timezone.now(), local_timezone).date()
        self.hora_cierre = timezone.localtime(timezone.now(), local_timezone).time()
        super(CerrarCaja, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.usuario.username} - {self.fecha_cierre} - {self.hora_cierre}"

class BanqueadoCaja(models.Model):
    usuario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    fecha_banqueado = models.DateField(default=datetime.now)
    monto_caja = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total_gastos = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total_ventas_tarjeta = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total_ventas_efectivo = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    diferencia_caja = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cierre_caja = models.ForeignKey(CerrarCaja, on_delete=models.CASCADE)
    monto_banqueado = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return f"{self.usuario.username} - {self.fecha_banqueado} - {self.cierre_caja.monto_cierre}"

    def toJSON(self):
        item = model_to_dict(self)
        item['usuario'] = self.usuario.username
        item['fecha_banqueado'] = self.fecha_banqueado.strftime('%Y-%m-%d')
        item['monto_caja'] = float(self.monto_caja)
        item['total_gastos'] = float(self.total_gastos)
        item['total_ventas_tarjeta'] = float(self.total_ventas_tarjeta)
        item['total_ventas_efectivo'] = float(self.total_ventas_efectivo)
        item['diferencia_caja'] = float(self.diferencia_caja)
        item['cierre_caja'] = float(self.cierre_caja.monto_cierre)
        item['monto_banqueado'] = float(self.monto_banqueado)
        return item

    class Meta:
        verbose_name = 'Banqueado'
        verbose_name_plural = 'Banqueados'
        ordering = ['-fecha_banqueado']

class GastoCaja(models.Model):
    # usuario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=150, verbose_name='Descripción')
    fecha_gasto = models.DateField(default=datetime.now)
    monto_gasto = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.id

    def toJSON(self):
        item = model_to_dict(self)
        # item['usuario'] = self.usuario.username
        item['fecha_gasto'] = self.fecha_gasto.strftime('%Y-%m-%d')
        item['monto_gasto'] = self.monto_gasto
        return item

    class Meta:
        verbose_name = 'Gasto'
        verbose_name_plural = 'Gastos'
        ordering = ['-id']

class StatusTrabajo(models.Model):
    name = models.CharField(max_length=150, verbose_name='Status Trabajo', unique=True)

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Status Trabajo'
        verbose_name_plural = 'Status Trabajo'
        ordering = ['id']

class ClienteTrabajo(models.Model):
    names = models.CharField(max_length=150, verbose_name='Nombre')
    surnames = models.CharField(max_length=150, verbose_name='Apellidos')
    phone = models.CharField(max_length=15, null=True, verbose_name='Telefono')
    vehiculo = models.CharField(max_length=150, null=True, blank=True, verbose_name='Vehiculo')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '{} {} / {} / {} '.format(self.names, self.surnames, self.phone, self.vehiculo)

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = self.get_full_name()
        return item

    class Meta:
        verbose_name = 'ClienteTaller'
        verbose_name_plural = 'ClientesTaller'
        ordering = ['id']

class Trabajo2(models.Model):
    status = models.ForeignKey(StatusTrabajo, on_delete=models.CASCADE, verbose_name='Status Trabajo')
    fecha_trabajo = models.DateField(default=datetime.now)
    cliente = models.ForeignKey(ClienteTrabajo, on_delete=models.CASCADE)
    detalle = models.CharField(max_length=700, verbose_name='Detalle')
    # image = models.ImageField(upload_to='taller/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    numero = models.CharField(max_length=10, verbose_name='Número de Orden', null=True, blank=True) #unique=True
    # presupuesto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.id

    # def get_image_url(self, image_field):
    #     if image_field:
    #         return '{}{}'.format(MEDIA_URL, image_field)
    #     return '{}{}'.format(STATIC_URL, 'img/empty.png')

    def toJSON(self):
        item = model_to_dict(self)
        item['cliente'] = self.cliente.toJSON()
        item['fecha_trabajo'] = self.fecha_trabajo.strftime('%Y-%m-%d')
        item['status'] = self.status.name
        # item['image'] = self.get_image_url(self.image)
        # item['presupuesto'] = self.presupuesto
        return item

    class Meta:
        verbose_name = 'Trabajo2'
        verbose_name_plural = 'Trabajos2'
        ordering = ['-id']

class Trabajo(models.Model):
    numero = models.CharField(max_length=10, unique=True, verbose_name='Número de Orden')
    fecha_trabajo = models.DateField(default=datetime.now)
    nombre = models.CharField(max_length=150, verbose_name='Nombre')
    apellido = models.CharField(max_length=150, verbose_name='Apellido')
    telefono = models.CharField(max_length=150, verbose_name='Teléfono')
    vehiculo = models.CharField(max_length=150, verbose_name='Vehículo/Color')
    detalle = models.CharField(max_length=500, verbose_name='Detalle')
    image = models.ImageField(upload_to='taller/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    presupuesto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.ForeignKey(StatusTrabajo, on_delete=models.CASCADE, verbose_name='Status Trabajo')

    def __str__(self):
        return f"{self.numero} - {self.fecha_trabajo}"

    def get_image_url(self, image_field):
        if image_field:
            return '{}{}'.format(MEDIA_URL, image_field)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    def toJSON(self):
        item = model_to_dict(self)
        item['fecha_trabajo'] = self.fecha_trabajo.strftime('%Y-%m-%d')
        item['status'] = self.status.name
        item['image'] = self.get_image_url(self.image)
        item['presupuesto'] = self.presupuesto
        return item

    class Meta:
        verbose_name = 'Trabajo'
        verbose_name_plural = 'Trabajos'
        ordering = ['-id']

class Presu(models.Model):
    id_taller = models.ForeignKey(Trabajo2, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Trabajo2, on_delete=models.CASCADE)
    date_cash = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.id

    def toJSON(self):
        item = model_to_dict(self)
        item['id_taller'] = self.id_taller.id
        item['cliente'] = self.cliente.cliente
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')
        item['date_cash'] = self.date_cash.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.detpresu_set.all()]
        return item

    def delete(self, using=None, keep_parents=False):
        for det in self.detpresu_set.all():
            det.prod.stock += det.cant
            det.prod.save()
        super(Presu, self).delete()

    class Meta:
        verbose_name = 'Presupuesto'
        verbose_name_plural = 'Presupuestos'
        ordering = ['-id']

class DetPresu(models.Model):
    presu = models.ForeignKey(Presu, on_delete=models.CASCADE)
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.prod.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['presu'])
        item['prod'] = self.prod.toJSON()
        item['price'] = format(self.price, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Presupuestot'
        verbose_name_plural = 'Detalle de Presupuestos'
        ordering = ['id']