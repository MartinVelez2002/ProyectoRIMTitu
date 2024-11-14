from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from Modulos.Coordinador.Calendario.models import Calendario_Model, TurnUsuario_Model
from Modulos.Login.models import Usuario

class Calendario_Form (ModelForm):
    class Meta:
        model = Calendario_Model
        fields = ['fecha_inicio','fecha_fin']
        widgets = {
            'fecha_inicio': forms.TimeInput(
                attrs={
                    'type': 'date'}),
            'fecha_fin': forms.TimeInput(
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
        fecha_inicio = cleaned_data.get("fecha_inicio")
        fecha_fin = cleaned_data.get("fecha_fin")

        if fecha_fin and fecha_inicio and fecha_fin <= fecha_inicio:
            self.add_error('fecha_fin', "La fecha fin debe ser posterior a la fecha de inicio.")

        return cleaned_data  

class TurnUsuarioUbicacion_Form (ModelForm):
    class Meta:
        model = TurnUsuario_Model
        fields = ['calendario', 'turno', 'usuario', 'ubicacion']
        widgets = {
            'usuario': forms.Select(),
            'calendario': forms.Select(),
            'turno': forms.Select(),
            'ubicacion': forms.Select(),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filtrar usuarios para mostrar solo los que no son superusuarios y tienen el rol de "Agente"
        self.fields['usuario'].queryset = Usuario.objects.filter(
            rol__name="Agente"
        )
        
        # Aplicar atributos comunes a todos los campos
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'input',
                'required': 'required'
            })


