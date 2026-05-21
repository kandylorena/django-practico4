# Guía — Actividad Módulo 6 Lección 4

## Formularios en Django (Form y ModelForm)

---

## Parte A — Instalación del proyecto desde cero

### 1. Crear el entorno virtual

```bash
python -m venv venv
```

### 2. Activar el entorno virtual

```bash
source venv/bin/activate
```

Verás aparecer `(venv)` al inicio del prompt.

### 3. Instalar Django

```bash
pip install django
```

Verificar:

```bash
python -m django --version
```

### 4. Crear el proyecto Django

Creamos el proyecto en el directorio actual (el `.` evita que cree una subcarpeta extra):

```bash
django-admin startproject config .
```

Esto genera:

```
config/
  __init__.py
  settings.py
  urls.py
  asgi.py
  wsgi.py
manage.py
```

### 5. Crear la aplicación

```bash
python manage.py startapp nucleo
```

Esto genera:

```
nucleo/
  __init__.py
  admin.py
  apps.py
  models.py
  tests.py
  views.py
  migrations/
```

### 6. Registrar la app en `config/settings.py`

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "nucleo",  # <-- agregar esta línea
]
```

### 7. Configurar la carpeta de templates

Crear la carpeta:

```bash
"templates"
```

En `config/settings.py`, buscar la línea `TEMPLATES` y modificar `DIRS`:

```python
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],  # <-- cambiar a ["templates"] si usas templates globales
        "APP_DIRS": True,
        ...
    },
]
```

Con `APP_DIRS: True`, Django ya busca plantillas dentro de `nucleo/templates/`. No hace falta tocar `DIRS` por ahora.

### 8. Crear la plantilla base `base.html`

`nucleo/templates/nucleo/base.html`:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Mi Proyecto{% endblock %}</title>
</head>
<body>
    <header>
        <h1>Mi Proyecto Django</h1>
        <nav>
            <a href="{% url 'contacto' %}">Contacto</a>
        </nav>
        <hr>
    </header>

    <main>
        {% block content %}
        {% endblock %}
    </main>

    <footer>
        <hr>
        <p>&copy; 2026 - Mi Proyecto Django</p>
    </footer>
</body>
</html>
```

### 9. Verificar que todo funciona

```bash
python manage.py runserver
```

Abrir `http://127.0.0.1:8000/` — debería mostrar la página de bienvenida de Django.

---

## Parte B — Actividad M6 L4

### 1. Crear la carpeta de la actividad

```bash
mkdir -p actividad_m6_l4
```

Dentro de esta carpeta guardaremos los archivos relevantes como referencia. Pero los archivos funcionales se crean dentro de la app `nucleo/`.

### 2. Crear el formulario — `nucleo/forms.py`

```python
from django import forms


class ContactoForm(forms.Form):
    nombre = forms.CharField(
        max_length=100,
        label="Nombre",
        widget=forms.TextInput(attrs={"placeholder": "Tu nombre"})
    )
    correo = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={"placeholder": "tu@correo.com"})
    )
    mensaje = forms.CharField(
        label="Mensaje",
        widget=forms.Textarea(attrs={"placeholder": "Escribe tu mensaje aquí", "rows": 5}),
        validators=[]
    )

    def clean_mensaje(self):
        mensaje = self.cleaned_data.get("mensaje")
        if len(mensaje) < 10:
            raise forms.ValidationError("El mensaje debe tener al menos 10 caracteres.")
        return mensaje
```

**Explicación:**
- `forms.Form` → formulario sin modelo asociado.
- Cada campo define su tipo (`CharField`, `EmailField`) y su widget HTML.
- El método `clean_mensaje` es un **validador personalizado**. Django lo llama automáticamente durante la validación.
- `ValidationError` lanza el error que se muestra en el template.

### 3. Crear la vista — `nucleo/views.py`

```python
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
```

**Explicación:**
- `if request.method == "POST"`: detecta si el usuario envió el formulario.
- `ContactoForm(request.POST)`: crea el formulario con los datos enviados.
- `form.is_valid()`: ejecuta todas las validaciones (incluyendo `clean_mensaje`).
- `form.cleaned_data`: diccionario con los datos **ya validados** y limpios.
- Si GET: se pasa un formulario vacío.

