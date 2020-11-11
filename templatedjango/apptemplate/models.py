from django.db import models

# Create your models here


# comienzo para las tablas de compras
# ----------------------------------------------------------


class Compras(models.Model):
    total_compra = models.CharField(max_length=400 ,blank=True, null=True)
    fecha_compra = models.CharField(max_length=400 ,blank=True, null=True)


    def __str__(self):
        return "compra {}".format(self.fecha_compra)


class Detalles_compras(models.Model):
    
    id_compra = models.CharField(max_length=400 ,blank=True, null=True)# conectado a la tabla compra
    id_insumo = models.CharField(max_length=400 ,blank=True, null=True) # conectado a la tabla produccion
    cantidad = models.CharField(max_length=400 ,blank=True, null=True)
    precio = models.CharField(max_length=400 ,blank=True, null=True)
    subtotal = models.CharField(max_length=400 ,blank=True, null=True)


    def __str__(self):
        return "detalles {}".format(self.subtotal)



# tablas de isnumos
# -------------------------------------------------------------
class Insumos_categoria(models.Model):
    
    Nombre = models.CharField(max_length=400 ,blank=True, null=True)
      
    def __str__(self):
        return "{}".format(self.Nombre)

class Insumos(models.Model):
    
    nombre = models.CharField(max_length=400 ,blank=True, null=True)
    unidad_de_medida = models.CharField(max_length=400 ,blank=True, null=True)
    cantidad = models.CharField(max_length=400 ,blank=True, null=True)
    categoria = models.ForeignKey(Insumos_categoria, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return "detalles {}".format(self.nombre)


class Detalles_insumos(models.Model):
    
    Cantidad = models.CharField(max_length=400 ,blank=True, null=True)
    id_insumos = models.CharField(max_length=400 ,blank=True, null=True)
    
    
    def __str__(self):
        return "detalles {}".format(self.estado)

# fin de tablas de isnumos
# ------------------------------------------------------

# en esta tabla se guardan los datos al presionar el boton registrar en la vista produccion 
class Produccion(models.Model):
    
    id_detalle_insumo = models.CharField(max_length=400 ,blank=True, null=True) # conectado a detalles insumos
    fecha_produccion = models.CharField(max_length=400 ,blank=True, null=True)
    estado_produccion = models.CharField(max_length=400 ,blank=True, null=True)
    fecha_acabado = models.CharField(max_length=400 ,blank=True, null=True)
    
    
    def __str__(self):
        return "detalles {}".format(self.estado)

class Detalles_Produccion(models.Model):
    id_produccion = models.CharField(max_length=400,blank=True, null=True) # conectado a produccion
    id_producto = models.CharField(max_length=400 ,blank=True, null=True) # conectado a producto
    cantidad_detalle = models.CharField(max_length=400 ,blank=True, null=True)
    cantidad_real_detalle = models.CharField(max_length=400 ,blank=True, null=True)

    def __str__(self):
        return "detalles {}".format(self.id_producto)
# ----------------------------------------------------
# fin tablas producccion

class Productos(models.Model):
    
    id_nombre_producto = models.CharField(max_length=400 ,blank=True, null=True)# conectado a la tabla compra
    # id_categoria = models.CharField(max_length=400 ,blank=True, null=True)
    descripcion_producto = models.CharField(max_length=400 ,blank=True, null=True) # conectado a la tabla produccion
    cantidad_stock = models.CharField(max_length=400 ,blank=True, null=True)
    imagen = models.CharField(max_length=400 ,blank=True, null=True)
    precio = models.CharField(max_length=400 ,blank=True, null=True)

    def __str__(self):
        return "detalles {}".format(self.subtotal)

class Categoria_productos(models.Model):
    
    nombre_categoria = models.CharField(max_length=400 ,blank=True, null=True)
    
    def __str__(self):
        return "{}".format(self.nombre_categoria)

class Nombre_productos(models.Model):
    
    nombre_productos = models.CharField(max_length=400 ,blank=True, null=True)
    categoria = models.ForeignKey(Categoria_productos, on_delete=models.CASCADE,blank=True, null=True)

    
    def __str__(self):
        return "{}".format(self.nombre_productos)



class Detalles_pedidos(models.Model):
    
    id_producto = models.CharField(max_length=400 ,blank=True, null=True)# conectado a la tabla producto
    id_pedido = models.CharField(max_length=400 ,blank=True, null=True)# conectado a la tabla pedido
    cantidad = models.CharField(max_length=400 ,blank=True, null=True)
    subtotal_producto = models.CharField(max_length=400 ,blank=True, null=True) 
    precio = models.CharField(max_length=400 ,blank=True, null=True)

    def __str__(self):
        return "detalles {}".format(self.subtotal)


class Pedidos(models.Model):
    
    id_cliente = models.CharField(max_length=400 ,blank=True, null=True)# conectado a la tabla producto
    estado_pedido = models.CharField(max_length=400 ,blank=True, null=True)# conectado a la tabla pedido
    fecha_pedido = models.CharField(max_length=400 ,blank=True, null=True)
    fecha_entrega = models.CharField(max_length=400 ,blank=True, null=True) 
    cantidad_total = models.CharField(max_length=400 ,blank=True, null=True)

    def __str__(self):
        return "detalles {}".format(self.subtotal)

class Clientes(models.Model):
    
    nombre_cliente = models.CharField(max_length=400 ,blank=True, null=True)# conectado a la tabla pedido
    direccion = models.CharField(max_length=400 ,blank=True, null=True)
    telefono = models.CharField(max_length=400 ,blank=True, null=True) 

    def __str__(self):
        return "detalles {}".format(self.subtotal)

class Ventas(models.Model):
    
    id_pedidos = models.CharField(max_length=400 ,blank=True, null=True)# conectado a la tabla pedido
    id_clientes = models.CharField(max_length=400 ,blank=True, null=True)# conectado a la tabla pedido
    fecha_venta = models.CharField(max_length=400 ,blank=True, null=True) 

    def __str__(self):
        return "detalles {}".format(self.subtotal)




