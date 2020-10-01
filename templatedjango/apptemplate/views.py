from django.shortcuts import render
from templatedjango.apptemplate.models import *

# Create your views here.


def compras(request):

    if request.method == 'POST':
        print('entro')
        id_insumo = request.POST.get('id_insumo')
        cantidad = request.POST.get('cantidad')
        precio = request.POST.get('precio')

        total = int(cantidad) * int(precio)

        print(categoria,nombre_producto,cantidad,precio,total)

        detalles_compras = Detalles_compras(id_insumo=id_insumo,cantidad=cantidad,precio=precio,subtotal=total,unidad_de_medida=unidad_medida)
        
        detalles_compras.save()

        # insumos = Insumos(nombre=nombre_producto)
        # insumos.save()

        detalles_compras = Detalles_compras.objects.all()
        insumos = Insumos.objects.(id=id_insumo)
        categoria_insumos = Insumos_categoria.objects.all()

        return render(request,'compras.html',{'compras':detalles_compras,'insumos':insumos,'categoria':categoria_insumos})


    insumos = Insumos.objects.all()
    detalles_compras = Detalles_compras.objects.all()
    categoria_insumos = Insumos_categoria.objects.all()
    print(insumos[0])
    return render(request,'compras.html',{'compras':detalles_compras,'insumos':insumos,'categoria':categoria_insumos})

def chorizo(request):

    return render(request,'prueba.html')

def prueba(request):

    return render(request,'prueba2.html')