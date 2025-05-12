from captcha.fields import CaptchaField
from django import forms
from gallery.models import Genre, Message


class GenreForm(forms.Form):
    """Форма фильтрации жанров"""
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Выберите жанры:",
        help_text="Можно выбрать несколько жанров.",
    )


class MessageForm(forms.ModelForm):
    captcha = CaptchaField(label='Введите код с картинки')

    class Meta:
        model = Message
        fields = ['name', 'email', 'text', ]
        labels = {
            'name': 'Имя',
            'email': 'Почта',
            'text': 'Сообщение',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'  # Стилизация формы
            self.fields[field_name].required = False  # убрал надпись Обязательное поле

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if email and len([_.email for _ in Message.objects.filter(email=email)]) >= 3:
            self.add_error(None, 'Дается 3 попытки отправлять сообщения от одного email.')
        return cleaned_data
