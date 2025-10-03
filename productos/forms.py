from django import forms
from .models import Producto, ImagenProducto

class MultipleFileInput(forms.ClearableFileInput):
    """Widget personalizado para múltiples archivos"""
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    """Field personalizado para múltiples archivos"""
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class ProductoForm(forms.ModelForm):
    imagenes = MultipleFileField(
        required=False,
        help_text="Puedes seleccionar múltiples imágenes (máximo 5)"
    )
    
    class Meta:
        model = Producto
        fields = [
            'nombre', 'descripcion', 'categoria', 'precio', 
            'condicion', 'stock', 'es_multiple', 'tipo_envio', 
            'tags'  # ❌ ELIMINADO: 'ubicacion'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Calculadora científica TI-84'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe tu producto detalladamente...'
            }),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01'
            }),
            'condicion': forms.Select(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
            'tipo_envio': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: libro, ingenieria, calculadora, usada'
            }),
        }
        help_texts = {
            'tags': 'Separa las palabras clave con comas',
            'es_multiple': 'Marca esta opción si tienes más de una unidad del mismo producto',
            'tipo_envio': 'La ubicación será automáticamente tu universidad',  # ✅ NUEVO
        }
    
    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio and precio <= 0:
            raise forms.ValidationError("El precio debe ser mayor a 0")
        return precio
    
    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock and stock < 1:
            raise forms.ValidationError("El stock debe ser al menos 1")
        return stock
    
    def clean_imagenes(self):
        """Validar que no se suban más de 5 imágenes"""
        imagenes = self.cleaned_data.get('imagenes', [])
        if len(imagenes) > 5:
            raise forms.ValidationError("No puedes subir más de 5 imágenes")
        return imagenes