from django.contrib import admin

from trade.models import PreOrder, Order


# Register your models here.
@admin.register(PreOrder)
class PreOrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'client_ip', 'item', 'quantity')
    list_display_link = ('pk', 'client_ip', 'item', 'quantity')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'order_number', 'client_ip', 'total_amount')
    list_display_link =  ('pk', 'order_number', 'client_ip', 'total_amount')