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
        fields = ['TipoNovedad', 'Descripcion', 'Estado']
        widgets = {
            'Descripcion': forms.TextInput(),
            'TipoNovedad': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super(Novedad_form, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Excluye el campo 'Estado' de recibir los atributos comunes
            if field_name != 'Estado':
                field.widget.attrs.update({
                    'class': 'form-control',
                    'required': True
                })
