from django.forms import ModelForm
from django import forms
from .models import Turno_Model


class Turno_Form (ModelForm):
    class Meta:
        model = Turno_Model
        fields = '__all__'
        widgets = {
            'Hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'Hora_fin': forms.TimeInput(attrs={'type': 'time'}),        
        }
    def __init__(self, *args, **kwargs):
        super(Turno_Form, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Excluye el campo 'Estado' de recibir los atributos comunes
            if field_name != 'Estado':
                field.widget.attrs.update({
                    'class': 'input',
                })