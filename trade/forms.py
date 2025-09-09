from django import forms
from captcha.fields import CaptchaField
from trade.models import CardContact
import re


class OrderForm(forms.ModelForm):
    captcha = CaptchaField(
        label='Введите код с картинки',
        error_messages={'invalid': 'Неверный код с картинки'}
    )

    class Meta:
        model = CardContact
        fields = ['name', 'email', 'phone', 'address']
        labels = {
            'name': 'ФИО',
            'email': 'Email',
            'phone': 'Телефон',
            'address': 'Адрес доставки',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иванов Иван Иванович'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@mail.ru'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 999 123-45-67'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3,
                                             'placeholder': 'г. Москва, ул. Примерная, д. 1, кв. 1, индекс 123456'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            # Проверка формата телефона
            phone_regex = r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$'
            if not re.match(phone_regex, phone):
                raise forms.ValidationError('Введите корректный номер телефона')
        return phone

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name and len(name.split()) < 2:
            raise forms.ValidationError('Введите полное ФИО (минимум 2 слова)')
        return name

    def clean_address(self):
        address = self.cleaned_data.get('address')
        if address and len(address) < 20:
            raise forms.ValidationError('Адрес должен содержать не менее 20 символов')
        return address