from django.shortcuts import render
from templatedjango.apptemplate.models import *
from templatedjango.apptemplate.forms import *
from django.contrib.auth import authenticate, login as dj_login
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.db.models import Q
import subprocess
import os
import datetime

# Create your views here.

# variable global para la fecha y hora actual
full_date_time = str(datetime.datetime.now()).split('.')[0]
# variable global para la fecha y hora actual


# VISTA DEL INICIO 

def inicio(request):

    if request.user.is_authenticated:
        view = 'inicio'
        return render(request, 'inicio/inicio.html',{'name':view})
    else:
        return redirect('/')

# codigo para consultar insumos y detalles compras y luego enviar a la vista 
# en forma de lista con diccionario las tablas detalles compras y 
# insumos juntos 

# ------------------------------------------------------------
# en este codigo de abajo con el for lo que se esta 
# realizando es un conteo a la tabla 
# de detalle compras para luego utilizar el id en la 
# tabla insumos y poder acceder al nombre y mostrar por medio de una lista

def filtrar_compras(id_filtro):
    detalles_compras = Detalles_compras.objects.filter(id_compra=int(id_filtro))
    cant = int(len(detalles_compras))
    compras = []
    for i in range(cant): 
        iden = int(detalles_compras[i].id_insumo)
        try:
            insumos2 = Insumos.objects.get(id=iden)   
            if detalles_compras[i].id_compra:

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

def objeto_listado():

    compras_fecha = Compras.objects.all()
    cant2 = int(len(compras_fecha))
    compras_array = []


    for i in range(cant2):
        compras_array += [
            {
                'total_compra':compras_fecha[i].total_compra,
                'fecha_compra':compras_fecha[i].fecha_compra,
                'compras':filtrar_compras(compras_fecha[i].id),
                'id':compras_fecha[i].id
            },
        ]
    return compras_array

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
    if request.user.is_authenticated:
        if request.method == 'POST':
            print('entro')
            id_insumo = request.POST.get('id_insumo')
            cantidad = request.POST.get('cantidad')
            precio = request.POST.get('precio')

            # cantidad = cantidad.replace('.', '')

            total = float(cantidad) * float(precio)

            precio = precio.replace('.', '')
            
            # CODIGO PARA FORMATEAR LOS NUMEROS
            # total = ('{:,}'.format(int(total)).replace(',','.'))
            # precio = ('{:,}'.format(int(precio)).replace(',','.'))

            # print(id_insumo,cantidad,precio,total)


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
    else:
        return redirect('/')


def editar(request):

    if request.user.is_authenticated:
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
    else:
        return redirect('/')



def registrar(request):
    if request.user.is_authenticated:
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
    else:
        return redirect('/')





def borrar(request):
    if request.user.is_authenticated:
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
    else:
        return redirect('/')



    # aca finaliza el codigo de la vista de compras 


# aca comienzan las vistas de insumos 
# ----------------------------------------------------------


def insumos(request):

    if request.user.is_authenticated:
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

                # espacio de auditoria

                auditoria = Auditoria(fecha_auditoria=full_date_time,accion_realizada='Se edito el insumo: "' + editar_insumos.nombre + '"')
                auditoria.save()

                # espacio de auditoria


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

                borrar_insumos = Insumos.objects.get(id=id_borrar)
                borrar_insumos.estado = 'borrado'
                borrar_insumos.save()

                categoria = Insumos_categoria.objects.all()
                insumos = Insumos.objects.all()
                return render(request,'insumos/insumos.html',{'categoria':categoria, 'insumos':insumos})




        categoria = Insumos_categoria.objects.all()
        insumos = Insumos.objects.all()
        return render(request,'insumos/insumos.html',{'categoria':categoria, 'insumos':insumos})
    else:
        return redirect('/')


# VISTA DE PRODUCCION 

# cuando vengas pelotudo tenes que cambiar la consuta pra guardar los productos en etalles produccion

