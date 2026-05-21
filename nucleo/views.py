from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from .forms import ContactoForm


def contacto(request):
    if request.method == "POST":
        form = ContactoForm(request.POST)
        if form.is_valid():
            # Procesar los datos (ej: enviar correo, guardar en BD)
            nombre = form.cleaned_data["nombre"]
            correo = form.cleaned_data["correo"]
            mensaje = form.cleaned_data["mensaje"]
            # Por ahora solo mostramos una pantalla de éxito
            return render(request, "nucleo/exito.html", {"nombre": nombre})
    else:
        form = ContactoForm()

    return render(request, "nucleo/contacto.html", {"form": form})
