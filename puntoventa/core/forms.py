from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100, label='Nombre de usuario')
    email = forms.EmailField(label='Dirección de correo electrónico')
    name = forms.CharField(max_length=100, label='Nombre completo')
    phone = forms.CharField(max_length=15, label='Número de teléfono')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirmar contraseña')
