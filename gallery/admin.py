from django.contrib import admin
from django.utils.html import format_html

from gallery.models import Genre, Series, Picture, Message

admin.AdminSite.site_header = "Natalis Dominini моё арт-пространство."
admin.AdminSite.index_title = "Администрирование сайта."


# Register your models here.


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name',)
    list_display_link = ('pk', 'name',)


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_link = ('name',)


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):

    def image_tag(self, obj):
        """Создаем вид мини-картинки в админке под каждую картину"""
        return format_html('<img src="{}" style="max-width:100px; max-height:100px"/>'.format(obj.picture.url))

    image_tag.short_description = 'Фотка картины'
    list_display = (
                    'pk', 'genre', 'series', 'series_number', 'name', 'size', 'paint_property', 'picture',
                    'description', 'image_tag')
    list_display_links = (
                    'pk', 'genre', 'series', 'series_number', 'name', 'size', 'paint_property', 'picture',
                    'description', 'image_tag')
    list_filter = ('id', 'name',)
    exclude = ('name', 'description', 'series_number',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'email', 'text', 'created_at',)
    list_display_links = ('pk', 'name', 'email', 'text', 'created_at',)
    list_filter = ('created_at',)