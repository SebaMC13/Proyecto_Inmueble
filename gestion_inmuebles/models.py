from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator


class Region(models.Model):
    nombre = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Regiones"

    def __str__(self):
        return f"{self.nombre} {self.id}"


class Comuna(models.Model):
    nombre = models.CharField(max_length=200)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} {self.id}"


class Usuario(AbstractUser):
    rut = models.CharField(max_length=13, unique=True, verbose_name="RUT")
    direccion = models.CharField(
        max_length=300, blank=True, null=True, verbose_name="Dirección"
    )
    telefono = models.CharField(
        max_length=12, blank=True, null=True, verbose_name="Teléfono"
    )
    TIPO_USUARIO = [("arrendador", "arrendador"), ("arrendatario", "arrendatario")]
    tipo_usuario_por_defecto = models.CharField(
        max_length=100, choices=TIPO_USUARIO, verbose_name="Tipo Usuario"
    )


class TipoInmueble(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre} {self.id}"


class Inmueble(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(verbose_name="Descripción")
    m2_construidos = models.FloatField(validators=[MinValueValidator(1)])
    m2_totales = models.FloatField(validators=[MinValueValidator(1)])
    estacionamientos = models.PositiveIntegerField()
    habitaciones = models.PositiveIntegerField()
    banos = models.PositiveIntegerField(verbose_name="Baños")
    direccion = models.CharField(max_length=200, verbose_name="Dirección")
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    tipo_inmueble = models.ForeignKey(TipoInmueble, on_delete=models.CASCADE)
    precio_mensual = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    dueno = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Dueño")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre


class Solicitud(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    texto = models.TextField()
    inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE)
    aceptado = models.BooleanField(null=True, blank=True)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_aceptacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Solicitudes"
