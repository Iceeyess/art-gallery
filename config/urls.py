"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.static import serve
from django.contrib.sitemaps import Sitemap
from gallery.models import Picture
from django.contrib.sitemaps.views import sitemap


class PictureSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Picture.objects.all()

    def lastmod(self, obj):
        return obj.created_at


sitemaps = {
    'pictures': PictureSitemap,
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),
    path('', include('gallery.urls', namespace='gallery')),
    path('trade/', include('trade.urls', namespace='trade')),
    path('robots.txt', serve, {
        'document_root': settings.STATIC_ROOT,
        'path': 'robots.txt'
    }),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'gallery.views.handler404'
handler500 = 'gallery.views.handler500'
handler403 = 'gallery.views.handler403'
handler400 = 'gallery.views.handler400'