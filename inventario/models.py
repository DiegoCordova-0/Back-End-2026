from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.

class Producto(models.Model):
    nombre= models.CharField(max_length=64)
    precio= models.IntegerField(default=0, validators=[MinValueValidator(0)])
    descripcion= models.CharField(max_length=128, blank=True, null=True)
    stock= models.IntegerField(default=0, validators=[MinValueValidator(0)])

    class Meta:
        ordering = ['nombre', 'id']
        constraints = [
            models.CheckConstraint(
                condition=models.Q(precio__gte=0),
                name='producto_precio_no_negativo',
            ),
            models.CheckConstraint(
                condition=models.Q(stock__gte=0),
                name='producto_stock_no_negativo',
            ),
        ]