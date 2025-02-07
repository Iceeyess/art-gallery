from email.policy import default

from django.db import models
from django.db.models import DO_NOTHING, CharField


NULLABLE = dict(null=True, blank=True)
size = dict(_40x60='40x60 см', _30x40='30x40 см', _50x60='50x60 см', _20x20='20x20 см')
paint = dict(oil='масляная краска', acrylic='акриловая краска', tempera='темпера краска')
# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name='жанр', help_text='введите жанр', **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'
        ordering = ['pk', ]

class Series(models.Model):
    name = models.CharField(max_length=100, verbose_name='серия',
                            help_text='серия, например, птица или обезьянки и т.д.', **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'серия'
        verbose_name_plural = 'серии'
        ordering = ['pk', ]

class Picture(models.Model):

    @property
    def get_name(self):
        return f'{self.series.name} {self.id}'

    @property
    def get_description(self):
        return f'Наименование модели - {self.get_name}, материал - {self.paint_property}, размер - {self.size}'

    genre = models.ForeignKey(Genre, on_delete=DO_NOTHING, help_text='внешний ключ на жанр')
    series = models.ForeignKey(Series, on_delete=DO_NOTHING, help_text='внешний ключ на стиль')
    name = models.CharField(max_length=100, default=get_name, help_text='серия плюс номер', **NULLABLE)
    size = models.CharField(choices=size, max_length=None, verbose_name='размер', help_text='выберите размер')
    paint_property = models.CharField(choices=paint, verbose_name='краска', help_text='выберите свойство краски')
    picture = models.ImageField(upload_to='gallery/', verbose_name='картина', help_text='загрузите картину')
    description = models.TextField(verbose_name='описание', default=get_description, help_text='опишите картину',
                                   **NULLABLE)



    def __str__(self):
        return f'Картина №{self.id}, стиль - {self.series}'

    class Meta:
        verbose_name = 'картина'
        verbose_name_plural = 'картины'
        ordering = ['pk', ]