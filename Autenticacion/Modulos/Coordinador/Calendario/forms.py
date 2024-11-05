from django.forms import ModelForm
from django import forms
from Modulos.Coordinador.Calendario.models import Calendario_Model, Turno_Model, TurnUsuario_Model


class Turno_Form (ModelForm):
    class Meta:
        model = Turno_Model
        fields = '__all__'
        widgets = {
            'Hora_inicio': forms.TimeInput,
            'Hora_fin': forms.TimeInput,        
        }
        
