from django import forms
from Modulos.Prioridad.models import Prioridad

class PrioridadForms(forms.ModelForm):
    class Meta:
        model = Prioridad
        fields= '__all__'
        Descripcion = forms.CharField(max_length=30)

    def __str__(self):
        return f'{self.Descripcion}'