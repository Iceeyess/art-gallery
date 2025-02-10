import os

from django.shortcuts import render

from gallery.apps import GalleryConfig
from gallery.forms import GenreForm
from gallery.models import Picture, Genre


# Create your views here.


def index(request, *args, **kwargs):
    """Главная страница"""
    if request.method == 'GET':
        form = GenreForm(request.GET)  # Загружаем форму для добавления картины
        form.is_valid()
        if form.cleaned_data.get('genres') == [_.id for _ in Genre.objects.all()] or not form.cleaned_data.get('genres'):
            pictures = Picture.objects.all()
        else:
            pictures = Picture.objects.filter(genre_id__in=[_.id for _ in form.cleaned_data.get('genres')])
    elif request.method == 'POST':
        ...
    data = dict(pictures=pictures, form=form)
    return render(request, os.path.join(GalleryConfig.name,'index.html'), context=data)