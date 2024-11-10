from django import forms
from Modulos.Coordinador.Ubicacion.models import Ubicacion_Model


class Ubicacion_Form(forms.ModelForm):
    class Meta:
        model = Ubicacion_Model
        fields = ['Sector', 'CallePrincipal', 'Interseccion', 'Estado']
        widgets = {
            'Sector': forms.TextInput(),
            'CallePrincipal': forms.TextInput(),
            'Interseccion': forms.TextInput(),
        }
        
        def __init__(self, *args, **kwargs):
            super(Ubicacion_Form, self).__init__(*args, **kwargs)
            for field in self.fields.items():
                if field != 'Estado':
                    field.widget.attrs.update({
                        'class': 'input',
                    })