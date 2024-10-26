from django import forms
from Modulos.Prioridad.models import Prioridad_Model

class PrioridadForms(forms.ModelForm):
    class Meta:
        model = Prioridad_Model
        fields= '__all__'
        Descripcion = forms.CharField(max_length=30)
