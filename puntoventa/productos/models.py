from django.db import models

# Create your models here.
class Producto(models.Model):
    categoria = models.CharField(max_length=100)
    nombre = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre