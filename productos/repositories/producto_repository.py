from django.db.models import Q
from productos.models import Producto, Categoria

class ProductoRepository:

    def obtener_productos_base(self):
        return Producto.objects.filter(
            estado='disponible'
        ).select_related(
            'categoria', 'vendedor'
        ).prefetch_related('imagenes')

    def filtrar(self, query=None, categoria_id=None):
        productos = self.obtener_productos_base()

        if query:
            productos = productos.filter(
                Q(nombre__icontains=query) |
                Q(descripcion__icontains=query) |
                Q(tags__icontains=query)
            )

        if categoria_id:
            productos = productos.filter(categoria_id=categoria_id)

        return productos

    def obtener_categorias(self):
        return Categoria.objects.filter(activa=True)
