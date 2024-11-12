from django import forms
from Modulos.Coordinador.Novedad.models import Novedad_Model, TipoNovedad_Model

class TipoNovedad_form(forms.ModelForm):
    class Meta:
        model = TipoNovedad_Model
        fields = ['Descripcion']
        widgets = {
            'Descripcion': forms.TextInput(
                attrs={'class': 'input'}
            )
        }

class Novedad_form(forms.ModelForm):
    class Meta:
        model = Novedad_Model
        fields = ['TipoNovedad', 'Descripcion']
        widgets = {
            'Descripcion': forms.TextInput(),
            'TipoNovedad': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super(Novedad_form, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
            'class': 'input',
            'required': 'required'
        })
