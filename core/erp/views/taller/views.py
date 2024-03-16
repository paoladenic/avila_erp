from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.template.loader import get_template
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from xhtml2pdf import pisa
from django.shortcuts import render

from core.erp.forms import *
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import *


class TrabajoListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Trabajo
    template_name = 'taller/list.html'
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
                for i in Trabajo.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Trabajos'
        context['create_url'] = reverse_lazy('erp:trabajo_create')
        context['list_url'] = reverse_lazy('erp:trabajo_list')
        context['entity'] = 'Trabajos'
        return context


class TrabajoCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Trabajo
    form_class = TrabajoForm
    template_name = 'taller/create.html'
    success_url = reverse_lazy('erp:trabajo_list')
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
        context['title'] = 'Crear un Registro'
        context['entity'] = 'Trabajos'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class TrabajoUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Trabajo
    form_class = TrabajoForm
    template_name = 'taller/create.html'
    success_url = reverse_lazy('erp:trabajo_list')
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
        context['title'] = 'Editar un Registro'
        context['entity'] = 'Trabajos'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class TrabajoDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Trabajo
    template_name = 'taller/delete.html'
    success_url = reverse_lazy('erp:trabajo_list')
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
        context['title'] = 'Eliminar un Registro'
        context['entity'] = 'Trabajos'
        context['list_url'] = self.success_url
        return context

class TrabajoInvoicePdfView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            trabajo = Trabajo.objects.get(pk=self.kwargs['pk'])
            template = get_template('taller/invoice.html')
            context = {
                'trabajo': trabajo,
                'comp': {
                    'phone': '+34 686 719 766',
                    'web': 'www.avilabikes.es',
                    'email': 'barcelona@avilabikes.es',
                    'address': 'C/ Provença 512, Bcn',
                    'company': 'AVILA BIKES',
                },
                'icon': '{}{}'.format(settings.STATIC_URL, 'img/avila.png')
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="ORDEN.pdf"'

            pisaStatus = pisa.CreatePDF(
                html, dest=response,
            )
            if pisaStatus.err:
                return HttpResponse('Error al generar el PDF: %s' % html)
            return response
        except Trabajo.DoesNotExist:
            return HttpResponseRedirect(reverse_lazy('erp:trabajo_list'))