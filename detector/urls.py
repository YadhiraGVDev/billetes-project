from django.urls import path
from . import views

# app_name = 'detector'   # 👈 descomenta solo si cambias todos los redirect() a 'detector:xxx'

urlpatterns = [
    # Pantalla de inicio / Splash
    path('', views.splash_screen, name='splash'),

    # Menú principal
    path('home/', views.menu, name='home'),

    # Detección (Cámara)
    # 👇 Esta vista ahora también analiza la calidad del billete
    #    (doblado, arrugado, roto) antes de la predicción.
    path('detectar/', views.upload_and_detect, name='upload'),

    # Preview de imagen
    path('preview/', views.preview_imagen, name='preview'),

    # Resultado de la detección
    # 👇 Aquí se muestran denominación + estado de calidad del billete
    path('resultado/<int:record_id>/', views.mostrar_resultado, name='resultado'),

    # Otras pantallas
    path('historial/', views.historial, name='historial'),
    path('estadisticas/', views.estadisticas, name='estadisticas'),
    path('instrucciones/', views.instrucciones, name='instrucciones'),
    path('configuracion/', views.configuracion, name='configuracion'),
    path('acerca-de/', views.acerca_de, name='acerca_de'),
path('configuracion/borrar-historial/', views.borrar_historial, name='borrar_historial'),
    # Cerrar sesión
    path('logout/', views.cerrar_sesion_manual, name='logout'),
]