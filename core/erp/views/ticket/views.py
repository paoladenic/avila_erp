import json
import os

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.http import JsonResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, View

# from core.erp.forms import SaleForm, ClientForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import *
from core.erp.forms import TicketForm
from core.erp.models import Ticket, DetTicket
from django.shortcuts import render
from xhtml2pdf import pisa

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from io import BytesIO
from django.http import Http404
from django.utils.timezone import make_aware
import datetime




class TicketListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Ticket
    template_name = 'ticket/list.html'
    permission_required = 'view_sale'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Ticket.objects.all()[0:15]:
                    data.append(i.toJSON())
            elif action == 'search_details_prod':
                data = []
                for i in DetTicket.objects.filter(ticket_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de 15 Ultimos Tickets'
        context['create_url'] = reverse_lazy('erp:ticket_create')
        context['list_url'] = reverse_lazy('erp:ticket_list')
        context['entity'] = 'Tickets'
        return context


class TicketCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'ticket/create.html'
    success_url = reverse_lazy('erp:ticket_list')
    permission_required = 'add_sale'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                # products = Product.objects.filter(stock__gt=0)
                # if len(term):
                #     products = products.filter(name__icontains=term, sku__icontains=term)
                products = Product.objects.filter(stock__gt=0).filter(Q(name__icontains=term) | Q(sku__icontains=term))
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['value'] = i.name
                    # item['text'] = i.name
                    data.append(item)
            elif action == 'search_autocomplete':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                data.append({'id': term, 'text': term})
                # products = Product.objects.filter(name__icontains=term, sku__icontains=term, stock__gt=0)
                products = Product.objects.filter(stock__gt=0).filter(Q(name__icontains=term) | Q(sku__icontains=term))
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['text'] = i.name
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                    ticket = Ticket()
                    print(timezone.get_current_timezone())
                    print(timezone.now())
                    print(datetime.datetime.now())
                    print(vents['date_joined'])
                    # ticket.date_joined = make_aware(vents['date_joined'], timezone=timezone.get_current_timezone())
                    ticket.date_joined = vents['date_joined']
                    tipo_pago_id = int(vents['tipo_pago'])
                    tipo_pago_instance = TipoPago.objects.get(pk=tipo_pago_id)
                    ticket.tipo_pago = tipo_pago_instance
                    ticket.subtotal = float(vents['subtotal'])
                    ticket.iva = float(vents['iva'])
                    ticket.total = float(vents['total'])
                    ticket.save()
                    for i in vents['products']:
                        det = DetTicket()
                        det.ticket_id = ticket.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.price = float(i['pvp'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                        det.prod.stock -= det.cant
                        det.prod.save()
                    data = {'id': ticket.id}
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo Ticket'
        context['entity'] = 'Tickets'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['det'] = []
        # context['frmClient'] = ClientForm()
        return context


class TicketUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'ticket/create.html'
    success_url = reverse_lazy('erp:ticket_list')
    permission_required = 'change_sale'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        instance = self.get_object()
        form = TicketForm(instance=instance)
        form.fields['cli'].queryset = Client.objects.filter(id=instance.cli.id)
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                # products = Product.objects.filter(stock__gt=0)
                # if len(term):
                #     products = products.filter(name__icontains=term, sku__icontains=term)
                products = Product.objects.filter(stock__gt=0).filter(Q(name__icontains=term) | Q(sku__icontains=term))
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['value'] = i.name
                    # item['text'] = i.name
                    data.append(item)
            elif action == 'search_autocomplete':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                data.append({'id': term, 'text': term})
                # products = Product.objects.filter(name__icontains=term, sku__icontains=term, stock__gt=0)
                products = Product.objects.filter(stock__gt=0).filter(Q(name__icontains=term) | Q(sku__icontains=term))
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['text'] = i.name
                    data.append(item)
            elif action == 'edit':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                    # sale = Sale.objects.get(pk=self.get_object().id)
                    ticket = self.get_object()
                    ticket.date_joined = vents['date_joined']
                    tipo_pago_id = int(vents['tipo_pago'])
                    tipo_pago_instance = TipoPago.objects.get(pk=tipo_pago_id)
                    ticket.tipo_pago = tipo_pago_instance
                    ticket.subtotal = float(vents['subtotal'])
                    ticket.iva = float(vents['iva'])
                    ticket.total = float(vents['total'])
                    ticket.save()
                    ticket.detticket_set.all().delete()
                    for i in vents['products']:
                        det = DetTicket()
                        det.ticket_id = ticket.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.price = float(i['pvp'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                        det.prod.stock -= det.cant
                        det.prod.save()
                    data = {'id': ticket.id}
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


    def get_details_product(self):
        data = []
        try:
            for i in DetTicket.objects.filter(ticket_id=self.get_object().id):
                item = i.prod.toJSON()
                item['cant'] = i.cant
                data.append(item)
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar un Ticket'
        context['entity'] = 'Tickets'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_details_product())
        # context['frmClient'] = ClientForm()
        return context


class TicketDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Ticket
    template_name = 'ticket/delete.html'
    success_url = reverse_lazy('erp:ticket_list')
    permission_required = 'delete_sale'
    url_redirect = success_url

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
        context['title'] = 'Eliminar un Ticket'
        context['entity'] = 'Tickets'
        context['list_url'] = self.success_url
        return context
    

class TicketInvoicePdfView(LoginRequiredMixin, View):
     
    def get(self, request, *args, **kwargs):
        try:
            template = get_template('ticket/invoice.html')
            context = {
                'ticket': Ticket.objects.get(pk=self.kwargs['pk']),
                'comp': {'name': 'Benjamin Torregrosa', 'ruc': '51299628Z', 'address': 'C/ Provença 512, Bcn', 'company': 'AVILA BIKES',},
                'icon': '{}{}'.format(settings.STATIC_URL, 'img/avila.png')
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="ticket.pdf"'

            # buffer = BytesIO()
            # pisaStatus = pisa.CreatePDF(html, dest=buffer)
            # pdf = buffer.getvalue()
            # buffer.close()
            # response.write(pdf)

            pisaStatus = pisa.CreatePDF(
                html, dest=response)
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('erp:ticket_list'))

