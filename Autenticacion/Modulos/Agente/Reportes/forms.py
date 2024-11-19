from django.forms import ModelForm
from django import forms
from .models import CabIncidente_Model, DetIncidente_Model


class CabIncidente_Form(ModelForm):
    class Meta:
        model = CabIncidente_Model
        fields = ['novedad', 'fecha', 'prioridad']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'})
        }
    
    def __init__(self, *args, **kwargs):
        super(CabIncidente_Form, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
            'class': 'input',
            'required': 'required'
        })
            
class DetalleIncidente_Form(ModelForm):
    class Meta:
        model = DetIncidente_Model
        fields = ['estado_incidente', 'evidencia','descripcion']

    def __init__(self, *args, **kwargs):
        super(DetalleIncidente_Form, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
            'class': 'input',
            'required': 'required'
        })
            
    def clean_evidencia(self):
        evidencia = self.cleaned_data.get('evidencia')

        # Verifica el tipo MIME (opcional)
        valid_mimetypes = ['image/jpeg', 'image/png', 'image/gif', 'video/mp4', 'video/quicktime', 'video/x-msvideo']
        if evidencia and evidencia.content_type not in valid_mimetypes:
            self.add_error('evidencia', "Tipo de archivo no permitido.")
        
        return evidencia