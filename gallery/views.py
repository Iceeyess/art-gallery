import os

from django.shortcuts import render

from gallery.apps import GalleryConfig
from gallery.forms import GenreForm, MessageForm
from gallery.models import Picture, Genre


# Create your views here.


def index(request, *args, **kwargs):
    """Главная страница"""
    form = GenreForm(request.GET)  # Загружаем форму для добавления картины
    form.is_valid()
    # if request.method == 'GET':
    if form.cleaned_data.get('genres') == [_.id for _ in Genre.objects.all()] or not form.cleaned_data.get('genres'):
        pictures = Picture.objects.all()
    else:
        pictures = Picture.objects.filter(genre_id__in=[_.id for _ in form.cleaned_data.get('genres')])
    post_form = MessageForm(request.POST)
    if request.method == 'POST':
        if post_form.is_valid():
            post_form.save()
    data = dict(pictures=pictures, form=form, post_form=post_form)
    return render(request, os.path.join(GalleryConfig.name,'index.html'), context=data)