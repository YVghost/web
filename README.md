# 🛒 MarketCampus — Plataforma Universitaria de Compra y Venta

MarketCampus es una plataforma web construida con **Django**, donde estudiantes pueden comprar y vender productos de manera segura. Incluye módulos de usuarios, productos, pagos, y un panel administrativo completamente.

-------------------------------

## Tecnologías utilizadas

- Python 3  
- Django 5  
- SQLite / PostgreSQL  
- HTML, CSS, JavaScript  
- ImageKit para manejo/optimización de imágenes  
- PayPal Sandbox para pruebas de pagos  
- Django  

------------------------------------

## Estructura del proyecto

```
marketcampus/
│── marketcampus/        # Configuración del proyecto
│── usuarios/            # Perfiles, autenticación, calificaciones
│── productos/           # Productos, imágenes, categorías
│── checkout/            # Módulo de pagos
│── templates/           # Templates personalizados (incluye admin)
│── static/              # Archivos estáticos globales
│── media/               # Archivos subidos por usuarios
│── db.sqlite3
│── manage.py
```

---------------------------------

# 🧩 🏆 Actualización Importante: **Custom Admin Template**

El proyecto incluye una mejora visual completa del panel de administración de Django:

### Mejoras añadidas:
- Nuevo diseño visual más moderno  
- Header personalizado con nombre del sistema  
- Fuentes y colores mejorados  
- Login administrativo estilizado  
- Dashboard más limpio y profesional  
- Mejor integración con los modelos de usuarios y productos  
------------------------------------------------------------

## Módulo de Usuarios (usuarios)

Incluye:

- Registro, login, logout  
- Perfiles con avatar, biografía, universidad  
- Calificaciones entre estudiantes  
- Prestigio y estadísticas generadas automáticamente  
- Administración avanzada con Django Admin personalizado  

-----------------------------------------------

##  Módulo de Productos (productos)

Incluye:

- Publicación de productos  
- Múltiples imágenes por producto (inlines en admin)  
- Categorías dinámicas  
- Sistema de favoritos  
- Seguimiento de visitas y estado del producto  

------------------------------------------

## Módulo de Pagos (checkout)

- Integración con PayPal Sandbox  
- Variables de entorno para credenciales  
- Sistema preparado para migrar a modo producción  

-----------------------------------------

##  Cómo ejecutar el proyecto

```
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Paneles :

```
http://127.0.0.1:8000/            # para ver pag productos
http://127.0.0.1:8000/admin/      # para ver panel admin
```

------------------------------------------

## Deploy
Compatible con:
- Render
https://marketu.onrender.com/productos/

--------------------------------------------


