from django.urls import path

from gallery.views import index, picture_detail
from trade.apps import TradeConfig
from trade.views import mark_to_buy, pre_order_detail, remove_from_cart, create_order

app_name = TradeConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('mark_to_buy/<int:pk>/', mark_to_buy, name='mark_to_buy'),
    path('pre_order/', pre_order_detail, name='pre_order_detail'),
    path('remove_from_cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('create_order/', create_order, name='create_order'),
]
