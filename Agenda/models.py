from django.db import models

# Create your models here.
class Contacto(models.Model):
    nombre = models.CharField(max_length=64)
    telefono = models.CharField(max_length=20, default='+56 9 ')
    correo = models.EmailField(max_length=128, blank=True, null=True)
    direccion = models.CharField(max_length=128, blank=True, null=True)