from django.contrib import admin
from django.urls import path, include
from Reserv import views  # Importa las vistas de la app 'orders'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Reserv.urls')),  # Aquí incluyes las rutas de la app Reserv
]
