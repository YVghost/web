from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegistroEstudianteForm
from .models import Estudiante

## REGISTRO 
def registro(request):
    if request.method == "POST":
        form = RegistroEstudianteForm(request.POST)
        if form.is_valid():
            estudiante = form.save()
            
            # Autenticar automáticamente al usuario
            user = authenticate(
                username=form.cleaned_data['correo'],
                password=form.cleaned_data['password1']
            )
            if user:
                login(request, user)
                messages.success(request, "¡Cuenta creada exitosamente!")
                return redirect("explorar")  
    else:
        form = RegistroEstudianteForm()
    
    return render(request, "usuarios/registro.html", {"form": form})

## LOGIN - (usando Django Auth)
def login_estudiante(request):
    if request.method == "POST":
        # Usar 'username' y 'password' que espera Django
        username = request.POST.get("username")  
        password = request.POST.get("password")
        
        # Autenticar con el sistema seguro de Django
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"¡Bienvenido de vuelta, {user.first_name}!")
            return redirect("explorar")  # Cambia por tu vista principal
        else:
            messages.error(request, "Correo o contraseña incorrectos")
    
    return render(request, "usuarios/login.html")

## LOGOUT - Corregido (usando Django Auth)
def logout_estudiante(request):
    logout(request)
    messages.success(request, "Has cerrado sesión exitosamente")
    return redirect("login")

## PERFIL
@login_required
def perfil(request, banner_id):
    try:
        estudiante = Estudiante.objects.get(user=request.user, banner_id=banner_id)
        return render(request, "usuarios/perfil.html", {"estudiante": estudiante})
    except Estudiante.DoesNotExist:
        messages.error(request, "Perfil no encontrado")
        return redirect("explorar")
