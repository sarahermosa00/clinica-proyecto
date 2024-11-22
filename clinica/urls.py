from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('productos/', include('productos.urls')),
    path('pacientes/', include('pacientes.urls')),
    path('salarios/', include('salarios.urls')),
    path('factura/', include('factura.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('reportes/', include('reportes.urls')),
    path('caja_chica/', include('caja_chica.urls')),
    path('', include('compartido.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
