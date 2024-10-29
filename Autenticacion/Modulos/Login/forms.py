from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.core.exceptions import ValidationError
from Modulos.Login.models import Usuario


class FormularioLogin(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(FormularioLogin, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'input'
        self.fields['password'].widget.attrs['class'] = 'input'


class FormularioRegistro(forms.ModelForm):
    password1 = forms.CharField(
        max_length=15,
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'required': 'required',
        })
    )

    password2 = forms.CharField(
        max_length=15,
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'required': 'required',
        })
    )


    class Meta:
        model = Usuario
        fields = ['username', 'email', 'cedula', 'nombre', 'apellido','rol']
        widgets = {
            'username': forms.TextInput(),
            'email': forms.EmailInput(),
            'cedula': forms.TextInput(attrs={'id':'inputCedula'}),
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
    
    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula')

        if cedula and len(cedula) > 10:
            self.add_error('cedula', 'La cédula debe tener un máximo de 10 caracteres.')  # Vincula el error al campo 'cedula'

        # Verificar si la cédula ya existe
        if cedula and Usuario.objects.filter(cedula=cedula).exists():
            self.add_error('cedula', 'Esta cédula ya está registrada.')  # Vincula el error al campo 'cedula'

        return cedula
    
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Las claves no coinciden')
        return cleaned_data
    
    

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user




    
















class ForgetPasswordForm(forms.Form):
    correo = forms.EmailField(  
            widget=forms.EmailInput(
            attrs=
            {'type': 'text',
             'class': 'input',
             'required': True}))

    
    
 
class CambiarPasswordForm(forms.Form):
    password1 = forms.CharField(max_length=15, widget=forms.PasswordInput(
        attrs={'type': 'password',
               'class': 'input',
               'required': 'required'
               }))

    password2 = forms.CharField(max_length=15, widget=forms.PasswordInput(
        attrs={'type': 'password',
               'class': 'input',
               'required': 'required'
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

        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Las claves no coinciden.')
        return cleaned_data