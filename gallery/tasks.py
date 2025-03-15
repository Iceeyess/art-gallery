import requests

from celery import shared_task
from django.conf import settings


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
