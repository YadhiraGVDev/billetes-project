from django.db import models
from django.contrib.auth.models import User


# ==========================================
# MODELO DE DETECCIÃ“N DE BILLETES
# ==========================================
class DetectionRecord(models.Model):
    imagen = models.ImageField(upload_to='billetes/')
    denominacion_detectada = models.CharField(max_length=50, blank=True, null=True)
    nivel_confianza = models.FloatField(blank=True, null=True)
    # --- CONFIRMACION DE LA DENOMINACION REAL ---
    denominacion_real = models.CharField(
        max_length=3,
        choices=[
            ('20', '$20'),
            ('50', '$50'),
            ('100', '$100'),
            ('200', '$200'),
            ('500', '$500'),
        ],
        blank=True,
        default=''
    )

    # --- GENERACION DEL DISEÑO DEL BILLETE ---
    generacion_billete = models.CharField(
        max_length=10,
        choices=[
            ('anterior', 'Diseño anterior'),
            ('actual', 'Diseño actual'),
        ],
        blank=True,
        default=''
    )
    fecha_analisis = models.DateTimeField(auto_now_add=True)

    # --- NUEVOS CAMPOS: CALIDAD DEL BILLETE ---
    doblado = models.BooleanField(default=False)
    arrugado = models.BooleanField(default=False)
    roto = models.BooleanField(default=False)
    puntaje_calidad = models.FloatField(default=100)
    detalles_calidad = models.JSONField(default=list, blank=True)

    # Si en tu migraciÃ³n anterior renombraste algÃºn campo (como el usuario),
    # asegÃºrate de mantenerlo aquÃ­. Por ejemplo:
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['-fecha_analisis']

    def __str__(self):
        return (
            f"{self.denominacion_detectada or 'Sin denominaciÃ³n'} - "
            f"{self.fecha_analisis.strftime('%Y-%m-%d %H:%M')}"
        )

    @property
    def estado_calidad(self):
        """Texto legible del estado del billete."""
        if self.roto:
            return "roto"
        if self.doblado and self.arrugado:
            return "doblado y arrugado"
        if self.doblado:
            return "doblado"
        if self.arrugado:
            return "arrugado"
        return "ok"

    @property
    def apto(self):
        """True si el billete no estÃ¡ roto, doblado ni arrugado."""
        return not (self.roto or self.doblado or self.arrugado)


# ==========================================
# NUEVO MODELO: PERFIL DE USUARIO
# ==========================================
class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    foto = models.ImageField(upload_to='perfiles/', null=True, blank=True)

    def __str__(self):
        return f"Perfil de {self.usuario.username}"
