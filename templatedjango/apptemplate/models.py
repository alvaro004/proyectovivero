from django.db import models

# Create your models here

class Compras(models.Model):
    total_compra = models.CharField(max_length=400 ,blank=True, null=True)
    fecha_compra = models.CharField(max_length=400 ,blank=True, null=True)

    def __str__(self):
        return "compra {}".format(self.fecha_compra)


class Detalles_compras(models.Model):
    
    id_insumo = models.CharField(max_length=400 ,blank=True, null=True)
    id_compra = models.CharField(max_length=400 ,blank=True, null=True)
    cantidad = models.CharField(max_length=400 ,blank=True, null=True)
    precio = models.CharField(max_length=400 ,blank=True, null=True)
    subtotal = models.CharField(max_length=400 ,blank=True, null=True)

    def __str__(self):
        return "detalles {}".format(self.)

