from datetime import datetime
import os
from itertools import zip_longest

from django.http import HttpResponse
from django.shortcuts import render
from ipware import get_client_ip
from gallery.apps import GalleryConfig
from gallery.forms import GenreForm, MessageForm
from gallery.models import Picture, Genre, Message
from gallery.tasks import send_tg_message
from trade.models import PreOrder
from django.views.decorators.cache import cache_page


# Create your views here.
def grouper(iterable, n, fillvalue=None):
    """Разбивает список на группы по n элементов.
    Данная разбивка нужна для отображения карточек-картин на одной линии по n-элементов"""
    args = [iter(iterable)] * n
    groups = zip_longest(*args, fillvalue=fillvalue)
    return [[item for item in group if item is not None] for group in groups]


def index(request, *args, **kwargs):
    """Главная страница
    На главной странице 2 формы: Форма фильтрации жанров с методом GET, и форма обратной связи с методом POST."""
    form = GenreForm(request.GET)  # Загружаем форму для добавления картины
    form.is_valid()
    client_ip, _ = get_client_ip(request)  # IP address
    if form.cleaned_data.get('genres') == [_.id for _ in Genre.objects.all()] or not form.cleaned_data.get('genres'):
        pictures = list(grouper(Picture.objects.all(), 3))
    else:
        pictures = Picture.objects.filter(genre_id__in=[_.id for _ in form.cleaned_data.get('genres')])
        pictures = list(grouper(pictures, 3))
    post_form = MessageForm(request.GET)
    if request.method == 'POST':
        post_form = MessageForm(request.POST)  # Загружаем форму для отправки сообщения
        if post_form.is_valid():  # Если данные валидны, то сохраняем и обнуляем данные
            form = post_form.save()
            form.client_ip = client_ip
            form.save()
            send_tg_message.delay(form.name, form.email, form.text, form.client_ip, form.created_at)  # Передает в телеграм сообщение владельцу
            post_form = MessageForm()
    data = dict(pictures=pictures, form=form, post_form=post_form,
                preorder_list=[preorder_item.item for preorder_item in PreOrder.objects.filter(client_ip=client_ip)])
    return render(request, os.path.join(GalleryConfig.name, 'index.html'), context=data)

def picture_detail(request, pk):
    client_ip, _ = get_client_ip(request)  # IP address
    obj = Picture.objects.get(pk=pk)
    preorder_list = [preorder_item.item for preorder_item in PreOrder.objects.filter(client_ip=client_ip)]
    return render(request, os.path.join(GalleryConfig.name, 'detail.html'), context={'object': obj,
                                                                                     'preorder_list': preorder_list})
def handler404(request, exception):
    return render(request, os.path.join(GalleryConfig.name, '404.html'), status=404)

def handler500(request):
    return render(request, os.path.join(GalleryConfig.name, '500.html'), status=500)

def handler403(request, exception):
    return render(request, os.path.join(GalleryConfig.name, '403.html'), status=403)

def handler400(request, exception):
    return render(request, os.path.join(GalleryConfig.name, '400.html'), status=400)

@cache_page(60 * 60)
def yml_feed(request):
    """Функция для отображения XML структуры для Yandex для фид товаров"""
    pictures = Picture.objects.all()

    yml_content = ['<?xml version="1.0" encoding="UTF-8"?>']
    yml_content.append('<yml_catalog date="{}">'.format(datetime.now().strftime("%Y-%m-%d %H:%M")))
    yml_content.append('  <shop>')
    yml_content.append('    <name>Natalis Domini(Наталис Домини) - авторские картины</name>')
    yml_content.append('    <company>Natalis Domini(Наталис Домини)</company>')
    yml_content.append('    <url>https://www.natalis-domini.ru/</url>')
    yml_content.append('    <currencies>')
    yml_content.append('      <currency id="RUR" rate="1"/>')
    yml_content.append('    </currencies>')
    yml_content.append('    <categories>')
    yml_content.append('      <category id="1">Картины маслом</category>')
    yml_content.append('    </categories>')
    yml_content.append('    <offers>')

    for picture in pictures:
        yml_content.append('      <offer id="{}">'.format(picture.pk))
        yml_content.append('        <url>https://www.natalis-domini.ru/{}</url>'.format(picture.pk))
        yml_content.append('        <price>{}</price>'.format(int(picture.price)))
        yml_content.append('        <currencyId>RUR</currencyId>')
        yml_content.append('        <categoryId>1</categoryId>')
        yml_content.append('        <picture>https://www.natalis-domini.ru{}</picture>'.format(picture.picture.url))
        yml_content.append('        <name>{}</name>'.format(picture.name))
        yml_content.append('        <description>{}</description>'.format(picture.description))
        yml_content.append('        <artist>Natalis Domini</artist>')
        yml_content.append('        <dimensions>{}</dimensions>'.format('/'.join(picture.size[1:].split('x') + ['0.5'])))
        yml_content.append('      </offer>')

    yml_content.append('    </offers>')
    yml_content.append('  </shop>')
    yml_content.append('</yml_catalog>')

    return HttpResponse('\n'.join(yml_content), content_type='application/xml')