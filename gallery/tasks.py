import datetime
import requests
from celery import shared_task
from django.conf import settings
from trade.models import PreOrder


@shared_task
def send_tg_message(name, email, text, ip_address, created_at):
    method = 'sendMessage'
    chat_id = settings.TG_CHAT_ID
    url = settings.TG_API_LINK + settings.TG_TOKEN_ACCESS_KEY + '/' + method
    params = {
        'chat_id': chat_id,
        # формируем текст сообщения с именем и текстом сообщения
        'text': f'Дата {created_at}, IP адрес {ip_address}, Новое сообщение от имя - {name}, '
                f'email - {email}, текст сообщения: "{text}"'
    }
    requests.get(url, params=params)


@shared_task
def send_tg_order_notification(order_number, total_amount, client_ip, name, email, phone, address, created_at,
                               order_items):
    """Отправка уведомления в Telegram о новом заказе с детальным содержимым"""
    method = 'sendMessage'
    chat_id = settings.TG_CHAT_ID
    url = settings.TG_API_LINK + settings.TG_TOKEN_ACCESS_KEY + '/' + method

    # Формируем текст сообщения о заказе
    message = f"🎨 *НОВЫЙ ЗАКАЗ НА САЙТЕ!*\n\n"
    message += f"📦 *Номер заказа:* #{order_number}\n"
    message += f"💰 *Общая сумма:* {total_amount} руб.\n"
    message += f"📅 *Дата заказа:* {created_at}\n"
    message += f"🌐 *IP адрес:* {client_ip}\n\n"

    # Добавляем детальное содержимое заказа
    message += f"🛒 *ДЕТАЛИ ЗАКАЗА:*\n"
    message += "┌" + "─" * 35 + "┐\n"

    total_items = 0
    for i, item in enumerate(order_items, 1):
        item_total = item['quantity'] * item['price']
        message += f"│ {i:2d}. {item['name'][:25]:<25} │\n"
        message += f"│     Кол-во: {item['quantity']:2d} шт. × {item['price']:6.2f} руб. │\n"
        message += f"│     Итого:  {item_total:8.2f} руб. │\n"
        if i < len(order_items):
            message += "├" + "─" * 35 + "┤\n"
        total_items += item['quantity']

    message += "└" + "─" * 35 + "┘\n"
    message += f"│ *Итого товаров:* {total_items} шт. │\n"
    message += f"│ *Общая сумма:* {total_amount:8.2f} руб. │\n"
    message += "└" + "─" * 35 + "┘\n\n"

    message += f"👤 *ДАННЫЕ КЛИЕНТА:*\n"
    message += f"• *ФИО:* {name}\n"
    message += f"• *Email:* {email}\n"
    message += f"• *Телефон:* {phone}\n"
    message += f"• *Адрес:* {address}\n\n"
    message += f"✅ *Заказ успешно создан!*"

    params = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"Ошибка отправки в Telegram: {e}")
        return False

@shared_task
def delete_preorder_items():
    """Функция удаления их корзины старых помеченных к покупке товаров.
    Если товар залежался более 1 часа, то удаляем его для всех покупателей. Функция мониторит раз в час."""
    systime = datetime.datetime.now()
    old_preorders = PreOrder.objects.filter(updated_at__lt=systime - datetime.timedelta(days=1))
    quantity = len(old_preorders)
    old_preorders.delete()
    print(f'Удалено {quantity} товаров из корзины')
    return None