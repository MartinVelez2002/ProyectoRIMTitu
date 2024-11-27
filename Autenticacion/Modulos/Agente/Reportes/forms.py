from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from .models import CabIncidente_Model, DetIncidente_Model


class CabIncidente_Form(ModelForm):
    class Meta:
        model = CabIncidente_Model
        fields = ['novedad', 'prioridad']

    def __init__(self, *args, **kwargs):
        super(CabIncidente_Form, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
                'required': 'required'
            })

    def clean_prioridad(self):
        prioridad = self.cleaned_data.get('prioridad')
        valid_prioridades = [choice[0] for choice in self.fields['prioridad'].choices]
        if prioridad not in valid_prioridades:
            raise ValidationError("La prioridad seleccionada no es válida.")
        return prioridad


class DetalleIncidente_Form(ModelForm):
    class Meta:
        model = DetIncidente_Model
        fields = ['evidencia', 'descripcion', 'comentarios_adicionales']
        widgets = {
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe detalladamente el seguimiento del incidente'
            }),
            'comentarios_adicionales': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Agrega comentarios adicionales (opcional)'
            }),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicar clase y atributo required a todos los campos excepto 'comentarios_adicionales'
        for field_name, field in self.fields.items():
            if field_name != 'comentarios_adicionales':
                field.widget.attrs.update({'class': 'form-control', 'required': 'required'})


        



    def clean_evidencia(self):
        evidencia = self.cleaned_data.get('evidencia')

        # Validar tamaño máximo del archivo (5 MB)
        max_size_mb = 50
        if evidencia and evidencia.size > max_size_mb * 1024 * 1024:
            raise forms.ValidationError(f"El archivo no debe exceder los {max_size_mb} MB.")

        # Verificar tipo MIME permitido
        valid_mimetypes = [
            'image/jpeg', 'image/png', 'image/gif', 
            'video/mp4', 'video/quicktime', 'video/x-msvideo'
        ]
        
        if evidencia and evidencia.content_type not in valid_mimetypes:
            raise ValidationError("El tipo de archivo no está permitido.")
        return evidencia

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')
        if not descripcion or len(descripcion.strip()) < 15:
            raise ValidationError("La descripción debe ser más detallada (mínimo 15 caracteres).")
        return descripcion