def produccion(request):
    if request.user.is_authenticated:
        productos_objetos = []

        if request.method == "POST":
            if request.POST.get('guardar'):
                id_productos = request.POST.get('id_producto')
                cantidad = request.POST.get('cantidad')

                get_producto = Productos.objects.get(id=id_productos)

                print(get_producto)
                print(cantidad)

                save_produccion = Detalles_Produccion(id_producto=get_producto,cantidad_detalle=cantidad)
                save_produccion.save()



            if request.POST.get('borrar'):
                id_borrar = request.POST.get('id_borrar')


                borrar_produccion = Detalles_Produccion.objects.filter(id=id_borrar)
                borrar_produccion.delete()

            if request.POST.get('editar'):

                iden = request.POST.get('iden')
                producto = request.POST.get('nombre_productos').split('-')[0]
                cantidad = request.POST.get('cantidad')

                print(producto)
                print(cantidad)

                get_producto = Productos.objects.get(id=producto)
                get_detalles = Detalles_Produccion.objects.get(id=iden)

                get_detalles.id_producto = get_producto
                get_detalles.cantidad_detalle = cantidad
                get_detalles.save()

            if request.POST.get('guardar_insumo'):

                cantidad_usar = request.POST.get('cantidad_usar')
                nombre_insumo = request.POST.get('nombre_insumo').split('-')[0]

                get_insumos = Insumos.objects.get(id=nombre_insumo)

                save_detalles_insumos = Detalles_insumos(id_insumos=get_insumos, Cantidad=cantidad_usar)
                save_detalles_insumos.save()

                print(get_insumos)

            if request.POST.get('borrar_insumo'):
                # print('entro en borrar insumo')
                id_borrar_insumo = request.POST.get('id_borrar')
                delete_insumo = Detalles_insumos.objects.get(id=id_borrar_insumo)
                delete_insumo.delete()

            if request.POST.get('editar_insumo'):
                print('editar')
                insumos_nombre = request.POST.get('insumos_nombre').split('-')[0]
                cantidad_usar_editar = request.POST.get('cantidad')
                id_insumo_editar = request.POST.get('editar_insumo')

                get_detalles_insumos = Detalles_insumos(id=id_insumo_editar)
                get_insumos = Insumos.objects.get(id=insumos_nombre)

                get_detalles_insumos.Cantidad = cantidad_usar_editar
                get_detalles_insumos.id_insumos = get_insumos
                get_detalles_insumos.save()

                # print(get_detalles_insumos)
                # print(get_insumos)    
                # print(id_insumo_editar)

            if request.POST.get('registrar_produccion'):
                print('entro en registrar')

                productos_registrar = request.POST.getlist('productos_enviar')
                insumos_registrar = request.POST.getlist('insumos_enviar')
                fecha_registrar = request.POST.get('fecha_enviar')

                save_produccion = Produccion(fecha_produccion=fecha_registrar,estado_produccion='En Proceso')
                save_produccion.save()

                get_produccion_last = Produccion.objects.last()


                for iterar_p in productos_registrar:
                    get_detalles_produccion = Detalles_Produccion.objects.get(id=iterar_p)
                    get_detalles_produccion.id_produccion = get_produccion_last
                    get_detalles_produccion.save()
                    # print(iterar_p)


                for iterar_i in insumos_registrar:
                    get_detalles_insumos = Detalles_insumos.objects.get(id=iterar_i)
                    get_detalles_insumos.id_produccion = get_produccion_last
                    get_detalles_insumos.save()
                    # print(iterar_i)

        Productos_para_produccion = Productos.objects.all()
        categoria = Categoria_productos.objects.all()
        insumos = Insumos.objects.all()
        categoria_insumos = Insumos_categoria.objects.all()
        productos_objetos = Detalles_Produccion.objects.all()
        detalles_insumos = Detalles_insumos.objects.all()


        return render(request,'produccion/produccion.html',{
            'nombre_productos':Productos_para_produccion,
            'categoria':categoria,
            'productos':productos_objetos,
            'insumos':insumos,
            'categoria_insumos':categoria_insumos,
            'detalles_insumos':detalles_insumos
        })


    else:
        return redirect('/')


