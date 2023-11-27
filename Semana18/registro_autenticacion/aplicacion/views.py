from django.shortcuts import render,redirect
from .formularios.registerform import NewUserForm
from .formularios.loginform import LoginForm
from django.http import HttpResponseRedirect
from .models import Productos,Proveedores
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

def reg_user(request):
    if request.method == "POST":
        formulario = NewUserForm(request.POST)
        if formulario.is_valid():
            formulario.save() 
        return HttpResponseRedirect("/") 
    else: 
        formulario = NewUserForm()
        return render(request,"Reg_user.html",{"form":formulario})

def iniciar_sesion(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required(login_url='login')
def index(request):
    es_estudiante = request.user.groups.filter(name='Estudiante').exists()
    es_admin = request.user.is_staff
    if es_estudiante or es_admin:
        proveedores = Proveedores.objects.all()
        productos = Productos.objects.all()
        return render(request, 'index.html', {'user': request.user, 'es_estudiante': es_estudiante, 'es_admin': es_admin,'proveedores':proveedores,'productos':productos})

def cerrar_sesion(request):
    logout(request) 
    return redirect('login')

def agregarProveedor(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        telefono = request.POST.get('telefono')
        proveedor = Proveedores(nombre=nombre, telefono=telefono)
        proveedor.save()
        return redirect('home')

    return render(request, "agregar_proveedor.html")

def agregarProducto(request):
    proveedores = Proveedores.objects.all()
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        stock = request.POST.get('stock')
        proveedor_nombre = request.POST.get('proveedor')
        proveedor = Proveedores.objects.get(nombre=proveedor_nombre)
        fk_prov = proveedor
        producto = Productos(nombre=nombre,stock=stock,fk_prov=fk_prov)
        producto.save()
        return redirect('home')

    return render(request, "agregar_producto.html",{'proveedores':proveedores})