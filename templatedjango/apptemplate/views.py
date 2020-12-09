from django.shortcuts import render
from templatedjango.apptemplate.models import *
from templatedjango.apptemplate.forms import *
from django.contrib.auth import authenticate, login as dj_login
from django.contrib.auth import logout
from django.shortcuts import redirect

# Create your views here.



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
    else:
        return redirect('/')


# VISTA DE PRODUCCION 

def produccion(request):
    if request.user.is_authenticated:
        productos_objetos = []

        if request.method == "POST":
            if request.POST.get('guardar'):
                id_productos = request.POST.get('id_producto')
                cantidad = request.POST.get('cantidad')

                detalles_Produccion = Detalles_Produccion(id_producto=id_productos, cantidad_detalle=cantidad)
                detalles_Produccion.save()
            
                productos_objetos = objetos_productos()
                # print(productos_objetos)
                # print(filtrar_produccion[0].id_producto)

                # print(id_borrar)

            if request.POST.get('borrar'):
                id_borrar = request.POST.get('id_borrar')

                print(id_borrar)

                borrar_produccion = Detalles_Produccion.objects.filter(id=id_borrar)
                borrar_produccion.delete()

            # if request.POST.get('editar'):
                



        if not productos_objetos:
            productos_objetos = objetos_productos()

        Productos_para_produccion = Nombre_productos.objects.all()
        categoria = Categoria_productos.objects.all()
        return render(request,'produccion/produccion.html',{'nombre_productos':Productos_para_produccion,'categoria':categoria,'productos':productos_objetos})
    else:
        return redirect('/')


# VISTA DE LISTADO DE PRODUCCION
def listado_produccion(request):
    return render(request,'produccion/listado_produccion.html')


# VISTA DEL INICIO 

def inicio(request):

    if request.user.is_authenticated:
        return render(request, 'inicio/inicio.html')
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

                save_productos = Productos.objects.last()
                nombre_producto = Nombre_productos.objects.get(id=id_producto)
                save_productos.id_nombre_producto = nombre_producto
                save_productos.descripcion_producto = descripcion
                save_productos.cantidad_stock = cantidad
                save_productos.precio = precio
                save_productos.save()
                
                print(id_producto,descripcion,cantidad,precio)
        else:
            form = DocumentForm(request.POST or None)

        
        categoria = Categoria_productos.objects.all()
        nombre_producto = Nombre_productos.objects.all()

        return render(request, 'productos/productos.html',{'categoria':categoria, 'nombre':nombre_producto, 'form':form})
    else:
        return redirect('/')


def listado_productos(request):

    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.POST.get('cambiar_valor'):
                iden = request.POST.get('id')
                cantidad = request.POST.get('cantidad_enviar')

                get_productos = Productos.objects.get(id=iden)
                get_productos.cantidad_stock = cantidad
                get_productos.save()

        productos = Productos.objects.all()
        print(productos)
        return render(request,'productos/listado_productos.html',{'productos':productos})
    else:
        return redirect('/')

def ventas(request):

    if request.user.is_authenticated:
        # if request.method == "POST":
        #     if request.POST.get('guardar'):
        categoria = Categoria_productos.objects.all()

        nombre_producto = Nombre_productos.objects.all()


        return render(request, 'ventas/ventas.html',{'categoria':categoria,'nombre_producto':nombre_producto})
    else:
        return redirect('/')



        


def login(request):
    if request.user.is_authenticated:
    # Do something for authenticated users.
        return redirect('/inicio')
    else:

        if request.method == 'POST':

            passsword = request.POST.get('pass')
            user = request.POST.get('user')
            user = authenticate(username=user, password=passsword)
            if user is not None:
                dj_login(request, user)
                # A backend authenticated the credentials
                return redirect('/inicio')

        return render(request,'login/login.html')

def logout_views(request):
    logout(request) 
    return redirect('/')


