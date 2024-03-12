# from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.views.generic import FormView
from core.erp.models import AbrirCaja
from core.user.models import *
from core.erp.forms import *
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.erp.mixins import ValidatePermissionRequiredMixin
from django.db.models import Sum, Q, F
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import TemplateView
import json

from django.http import HttpResponse
from django.views.generic import FormView




class CashFlowView(LoginRequiredMixin, TemplateView):
    template_name = 'cash/main.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cash Flow'
        context['create_url'] = reverse_lazy('erp:cash_open')
        context['gasto_url'] = reverse_lazy('erp:gasto_list')
        context['list_url'] = reverse_lazy('erp:cash_report')
        context['close_url'] = reverse_lazy('erp:cash_close')
        context['balance_url'] = reverse_lazy('erp:balance_dia')
        context['entity'] = 'CashFlow'
        return context
    
class CashOpenView(LoginRequiredMixin, FormView):
    template_name = 'cash/open.html'
    form_class = AbrirCajaForm
    success_url = reverse_lazy('erp:open_detail')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # Verificar si ya hay una apertura para este día
        fecha_apertura = timezone.now().date()
        if AbrirCaja.objects.filter(fecha_apertura=fecha_apertura).exists():
            # Si ya existe un registro de apertura para este día, redirigir a la página de detalle
            return redirect('erp:open_detail')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        usuario = self.request.user
        fecha_apertura = timezone.now().date()
        hora_apertura = timezone.now().time()
        monto_apertura = form.cleaned_data['total']
        abrir_caja = AbrirCaja(usuario=usuario, fecha_apertura=fecha_apertura, hora_apertura=hora_apertura, monto_apertura=monto_apertura)
        # abrir_caja = AbrirCaja(usuario=usuario, fecha_apertura=fecha_apertura, monto_apertura=monto_apertura)
        abrir_caja.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Abrir Día'
        context['list_url'] = reverse_lazy('erp:cash_flow')
        context['entity'] = 'AbrirDia'
        return context

class CashOpenDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'cash/open_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalle Apertura Día'
        context['list_url'] = reverse_lazy('erp:cash_flow')
        context['entity'] = 'DiaAperturaDetalle'

        # Obtener el objeto de apertura del día actual
        abrir_caja = AbrirCaja.objects.filter(fecha_apertura=timezone.now()).order_by('-fecha_apertura').first()

        # Agregar los datos necesarios al contexto
        context['monto_apertura'] = abrir_caja.monto_apertura
        context['fecha_apertura'] = abrir_caja.fecha_apertura
        context['hora_apertura'] = abrir_caja.hora_apertura
        context['usuario'] = abrir_caja.usuario.username

        return context
    
    
class CashReportView(LoginRequiredMixin, TemplateView):
    template_name = 'cash/report.html'
    form_class = ReportForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_report':
                data = []
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                search = BanqueadoCaja.objects.all()
                if len(start_date) and len(end_date):
                    search = search.filter(fecha_banqueado__range=[start_date, end_date])
                for i in search:
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Informes Caja'
        context['entity'] = 'CashReport'
        context['back_url'] = reverse_lazy('erp:cash_flow')
        context['form'] = ReportForm()
        return context

    
