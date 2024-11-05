from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.core.exceptions import ValidationError
from Modulos.Login.models import Usuario


class FormularioLogin(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(FormularioLogin, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'input'
        self.fields['password'].widget.attrs.update({'class': 'input', 'id': 'contraseña'})



class FormularioRegistro(forms.ModelForm):
    password1 = forms.CharField(
        max_length=15,
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'required': 'required',
            'id':'passw1'
        })
    )

    password2 = forms.CharField(
        max_length=15,
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'required': 'required',
            'id':'passw2'
        })
    )


    class Meta:
        model = Usuario
        fields = ['username', 'email', 'cedula', 'nombre', 'apellido','rol']
        widgets = {
            'username': forms.TextInput(),
            'email': forms.EmailInput(),
            'cedula': forms.TextInput(),
            'nombre': forms.TextInput(),
            'apellido': forms.TextInput(),
            'rol': forms.Select()
        }
        
    def __init__(self, *args, **kwargs):
        super(FormularioRegistro, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
            'class': 'input',
            'required': 'required'
        })
    
    
    """
        Validar contraseñas
        Método que valida que ambas contraseñas sean iguales, antes de ser encriptadas y guardadas
        en la base de datos. Se retorna la clave válida.
    """
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Las claves no coinciden')
        return cleaned_data
    



class ForgetPasswordForm(forms.Form):
    correo = forms.EmailField(  
            widget=forms.EmailInput(
            attrs=
            {'type': 'text',
             'class': 'input',
             'required': 'required'}))

    
    
 
class CambiarPasswordForm(forms.Form):
    password_actual = forms.CharField(max_length=15, widget=forms.PasswordInput(
        attrs={'type': 'password',
               'class': 'input',
               'id':'passw_actual'
              
               }), required=False)
    
    password1 = forms.CharField(max_length=15, widget=forms.PasswordInput(
        attrs={'type': 'password',
               'class': 'input',
               'required': 'required',
               'id':'passw_new'
               }))

    password2 = forms.CharField(max_length=15, widget=forms.PasswordInput(
        attrs={'type': 'password',
               'class': 'input',
               'required': 'required',
               'id':'passw_new_conf'
               }))

  
    """
        Validar contraseñas
        Método que valida que ambas contraseñas sean iguales, antes de ser encriptadas y guardadas
        en la base de datos. Se retorna la clave válida.
    """
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        password_actual = cleaned_data.get('password_actual')
        
        if password1 and password2 and password1 != password2:
            self.add_error('password1', 'Las claves no coinciden.')
        return cleaned_data