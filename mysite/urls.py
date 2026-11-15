from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from detector.views import RegistroView  # 👈 Importamos el registro

urlpatterns = [
    path('admin/', admin.site.urls),

    # Rutas de autenticación
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='splash'), name='logout'),  # 👈 Ruta de logout
    path('registro/', RegistroView.as_view(), name='registro'),

    # Rutas de la app
    # 👇 Incluye /detectar/ (análisis de calidad + predicción) y
    #    /resultado/<id>/ (muestra denominación + estado del billete).
    #    No se requieren rutas nuevas para el análisis de calidad.
    path('', include('detector.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)