class BalanceDiaView(LoginRequiredMixin, TemplateView):
    template_name = 'cash/balance.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Status Día'
        context['list_url'] = reverse_lazy('erp:cash_flow')
        context['open_url'] = reverse_lazy('erp:open_detail')
        context['gasto_url'] = reverse_lazy('erp:gasto_list')
        context['factura_url'] = reverse_lazy('erp:sale_list')
        context['ticket_url'] = reverse_lazy('erp:ticket_list')
        context['entity'] = 'Status'

        # Obtener la información del día actual
        fecha_actual = timezone.now().date()

        # Obtener el objeto de apertura del día actual
        abrir_caja = AbrirCaja.objects.filter(fecha_apertura=fecha_actual).first()
        if abrir_caja:
            monto_apertura = abrir_caja.monto_apertura
        else:
            monto_apertura = Decimal('0.00')
        context['monto_apertura'] = monto_apertura

        # Obtener el total de gastos del día actual
        total_gastos = GastoCaja.objects.filter(fecha_gasto=fecha_actual).aggregate(Sum('monto_gasto'))['monto_gasto__sum']
        context['total_gastos'] = total_gastos if total_gastos else 0.00

        # Obtener el total de ventas del día actual
        total_ventas = Sale.objects.filter(date_joined=fecha_actual).aggregate(Sum('total'))['total__sum']
        context['total_facturas'] = total_ventas if total_ventas else 0.00

        # Obtener el total de tickets del día actual
        total_tickets = Ticket.objects.filter(date_cash=fecha_actual).aggregate(Sum('total'))['total__sum']
        context['total_tickets'] = total_tickets if total_tickets else 0.00

        # Obtener el monto total de ventas y tickets en tarjeta y efectivo del día actual
        ventas = Sale.objects.filter(date_joined=fecha_actual).aggregate(
            total_tarjeta=Sum('total', filter=Q(tipo_pago__name='Tarjeta')),
            total_efectivo=Sum('total', filter=Q(tipo_pago__name='Efectivo'))
        )
        tickets = Ticket.objects.filter(date_cash=fecha_actual).aggregate(
            total_tarjeta=Sum('total', filter=Q(tipo_pago__name='Tarjeta')),
            total_efectivo=Sum('total', filter=Q(tipo_pago__name='Efectivo'))
        )

        # total_tarjeta = (ventas['total_tarjeta'] or 0.00) + (tickets['total_tarjeta'] or 0.00)
        # total_efectivo = (ventas['total_efectivo'] or 0.00) + (tickets['total_efectivo'] or 0.00)
        total_tarjeta = (float(ventas['total_tarjeta'] or Decimal('0.00'))) + (float(tickets['total_tarjeta'] or Decimal('0.00')))
        total_efectivo = (float(ventas['total_efectivo'] or Decimal('0.00'))) + (float(tickets['total_efectivo'] or Decimal('0.00')))
        context['total_ventas_tarjeta'] = total_tarjeta
        context['total_ventas_efectivo'] = total_efectivo

        if total_gastos is None:
            total_gastos = Decimal('0.00')

        # total_caja_efectivo = (abrir_caja.monto_apertura + total_efectivo) - total_gastos
        total_caja_efectivo = (monto_apertura + Decimal(total_efectivo)) - Decimal(total_gastos)
        context['total_caja_efectivo'] = total_caja_efectivo
        
        return context

    
class CashCloseView(LoginRequiredMixin, FormView):
    template_name = 'cash/close.html'
    form_class = CerrarCajaForm
    success_url = reverse_lazy('erp:close_detail')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # Verificar si ya hay una apertura para este día
        fecha_banqueado = timezone.now().date()
        if BanqueadoCaja.objects.filter(fecha_banqueado=fecha_banqueado).exists():
            # Si ya existe un registro de apertura para este día, redirigir a la página de detalle
            return redirect('erp:close_detail2')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        usuario = self.request.user
        fecha_cierre = timezone.now().date()
        hora_cierre = timezone.now().time()
        monto_cierre = form.cleaned_data['total']
        cerrar_caja = CerrarCaja(usuario=usuario, fecha_cierre=fecha_cierre, hora_cierre=hora_cierre, monto_cierre=monto_cierre)
        cerrar_caja.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cerrar Día'
        context['list_url'] = reverse_lazy('erp:cash_flow')
        context['entity'] = 'CerrarDia'
        fecha_actual = timezone.now()
        
        abrir_caja = AbrirCaja.objects.filter(fecha_apertura=fecha_actual).first()
        if abrir_caja:
            context['monto_apertura'] = abrir_caja.monto_apertura if abrir_caja else 0.00

            # Obtener el monto total de ventas y tickets en tarjeta y efectivo del día actual
            ventas = Sale.objects.filter(date_joined=fecha_actual).aggregate(total_efectivo=Sum('total', filter=Q(tipo_pago__name='Efectivo')))
            tickets = Ticket.objects.filter(date_cash=fecha_actual).aggregate(total_efectivo=Sum('total', filter=Q(tipo_pago__name='Efectivo')))
            # total_efectivo = (ventas['total_efectivo'] or 0.00) + (tickets['total_efectivo'] or 0.00)
            total_efectivo = (float(ventas['total_efectivo'] or Decimal('0.00'))) + (float(tickets['total_efectivo'] or Decimal('0.00')))
            context['total_ventas_efectivo'] = total_efectivo

            total_gastos = GastoCaja.objects.filter(fecha_gasto=timezone.now().date()).aggregate(Sum('monto_gasto'))['monto_gasto__sum']
            context['total_gastos'] = total_gastos if total_gastos else 0.00

            if total_gastos is None:
                total_gastos = Decimal('0.00')

            total_caja_efectivo = (Decimal(abrir_caja.monto_apertura) + Decimal(total_efectivo)) - Decimal(total_gastos)
            context['total_caja_efectivo'] = total_caja_efectivo
        else:
            context['monto_apertura'] = None
            context['total_ventas_efectivo'] = 0.00
            context['total_gastos'] = 0.00
            context['total_caja_efectivo'] = 0.00
            context['error_message'] = "------------ ANTES DE CONTINUAR, DEBES ABRIR EL DÍA ------------"

        return context


class CashCloseDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'cash/close_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalle Cierre Día'
        context['list_url'] = reverse_lazy('erp:close_banqueado')
        context['entity'] = 'DiaCierreDetalle'

        fecha_actual = timezone.now()

        abrir_caja = AbrirCaja.objects.filter(fecha_apertura=fecha_actual).first()
        context['monto_apertura'] = abrir_caja.monto_apertura if abrir_caja else 0.00
        ventas = Sale.objects.filter(date_joined=fecha_actual).aggregate(total_efectivo=Sum('total', filter=Q(tipo_pago__name='Efectivo')))
        tickets = Ticket.objects.filter(date_cash=fecha_actual).aggregate(total_efectivo=Sum('total', filter=Q(tipo_pago__name='Efectivo')))
        total_efectivo = (float(ventas['total_efectivo'] or Decimal('0.00'))) + (float(tickets['total_efectivo'] or Decimal('0.00')))
        context['total_ventas_efectivo'] = total_efectivo
        total_gastos = GastoCaja.objects.filter(fecha_gasto=timezone.now().date()).aggregate(Sum('monto_gasto'))['monto_gasto__sum']
        context['total_gastos'] = total_gastos if total_gastos else 0.00
        if total_gastos is None:
            total_gastos = Decimal('0.00')
        total_caja_efectivo = (abrir_caja.monto_apertura + Decimal(total_efectivo)) - Decimal(total_gastos)
        context['total_caja_efectivo'] = total_caja_efectivo
        
        cerrar_caja = CerrarCaja.objects.filter(fecha_cierre=fecha_actual).first()
        context['monto_cierre'] = cerrar_caja.monto_cierre
        context['fecha_cierre'] = cerrar_caja.fecha_cierre
        context['hora_cierre'] = cerrar_caja.hora_cierre
        context['usuario'] = cerrar_caja.usuario.username

        diferencia_caja = total_caja_efectivo - cerrar_caja.monto_cierre
        context['diferencia_caja'] = diferencia_caja

        return context
    
class CashCloseBanqueadoView(LoginRequiredMixin, FormView):
    template_name = 'cash/close_banqueado.html'
    form_class = BanqueadoCajaForm
    success_url = reverse_lazy('erp:close_detail2')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # Verificar si ya hay una apertura para este día
        fecha_banqueado = timezone.now().date()
        if BanqueadoCaja.objects.filter(fecha_banqueado=fecha_banqueado).exists():
            # Si ya existe un registro de apertura para este día, redirigir a la página de detalle
            return redirect('erp:close_detail2')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        usuario = self.request.user
        fecha_banqueado = timezone.now().date()
        monto_caja = form.cleaned_data['total']
        total_gastos = GastoCaja.objects.filter(fecha_gasto=timezone.now().date()).aggregate(Sum('monto_gasto'))['monto_gasto__sum']
        total_gastos = total_gastos if total_gastos else 0.00
        ventas = Sale.objects.filter(date_joined=timezone.now().date()).aggregate(
            total_tarjeta=Sum('total', filter=Q(tipo_pago__name='Tarjeta')),
            total_efectivo=Sum('total', filter=Q(tipo_pago__name='Efectivo'))
        )
        tickets = Ticket.objects.filter(date_cash=timezone.now().date()).aggregate(
            total_tarjeta=Sum('total', filter=Q(tipo_pago__name='Tarjeta')),
            total_efectivo=Sum('total', filter=Q(tipo_pago__name='Efectivo'))
        )

        total_ventas_efectivo = (float(ventas['total_efectivo'] or Decimal('0.00'))) + (float(tickets['total_efectivo'] or Decimal('0.00')))
        total_ventas_tarjeta = (float(ventas['total_tarjeta'] or Decimal('0.00'))) + (float(tickets['total_tarjeta'] or Decimal('0.00')))

        cerrar_caja = CerrarCaja.objects.filter(fecha_cierre=timezone.now().date()).first()
        cierre_caja = cerrar_caja.monto_cierre

        abrir_caja = AbrirCaja.objects.filter(fecha_apertura=timezone.now().date()).first()
        monto_apertura = abrir_caja.monto_apertura

        total_caja_efectivo = (abrir_caja.monto_apertura + Decimal(total_ventas_efectivo)) - Decimal(total_gastos)

        diferencia_caja = total_caja_efectivo - cierre_caja

        monto_banqueado = cierre_caja - monto_caja
        
        banqueado_caja = BanqueadoCaja(
            usuario=usuario, 
            fecha_banqueado=fecha_banqueado, 
            monto_caja=monto_caja, 
            total_gastos=total_gastos, 
            total_ventas_tarjeta=total_ventas_tarjeta, 
            total_ventas_efectivo=total_ventas_efectivo, 
            diferencia_caja=diferencia_caja,
            cierre_caja=cerrar_caja, 
            monto_banqueado=monto_banqueado
        )
        banqueado_caja.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cerrar Día'
        context['list_url'] = reverse_lazy('erp:close_detail')
        context['entity'] = 'BanqueadoDetalleDia'

        fecha_actual = timezone.now()
        cerrar_caja = CerrarCaja.objects.filter(fecha_cierre=fecha_actual).first()
        context['monto_cierre'] = cerrar_caja.monto_cierre

        return context  
    
