from django.forms import forms

from gallery.models import Picture


class PictureForms(forms.Form):
    class Meta:
        model = Picture

    def clean(self):
        clean = self.cleaned_data
        pass