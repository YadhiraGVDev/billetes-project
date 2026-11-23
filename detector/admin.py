from django.contrib import admin
from django.utils.html import format_html

from .models import DetectionRecord, Perfil


@admin.register(DetectionRecord)
class DetectionRecordAdmin(admin.ModelAdmin):
    # --- Listado ---
    list_display = (
        'id',
        'denominacion_detectada',
        'nivel_confianza_fmt',
        'estado_calidad_badge',
        'puntaje_calidad_fmt',
        'fecha_analisis',
    )
    list_filter = (
        'roto',
        'doblado',
        'arrugado',
        'denominacion_detectada',
        'fecha_analisis',
    )
    search_fields = ('denominacion_detectada',)
    ordering = ('-fecha_analisis',)
    date_hierarchy = 'fecha_analisis'
    readonly_fields = ('fecha_analisis', 'vista_previa_imagen')

    # --- Detalle ---
    fieldsets = (
        ('Datos del billete', {
            'fields': ('imagen', 'vista_previa_imagen', 'denominacion_detectada', 'nivel_confianza')
        }),
        ('Estado de calidad', {
            'fields': ('roto', 'doblado', 'arrugado', 'puntaje_calidad', 'detalles_calidad')
        }),
        ('Metadatos', {
            'fields': ('fecha_analisis',),
            'classes': ('collapse',),
        }),
    )

    # ---------- Columnas personalizadas ----------
    @admin.display(description='Confianza', ordering='nivel_confianza')
    def nivel_confianza_fmt(self, obj):
        if obj.nivel_confianza is None:
            return '—'
        return f'{obj.nivel_confianza:.2f}'

    @admin.display(description='Estado', ordering='puntaje_calidad')
    def estado_calidad_badge(self, obj):
        if obj.roto:
            return format_html(
                '<span style="background:#dc3545;color:white;'
                'padding:2px 8px;border-radius:4px;">❌ ROTO</span>'
            )
        if obj.doblado and obj.arrugado:
            return format_html(
                '<span style="background:#fd7e14;color:white;'
                'padding:2px 8px;border-radius:4px;">⚠️ DOBLADO+ARRUGADO</span>'
            )
        if obj.doblado:
            return format_html(
                '<span style="background:#ffc107;color:black;'
                'padding:2px 8px;border-radius:4px;">⚠️ DOBLADO</span>'
            )
        if obj.arrugado:
            return format_html(
                '<span style="background:#ffc107;color:black;'
                'padding:2px 8px;border-radius:4px;">⚠️ ARRUGADO</span>'
            )
        return format_html(
            '<span style="background:#28a745;color:white;'
            'padding:2px 8px;border-radius:4px;">✅ OK</span>'
        )

    @admin.display(description='Calidad')
    def puntaje_calidad_fmt(self, obj):
        p = obj.puntaje_calidad or 0
        if p >= 80:
            color = '#28a745'  # verde
        elif p >= 50:
            color = '#ffc107'  # amarillo
        else:
            color = '#dc3545'  # rojo
        return format_html(
            '<b style="color:{};">{}/100</b>', color, f"{p:.0f}"
        )

    @admin.display(description='Vista previa')
    def vista_previa_imagen(self, obj):
        if not obj.imagen:
            return '—'
        return format_html(
            '<img src="{}" style="max-height:250px;border:1px solid #ccc;'
            'border-radius:6px;" />',
            obj.imagen.url,
        )


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'foto_preview')
    search_fields = ('usuario__username', 'usuario__email')
    readonly_fields = ('foto_preview',)

    @admin.display(description='Foto')
    def foto_preview(self, obj):
        if not obj.foto:
            return '—'
        return format_html(
            '<img src="{}" style="height:40px;width:40px;'
            'border-radius:50%;object-fit:cover;" />',
            obj.foto.url,
        )