from django.forms import ModelForm
from django import forms
from Modulos.Coordinador.Calendario.models import Calendario_Model, TurnUsuario_Model


class Calendario_Form (ModelForm):
    class Meta:
        model = Calendario_Model
        fields = '__all__'
        widgets = {
            'Fecha_inicio': forms.TimeInput(
                attrs={
                    'type': 'date'}),
            'Fecha_fin': forms.TimeInput(
                attrs={
                    'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super(Calendario_Form, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Excluye el campo 'Estado' de recibir los atributos comunes
            if field_name != 'Estado':
                field.widget.attrs.update({
                    'class': 'input',
                })

class TurnUsuarioUbicacion_Form (ModelForm):
    class Meta:
        model = TurnUsuario_Model
        fields = ['Calendario', 'Turno', 'Usuario', 'Ubicacion']
        widgets = {
            'Usuario': forms.Select(),
            'Calendario': forms.Select(),
            'Turno': forms.Select(),
            'Ubicacion': forms.Select(),
        }
    def __init__(self, *args, **kwargs):
        super(TurnUsuarioUbicacion_Form, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Excluye el campo 'Estado' de recibir los atributos comunes
            if field_name != 'Estado':
                field.widget.attrs.update({
                    'class': 'input',
                })

