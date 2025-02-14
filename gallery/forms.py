from django import forms
from django.db.models import CharField, TextField, EmailField
from django.forms import Textarea

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

    class Meta:
        model = Message
        fields = '__all__'
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

    def clean_email(self):
        """Валидация почты, дается 3 попытки отправки сообщений с одного email"""
        email = self.cleaned_data.get('email')
        if len([_.email for _ in Message.objects.filter(email=email)]) >= 3:
            raise forms.ValidationError('Дается 3 попытки отправлять сообщения от одного email.')

        return email