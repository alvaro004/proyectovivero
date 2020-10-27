from django.shortcuts import render
from templatedjango.apptemplate.models import *

# Create your views here.



# codigo para consultar insumos y detalles compras y luego enviar a la vista 
# en forma de lista con diccionario las tablas detalles compras y 
# insumos juntos 

# ------------------------------------------------------------
# en este codigo de abajo con el for lo que se esta 
# realizando es un conteo a la tabla 
# de detalle compras para luego utilizar el id en la 
# tabla insumos y poder acceder al nombre y mostrar por medio de una lista


def objetocompras():
    detalles_compras = Detalles_compras.objects.all()
    cant = int(len(detalles_compras))
    compras = []

    for i in range(cant): 
        iden = int(detalles_compras[i].id_insumo)
        try:
            insumos2 = Insumos.objects.get(id=iden)   
            if not detalles_compras[i].id_compra:

                compras += [
                    {
                        'id_insumo':insumos2.id,
                        'id_detalles_compras':detalles_compras[i].id,
                        'nombre':insumos2.nombre,
                        'unidad_medida':insumos2.unidad_de_medida,
                        'cantidad':detalles_compras[i].cantidad,
                        'precio':detalles_compras[i].precio,
                        'subtotal':detalles_compras[i].subtotal,
                        'categoria':insumos2.categoria.Nombre,
                    },
                ]
        except:
            compras =[]
    return compras

def objetos_productos():

    detalles_Produccion = Detalles_Produccion.objects.all()
    cant = int(len(detalles_Produccion))
    productos_objeto = []

    for i in range(cant):
        try:
            iden = int(detalles_Produccion[i].id_producto)
            productos = Nombre_productos.objects.get(id=iden)
            productos_objeto += [
                {
                    'id_produccion':detalles_Produccion[i].id,
                    'nombre':productos.nombre_productos,
                    'categoria':productos.categoria,
                    'cantidad':detalles_Produccion[i].cantidad_detalle,

                },
            ]
        except:
            productos_objeto = []
            
    return productos_objeto


# este es el codigo de la vista de compras 
# ---------------------------------------------------------

def compras(request):

    if request.method == 'POST':
        print('entro')
        id_insumo = request.POST.get('id_insumo')
        cantidad = request.POST.get('cantidad')
        precio = request.POST.get('precio')

        # cantidad = cantidad.replace('.', '')
        precio = precio.replace('.', '')

    
        total = float(cantidad) * float(precio)

        print(id_insumo,cantidad,precio,total)

        # analogia consulta en SQL

        detalles_compras = Detalles_compras(id_insumo=id_insumo,cantidad=cantidad,precio=precio,subtotal=total)
        
        detalles_compras.save()

        detalles_compras = Detalles_compras.objects.all()
        insumos = Insumos.objects.all()

        # se ha optimizado el codigo llamando a una funcion que retorna el objeto para envoar 
        # a vistas con las tablas detalles compras y insumos juntas
        comprasiter = objetocompras()
        # print(comprasiter)

        return render(request,'compras/compras.html',{'compras':comprasiter,'insumos':insumos})

    insumos = Insumos.objects.all()

    return render(request,'compras/compras.html',{'insumos':insumos})

def editar(request):

    iden = request.POST.get('iden')
    producto = request.POST.get('producto')
    cantidad = request.POST.get('cantidad')
    precio = request.POST.get('precio')

    precio = precio.replace('.', '')

    compras = Detalles_compras.objects.get(id=iden)

    compras.id_insumo = producto
    compras.cantidad = cantidad
    compras.precio = precio 
    compras.subtotal = float(cantidad) * float(precio)

    compras.save()

    insumos = Insumos.objects.all()
    detalles_compras = Detalles_compras.objects.all()

    # se ha optimizado el codigo llamando a una funcion que retorna el objeto para envoar 
    # a vistas con las tablas detalles compras y insumos juntas

    comprasiter = objetocompras()

    categoria_insumos = Insumos_categoria.objects.all()
    # print(insumos[0])
    return render(request,'compras/compras.html',{'compras':comprasiter,'insumos':insumos,'categoria':categoria_insumos})