# VISTA DE LISTADO DE PRODUCCION
def listado_produccion(request):

    if request.user.is_authenticated:
        
        if request.POST.get('terminar_produccion'):
            
            id_produccion = request.POST.getlist('detalles_produccion_registrar')
            id_producto = request.POST.getlist('id_producto')
            cantidad_final = request.POST.getlist('cantidad_final')

            id_insumos = request.POST.getlist('detalles_insumos_registrar')
            cantidad_restar_insumos = request.POST.getlist('insumos_restar_enviar')

            fecha_final = request.POST.get('fecha_produccion')

            # en este for se itera con los id de la produccion para sumar la cantidad a los productos y guardar la cantidad final utilizada

            for i in range(int(len(id_produccion))):

                get_produccion = Detalles_Produccion.objects.get(id=id_produccion[i])
                get_produccion.cantidad_real_detalle = cantidad_final[i]
                get_produccion_estado = Produccion.objects.get(id=get_produccion.id_produccion.id)
                get_produccion_estado.estado_produccion = "Terminado"
                get_produccion_estado.fecha_acabado = fecha_final

                # guardando el estado y la cantidad final

                get_produccion_estado.save()
                get_produccion.save()

                # guardando la suma en productos

                get_producto = Productos.objects.get(id=get_produccion.id_producto.id)

                suma = int(get_producto.cantidad_stock,10) + int(cantidad_final[i],10)

                get_producto.cantidad_stock = str(suma)
                get_producto.save()

                print(get_produccion)

            for i in range(int(len(id_insumos))):

                get_insumos = Insumos.objects.get(id=id_insumos[i])

                # aca se hace la resta para guardar en insumos

                resta = int(get_insumos.cantidad,10) - int(cantidad_restar_insumos[i],10) 
                get_insumos.cantidad = str(resta)
                get_insumos.save()



            # print(id_produccion)
            # print(cantidad_final)
            # print(id_producto)
            # print(id_insumos)
            
            # print(fecha_final)

        show_detalles_produccion = Detalles_Produccion.objects.all()
        show_produccion = Produccion.objects.all()
        show_detalles_insumos = Detalles_insumos.objects.all()
        return render(request,'produccion/listado_produccion.html',{'detalles_produccion':show_detalles_produccion,'produccion':show_produccion,'detalles_insumos':show_detalles_insumos})
    else:
        return redirect('/')

        


    



        

#VISTA DEL LISTADO DE LAS COMPRAS

def ver_compras(request):
    if request.user.is_authenticated:
        compras = objeto_listado()

        
        # print(imprimir[1]['compras'][0]['nombre'])
        return render(request, 'compras/listado_compras.html',{'compras':compras})
    else:
        return redirect('/')

#VISTA DE PRODUCTOS

def productos(request):

    if request.user.is_authenticated:
    # Do something for authenticated users.
        if request.method == "POST":
            if request.POST.get('guardar'):
                form = DocumentForm(request.POST, request.FILES)
                form.save()
                id_producto = request.POST.get('id_producto')
                descripcion = request.POST.get('descripcion')
                cantidad = request.POST.get('cantidad')
                precio = request.POST.get('precio')
                # precio = ('{:,}'.format(int(precio)).replace(',','.'))

                save_productos = Productos.objects.last()
                nombre_producto = Nombre_productos.objects.get(id=id_producto)
                save_productos.id_nombre_producto = nombre_producto
                save_productos.descripcion_producto = descripcion
                save_productos.cantidad_stock = cantidad
                save_productos.precio = precio
                save_productos.save()
                
                # print(id_producto,descripcion,cantidad,precio)

            if request.POST.get('agregar_nombre'):
                id_categoria = request.POST.get('id_categoria')
                nombre_producto = request.POST.get('nombre_producto')

                get_categoria = Categoria_productos.objects.get(id=id_categoria) 
                save_productos = Nombre_productos(nombre_productos=nombre_producto,categoria=get_categoria)
                save_productos.save()
                # print('entro en agregar')

                
                

        else:
            form = DocumentForm(request.POST or None)
        
        categoria = Categoria_productos.objects.all()
        nombre_producto = Nombre_productos.objects.all()

        try:
            return render(request, 'productos/productos.html',{'categoria':categoria, 'nombre':nombre_producto, 'form':form})
        except:
            form = DocumentForm()
            return render(request, 'productos/productos.html',{'categoria':categoria, 'nombre':nombre_producto, 'form':form})

    else:
        return redirect('/')


