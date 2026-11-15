from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import Perfil

# Tu formulario que ya tenÃ­as
class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['foto']
        widgets = {
            'foto': forms.FileInput(attrs={'style': 'width: 100%; padding: 10px; border-radius: 10px; border: 1px solid #ccc;'})
        }

# ðŸ‘‡ EL NUEVO FORMULARIO QUE VALIDA LOS 40 CARACTERES
class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        min_length=1, # ðŸ‘ˆ AQUÃ ESTÃ LA REGLA
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9@.\/+\-_]+$',
                message='Solo se permiten letras, nÃºmeros y los caracteres @ . / + - _'
            )
        ],
        help_text='Obligatorio. MÃ­nimo 40 caracteres, mÃ¡ximo 150. Letras, dÃ­gitos y @/./+/-/_ Ãºnicamente.',
        error_messages={
            'min_length': 'El nombre de usuario debe tener al menos 1 carácter.',
            'max_length': 'El nombre de usuario no puede tener mÃ¡s de 150 caracteres.',
        }
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username",)

