from productos.repositories.producto_repository import ProductoRepository

class ProductoService:

    def __init__(self):
        self.repository = ProductoRepository()

    def explorar_productos(self, query=None, categoria_id=None):
        productos = self.repository.filtrar(query, categoria_id)
        categorias = self.repository.obtener_categorias()

        return {
            'productos': productos,
            'categorias': categorias,
            'query': query,
            'categoria_seleccionada': categoria_id,
        }