class CashCloseDetailView2(LoginRequiredMixin, TemplateView):
    template_name = 'cash/close_detail2.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalle Cierre Día'
        context['list_url'] = reverse_lazy('erp:cash_flow')
        context['entity'] = 'DiaBanqueadoDetalle'

        # Obtener la información del día actual
        fecha_actual = timezone.now().date()

        # Obtener el objeto de apertura del día actual
        abrir_caja = AbrirCaja.objects.filter(fecha_apertura=fecha_actual).first()
        context['usuario_apertura'] = abrir_caja.usuario
        context['monto_apertura'] = abrir_caja.monto_apertura if abrir_caja else 0.00
        context['hora_apertura'] = abrir_caja.hora_apertura
        context['fecha_apertura'] = abrir_caja.fecha_apertura

         # Obtener el objeto de apertura del día actual
        cerrar_caja = CerrarCaja.objects.filter(fecha_cierre=fecha_actual).first()
        context['monto_cierre'] = cerrar_caja.monto_cierre if cerrar_caja else 0.00
        context['fecha_cierre'] = cerrar_caja.fecha_cierre
        context['hora_cierre'] = cerrar_caja.hora_cierre
        context['usuario_cierre'] = cerrar_caja.usuario.username

        banqueado_caja = BanqueadoCaja.objects.filter(fecha_banqueado=fecha_actual).first()
        context['monto_caja'] = banqueado_caja.monto_caja if banqueado_caja else 0.00
        context['total_gastos'] = banqueado_caja.total_gastos if banqueado_caja else 0.00
        context['total_ventas_tarjeta'] = banqueado_caja.total_ventas_tarjeta if banqueado_caja else 0.00
        context['total_ventas_efectivo'] = banqueado_caja.total_ventas_efectivo if banqueado_caja else 0.00
        context['diferencia_caja'] = banqueado_caja.diferencia_caja if banqueado_caja else 0.00
        context['monto_banqueado'] = banqueado_caja.monto_banqueado if banqueado_caja else 0.00

        return context



class GastoListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = GastoCaja
    template_name = 'cash/gasto_list.html'
    permission_required = 'view_product', 'change_product', 'delete_product', 'add_product'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in GastoCaja.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Gastos de Caja'
        context['create_url'] = reverse_lazy('erp:gasto_create')
        context['list_url'] = reverse_lazy('erp:cash_flow')
        context['entity'] = 'Gastos'
        return context


class GastoCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = GastoCaja
    form_class = GastoForm
    template_name = 'cash/gasto_create.html'
    success_url = reverse_lazy('erp:gasto_list')
    permission_required = 'add_product'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo Gasto de Caja'
        context['entity'] = 'Gastos'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class GastoUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = GastoCaja
    form_class = GastoForm
    template_name = 'cash/gasto_create.html'
    success_url = reverse_lazy('erp:gasto_list')
    permission_required = 'change_product'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Gasto de Caja'
        context['entity'] = 'Gastos'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class GastoDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = GastoCaja
    template_name = 'cash/gasto_delete.html'
    success_url = reverse_lazy('erp:gasto_list')
    permission_required = 'delete_product'
    url_redirect = success_url

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Gasto de Caja'
        context['entity'] = 'Gastos'
        context['list_url'] = self.success_url
        return context
