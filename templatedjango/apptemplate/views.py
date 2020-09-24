from django.shortcuts import render

# Create your views here.


def index(request):
    variable = 'hola mundo'

    return render(request,'index.html',{'var':variable})

def chorizo(request):

    return render(request,'prueba.html')

def prueba(request):

    return render(request,'prueba2.html')