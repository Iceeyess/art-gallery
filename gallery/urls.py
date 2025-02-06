from gallery.apps import GalleryConfig
from django.urls import path

from gallery.views import index

app_name = GalleryConfig.name

urlpatterns = [
    path('', index, name='index'),
]
