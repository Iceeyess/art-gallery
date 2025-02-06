import os

from django.shortcuts import render

from gallery.apps import GalleryConfig


# Create your views here.
def index(request):
    return render(request, os.path.join(GalleryConfig.name,'index.html'))