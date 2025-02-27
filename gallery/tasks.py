import requests

from celery import shared_task
from django.conf import settings


@shared_task
def send_tg_message(name, email, text):
    method = 'sendMessage'
    chat_id = settings.TG_CHAT_ID
    url = settings.TG_API_LINK + settings.TG_TOKEN_ACCESS_KEY + '/' + method
    params = {
        'chat_id': chat_id,
        # формируем текст сообщения с именем и текстом сообщения
        'text': f'Новое сообщение от имя - {name}, email - {email}, текст сообщения: "{text}"'
    }
    requests.get(url, params=params)
