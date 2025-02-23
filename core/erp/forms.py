from datetime import datetime
from django import forms
from django.forms import *
from django.forms import ModelForm
from django.utils import timezone
from core.erp.models import *


class CategoryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                    'class': 'form-control',
                }
            ),
            'desc': Textarea(
                attrs={
                    'placeholder': 'Ingrese una descripción',
                    'rows': 2,
                    'cols': 2
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ProductForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                    'class': 'form-control',
                }
            ),
            'cat': Select(
                attrs={
                    'class': 'select2',
                    'style': 'width: 100%'
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ClientForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['names'].widget.attrs['autofocus'] = True

    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'names': TextInput(
                attrs={
                    'placeholder': 'Ingrese los nombres',
                    'class': 'form-control',
                }
            ),
            'surnames': TextInput(
                attrs={
                    'placeholder': 'Ingrese los apellidos',
                    'class': 'form-control',
                }
            ),
            'dni': TextInput(
                attrs={
                    'placeholder': 'Ingrese el dni',
                    'class': 'form-control',
                }
            ),
            'address': TextInput(
                attrs={
                    'placeholder': 'Ingrese la dirección',
                    'class': 'form-control',
                }
            ),
            'phone': TextInput(
                attrs={
                    'placeholder': 'Ingrese el telefono',
                    'class': 'form-control',
                }
            ),
            'email': TextInput(
                attrs={
                    'placeholder': 'Ingrese el email',
                    'class': 'form-control',
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class SaleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cli'].queryset = Client.objects.none()

    class Meta:
        model = Sale
        fields = '__all__'
        widgets = {
            'cli': Select(attrs={
                'class': 'custom-select select2',
            }),
            'date_joined': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'date_joined',
                    'data-target': '#date_joined',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'tipo_pago': Select(attrs={
                'class': 'custom-select select2',
            }),
            'iva': TextInput(attrs={
                'class': 'form-control',
            }),
            'desc': TextInput(attrs={
                'class': 'form-control',
            }),
            'subtotal': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'total': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'cash': TextInput(attrs={
                'class': 'form-control',
            }),
            'card': TextInput(attrs={
                'class': 'form-control',
            })
        }

class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'
        widgets = {
            'date_cash': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'date_cash',
                    'data-target': '#date_cash',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'tipo_pago': Select(attrs={
                'class': 'custom-select select2',
            }),
            'iva': TextInput(attrs={
                'class': 'form-control',
            }),
            'desc': TextInput(attrs={
                'class': 'form-control',
            }),
            'subtotal': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'total': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'cash': TextInput(attrs={
                'class': 'form-control',
            }),
            'card': TextInput(attrs={
                'class': 'form-control',
            })
        }

class AbrirCajaForm(ModelForm):
    total = DecimalField(max_digits=10, decimal_places=2, widget=HiddenInput())

    class Meta:
        model = AbrirCaja
        fields = ['total']

class CerrarCajaForm(ModelForm):
    total = DecimalField(max_digits=10, decimal_places=2, widget=HiddenInput())

    class Meta:
        model = CerrarCaja
        fields = ['total']

class BanqueadoCajaForm(ModelForm):
    total = DecimalField(max_digits=10, decimal_places=2, widget=HiddenInput())

    class Meta:
        model = BanqueadoCaja
        fields = ['total']

class GastoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = GastoCaja
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese una descripción',
                    'class': 'form-control',
                }
            ),
            'fecha_gasto': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha_gasto',
                    'data-target': '#fecha_gasto',
                    'data-toggle': 'datetimepicker'
                }
            )
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ReportForm(Form):
    date_range = CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))


class TrabajoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['numero'].widget.attrs['autofocus'] = True

    class Meta:
        model = Trabajo
        fields = '__all__'
        widgets = {
            'numero': TextInput(
                attrs={
                    'placeholder': 'Ingrese el Número de Orden',
                }
            ),
            'fecha_trabajo': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha_trabajo',
                    'data-target': '#fecha_trabajo',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre',
                }
            ),
            'apellido': TextInput(
                attrs={
                    'placeholder': 'Ingrese los apellidos',
                }
            ),
            'telefono': TextInput(
                attrs={
                    'placeholder': 'Ingrese el teléfono',
                }
            ),
            'vehiculo': TextInput(
                attrs={
                    'placeholder': 'Descripción y color del vehículo',
                }
            ),
            'presupuesto': TextInput(
                attrs={
                    'placeholder': 'A Pagar',
                }
            ),
            'detalle': Textarea(
                attrs={
                    'placeholder': 'Detalle del trabajo',
                    'rows': 3,
                    'cols': 2
                }
            ),
            'status': Select(attrs={
                'class': 'custom-select select2',
            }),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
    
    
class TrabajoForm2(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].queryset = ClienteTrabajo.objects.all()

    class Meta:
        model = Trabajo2
        fields = '__all__'
        widgets = {
            'status': Select(
                attrs={
                    'class': 'custom-select select2',
                }
            ),
            'fecha_trabajo': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha_trabajo',
                    'data-target': '#fecha_trabajo',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'cliente': Select(
                attrs={
                    'class': 'custom-select select2',
                }
            ),
            'detalle': Textarea(
                attrs={
                    'placeholder': 'Detalle del trabajo',
                    'class': 'form-control',
                    'rows': 6,
                    'cols': 2
                }
            ),
            'numero': TextInput(
                attrs={
                    'placeholder': 'No Necesario',
                    'class': 'form-control',
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
    
class ClienteTrabajoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['names'].widget.attrs['autofocus'] = True

    class Meta:
        model = ClienteTrabajo
        fields = '__all__'
        widgets = {
            'names': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre',
                    'class': 'form-control',
                }
            ),
            'surnames': TextInput(
                attrs={
                    'placeholder': 'Ingrese los apellidos',
                    'class': 'form-control',
                }
            ),
            'phone': TextInput(
                attrs={
                    'placeholder': 'Ingrese el telefono',
                    'class': 'form-control',
                }
            ),
            'vehiculo': TextInput(
                attrs={
                    'placeholder': 'Ingrese el vehículo',
                    'class': 'form-control',
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data