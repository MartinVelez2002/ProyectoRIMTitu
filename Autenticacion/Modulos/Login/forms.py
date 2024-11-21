from django import forms
from django.core.exceptions import ValidationError
from Modulos.Login.models import Usuario, Rol




class Rol_Form(forms.ModelForm):
    class Meta: 
        model = Rol
        fields = ['name']
        widgets = {'name': forms.TextInput(attrs={'class':'input'})}

    def clean_rol(self):
        rol = self.cleaned_data.get('name')
        if not rol.isalpha():
            raise ValidationError('El nombre del rol solo puede contener letras sin caracteres especiales ni números.')
        return rol

class FormularioLogin(forms.Form):
    username = forms.CharField(max_length=15)
    password = forms.CharField(widget=forms.PasswordInput)
  

    def __init__(self, *args, **kwargs):
        super(FormularioLogin, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'input'
        self.fields['password'].widget.attrs.update({'class': 'input', 'id': 'contraseña'})

    
# class FormularioLogin(forms.Form):
#     username = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class':'input'}))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'type': 'password',
#     'class': 'input', 
#     'id':'contraseña'}))
    
#     captcha = ReCaptchaField()   
    

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
            self.add_error('password1', 'Las contraseñas no coinciden.')
        return cleaned_data
    
    
    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula')
        if Usuario.objects.filter(cedula=cedula).exists():
            raise ValidationError("Este número de cédula ya está registrado.")
        
        
        cedula = str(cedula)
        if not cedula.isdigit():
            raise ValidationError('La cédula debe contener solo datos numéricos.')
        longitud = len(cedula)
        if longitud != 10:
            raise ValidationError('Cantidad de dígitos incorrecta.')
        
        coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
        total = 0
        
        for i in range(9):
            digito = int(cedula[i])
            coeficiente = coeficientes[i]
            producto = digito * coeficiente
            if producto > 9:
                producto -= 9
            total += producto
        
        digito_verificador = (total * 9) % 10
        if digito_verificador != int(cedula[9]):
            raise ValidationError('La cédula no es válida.')
        
        return cedula
        


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise ValidationError("Este correo electrónico ya está registrado.")
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Usuario.objects.filter(username=username).exists():
            raise ValidationError("Este nombre de usuario ya está registrado.")
        return username
    
    
class FormularioEditarPersonal(FormularioRegistro):
    class Meta(FormularioRegistro.Meta):
        fields = ['username', 'email', 'cedula', 'nombre', 'apellido', 'rol']

    def __init__(self, *args, **kwargs):
        super(FormularioEditarPersonal, self).__init__(*args, **kwargs)
        # Elimina los campos de contraseña del formulario
        if 'password1' in self.fields:
            del self.fields['password1']
        if 'password2' in self.fields:
            del self.fields['password2']
    
    def clean_username(self):
        username = self.cleaned_data['username']
        user = self.instance  # Obtiene el usuario actual que se está editando

        # Si el username no ha cambiado, no validamos la unicidad
        if username != user.username and Usuario.objects.filter(username=username).exists():
            raise ValidationError("El usuario ya está registrado.")
        
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        user = self.instance  # Obtiene el usuario actual que se está editando

        # Si el email no ha cambiado, no validamos la unicidad
        if email != user.email and Usuario.objects.filter(email=email).exists():
            raise ValidationError("El correo ya está registrado.")
        
        return email

    def clean_cedula(self):
        cedula = self.cleaned_data['cedula']
        user = self.instance  # Obtiene el usuario actual que se está editando

        # Si la cédula no ha cambiado, no validamos la unicidad
        if cedula != user.cedula and Usuario.objects.filter(cedula=cedula).exists():
            raise ValidationError("La cédula ya está registrada.") 
        return cedula
   
    



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
            self.add_error('password1', 'Las contraseñas no coinciden.')
        return cleaned_data