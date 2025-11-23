from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.forms import modelformset_factory
from ipware import get_client_ip
from django import forms
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import json
from datetime import datetime


from gallery.models import Picture
from trade.models import PreOrder, CardContact, Order, OrderItem
from trade.forms import OrderForm
from trade.models import generate_order_number
from gallery.tasks import send_tg_order_notification


def mark_to_buy(request, pk):
    """Метод для пометки товара для покупки."""
    quantity = request.GET.get('quantity', 1)

    # Получаем next параметр или используем текущий URL как fallback
    next_url = request.GET.get('next') or request.META.get('HTTP_REFERER') or reverse('gallery:index')

    obj = get_object_or_404(Picture, pk=pk)
    client_ip, _ = get_client_ip(request)
    preorder_by_ip = PreOrder.objects.filter(client_ip=client_ip, item=obj)

    if not preorder_by_ip.exists():
        PreOrder.objects.create(item=obj, quantity=quantity, client_ip=client_ip)
    elif preorder_by_ip.exists():
        preorder_by_ip.delete()

    return redirect(next_url)


def pre_order_detail(request):
    """Редактирование корзины."""
    client_ip, _ = get_client_ip(request)
    queryset = PreOrder.objects.filter(client_ip=client_ip)

    pre_order_formset = modelformset_factory(
        PreOrder,
        fields=['quantity'],
        extra=0,
        can_delete=True,
        widgets={'quantity': forms.NumberInput(attrs={'min': 1, 'max': 10, 'class': 'form-control'})}
    )

    total_sum = 0

    if request.method == 'POST':
        formset = pre_order_formset(request.POST, queryset=queryset)
        if formset.is_valid():
            instances = formset.save(commit=False)

            for obj in formset.deleted_objects:
                obj.delete()

            for instance in instances:
                instance.save()

            return HttpResponseRedirect(reverse('trade:pre_order_detail'))
    else:
        formset = pre_order_formset(queryset=queryset)

    for pre_order in queryset:
        total_sum += pre_order.item.price * pre_order.quantity

    order_form = OrderForm()

    return render(request, 'trade/preorder_detail.html', {
        'formset': formset,
        'total_sum': total_sum,
        'preorder_items': queryset,
        'order_form': order_form
    })


def remove_from_cart(request, item_id):
    """Удаление товара из корзины"""
    client_ip, _ = get_client_ip(request)
    item = get_object_or_404(PreOrder, id=item_id, client_ip=client_ip)
    item.delete()
    return redirect('trade:pre_order_detail')


@csrf_exempt
@transaction.atomic
def create_order(request):
    """Создание заказа через AJAX"""
    if request.method == 'POST':
        try:
            client_ip, _ = get_client_ip(request)
            preorder_items = PreOrder.objects.filter(client_ip=client_ip)

            if not preorder_items.exists():
                return JsonResponse({'success': False, 'error': 'Корзина пуста'})

            form = OrderForm(request.POST)

            if form.is_valid():
                # Создаем заказ с простым номером
                order_number = generate_order_number()
                total_amount = sum(item.item.price * item.quantity for item in preorder_items)

                order = Order.objects.create(
                    order_number=order_number,
                    client_ip=client_ip,
                    total_amount=total_amount
                )

                # Добавляем товары в заказ и формируем список для Telegram
                order_items = []
                for preorder_item in preorder_items:
                    order_item = OrderItem.objects.create(
                        order=order,
                        item=preorder_item.item,
                        quantity=preorder_item.quantity,
                        price=preorder_item.item.price
                    )
                    order_items.append({
                        'name': preorder_item.item.name,
                        'quantity': preorder_item.quantity,
                        'price': float(preorder_item.item.price)
                    })

                # Сохраняем контакты
                contact = form.save(commit=False)
                contact.order = order
                contact.save()

                # Очищаем корзину
                preorder_items.delete()

                # Отправляем уведомление в Telegram с содержимым заказа
                send_tg_order_notification.delay(
                    order_number=order_number,
                    total_amount=float(total_amount),
                    client_ip=client_ip,
                    name=contact.name,
                    email=contact.email,
                    phone=contact.phone,
                    address=contact.address,
                    created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    order_items=order_items  # Передаем содержимое заказа
                )

                # Формируем данные для ответа
                order_data = {
                    'order_number': order_number,
                    'total_amount': float(total_amount),
                    'contact': {
                        'name': contact.name,
                        'email': contact.email,
                        'phone': contact.phone,
                        'address': contact.address
                    }
                }

                return JsonResponse({
                    'success': True,
                    'message': f'Ваш заказ № {order_number} успешно оформлен!',
                    'order': order_data
                })
            else:
                return JsonResponse({'success': False, 'errors': form.errors})

        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Произошла ошибка: {str(e)}'})

    return JsonResponse({'success': False, 'error': 'Неверный метод запроса'})