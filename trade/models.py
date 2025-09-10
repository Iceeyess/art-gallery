from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from gallery.models import Picture

# Create your models here.

NULLABLE = {'blank': True, 'null': True}


class PreOrder(models.Model):
    """Модель корзины(предзаказ). После утверждения, модель стирается.
    Используется как промежуточная таблица.
    Можно было бы привязать к юзеру, но в нашем случае регистрация и модели юзера не предусмотрено"""
    client_ip = models.GenericIPAddressField(verbose_name='IP-адрес клиента', **NULLABLE)
    item = models.ForeignKey(Picture, on_delete=models.CASCADE, verbose_name='товар', related_name='preorder_item')
    quantity = models.PositiveIntegerField(default=1, verbose_name='количество', validators=[MinValueValidator(1),
                                                                                             MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='дата обновления')


    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'корзины'

    def __str__(self):
        return f"Предзаказ для клиента {self.client_ip} ({self.item.name})"

    @property
    def total_price(self):
        return self.quantity * self.item.price

class Order(models.Model):
    """Модель заказа"""
    order_number = models.CharField(max_length=50, verbose_name='номер заказа', unique=True)
    client_ip = models.GenericIPAddressField(verbose_name='IP-адрес клиента', **NULLABLE)
    items = models.ManyToManyField(Picture, through='OrderItem', verbose_name='товары')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='общая сумма', default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='дата обновления')

    def __str__(self):
        return f"Заказ #{self.order_number}"

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'


class OrderItem(models.Model):
    """Промежуточная модель для товаров в заказе"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='заказ')
    item = models.ForeignKey(Picture, on_delete=models.CASCADE, verbose_name='товар')
    quantity = models.PositiveIntegerField(verbose_name='количество')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='цена за единицу')

    def __str__(self):
        return f"{self.item.name} - {self.quantity} шт."

    class Meta:
        verbose_name = 'позиция заказа'
        verbose_name_plural = 'позиции заказа'


class CardContact(models.Model):
    """Модель контактов для отправки товара покупателю"""
    order = models.OneToOneField(Order, on_delete=models.CASCADE, verbose_name='заказ', related_name='contacts')
    name = models.CharField(max_length=100, verbose_name='ФИО')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    address = models.TextField(verbose_name='Адрес доставки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='дата обновления')

    def __str__(self):
        return f"Контакты для заказа #{self.order.order_number}"

    class Meta:
        verbose_name = 'контакты'
        verbose_name_plural = 'контакты'


import uuid
from django.utils import timezone

def generate_order_number():
    """Генерация уникального номера заказа"""
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    unique_id = str(uuid.uuid4())[:8].upper()
    return f"ORDER-{timestamp}-{unique_id}"