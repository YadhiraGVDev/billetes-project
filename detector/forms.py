
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import Perfil


# Formulario de perfil
class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['foto']
        widgets = {
            'foto': forms.FileInput(attrs={
                'style': 'width: 100%; padding: 10px; border-radius: 10px; border: 1px solid #ccc;'
            })
        }


# Formulario de registro de usuarios
class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label='Nombre de usuario',
        max_length=150,
        min_length=40,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9@.\/+\-_]+$',
                message='Solo se permiten letras, números y los caracteres @ . / + - _.'
            )
        ],
        help_text='',
        error_messages={
            'min_length': 'El nombre de usuario debe tener al menos 40 caracteres.',
            'max_length': 'El nombre de usuario no puede tener más de 150 caracteres.',
        }
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username',)
