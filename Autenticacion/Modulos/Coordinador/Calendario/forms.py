from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from Modulos.Coordinador.Calendario.models import Calendario_Model, TurnUsuario_Model


class Calendario_Form (ModelForm):
    class Meta:
        model = Calendario_Model
        fields = ['Fecha_inicio','Fecha_fin']
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
        for field in self.fields.values():
            field.widget.attrs.update({
            'class': 'input',
            'required': 'required'
        })
            
    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get("Fecha_inicio")
        fecha_fin = cleaned_data.get("Fecha_fin")

        if fecha_fin and fecha_inicio and fecha_fin <= fecha_inicio:
            self.add_error('Fecha_fin', "La fecha fin debe ser posterior a la fecha de inicio.")

        return cleaned_data  

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
        for field in self.fields.values():
            field.widget.attrs.update({
            'class': 'input',
            'required': 'required'
        })


