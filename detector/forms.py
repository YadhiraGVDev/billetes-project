from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import Perfil

# Tu formulario que ya tenías
class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['foto']
        widgets = {
            'foto': forms.FileInput(attrs={'style': 'width: 100%; padding: 10px; border-radius: 10px; border: 1px solid #ccc;'})
        }

# 👇 EL NUEVO FORMULARIO QUE VALIDA LOS 40 CARACTERES
class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        min_length=40, # 👈 AQUÍ ESTÁ LA REGLA
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9@.\/+\-_]+$',
                message='Solo se permiten letras, números y los caracteres @ . / + - _'
            )
        ],
        help_text='Obligatorio. Mínimo 40 caracteres, máximo 150. Letras, dígitos y @/./+/-/_ únicamente.',
        error_messages={
            'min_length': 'El nombre de usuario debe tener al menos 40 caracteres.',
            'max_length': 'El nombre de usuario no puede tener más de 150 caracteres.',
        }
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username",)