def listado_productos(request):

    if request.user.is_authenticated:
        productos = Productos.objects.all()

        if request.method == 'POST':
            if request.POST.get('cambiar_valor'):
                iden = request.POST.get('id')
                cantidad = request.POST.get('cantidad_enviar')

                get_productos = Productos.objects.get(id=iden)
                get_productos.cantidad_stock = cantidad
                get_productos.save()
    
        if request.POST.get('editar'):

                #se estira el id del registro que se va a editar
                iden = request.POST.get('iden')             
                precio = request.POST.get('precio')
                
                get_productos = Productos.objects.get(id=iden)

                # espacio de auditoria

                save_auditoria = Auditoria(fecha_auditoria=full_date_time,accion_realizada='Se edito el producto: "' + get_productos.id_nombre_producto.nombre_productos + '" con precio: ' + get_productos.precio + ', al precio actual de: ' + precio)
                save_auditoria.save()

                # espacio de auditoria

                get_productos.precio = precio
                get_productos.save()

                
        filtroNombre = request.POST.get('filtroNombre')
    
        # for mostrar in productos:
        #     hola = mostrar.id_nombre_producto.nombre_productos
        #     print(hola)

        if filtroNombre != '' and filtroNombre is not None:       
            productos = productos.filter(Q(precio = filtroNombre) | Q(descripcion_producto__icontains = filtroNombre) | Q(cantidad_stock = filtroNombre) | Q( id_nombre_producto__nombre_productos__icontains = filtroNombre))


        return render(request,'productos/listado_productos.html',{'productos':productos})
    else:
        return redirect('/')

def ventas(request):

    if request.user.is_authenticated:

        detalles_pedidos = Detalles_pedidos.objects.all()
        pedidos = Pedidos.objects.all()
        ventas = Ventas.objects.all()

        return render(request, 'ventas/ventas.html',{'ventas':ventas,'pedidos':pedidos,'detalles_pedidos':detalles_pedidos})
    else:
        return redirect('/')



def login(request):
    if request.user.is_authenticated:
    # Do something for authenticated users.
        return redirect('/home')
    else:

        if request.method == 'POST':

            passsword = request.POST.get('pass')
            user = request.POST.get('user')
            user = authenticate(username=user, password=passsword)
            if user is not None:
                dj_login(request, user)
                # A backend authenticated the credentials
                return redirect('/home')

        return render(request,'login/login.html')

def logout_views(request):
    logout(request) 
    return redirect('/')

# VISTA NOMBRE PRODUCTOS 

def nombre_productos(request):

    if request.user.is_authenticated:

        if request.method == "POST":
            if request.POST.get('guardar'):
                
                id_categoria = request.POST.get('categoria')
                nombre_productos = request.POST.get('nombre_productos')
                
                get_categoria = Categoria_productos.objects.get(id=id_categoria)
                save_nombre_productos = Nombre_productos(nombre_productos=nombre_productos, categoria=get_categoria)
                save_nombre_productos.save()

            if request.POST.get('borrar'):
                id_borrar = request.POST.get('id_borrar')
                get_productos = Nombre_productos.objects.get(id=id_borrar)
                get_productos.estado = 'borrado'
                get_productos.save()

            if request.POST.get('editar'):


                #se estira el id del registro que se va a editar
                iden = request.POST.get('iden') 
                #se estira el id de la categoria se va a editar
                id_categoria = request.POST.get('categoria')
                nombre = request.POST.get('nombre')
                print(id_categoria)
                

                editar_nombre_productos = Nombre_productos.objects.get(id=iden)

                get_categoria = Categoria_productos.objects.get(id=id_categoria)
                editar_nombre_productos.nombre_productos = nombre
                editar_nombre_productos.categoria = get_categoria                
                editar_nombre_productos.save()

            
        categoria = Categoria_productos.objects.all()
        nombre_productos = Nombre_productos.objects.all()

        return render(request, 'nombre_productos/nombre_productos.html',{'categoria':categoria, 'nombre':nombre_productos})
    else:
        return redirect('/')

# VISTA PEDIDOS

