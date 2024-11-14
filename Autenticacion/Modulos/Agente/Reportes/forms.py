from django import forms
from .models import Reportes_Model

class Reportes_Form_C(forms.ModelForm):
    class Meta:
        model = Reportes_Model
        fields = ['novedad', 'prioridad', 'evidencia', 'descripcion']
        # widgets = {
        #     'descripcion': forms.Textarea(),
        # }
    def __init__(self, *args, **kwargs):
        super(Reportes_Form_C, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            if field.name != 'descripcion':
                field.widget.attrs.update({
                    'class': 'input',
                    'required': True
                })


    def clean_evidencia(self):
        evidencia = self.cleaned_data.get('evidencia')

        # Verifica el tipo MIME (opcional)
        valid_mimetypes = ['image/jpeg', 'image/png', 'image/gif', 'video/mp4', 'video/quicktime', 'video/x-msvideo']
        if evidencia and evidencia.content_type not in valid_mimetypes:
            self.add_error("Tipo de archivo no permitido.")
        
        return evidencia