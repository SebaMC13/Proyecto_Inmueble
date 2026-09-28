from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth import login
from . import models
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.core.exceptions import PermissionDenied


def index(request):
    inmuebles = models.Inmueble.objects.all()
    region_id = request.GET.get("region")
    if region_id:
        inmuebles = inmuebles.filter(comuna__region=region_id)

    comuna_id = request.GET.get("comuna")
    if comuna_id:
        inmuebles = inmuebles.filter(comuna=comuna_id)
    regiones = models.Region.objects.annotate(total_inmuebles=Count("comuna__inmueble"))
    comunas = models.Comuna.objects.annotate(total_inmuebles=Count("inmueble"))
    contexto = {"inmuebles": inmuebles, "regiones": regiones, "comunas": comunas}
    return render(request, "index.html", contexto)


def registro(request):
    if request.method == "POST":
        form = forms.CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("indice")
    else:
        form = forms.CustomUserCreationForm()

    return render(request, "registration/register.html", {"form": form})


def dashboard(request):
    inmuebles = models.Inmueble.objects.filter(dueno=request.user)
    contexto = {"inmuebles": inmuebles}
    return render(request, "dashboard.html", contexto)


def act_perfil(request):
    if request.method == "POST":
        form = forms.ActualizarUsuarioForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = forms.ActualizarUsuarioForm(instance=request.user)

    return render(request, "act_perfil.html", {"form": form})


def nuevo_inmueble(request):
    if request.method == "POST":
        form = forms.NuevoInmuebleForm(request.POST)
        if form.is_valid():
            inmueble = form.save(commit=False)
            inmueble.dueno = request.user
            inmueble.save()
            return redirect("dashboard")
    else:
        form = forms.NuevoInmuebleForm()
    return render(request, "nuevo_inmueble.html", {"form": form})


def actualizar_inmueble(request, id):
    inmueble = get_object_or_404(klass=models.Inmueble, id=id)
    if request.method == "POST":
        form = forms.ActualizarInmuebleForm(request.POST, instance=inmueble)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = forms.ActualizarInmuebleForm(instance=inmueble)

    return render(
        request, "actualizar_inmueble.html", {"form": form, "inmueble": inmueble}
    )


def borrar_inmueble(request, id: int):
    if request.method == "POST":
        inmueble = get_object_or_404(klass=models.Inmueble, id=id)
        if inmueble.dueno != request.user:
            raise PermissionDenied("ACCESO DENEGADO (no es dueño de esta vivienda)")
        inmueble.delete()
    return redirect("dashboard")
