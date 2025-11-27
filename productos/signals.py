# productos/signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def crear_categorias(sender, **kwargs):
    if sender.name != 'productos':
        return

    from productos.models import Categoria

    categorias = [
        ('libros_texto', '📚 Libros de Texto', 'Libros de texto universitarios y material didáctico.'),
        ('apuntes_guias', '📝 Apuntes y Guías', 'Apuntes, resúmenes y guías de estudio.'),
        ('electronica', '💻 Electrónica', 'Dispositivos y accesorios electrónicos.'),
        ('instrumentos_laboratorio', '🔬 Instrumentos Lab', 'Material de laboratorio académico.'),
        ('ropa', '👕 Ropa', 'Ropa universitaria o casual.'),
        ('deportes', '⚽ Deportes', 'Accesorios y equipo deportivo.'),
        ('comida', '🍕 Comida', 'Snacks o alimentos preparados.'),
        ('accesorios', '🎒 Accesorios', 'Mochilas, estuches y más.'),
        ('muebles_hogar', '🛋️ Muebles Hogar', 'Artículos para la habitación o departamento.'),
        ('arte_musica', '🎨 Arte y Música', 'Arte, instrumentos y materiales creativos.'),
        ('servicios', '🛠️ Servicios', 'Clases, tutorías o trabajos ofrecidos.'),
        ('otros', '📦 Otros', 'Productos que no encajan en las demás categorías.'),
    ]

    for clave, icono, descripcion in categorias:
        Categoria.objects.get_or_create(
            nombre=clave,
            defaults={
                'descripcion': descripcion,
                'icono': icono,
                'activa': True
            }
        )
