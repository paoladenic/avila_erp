from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import JsonResponse, request
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/main.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Accesos'
        context['open_url'] = reverse_lazy('erp:cash_open')
        context['ticket_url'] = reverse_lazy('erp:ticket_create')
        context['product_url'] = reverse_lazy('erp:product_create')
        context['cerrar_url'] = reverse_lazy('erp:cash_close')
        context['entity'] = 'Status'

        return context