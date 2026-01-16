from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseForbidden
from django.contrib.auth import get_user_model
from .forms import RegistroForm
from .models import SitioTuristico, Tour, Reserva


# -------------------------
# AUTENTICACIÓN
# -------------------------

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('inicio')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})


@login_required
def perfil(request):
    return render(request, 'perfil.html')


# -------------------------
# PÁGINA PRINCIPAL
# -------------------------

@login_required
def inicio(request):
    sitios = SitioTuristico.objects.all()
    return render(request, 'inicio.html', {'sitios': sitios})


# -------------------------
# TOURS
# -------------------------

from .ia import recomendar_tours

@login_required
def tours(request):
    tours = Tour.objects.all()
    recomendaciones = recomendar_tours(request.user)

    return render(request, 'tours.html', {
        'tours': tours,
        'recomendados': recomendaciones['similares'],
        'destacados': recomendaciones['destacados'],
        'populares': recomendaciones['populares'],
    })



@staff_member_required
def admin_tours(request):
    tours = Tour.objects.all()
    return render(request, 'admin_tours.html', {'tours': tours})


@staff_member_required
def crear_tour(request):
    if request.method == 'POST':
        Tour.objects.create(
            nombre=request.POST['nombre'],
            descripcion=request.POST['descripcion'],
            precio=request.POST['precio'],
            imagen=request.FILES.get('imagen'),
            destacado='destacado' in request.POST
        )
        return redirect('admin_tours')

    return render(request, 'crear_tour.html')


@staff_member_required
def editar_tour(request, tour_id=None, id=None):
    tour_id = tour_id or id
    tour = get_object_or_404(Tour, id=tour_id)

    if request.method == 'POST':
        tour.nombre = request.POST['nombre']
        tour.descripcion = request.POST['descripcion']
        tour.precio = request.POST['precio']
        tour.destacado = 'destacado' in request.POST

        if request.FILES.get('imagen'):
            tour.imagen = request.FILES['imagen']

        tour.save()
        return redirect('admin_tours')

    return render(request, 'editar_tour.html', {'tour': tour})


@staff_member_required
def eliminar_tour(request, tour_id=None, id=None):
    tour_id = tour_id or id
    tour = get_object_or_404(Tour, id=tour_id)

    if request.method == 'POST':
        tour.delete()
        return redirect('admin_tours')

    return render(request, 'eliminar_tour.html', {'tour': tour})


# -------------------------
# SITIOS TURÍSTICOS
# -------------------------

@staff_member_required
def crear_sitio(request):
    if request.method == 'POST':
        SitioTuristico.objects.create(
            nombre=request.POST['nombre'],
            descripcion=request.POST['descripcion'],
            ubicacion=request.POST['ubicacion'],
            precio=request.POST['precio'],
            destacado='destacado' in request.POST,
            imagen=request.FILES.get('imagen')
        )
        return redirect('inicio')

    return render(request, 'crear_sitio.html')


@staff_member_required
def editar_sitio(request, id):
    sitio = get_object_or_404(SitioTuristico, id=id)

    if request.method == 'POST':
        sitio.nombre = request.POST['nombre']
        sitio.descripcion = request.POST['descripcion']
        sitio.ubicacion = request.POST['ubicacion']
        sitio.precio = request.POST['precio']
        sitio.destacado = 'destacado' in request.POST

        if request.FILES.get('imagen'):
            sitio.imagen = request.FILES['imagen']

        sitio.save()
        return redirect('inicio')

    return render(request, 'editar_sitio.html', {'sitio': sitio})


@staff_member_required
def eliminar_sitio(request, id):
    sitio = get_object_or_404(SitioTuristico, id=id)
    sitio.delete()
    return redirect('inicio')


# -------------------------
# RESERVAS
# -------------------------

@login_required
def reservar(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)

    if request.method == 'POST':
        Reserva.objects.create(
            usuario=request.user,
            tour=tour,
            personas=request.POST['personas']
        )
        return redirect('mis_reservas')

    return render(request, 'reservar.html', {'tour': tour})


@login_required
def mis_reservas(request):
    reservas = Reserva.objects.filter(usuario=request.user)
    return render(request, 'mis_reservas.html', {'reservas': reservas})


@staff_member_required
def todas_las_reservas(request):
    reservas = Reserva.objects.all().order_by('-fecha_reserva')
    return render(request, 'todas_reservas.html', {'reservas': reservas})


# -------------------------
# CONFIRMACIÓN DE RESERVA
# -------------------------

@login_required
def confirmacion(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    return render(request, 'confirmacion.html', {'reserva': reserva})


# -------------------------
# USUARIOS (ADMIN)
# -------------------------

User = get_user_model()

@staff_member_required
def ver_usuarios(request):
    usuarios = User.objects.all().order_by('-date_joined')
    return render(request, 'usuarios/ver_usuarios.html', {'usuarios': usuarios})