def registrar(request):


    id_para_compras = request.POST.getlist('id_para_compras')
    fecha = request.POST.get('fecha')
    total = request.POST.get('total_compra')
    

    print(id_para_compras)

    # aca se realiza la consulta para guardar la fecha y la hora de la compra y 
    # luego se procede a guardar el id de la compra 

    compras = Compras(total_compra=total,fecha_compra=fecha)
    compras.save()
    cantidad_compras = int(len(Compras.objects.all())) - 1

    id_compras = Compras.objects.all()

    compra_para_guardar = id_compras[cantidad_compras].id

    cantidad_id = int(len(id_para_compras))

    # aca se utiliza los id enviados por post en una lista para filtrar las compras realizadas y 
    # agregar a dichas compras el id de la compra con la fecha realizada
    # luego tambien se suma la cantidad comprada del insumo con la que ya se aniadio anteriormente
    # en la vista insumos

    for i in range(cantidad_id):
        get_compras = Detalles_compras.objects.get(id=id_para_compras[i])
        get_compras.id_compra = compra_para_guardar
        
        sumar_cantidad = Insumos.objects.get(id=get_compras.id_insumo)
        sumar_cantidad.cantidad = int(sumar_cantidad.cantidad) + int(get_compras.cantidad)
        sumar_cantidad.save()

        get_compras.save()


    detalles_compras = Detalles_compras.objects.all()
    insumos = Insumos.objects.all()

    # se ha optimizado el codigo llamando a una funcion que retorna el objeto para envoar 
    # a vistas con las tablas detalles compras y insumos juntas

    comprasiter = objetocompras()

    categoria_insumos = Insumos_categoria.objects.all()
    # print(insumos[0])
    return render(request,'compras/compras.html',{'compras':comprasiter,'insumos':insumos,'categoria':categoria_insumos})



def borrar(request):


    id_borrar = request.POST.get('id_borrar')

    consulta_borrar = Detalles_compras.objects.filter(id=id_borrar)
    consulta_borrar.delete()


    detalles_compras = Detalles_compras.objects.all()
    insumos = Insumos.objects.all()

    # se ha optimizado el codigo llamando a una funcion que retorna el objeto para envoar 
    # a vistas con las tablas detalles compras y insumos juntas

    comprasiter = objetocompras()

    categoria_insumos = Insumos_categoria.objects.all()
    # print(insumos[0])
    return render(request,'compras/compras.html',{'compras':comprasiter,'insumos':insumos,'categoria':categoria_insumos})

    # aca finaliza el codigo de la vista de compras 
    # ----------------------------------------------------------------------

    # iniciando codigo de prueba de visualizacion de las compras por fecha 

def ver_compras(request):
    # id_ver_compra = request.POST.get('id_ver_compras')

    # print(id_ver_compra)
    if request.method == 'POST':

        id_ver_compra = request.POST.get('id_ver_compras')


        detalles_compras = Detalles_compras.objects.filter(id_compra=id_ver_compra)
        insumos = Insumos.objects.all()
        
        # se ha optimizado el codigo llamando a una funcion que retorna el objeto para envoar 
        # a vistas con las tablas detalles compras y insumos juntas
        cant = int(len(detalles_compras))
        comprasiter = []

        for i in range(cant): 
            iden = int(detalles_compras[i].id_insumo)
            try:
                insumos2 = Insumos.objects.get(id=iden)   
                if detalles_compras[i].id_compra:

                    comprasiter += [
                        {
                            'id_insumo':insumos2.id,
                            'id_detalles_compras':detalles_compras[i].id,
                            'nombre':insumos2.nombre,
                            'unidad_medida':insumos2.unidad_de_medida,
                            'cantidad':detalles_compras[i].cantidad,
                            'precio':detalles_compras[i].precio,
                            'subtotal':detalles_compras[i].subtotal,
                            'categoria':insumos2.categoria.Nombre,
                        },
                    ]
            except:
                    comprasiter += [
                        {
                            'id_insumo':'no se encuentra',
                            'id_detalles_compras':detalles_compras[i].id,
                            'nombre':'se borro el insumo',
                            'unidad_medida':'se borro el insumo',
                            'cantidad':detalles_compras[i].cantidad,
                            'precio':detalles_compras[i].precio,
                            'subtotal':detalles_compras[i].subtotal,
                            'categoria':'se borro el insumo',
                        },
                    ]
               

        compras = Compras.objects.all()
        fecha_compra = Compras.objects.get(id=id_ver_compra)

        return render(request,'ver_compras.html',{'compras':compras,'ver_compras':comprasiter,'fecha':fecha_compra.fecha_compra})

    compras = Compras.objects.all()
    return render(request,'ver_compras.html',{'compras':compras})




