from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),

    path('registro/', views.registro, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),

    path('perfil/', views.perfil, name='perfil'),

    # TOURS (usuarios)
    path('tours/', views.tours, name='tours'),
    path('reservar/<int:tour_id>/', views.reservar, name='reservar'),
    path('confirmacion/<int:reserva_id>/', views.confirmacion, name='confirmacion'),
    path('mis-reservas/', views.mis_reservas, name='mis_reservas'),

    # ADMIN – TOURS
    path('admin/tours/', views.admin_tours, name='admin_tours'),
    path('admin/tours/crear/', views.crear_tour, name='crear_tour'),
    path('admin/tours/editar/<int:tour_id>/', views.editar_tour, name='editar_tour'),
    path('admin/tours/eliminar/<int:tour_id>/', views.eliminar_tour, name='eliminar_tour'),

    # ADMIN – SITIOS
    path('admin/sitios/crear/', views.crear_sitio, name='crear_sitio'),
    path('admin/sitios/editar/<int:id>/', views.editar_sitio, name='editar_sitio'),
    path('admin/sitios/eliminar/<int:id>/', views.eliminar_sitio, name='eliminar_sitio'),

    # ADMIN – RESERVAS Y USUARIOS
    path('admin/reservas/', views.todas_las_reservas, name='todas_reservas'),
    path('admin/usuarios/', views.ver_usuarios, name='ver_usuarios'),
]

