from django.forms import ModelForm
from django import forms
from .models import Turno_Model


class Turno_Form (ModelForm):
    class Meta:
        model = Turno_Model
        fields = ['hora_inicio','hora_fin']
        widgets = {
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time'}),        
        }
    
    def __init__(self, *args, **kwargs):
        super(Turno_Form, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
            'class': 'input',
            'required': 'required'
        })