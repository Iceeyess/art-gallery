from django.contrib import admin

from gallery.models import Genre, Series, Picture


# Register your models here.
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', )
    list_display_link = ('pk', 'name', )

@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_display_link = ('name', )

@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ('pk', 'genre', 'series', 'name', 'size', 'paint_property', 'picture', 'description')
    list_display_links = ('pk', 'name', 'name', 'size', 'paint_property', )
    list_filter = ('id', 'name', )
