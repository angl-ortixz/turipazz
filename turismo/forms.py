from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class RegistroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = [
            'email',
            'nombre',
            'apellido',
            'telefono',
            'password1',
            'password2'
        ]
