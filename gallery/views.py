import os
from itertools import zip_longest

from django.shortcuts import render

from gallery.apps import GalleryConfig
from gallery.forms import GenreForm, MessageForm
from gallery.models import Picture, Genre, Message
from gallery.tasks import send_tg_message


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
    if form.cleaned_data.get('genres') == [_.id for _ in Genre.objects.all()] or not form.cleaned_data.get('genres'):
        pictures = list(grouper(Picture.objects.all(), 3))
    else:
        pictures = Picture.objects.filter(genre_id__in=[_.id for _ in form.cleaned_data.get('genres')])
        pictures = list(grouper(pictures, 3))
    post_form = MessageForm(request.GET)
    if request.method == 'POST':
        post_form = MessageForm(request.POST)  # Загружаем форму для отправки сообщения
        if post_form.is_valid():  # Если данные валидны, то сохраняем и обнуляем данные
            post_form.save()
            name, email, text = Message.objects.last().name, Message.objects.last().email, Message.objects.last().text
            send_tg_message.delay(name, email, text)  # Передает в телеграм сообщение владельцу
            post_form = MessageForm()
    data = dict(pictures=pictures, form=form, post_form=post_form)
    return render(request, os.path.join(GalleryConfig.name, 'index.html'), context=data)


def picture_detail(request, pk):
    obj = Picture.objects.get(pk=pk)
    return render(request, os.path.join(GalleryConfig.name, 'detail.html'), context={'object': obj})
