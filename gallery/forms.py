from django import forms
from django.db.models import CharField, TextField, EmailField
from django.forms import Textarea

from gallery.models import Genre, Message


class GenreForm(forms.Form):
    # all = forms.BooleanField(label='Все', required=False)
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
        widgets = {
            'name': Textarea(attrs={'class': 'form-control', 'rows': 1}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['email'].required = False
        self.fields['text'].required = False