# aca comienzan las vistas de insumos 
# ----------------------------------------------------------


def insumos(request):

    if request.method == "POST":
        if request.POST.get('guardar'):  

            insumo_categoria = request.POST.get('categoria')
            nombre = request.POST.get('producto')
            cantidad = request.POST.get('cantidad')
            medida = request.POST.get('medida')

            # filtrar_categoria = Insumos_categoria.objects.get(id=insumo_categoria)
            Guardar_insumos = Insumos(cantidad=cantidad,nombre=nombre,unidad_de_medida=medida,categoria_id=insumo_categoria)
            Guardar_insumos.save()


            categoria = Insumos_categoria.objects.all()
            insumos = Insumos.objects.all()
            return render(request,'insumos/insumos.html',{'categoria':categoria, 'insumos':insumos})
        
        if request.POST.get('editar'):


            iden = request.POST.get('iden')
            insumo_categoria = request.POST.get('categoria')
            nombre = request.POST.get('nombre')
            cantidad = request.POST.get('cantidad')
            medida = request.POST.get('medida')

            editar_insumos = Insumos.objects.get(id=iden)

            editar_insumos.cantidad = cantidad
            editar_insumos.categoria_id = insumo_categoria
            editar_insumos.nombre = nombre
            editar_insumos.unidad_de_medida = medida

            editar_insumos.save()
        

            

            categoria = Insumos_categoria.objects.all()
            insumos = Insumos.objects.all()
            return render(request,'insumos/insumos.html',{'categoria':categoria, 'insumos':insumos})

        if request.POST.get('borrar'):

            id_borrar = request.POST.get('id_borrar')

            borrar_insumos = Insumos.objects.filter(id=id_borrar)
            borrar_insumos.delete()

            categoria = Insumos_categoria.objects.all()
            insumos = Insumos.objects.all()
            return render(request,'insumos/insumos.html',{'categoria':categoria, 'insumos':insumos})




    categoria = Insumos_categoria.objects.all()
    insumos = Insumos.objects.all()
    return render(request,'insumos/insumos.html',{'categoria':categoria, 'insumos':insumos})

# VISTA DE PRODUCCION 

def produccion(request):

    if request.method == "POST":
        if request.POST.get('guardar'):
            id_productos = request.POST.get('id_producto')
            cantidad = request.POST.get('cantidad')

            detalles_Produccion = Detalles_Produccion(id_producto=id_productos, cantidad_detalle=cantidad)
            detalles_Produccion.save()

            
                
            productos_objetos = objetos_productos()
            print(productos_objetos)
            # print(filtrar_produccion[0].id_producto)


    
    productos_objetos = objetos_productos()

    Productos_para_produccion = Nombre_productos.objects.all()
    categoria = Categoria_productos.objects.all()
    return render(request,'produccion/produccion.html',{'nombre_productos':Productos_para_produccion,'categoria':categoria,'productos':productos_objetos})


# VISTA DE LISTADO DE PRODUCCION
def listado_produccion(request):
    return render(request,'produccion/listado_produccion.html')