from django import forms
from templatedjango.apptemplate.models import *

class DocumentForm(forms.ModelForm):

    imagen = forms.FileField(
        label='',
        widget=forms.FileInput(
            attrs={
                "id":"inputGroupFile01",                
                "class": "custom-file-input",
                "aria-describedby":"inputGroupFileAddon01"
            }
        ))

    class Meta:
        model = Productos
        fields = ('imagen',)  