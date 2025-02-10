from django import forms

from gallery.models import Genre



class GenreForm(forms.Form):
    # all = forms.BooleanField(label='Все', required=False)
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Выберите жанры:",
        help_text="Можно выбрать несколько жанров.",
    )

