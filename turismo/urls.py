from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('registro/', views.registro, name='registro'),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),

    path('tours/', views.tours, name='tours'),
    path('reservar/<int:tour_id>/', views.reservar, name='reservar'),
    path('confirmacion/<int:reserva_id>/', views.confirmacion, name='confirmacion'),
    path('perfil/', views.perfil, name='perfil'),

    path('mis-reservas/', views.mis_reservas, name='mis_reservas'),
    path('admin-reservas/', views.todas_las_reservas, name='todas_reservas'),

    path('admin-tours/', views.admin_tours, name='admin_tours'),
    path('admin-tours/crear/', views.crear_tour, name='crear_tour'),
    path('admin-tours/editar/<int:id>/', views.editar_tour, name='editar_tour'),
    path('admin-tours/eliminar/<int:id>/', views.eliminar_tour, name='eliminar_tour'),

    path('crear-sitio/', views.crear_sitio, name='crear_sitio'),
    path('editar-sitio/<int:id>/', views.editar_sitio, name='editar_sitio'),
    path('eliminar-sitio/<int:id>/', views.eliminar_sitio, name='eliminar_sitio'),

    path('usuarios/', views.ver_usuarios, name='ver_usuarios'),
]
