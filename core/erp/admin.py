from django.contrib import admin
from core.erp.models import *
from import_export.admin import ImportExportModelAdmin

admin.site.register(Category)
admin.site.register(TipoPago)
admin.site.register(AbrirCaja)
admin.site.register(CerrarCaja)
admin.site.register(BanqueadoCaja)
admin.site.register(GastoCaja)
admin.site.register(Product, ImportExportModelAdmin)
admin.site.register(Client)
admin.site.register(Sale)
admin.site.register(DetSale)
admin.site.register(Ticket)
admin.site.register(DetTicket)
admin.site.register(StatusTrabajo)
admin.site.register(Trabajo)
admin.site.register(Trabajo2)
admin.site.register(ClienteTrabajo)

