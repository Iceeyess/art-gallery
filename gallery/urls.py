from gallery.apps import GalleryConfig
from django.urls import path

from gallery.views import index, picture_detail

app_name = GalleryConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('<int:pk>', picture_detail, name='detail'),
]
