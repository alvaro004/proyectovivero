from django.shortcuts import render
from templatedjango.apptemplate.models import *

# Create your views here.


def compras(request):

    if request.method == 'POST':
        print('entro')
        categoria = request.POST.get('categoria')
        nombre_producto = request.POST.get('nombre_producto')
        cantidad = request.POST.get('cantidad')
        precio = request.POST.get('precio')

        total = int(cantidad) * int(precio)

        print(categoria,nombre_producto,cantidad,precio,total)

        detalles_compras = Detalles_compras(id_insumo=categoria,cantidad=cantidad,precio=precio,subtotal=total)
        
        detalles_compras.save()

        insumos = Insumos(nombre=nombre_producto)

        detalles_compras = Detalles_compras.objects.all()


        return render(request,'compras.html',{'compras':detalles_compras})


    return render(request,'compras.html')

def chorizo(request):

    return render(request,'prueba.html')

def prueba(request):

    return render(request,'prueba2.html')