"""templatedjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from templatedjango.apptemplate.views import *
from django.conf import settings             # add this
from django.conf.urls.static import static 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('compras', compras),
    path('editar', editar),
    path('registrar', registrar),
    path('borrar', borrar),
    path('ver_compras', ver_compras),
    path('insumos', insumos),
    path('produccion', produccion),
    path('listado_produccion', listado_produccion),
    path('home', inicio),
    path('', login),
    path('logout', logout_views),
    # path('listado_compras', listado_compras),
    path('productos', productos),
    path('listado_productos', listado_productos),
    path('ventas', ventas),
    path('nombre_productos', nombre_productos),
    path('pedidos', pedidos),
    path('clientes', clientes),
    path('listado_pedidos', listado_pedidos),
    path('login2', login2),
    path('auditoria', auditoria),
    path('backup', backup),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
