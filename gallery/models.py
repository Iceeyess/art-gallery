from email.policy import default

from django.db import models
from django.db.models import DO_NOTHING, CharField

NULLABLE = dict(null=True, blank=True)
size = dict(_40x60='40x60 см', _30x40='30x40 см', _50x60='50x60 см', _20x20='20x20 см')
paint = dict(oil='масляные', acrylic='акриловые', tempera='темпера')
materials = dict(thick_cardboard='плотный картон, хлопок', fiberboard_canvas='холст на ДВП, хлопок',
                 canvas_on_a_stretcher='холст на подрамнике')


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
    genre = models.ForeignKey(Genre, verbose_name='жанр', on_delete=DO_NOTHING, help_text='внешний ключ на жанр')
    series = models.ForeignKey(Series, verbose_name='серия', on_delete=DO_NOTHING, help_text='внешний ключ на стиль')
    series_number = models.PositiveIntegerField(verbose_name='порядковый номер серии',
                                                help_text='номер формируется автоматически', **NULLABLE)
    name = models.CharField(max_length=100, verbose_name='название', help_text='серия плюс номер', **NULLABLE)
    size = models.CharField(choices=size, max_length=100, verbose_name='размер', help_text='выберите размер')
    material = models.CharField(max_length=100, verbose_name='материал', help_text='выберите материал',
                                choices=materials)
    paint_property = models.CharField(max_length=100, choices=paint, verbose_name='краска',
                                      help_text='выберите свойство краски')
    picture = models.ImageField(upload_to='gallery/', verbose_name='путь к картине', help_text='загрузите картину')
    description = models.TextField(verbose_name='описание', help_text='опишите картину',
                                   **NULLABLE)

    def __str__(self):
        return f'Картина №{self.id}, стиль - {self.series}'

    def save(self, *args, **kwargs):
        """Переопределен для автосохранения полей self.name, self.description, self.series_number"""
        # Определяем последний сохраненный объект из этой же серии, СТРОГО ДО СОХРАНЕНИЯ В БД!
        num = getattr(Picture.objects.filter(series=self.series).order_by().last(), 'series_number', None)
        super().save(*args, **kwargs)
        self.series_number = num + 1 if num else 1  # Сохраняем № серии
        self.name = f'Серия {self.series.name} № {self.series_number}'
        self.description = (f'{self.name}, {paint.get(self.paint_property)} краски, размер '
                            f'{size.get(self.size)}')
        # Два раза вызов родительского сохранения из-за ID номера в БД
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'картина'
        verbose_name_plural = 'картины'
        ordering = ['pk', ]
