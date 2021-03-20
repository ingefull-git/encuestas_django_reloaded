from django.contrib import admin
from django.urls import path, include
from core.apps.encuesta.views import ListaPreguntas


urlpatterns = [
    path('', ListaPreguntas.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('login/', include('core.apps.login.urls')),
    path('encuesta/', include('core.apps.encuesta.urls')),

]
