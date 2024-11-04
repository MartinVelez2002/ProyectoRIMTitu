from django import forms
from Modulos.Coordinador.Novedad.models import Novedad_Model, TipoNovedad_Model

class TipoNovedad_form(forms.ModelForm):
    class Meta:
        model = TipoNovedad_Model
        fields = '__all__'
        widgets = {
            'Descripcion': forms.TextInput(
                attrs={'class': 'form-control'}
            )
        }


class Novedad_form(forms.ModelForm):
    class Meta:
        model = Novedad_Model
        fields = ['TipoNovedad','Descripcion','Estado'] 
        widgets = {
            'Descripcion': forms.TextInput(
                attrs={'class': 'form-control', 'required': True}
            ),
            'TipoNovedad': forms.Select(
                attrs={'class': 'form-control', 'required': True}
            ),
        }
