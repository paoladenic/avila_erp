from django.urls import path
from core.erp.views.category.views import *
from core.erp.views.client.views import *
from core.erp.views.dashboard.views import *
from core.erp.views.product.views import *
from core.erp.views.sale.views import *
from core.erp.views.ticket.views import *
from core.erp.views.cash.views import *
from core.erp.views.taller.views import *

app_name = 'erp'

urlpatterns = [
     # category
    path('category/list/', CategoryListView.as_view(), name='category_list'),
    path('category/add/', CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    # client
    path('client/list/', ClientListView.as_view(), name='client_list'),
    path('client/add/', ClientCreateView.as_view(), name='client_create'),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    # product
    path('product/list/', ProductListView.as_view(), name='product_list'),
    path('product/add/', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    # home
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # sale
    path('sale/list/', SaleListView.as_view(), name='sale_list'),
    path('sale/add/', SaleCreateView.as_view(), name='sale_create'),
    path('sale/delete/<int:pk>/', SaleDeleteView.as_view(), name='sale_delete'),
    path('sale/update/<int:pk>/', SaleUpdateView.as_view(), name='sale_update'),
    path('sale/invoice/pdf/<int:pk>/', SaleInvoicePdfView.as_view(), name='sale_invoice_pdf'),
    # ticket
    path('ticket/list/', TicketListView.as_view(), name='ticket_list'),
    path('ticket/add/', TicketCreateView.as_view(), name='ticket_create'),
    path('ticket/delete/<int:pk>/', TicketDeleteView.as_view(), name='ticket_delete'),
    path('ticket/update/<int:pk>/', TicketUpdateView.as_view(), name='ticket_update'),
    path('ticket/invoice/pdf/<int:pk>/', TicketInvoicePdfView.as_view(), name='ticket_invoice_pdf'),
    # cash
    path('cash/main/', CashFlowView.as_view(), name='cash_flow'),
    path('cash/open/', CashOpenView.as_view(), name='cash_open'),
    path('cash/open/detail/', CashOpenDetailView.as_view(), name='open_detail'),
    path('cash/close/', CashCloseView.as_view(), name='cash_close'),
    path('cash/close/detail/', CashCloseDetailView.as_view(), name='close_detail'),
    path('cash/close/banqueado/', CashCloseBanqueadoView.as_view(), name='close_banqueado'),
    path('cash/close/detail2/', CashCloseDetailView2.as_view(), name='close_detail2'),
    path('cash/gasto_list/', GastoListView.as_view(), name='gasto_list'),
    path('cash/gasto_add/', GastoCreateView.as_view(), name='gasto_create'),
    path('cash/gasto_update/<int:pk>/', GastoUpdateView.as_view(), name='gasto_update'),
    path('cash/gasto_delete/<int:pk>/', GastoDeleteView.as_view(), name='gasto_delete'),
    path('cash/balance_dia/', BalanceDiaView.as_view(), name='balance_dia'),
    path('cash/report/', CashReportView.as_view(), name='cash_report'),
    # taller
    path('taller/list/', TrabajoListView.as_view(), name='trabajo_list'),
    path('taller/add/', TrabajoCreateView.as_view(), name='trabajo_create'),
    path('taller/update/<int:pk>/', TrabajoUpdateView.as_view(), name='trabajo_update'),
    path('taller/delete/<int:pk>/', TrabajoDeleteView.as_view(), name='trabajo_delete'),
    path('taller/invoice/pdf/<int:pk>/', TrabajoInvoicePdfView.as_view(), name='trabajo_invoice_pdf'),
    path('taller/cliente_list/', ClienteTrabajoListView.as_view(), name='clientetrabajo_list'),
    path('taller/cliente_add/', ClienteTrabajoCreateView.as_view(), name='clientetrabajo_create'),
    path('taller/cliente_update/<int:pk>/', ClienteTrabajoUpdateView.as_view(), name='clientetrabajo_update'),
    path('taller/cliente_delete/<int:pk>/', ClienteTrabajoDeleteView.as_view(), name='clientetrabajo_delete'),
    path('taller/list2/', TrabajoListView2.as_view(), name='trabajo_list2'),
    path('taller/add2/', TrabajoCreateView2.as_view(), name='trabajo_create2'),
    path('taller/update2/<int:pk>/', TrabajoUpdateView2.as_view(), name='trabajo_update2'),
    path('taller/delete2/<int:pk>/', TrabajoDeleteView2.as_view(), name='trabajo_delete2'),
    path('taller/invoice2/pdf/<int:pk>/', TrabajoInvoicePdfView2.as_view(), name='trabajo_invoice_pdf2'),
]
