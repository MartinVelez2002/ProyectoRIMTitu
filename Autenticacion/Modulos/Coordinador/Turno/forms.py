from django.forms import ModelForm
from django import forms
from .models import Turno_Model


class Turno_Form (ModelForm):
    class Meta:
        model = Turno_Model
        fields = ['Hora_inicio','Hora_fin']
        widgets = {
            'Hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'Hora_fin': forms.TimeInput(attrs={'type': 'time'}),        
        }
    
    def __init__(self, *args, **kwargs):
        super(Turno_Form, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
            'class': 'input',
            'required': 'required'
        })