from django.urls import path

from core.reports.views import *

urlpatterns = [
    # reports
    path('sale/', ReportSaleView.as_view(), name='sale_report'),
    path('ticket/', ReportTicketView.as_view(), name='ticket_report'),
]