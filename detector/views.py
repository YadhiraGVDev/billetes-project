import base64
import json
import logging
import os
import re  # 👈 NUEVO: Importado para las validaciones de caracteres

from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.files.base import ContentFile
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.http import require_POST, require_http_methods

from .models import DetectionRecord, Perfil
from .forms import PerfilForm, CustomUserCreationForm
from .predictor import predict_bill
from detector.services.calidad import AnalizadorCalidadBillete

logger = logging.getLogger(__name__)

# Extensiones permitidas y tamaño máximo (10 MB)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10 MB

# Instancia única del analizador (se reutiliza en cada request)
analizador_calidad = AnalizadorCalidadBillete()


# ==========================================
# 1. SPLASH
# ==========================================
def splash_screen(request):
    return render(request, 'detector/splash.html')


# ==========================================
# 2. MENÚ PRINCIPAL (Enviamos el perfil)
# ==========================================
def menu(request):
    perfil = getattr(request.user, 'perfil', None) if request.user.is_authenticated else None
    return render(request, 'detector/menu.html', {'perfil': perfil})


# ==========================================
# 3. DETECCIÓN (Cámara) - SIN PERFIL (Para que salga el robot)
# ==========================================
@require_http_methods(["GET", "POST"])
def upload_and_detect(request):
    if request.method == 'GET':
        return render(request, 'detector/upload.html')  # No enviamos perfil

    # --- Parseo seguro del JSON ---
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    image_base64 = data.get('image')
    if not image_base64 or not isinstance(image_base64, str):
        return JsonResponse({'error': 'No se recibió imagen'}, status=400)

    # --- Validación del formato data URI ---
    try:
        format_part, imgstr = image_base64.split(';base64,', 1)
        ext = format_part.split('/')[-1].lower()
    except ValueError:
        return JsonResponse({'error': 'Formato de imagen inválido'}, status=400)

    if ext not in ALLOWED_EXTENSIONS:
        return JsonResponse(
            {'error': f'Extensión no permitida: {ext}'}, status=400
        )

    # --- Decodificación segura ---
    try:
        decoded = base64.b64decode(imgstr, validate=True)
    except (base64.binascii.Error, ValueError):
        return JsonResponse({'error': 'Base64 inválido'}, status=400)

    if len(decoded) > MAX_IMAGE_SIZE:
        return JsonResponse({'error': 'Imagen demasiado grande'}, status=413)

    # --- Análisis de CALIDAD (antes de crear el registro) ---
    try:
        calidad = analizador_calidad.analizar_desde_bytes(decoded)
    except Exception:
        logger.exception("Error al analizar la calidad del billete")
        calidad = {
            "doblado": False,
            "arrugado": False,
            "roto": False,
            "puntaje_calidad": 100,
            "detalles": ["Análisis de calidad no disponible"],
        }

    # --- Predicción de denominación ---
    image_file = ContentFile(decoded, name=f'billete_temp.{ext}')

    record = DetectionRecord(imagen=image_file)
    # Guardamos la calidad ya calculada directamente en el registro
    record.doblado = calidad["doblado"]
    record.arrugado = calidad["arrugado"]
    record.roto = calidad["roto"]
    record.puntaje_calidad = calidad["puntaje_calidad"]
    record.detalles_calidad = calidad["detalles"]
    record.save()  # Necesario para tener .path

    try:
        texto_ia, confianza = predict_bill(record.imagen.path)
    except Exception:
        logger.exception("Error al predecir el billete")
        record.delete()
        return JsonResponse({'error': 'No se pudo procesar la imagen'}, status=500)

    denominacion_limpia = (
        (texto_ia or "")
        .replace("MXN", "")
        .replace("$", "")
        .strip()
    )

    record.denominacion_detectada = denominacion_limpia or None
    record.nivel_confianza = confianza
    record.save(update_fields=['denominacion_detectada', 'nivel_confianza'])

    return JsonResponse({'redirect_url': f'/resultado/{record.id}/'})


# ==========================================
# 4. RESULTADO (Enviamos el perfil)
# ==========================================
def mostrar_resultado(request, record_id):
    perfil = getattr(request.user, 'perfil', None) if request.user.is_authenticated else None
    registro = get_object_or_404(DetectionRecord, id=record_id)
    return render(request, 'detector/result.html', {'registro': registro, 'perfil': perfil})


# ==========================================
# 5. OTRAS PANTALLAS (Enviamos el perfil)
# ==========================================
def historial(request):
    perfil = getattr(request.user, 'perfil', None) if request.user.is_authenticated else None
    registros = DetectionRecord.objects.all().order_by('-fecha_analisis')
    return render(request, 'detector/historial.html', {'registros': registros, 'perfil': perfil})


def estadisticas(request):
    perfil = getattr(request.user, 'perfil', None) if request.user.is_authenticated else None
    registros = DetectionRecord.objects.all()
    total_detecciones = registros.count()

    base_qs = (
        registros
        .exclude(denominacion_detectada__isnull=True)
        .exclude(denominacion_detectada__exact='')
        .values('denominacion_detectada')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    top = base_qs.first()
    if top:
        denominacion_top = top['denominacion_detectada']
        porcentaje_top = (
            round((top['total'] / total_detecciones) * 100, 1)
            if total_detecciones else 0
        )
    else:
        denominacion_top = "Sin datos"
        porcentaje_top = 0

    distribucion = list(base_qs)
    datos_grafico = {
        'labels': [d['denominacion_detectada'] for d in distribucion],
        'values': [d['total'] for d in distribucion],
    }

    # --- NUEVAS ESTADÍSTICAS DE CALIDAD ---
    total_rotos = registros.filter(roto=True).count()
    total_doblados = registros.filter(doblado=True).count()
    total_arrugados = registros.filter(arrugado=True).count()
    total_buenos = registros.filter(
        roto=False, doblado=False, arrugado=False
    ).count()

    context = {
        'total_detecciones': total_detecciones,
        'denominacion_top': denominacion_top,
        'porcentaje_top': porcentaje_top,
        'datos_grafico': datos_grafico,
        'perfil': perfil,  # 👈 Enviamos perfil
        # Calidad
        'total_rotos': total_rotos,
        'total_doblados': total_doblados,
        'total_arrugados': total_arrugados,
        'total_buenos': total_buenos,
    }
    return render(request, 'detector/estadisticas.html', context)


def instrucciones(request):
    perfil = getattr(request.user, 'perfil', None) if request.user.is_authenticated else None
    return render(request, 'detector/instrucciones.html', {'perfil': perfil})


# 👇 VISTA DE CONFIGURACIÓN ACTUALIZADA PARA LA FOTO
@login_required
def configuracion(request):
    perfil, created = Perfil.objects.get_or_create(usuario=request.user)

    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('configuracion')
    else:
        form = PerfilForm(instance=perfil)

    return render(request, 'detector/configuracion.html', {
        'form': form,
        'perfil': perfil
    })


def acerca_de(request):
    perfil = getattr(request.user, 'perfil', None) if request.user.is_authenticated else None
    return render(request, 'detector/acerca_de.html', {'perfil': perfil})


def preview_imagen(request):
    return render(request, 'detector/preview.html')


@require_POST
def cerrar_sesion_manual(request):
    logout(request)
    return redirect('splash')


class RegistroView(generic.CreateView):
    form_class = CustomUserCreationForm  # 👈 Usamos el nuevo formulario
    success_url = reverse_lazy('home')
    template_name = 'registration/registro.html'

    def form_valid(self, form):
        respuesta = super().form_valid(form)
        login(self.request, self.object)

        # Creamos el perfil vacío
        Perfil.objects.create(usuario=self.object)

        return respuesta