from django import forms
from Modulos.Coordinador.Ubicacion.models import Ubicacion_Model

class Ubicacion_Form(forms.ModelForm):
    class Meta:
        model = Ubicacion_Model
        fields = ['lugar', 'sector']
        widgets = {
            'lugar': forms.TextInput(attrs={
                'id':'lugar_input',
                }),
            'sector': forms.TextInput(attrs={
                'id':'sector_input'
            })
        }
    def __init__(self, *args, **kwargs):
        super(Ubicacion_Form, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
            'class': 'input',
            'required': 'required'
        })

# class Ubicacion_Form(forms.ModelForm):
#     class Meta:
#         model = Ubicacion_Model
#         fields = ['lugar', 'sector', 'calleprincipal']
#         widgets = {
#             'lugar': forms.TextInput(attrs={
#                 'id':'lugar_input'}),
#             'sector': forms.TextInput(attrs={
#                 'id':'sector_input'}),
#             'callePrincipal': forms.TextInput(
#                 attrs={
#                 'id':'calle_principal_input'}),
#                 }
        
        
                    
#     def __init__(self, *args, **kwargs):
#         super(Ubicacion_Form, self).__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs.update({
#             'class': 'input',
#             'required': 'required'
#         })