from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseForbidden

from .forms import RegistroForm
from .models import SitioTuristico, Tour, Reserva

User = get_user_model()


# ---------- AUTENTICACIÓN ----------

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


# ---------- VISTAS USUARIO ----------

@login_required
def inicio(request):
    sitios = SitioTuristico.objects.all()
    return render(request, 'inicio.html', {'sitios': sitios})


@login_required
def tours(request):
    tours = Tour.objects.all()
    destacados = Tour.objects.filter(destacado=True)
    return render(request, 'tours.html', {
        'tours': tours,
        'destacados': destacados
    })


@login_required
def reservar(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)

    if request.method == 'POST':
        reserva = Reserva.objects.create(
            usuario=request.user,
            tour=tour,
            personas=request.POST['personas']
        )
        return redirect('confirmacion', reserva.id)

    return render(request, 'reservar.html', {'tour': tour})


@login_required
def confirmacion(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    return render(request, 'confirmacion.html', {'reserva': reserva})


@login_required
def perfil(request):
    return render(request, 'perfil.html')


@login_required
def mis_reservas(request):
    reservas = Reserva.objects.filter(usuario=request.user)
    return render(request, 'mis_reservas.html', {'reservas': reservas})


# ---------- ADMIN / STAFF ----------

@staff_member_required
def ver_usuarios(request):
    usuarios = User.objects.all().order_by('-date_joined')
    return render(request, 'usuarios/ver_usuarios.html', {'usuarios': usuarios})


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
            imagen=request.FILES.get('imagen')
        )
        return redirect('admin_tours')

    return render(request, 'crear_tour.html')



