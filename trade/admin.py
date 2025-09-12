from django.contrib import admin

from trade.models import PreOrder, Order, OrderItem, CardContact


# Register your models here.
@admin.register(PreOrder)
class PreOrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'client_ip', 'item', 'quantity')
    list_display_link = ('pk', 'client_ip', 'item', 'quantity')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'order_number', 'client_ip', 'total_amount')
    list_display_link =  ('pk', 'order_number', 'client_ip', 'total_amount')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('pk', 'order', 'item', 'quantity', 'price')
    list_display_link =  ('pk', 'order', 'item', 'quantity', 'price')
    list_filter = ('order', 'item')

@admin.register(CardContact)
class CardContactAdmin(admin.ModelAdmin):
    list_display = ('pk', 'order', 'name', 'email', 'address', 'created_at', 'updated_at')
    list_display_link = ('pk', 'order', 'name', 'email', 'address', 'created_at', 'updated_at')
    list_filter = ('order', 'name', 'email')