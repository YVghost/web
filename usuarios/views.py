from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from .forms import RegistroEstudianteForm
from .models import Estudiante
from django.contrib import messages

## register

def registro(request):
    if request.method == "POST":
        form = RegistroEstudianteForm(request.POST)
        if form.is_valid():
            estudiante = form.save(commit=False)
            estudiante.save()
            return redirect("registro")
    else:
        form = RegistroEstudianteForm()
    return render(request, "usuarios/registro.html", {"form": form})

## login

def login_estudiante(request):
    if request.method == "POST":
        correo = request.POST.get("correo")
        apodo = request.POST.get("apodo")
        try:
            estudiante = Estudiante.objects.get(correo=correo, apodo=apodo)
            request.session["estudiante_id"] = estudiante.banner_id
            return redirect("perfil", banner_id=estudiante.banner_id)
        except Estudiante.DoesNotExist:
            messages.error(request, "Correo o apodo incorrecto")
    return render(request, "usuarios/login.html")

## logout|

def logout_estudiante(request):
    request.session.flush()
    return redirect("login")

## listar

def lista_estudiantes(request):
    estudiantes = Estudiante.objects.all()
    return render(request, "usuarios/lista.html", {"estudiantes": estudiantes})

## perfil

def perfil(request, banner_id):
    estudiante = get_object_or_404(Estudiante, banner_id=banner_id)
    return render(request, "usuarios/perfil.html", {"estudiante": estudiante})