### 4. Crear la plantilla del formulario — `nucleo/templates/nucleo/contacto.html`

```html
{% extends "nucleo/base.html" %}

{% block title %}Contacto{% endblock %}

{% block content %}
    <h2>Formulario de Contacto</h2>

    <form method="post" novalidate>
        {% csrf_token %}

        {% if form.non_field_errors %}
            <div class="errores">
                {% for error in form.non_field_errors %}
                    <p>{{ error }}</p>
                {% endfor %}
            </div>
        {% endif %}

        {% for field in form %}
            <div>
                <p>
                    {{ field.label_tag }}
                    {{ field }}
                </p>
                {% if field.errors %}
                    <ul style="color: red;">
                        {% for error in field.errors %}
                            <li>{{ error }}</li>
                        {% endfor %}
                    </ul>
                {% endif %}
            </div>
        {% endfor %}

        <button type="submit">Enviar</button>
    </form>

    <p><a href="{% url 'contacto' %}">Limpiar formulario</a></p>
{% endblock %}
```

**Explicación:**
- `{% extends "nucleo/base.html" %}`: hereda la estructura de `base.html`.
- `{% csrf_token %}`: protección obligatoria contra CSRF en Django.
- `novalidate` en `<form>`: desactiva la validación nativa del navegador para poder ver los errores de Django.
- `{{ field.label_tag }}`: renderiza la etiqueta `<label>`.
- `{{ field }}`: renderiza el `<input>` correspondiente.
- `{{ field.errors }}`: lista de errores de ese campo específico.
- `form.non_field_errors`: errores generales del formulario.

### 5. Crear la plantilla de éxito — `nucleo/templates/nucleo/exito.html`

```html
{% extends "nucleo/base.html" %}

{% block title %}Mensaje Enviado{% endblock %}

{% block content %}
    <h2>¡Mensaje enviado con éxito!</h2>
    <p>Gracias, <strong>{{ nombre }}</strong>. Hemos recibido tu mensaje.</p>
    <p><a href="{% url 'contacto' %}">Enviar otro mensaje</a></p>
{% endblock %}
```

### 6. Configurar las URLs

`config/urls.py`:

```python
from django.contrib import admin
from django.urls import path
from nucleo import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("contacto/", views.contacto, name="contacto"),
]
```

### 7. Probar

```bash
python manage.py runserver
```

Abrir `http://127.0.0.1:8000/contacto/`.

**Prueba los siguientes casos:**
1. Enviar vacío → ver errores de "Este campo es obligatorio".
2. Escribir "hola" en mensaje → error "debe tener al menos 10 caracteres".
3. Correo inválido → error "Introduzca una dirección de correo electrónico válida".
4. Todo correcto → página de éxito.

---

## Resumen de archivos creados

```
django-practico4/
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py           # ← se agrega ruta contacto/
│   ├── asgi.py
│   └── wsgi.py
├── nucleo/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py           # ← NUEVO: ContactoForm
│   ├── models.py
│   ├── templates/
│   │   └── nucleo/
│   │       ├── base.html   # ← NUEVO: plantilla base
│   │       ├── contacto.html  # ← NUEVO: formulario
│   │       └── exito.html     # ← NUEVO: confirmación
│   ├── tests.py
│   └── views.py           # ← se modifica: vista contacto
├── actividad_m6_l4/       # ← carpeta de referencia
├── manage.py
├── GUIA_M6_L4.md          # ← este archivo
├── .gitignore
└── README.md
```

---

## Buenas prácticas aplicadas

| Práctica | Aplicación |
|---|---|
| Separación de responsabilidades | Form en `forms.py`, vista en `views.py`, template en `templates/` |
| Reutilización de plantillas | `base.html` con bloques `{% block %}` |
| Validación del lado del servidor | `clean_mensaje()` con `ValidationError` |
| Protección CSRF | `{% csrf_token %}` en el formulario |
| Manejo de errores por campo | `{{ field.errors }}` renderizado bajo cada campo |
| Datos limpios | `form.cleaned_data` en vez de `request.POST` directo |
