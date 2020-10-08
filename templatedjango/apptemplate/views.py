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
    return compras


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

        detalles_compras = Detalles_compras(id_insumo=id_insumo,cantidad=cantidad,precio=precio,subtotal=total)
        
        detalles_compras.save()

        detalles_compras = Detalles_compras.objects.all()
        insumos = Insumos.objects.all()

        # se ha optimizado el codigo llamando a una funcion que retorna el objeto para envoar 
        # a vistas con las tablas detalles compras y insumos juntas
        comprasiter = objetocompras()
        # print(comprasiter)

        categoria_insumos = Insumos_categoria.objects.all()

        return render(request,'compras/compras.html',{'compras':comprasiter,'insumos':insumos,'categoria':categoria_insumos})

    comprasiter = objetocompras()

    categoria_insumos = Insumos_categoria.objects.all()
    insumos = Insumos.objects.all()
    # print(insumos[0])
    return render(request,'compras/compras.html',{'compras':comprasiter,'insumos':insumos,'categoria':categoria_insumos})

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

    for i in range(cantidad_id):
        get_compras = Detalles_compras.objects.get(id=id_para_compras[i])
        get_compras.id_compra = compra_para_guardar
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

        compras = Compras.objects.all()
        fecha_compra = Compras.objects.get(id=id_ver_compra)

        return render(request,'ver_compras.html',{'compras':compras,'ver_compras':comprasiter,'fecha':fecha_compra.fecha_compra})

    compras = Compras.objects.all()
    return render(request,'ver_compras.html',{'compras':compras})