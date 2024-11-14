from django import forms
from .models import Reportes_Model

class Reportes_Form_C(forms.ModelForm):
    class Meta:
        model = Reportes_Model
        fields = ['novedad', 'prioridad', 'evidencia', 'descripcion']
    
    def __init__(self, *args, **kwargs):
        super(Reportes_Form_C, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'input'
            })