def pedidos(request):

    if request.user.is_authenticated:

        if request.POST.get('guardar'):

            id_producto = request.POST.get('nombre_productos').split('-')[0]
            cantidad_pedido = request.POST.get('cantidad_pedido')
            precio_pedido = request.POST.get('precio_pedido')
            precio_producto = request.POST.get('precio_producto')

            get_productos = Productos.objects.get(id=id_producto)

            save_detalles_pedidos = Detalles_pedidos(id_producto=get_productos,cantidad=cantidad_pedido,precio=precio_producto,subtotal_producto=precio_pedido)
            save_detalles_pedidos.save()

            # print(get_productos)
            # print(cantidad_pedido)
            # print(precio_pedido)
            # print(precio_producto)

        if request.POST.get('borrar'):

            id_pedido_borrar = request.POST.get('id_borrar')

            print(id_pedido_borrar)

            get_pedido_borrar = Detalles_pedidos.objects.get(id=id_pedido_borrar)
            get_pedido_borrar.delete()

        if request.POST.get('registrar_pedido'):

            fecha_pedido = request.POST.get('fecha_pedido')
            id_pedido = request.POST.getlist('id_pedidos')
            enviar_cliente = request.POST.get('enviar_cliente')
            total_pedido = request.POST.get('total_pedido')

            print('entro en registrar')
            print(fecha_pedido)
            print(id_pedido)
            print(enviar_cliente)
            print(total_pedido)

            # codigo para guardar el pedido antes de registrar 

            get_cliente = Clientes.objects.get(id=enviar_cliente)

            save_pedido = Pedidos(id_cliente=get_cliente,estado_pedido='En Proceso',fecha_pedido=fecha_pedido,precio_total=total_pedido)
            save_pedido.save()

            get_last_pedido = Pedidos.objects.last()

            for pedidos in id_pedido:
                
                save_pedido_final = Detalles_pedidos.objects.get(id=pedidos)
                save_pedido_final.id_pedido = get_last_pedido
                save_pedido_final.save()



        clientes = Clientes.objects.all()
        categoria = Categoria_productos.objects.all()
        nombre_productos = Productos.objects.all()
        detalles_pedidos = Detalles_pedidos.objects.all()

        return render(request, 'pedidos/pedidos.html',{'clientes':clientes, 'categoria':categoria, 'productos':nombre_productos,'pedidos':detalles_pedidos})
    else:
        return redirect('/')

# VISTA CLIENTES

def clientes(request):

    if request.user.is_authenticated:

        if request.method == "POST":
            if request.POST.get('guardar'):
                
                nombre_cliente = request.POST.get('nombre_cliente')
                direccion = request.POST.get('direccion')
                telefono = request.POST.get('telefono')

                save_clientes = Clientes(nombre_cliente=nombre_cliente, direccion=direccion, telefono=telefono)
                save_clientes.save()

        if request.POST.get('borrar'):
                id_borrar = request.POST.get('id_borrar')
                get_clientes = Clientes.objects.get(id=id_borrar)
                get_clientes.estado = 'borrado'
                get_clientes.save()

        if request.POST.get('editar'):


                #se estira el id del registro que se va a editar
                iden = request.POST.get('iden')             
                nombre_cliente = request.POST.get('nombre_cliente')
                direccion = request.POST.get('direccion')
                telefono = request.POST.get('telefono')
                

                editar_clientes = Clientes.objects.get(id=iden)

                
                editar_clientes.nombre_cliente = nombre_cliente
                editar_clientes.direccion = direccion 
                editar_clientes.telefono = telefono           
                editar_clientes.save()

        
        clientes = Clientes.objects.all()

        return render(request, 'clientes/clientes.html',{'clientes':clientes})
    else:
        return redirect('/')

    
