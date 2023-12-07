# ToDoApp_Project
Aplicacion Web para tareas

#Creacion de la aplicación web ToDoApp_AdaSchool

## Creamos un Entorno Virtual (Virtual Environment) por buenas practicas.

  - [Guia para Windows](https://micro.recursospython.com/recursos/como-crear-un-entorno-virtual-venv.html):

1. Abrimos la terminal y nos ubicamos en la carpeta donde queremos crear el entorno virtual.
2. Escribe en la terminal: ```python -m venv env```
3. Escribe en la terminal: ```env\Scripts\activate``` o ```env\Scripts\activate.bat```

PD:
   Usar nombres como venv o env para llamar a tus entornos virtuales, es una buena practica.
    
## Instalación de Django y DRF: 
Primero, necesitamos tener instalado Django y DRF en tu computadora. Para instalar Django y DRF, abre la terminal y escribe: ```pip install django djangorestframework```

## Comenzamos con la aplicación web

Creamos el proyecto con el nombre 'todoapp' 
```
django-admin startproject todoapp
``` 
Nos ubicamos adentro de la carpetal del proyecto 
```
cd todoapp
```
Creamos nuestra aplicacion adentro del proyecto
```
python manage.py starapp taks
```
Ahora nos ubicamos en la carpeta `todoapp/settings.py`

Debemos adjuntar lo siguiente en `INSTALLED_APPS` el nombre de nuestra aplicación
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework', # agregamos drf
    'tasks', # agregamos la app
]
```

Definimos los modelos en la carpeta de la aplicación `tasks/models.py`
```python
from django.db import models
from django.utils import timezone

class Task(models.Model):
    STATUS_CHOICES = (
        ('P', 'Pendiente'),
        ('C', 'Completado'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')

    def __str__(self):
        return self.title
```

Tenemos que realizar las migraciones con los siguientes comando en la consola:

```
# Hace las migraciones correspodientes para tu modelo de tareas, para definir cómo se estructurará la base de datos
python manage.py makemigrations tasks

```

# Despues, ejecuta el soigueinte comando, se generarán las migraciones para crear la tabla en la base de datos
python manage.py migrate
```
Ahora revisa la base de datos `db.sqlite3` y observa si ya se encuentran creadas las tablas

## Serializar

Creamos el archivo para serializar en la carpeta de nuestra app: `tasks/serializers.py`

```python
from rest_framework import serializers
from .models import Task

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'created_at' , 'status'] # ['__all__']
```

## Vistas para nuestra aplicación web

En nuestro archivo `views.py` que esta dentro de nuestra carpeta `task`:
```python
from rest_framework import generics
from .models import Task
from .serializers import PostSerializer

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = PostSerializer


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = PostSerializer

```
## Configuración de las URL

Creamos el archivo `urls.py` dentro de `tasks`, configura las URL para tu vista:

```python
from django.urls import path
from .views import PostListCreateView, PostDetailView

urlpatterns = [
    path('api/posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('api/posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
]
```

y luego en el archivo `todoapp/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tasks.urls')),
]

```

## Ejecutamos el proyecto
```
python manage.py runserver
```


## Agregando los templates

Ahora vamos a decidir cómo queremos que se vea nuestra habitación de tareas. Para hacer esto, crea una nueva carpeta llamada `templates` dentro de la carpeta `tasks`. Dentro de la carpeta `templates`, crearemos nuestros archivos `.html`:

```tasks/templates/base.html```

```html 
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{% static 'tasks/style.css' %}">
    <title>{% block title %}ToDoApp{% endblock %}</title>
</head>
<body>
    <div class="container">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```

```tasks/templates/post_list.html```

```html
{% extends 'base.html' %}

{% block title %}ToDoApp - Task{% endblock %}

{% block content %}
    <h1>ToDoApp - Last Task</h1>
    {% for post in posts %}
        <div class="post">
            <h2>{{ post.title }}</h2>
            <p>{{ post.content }}</p>
            <p class="date">Published on {{ post.pub_date }}</p>
            <a href="{% url 'post-detail-template' pk=post.id %}">Read more</a>
        </div>
    {% endfor %}
{% endblock %}
```

```tasks/templates/post_detail.html```


```html
{% extends 'base.html' %}

{% block title %}ToDoApp - {{ post.title }}{% endblock %}

{% block content %}
    <h1>{{ post.title }}</h1>
    <p>{{ post.content }}</p>
    <p class="date">Published on {{ post.pub_date }}</p>
    <a href="{% url 'post-list' %}">Back to task</a>
{% endblock %}
```
## Estilos(CSS)

```tasks/static/tasks/style.css```

```css
@import url('https://fonts.googleapis.com/css2?family=Comfortaa:wght@300;400;500&display=swap');

body {
    font-family: 'Comfortaa', cursive;
    margin: 20px;
    padding: 20px;
    background-color: #FFDAB9;
    transition: all 0.5s ease;
}

.container {
    max-width: 800px;
    margin: 0 auto;
    background-color: #FFE4B5;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    transition: all 0.5s ease;
}

.container:hover {
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
}

h1, h2 {
    color: #8B4513;
}

.post {
    margin-bottom: 20px;
    border-bottom: 1px solid #ddd;
    padding-bottom: 10px;
    transition: all 0.5s ease;
}

.post:hover {
    transform: scale(1.01);
}

p.date {
    color: #999;
    font-style: italic;
}
```
Este archivo CSS utiliza una fuente de Google Fonts llamada ‘Comfortaa’ para darle un aspecto más amigable a la aplicación. Los colores se han elegido para transmitir calidez y motivación. Las animaciones se han añadido para hacer la interacción con la aplicación más dinámica y agradable.


Ahora agregamos creamos los endpoints para estos templates. Asi que actualizamos el archivo `tasks/views.py` quedando ahora asi:

```python
from rest_framework import generics
from .models import Task
from .serializers import PostSerializer
from django.shortcuts import render, get_object_or_404

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = PostSerializer


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = PostSerializer

def post_list(request):
    posts = Task.objects.all()
    return render(request, 'post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Task, pk=pk)
    return render(request, 'post_detail.html', {'post': post})
```

Creamos las funciones `post_list` y `post_detail` que quedaran como endpoints que devolveran un archivo html gracias `render`

Ahora pasamos a los `tasks/urls.py`

```python
from django.urls import path
from .views import PostListCreateView, PostDetailView, post_list, post_detail

urlpatterns = [
    path('api/posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('api/posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/', post_list, name='post-list'),
    path('posts/<int:pk>/', post_detail, name='post-detail-template'),
]
```

## Usaremos Token para la atenticación

Proceso de verificar la identidad mediante la comprobación de un token. 
Un `token` es un elemento simbólico que expide una fuente de confianza. Las fichas pueden ser físicas (como una llave USB) o digitales (un mensaje generado por ordenador o una firma digital)

Añadimos a `todoapp/settings.py`
en `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    # codigo anterior...,
    'rest_framework',
    'tasks',
    'rest_framework.authtoken' # Anexamos esta linea
]
```
Y agregamos este fragmento de codigo al final se archivo `todoapp/settings.py`}

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}
```
Actualizamos las vistas de DRF creadas con generics, en `tasks/views.py`

```python
from rest_framework import generics, permissions
from .models import Task
from .serializers import PostSerializer
from django.shortcuts import render, get_object_or_404

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated] # Adjuntamos esta linea


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated] # Ajuntamos esta linea

