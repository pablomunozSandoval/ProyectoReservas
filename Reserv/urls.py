from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('citas/', views.citas_view, name='citas'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('mis-citas/', views.mis_citas, name='mis_citas'),
    path('reserve/<int:doctor_id>/', views.reserve_view, name='reserve'),
    
]

