from django.db import models

# Create your models here


# comienzo para las tablas de compras
# ----------------------------------------------------------


class Compras(models.Model):
    cantidad_compra = models.CharField(max_length=400 ,blank=True, null=True)
    total_compra = models.CharField(max_length=400 ,blank=True, null=True)
    fecha_compra = models.CharField(max_length=400 ,blank=True, null=True)
    nombre_compra = models.CharField(max_length=400 ,blank=True, null=True)


    def __str__(self):
        return "compra {}".format(self.fecha_compra)


class Detalles_compras(models.Model):
    
    id_compra = models.CharField(max_length=400 ,blank=True, null=True)# conectado a la tabla compra
    id_produccion = models.CharField(max_length=400 ,blank=True, null=True) # conectado a la tabla produccion
    id_categoria_compra = models.CharField(max_length=400 ,blank=True, null=True)
    precio = models.CharField(max_length=400 ,blank=True, null=True)
    subtotal = models.CharField(max_length=400 ,blank=True, null=True)

    def __str__(self):
        return "detalles {}".format(self.subtotal)

class Categoria_compras(models.Model):
    
    nombre_categoria = models.CharField(max_length=400 ,blank=True, null=True)
    
    def __str__(self):
        return "detalles {}".format(self.nombre_categoria)


# ----------------------------------------------
# fin de las tablas compras



# tablas de produccion 
# -------------------------------------------------------------
class Produccion(models.Model):
    
    Fecha_estimada = models.CharField(max_length=400 ,blank=True, null=True)
    estado = models.CharField(max_length=400 ,blank=True, null=True)
    
    
    def __str__(self):
        return "detalles {}".format(self.estado)

class Detalles_Produccion(models.Model):
    id_produccion = models.CharField(max_length=400,blank=True, null=True)
    id_producto = models.CharField(max_length=400 ,blank=True, null=True)
    producto = models.CharField(max_length=400 ,blank=True, null=True)

    def __str__(self):
        return "detalles {}".format(self.estado)
# ----------------------------------------------------
# fin tablas producccion

class Productos(models.Model):
    
    Nombre_producto = models.CharField(max_length=400 ,blank=True, null=True)# conectado a la tabla compra
    id_categoria = models.CharField(max_length=400 ,blank=True, null=True)
    descripcion_producto = models.CharField(max_length=400 ,blank=True, null=True) # conectado a la tabla produccion
    cantidad_stock = models.CharField(max_length=400 ,blank=True, null=True)
    imagen = models.CharField(max_length=400 ,blank=True, null=True)
    precio = models.CharField(max_length=400 ,blank=True, null=True)

    def __str__(self):
        return "detalles {}".format(self.subtotal)

class Categoria_productos(models.Model):
    
    nombre_categoria = models.CharField(max_length=400 ,blank=True, null=True)
    
    def __str__(self):
        return "detalles {}".format(self.nombre_categoria)



class Detalles_pedidos(models.Model):
    
    Nombre_producto = models.CharField(max_length=400 ,blank=True, null=True)# conectado a la tabla compra
    id_categoria = models.CharField(max_length=400 ,blank=True, null=True)
    descripcion_producto = models.CharField(max_length=400 ,blank=True, null=True) # conectado a la tabla produccion
    cantidad_stock = models.CharField(max_length=400 ,blank=True, null=True)
    imagen = models.CharField(max_length=400 ,blank=True, null=True)
    precio = models.CharField(max_length=400 ,blank=True, null=True)

    def __str__(self):
        return "detalles {}".format(self.subtotal)
