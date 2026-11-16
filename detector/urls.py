from django.urls import path
from . import views

urlpatterns = [
    # Pantalla de inicio / Splash
    path('', views.splash_screen, name='splash'),

    # Menú principal
    path('home/', views.menu, name='home'),

    # Detección (Cámara)
    path('detectar/', views.upload_and_detect, name='upload'),

    # Preview de imagen
    path('preview/', views.preview_imagen, name='preview'),

    # Resultado de la detección
    path('resultado/<int:record_id>/', views.mostrar_resultado, name='resultado'),

    # Otras pantallas
    path('historial/', views.historial, name='historial'),
    path('estadisticas/', views.estadisticas, name='estadisticas'),
    path('instrucciones/', views.instrucciones, name='instrucciones'),
    path('configuracion/', views.configuracion, name='configuracion'),
    path('acerca-de/', views.acerca_de, name='acerca_de'),
    
    # Borrar historial (Alineado)
    path('configuracion/borrar-historial/', views.borrar_historial, name='borrar_historial'),

    # Cerrar sesión
    path('logout/', views.cerrar_sesion_manual, name='logout'),
]