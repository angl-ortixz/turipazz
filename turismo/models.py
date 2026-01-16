from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El correo es obligatorio")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.CharField(max_length=15, blank=True)

    objects = UsuarioManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nombre", "apellido"]

    def __str__(self):
        return self.email


class SitioTuristico(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    ubicacion = models.CharField(max_length=150)
    imagen = models.ImageField(upload_to="sitios/", blank=True, null=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    destacado = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre


class Tour(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    imagen = models.ImageField(upload_to="tours/", blank=True, null=True)
    destacado = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre


class Reserva(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    personas = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.usuario.email} - {self.tour.nombre}"


