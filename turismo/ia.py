from .models import Tour, Reserva
from django.db.models import Count

def recomendar_tours(usuario):
    # 1. Tours más reservados
    populares = (
        Reserva.objects.values('tour')
        .annotate(total=Count('tour'))
        .order_by('-total')[:5]
    )

    populares_ids = [p['tour'] for p in populares]
    populares_tours = Tour.objects.filter(id__in=populares_ids)

    # 2. Tours destacados
    destacados = Tour.objects.filter(destacado=True)[:5]

    # 3. Tours similares a lo reservado por el usuario
    reservas = Reserva.objects.filter(usuario=usuario)
    if reservas.exists():
        precios = [r.tour.precio for r in reservas]
        promedio = sum(precios) / len(precios)
        similares = Tour.objects.filter(precio__range=(promedio-50, promedio+50))
    else:
        similares = Tour.objects.none()

    return {
        "populares": populares_tours,
        "destacados": destacados,
        "similares": similares[:5]
    }