def listado_pedidos(request):

    if request.user.is_authenticated:
        if request.POST.get('finalizar_pedido'):
            fecha_pedido = request.POST.get('fecha_finalizar_pedido')
            id_pedido = request.POST.get('id_pedido')


            # print('finalizar_pedido')
            # print(fecha_pedido)
            # print(id_pedido)

            # en la linea de abajo se guarda la venta para despues instanciar el ultimo registro
    
            save_venta = Ventas(fecha_venta=fecha_pedido)
            save_venta.save()

            get_venta = Ventas.objects.last()

            # luego se estira el pedido con el id que rse recibio de la vista de listado pedido para luego guardar el id de la vista de ventas estirada anteriormente

            get_pedido = Pedidos.objects.get(id=id_pedido)
            get_pedido.id_ventas = get_venta
            get_pedido.estado_pedido = "Terminado"

            # en esta porcion de codigo se ealiza consutas para estirar el producto del cual se va a restar la cantidad que se solicito en el pedido una vez confirmado el mismo

            get_detalles_pedidos = Detalles_pedidos.objects.last()
            get_productos = Productos.objects.get(id=get_detalles_pedidos.id_producto.id)


            cantidad_actual_productos = int(get_productos.cantidad_stock)
            cantidad_restar_productos = int(get_detalles_pedidos.cantidad)

            resultado_resta_productos = cantidad_actual_productos - cantidad_restar_productos

            # print(type(cantidad_actual_productos))
            # print(type(cantidad_restar_productos))
            # print(resultado_resta_productos)

            get_productos.cantidad_stock = str(resultado_resta_productos)

            get_productos.save()
            get_pedido.save()

        if request.POST.get('borrar'):
                id_borrar = request.POST.get('id_borrar')
                get_pedidos = Pedidos.objects.get(id=id_borrar)

                # espacio de auditoria

                save_auditoria = Auditoria(fecha_auditoria=full_date_time,accion_realizada="Se elimino el pedido con la fecha: " + get_pedidos.fecha_pedido)
                save_auditoria.save()
                # espacio de auditoria

                get_pedidos.delete()



        pedidos = Pedidos.objects.all()
        detalles_pedidos = Detalles_pedidos.objects.all()

        return render(request, 'pedidos/listado_pedidos.html',{'pedidos':pedidos,'detalles_pedidos':detalles_pedidos})
    else:
        return redirect('/')


def login2(request):


    if request.user.is_authenticated:
    # Do something for authenticated users.
        return redirect('/home')
    else:

        if request.method == 'POST':

            passsword = request.POST.get('pass')
            user = request.POST.get('user')
            user = authenticate(username=user, password=passsword)
            if user is not None:
                dj_login(request, user)
                # A backend authenticated the credentials
                return redirect('/home')

        return render(request,'login/login2.html')

def auditoria(request):

    if request.user.is_authenticated:

        auditoria = Auditoria.objects.all()
        return render(request, 'auditoria/auditoria.html',{'auditoria':auditoria})
    else:
        return redirect('/')

def gestionar_usuario(request):

    if request.user.is_authenticated:
        return render(request, 'gestionar_usuario/gestionar_usuario.html')
    else:
        return redirect('/')

def back_up(request):

    if request.user.is_authenticated:

        if request.POST.get('make_backup'):

            # print('entro en crear abckup')

            # from subprocess import Popen, PIPE

            # process = Popen(['python', 'manage.py dumpdata > db.json'], stdout=PIPE, stderr=PIPE)
            # stdout, stderr = process.communicate()

            # subprocess.call(["python ", "manage.py ","dumpdata"])

            # subprocess.run(["python", "manage.py","dumpdata", " >. db.json"], stdout=subprocess.PIPE)


            full_date_time = str(datetime.datetime.now()).split('.')[0].replace(' ','_').replace(':','_').replace('-','_')
            full_date_time_for_db = str(datetime.datetime.now()).split('.')[0]

            save_back_up = Back_up(nombre_back_up=full_date_time_for_db,nombre_archivo=full_date_time)
            save_back_up.save()

            print(full_date_time)
            os.system("python manage.py dumpdata --exclude auth.permission --exclude contenttypes > backup/" + full_date_time + ".json")




        if request.POST.get('restore_back_up'):
            back_up = Back_up.objects.last()
            nombre_archivo = back_up.nombre_archivo

            print(nombre_archivo)
            os.system("python manage.py loaddata backup/" + nombre_archivo + ".json")

            # print('entro en restore')

        
        back_up = Back_up.objects.last()

        return render(request, 'backup/backup.html',{'back_up':back_up})



    else:
        return redirect('/')

        