def post_list(request):
    posts = Task.objects.all()
    return render(request, 'post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Task, pk=pk)
    return render(request, 'post_detail.html', {'post': post})
```

Creamos un endpoint `api-token-auth` para que un usuario pueda obtener su respectivo `token` mediante un metodo POST y realizas las siguientes importaciones.

```python
    #codigo anterior
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
   # resto del codigo ...
]
```

## Creacion de super usuario para Django Admin

Abrimos la terminal y ejecutamos el comando `python manage.py createsuperuser`
Escribimos nuestros nombre en este caso usare el mio, `username: joserosal`
Creamos nuestra passoword, `password: 2487548123Jr`
y hemos creado nuestro super usuarios satisfactoriamente.
Genramos nuestro token, para la antenticación en el apartado de `Token`

## Creamos mas usuarios en la interfaz de Django-Admin
Generamos 2 usuarios mas para la asignacion de tareas.
`username: anaramirez`
`password: 2487548123Ar`
`username: mirandalopez`
`password: 2487548123Ml`

y le generamos los `Token` en el apartado de tokens.

Ya tenemos nuestros usuarios y con nuestros tokens para la autenticación

## Agregamos la documentación para la Aplicación Web

Usaremos Swagger: Swagger es una documentación online que se genera sobre una API. Por lo tanto, en esta herramienta podemos ver todos los endpoint que hemos desarrollado en nuestra API Swagger. Además, nos demuestra cómo son los elementos o datos que debemos pasar para hacer que funcione y nos permite probarlos directamente en su interfaz.

Empezamos Instalandolo: escribimos en la consola ``` pip isntall drf-yasg```

Agregamos a `todoapp/settings.py`
en `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    # codigo anterior...,
    'rest_framework',
    'tasks',
    'drf-yasg', # adjuntamos en linea
]
```
 Añadimos a `todoapp/settings.py`

```

Vamos ahora a las ```todoapp/urls.py```

```python
#...codigo anterior
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
openapi.Info(
        title="ToDoApp",
        default_version='v1',
        description="Aplicación Web para tareas",
        terms_of_service="",
        contact=openapi.Contact(email="rosaljose125@gmail.com"),
        license=openapi.License(name="Copyright all rights reserved")
    ),
    public=True,
    permission_classes = (permissions.AllowAny,),
)

urlpatterns = [
#...codigo anterior
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-ui')
]
```
