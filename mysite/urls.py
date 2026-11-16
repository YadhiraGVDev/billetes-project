from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from detector.views import RegistroView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Rutas de autenticación
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='splash'), name='logout'),
    path('registro/', RegistroView.as_view(), name='registro'),

    # Rutas de la app
    path('', include('detector.urls')),
]

# Servir archivos multimedia en modo desarrollo (Local)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)