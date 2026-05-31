"""
Módulo de Modelos — Unidad I
Clases base con __slots__ para optimización de memoria.
"""


class Producto:
    """Representa un producto en el inventario.
    
    Usa __slots__ para optimizar el uso de memoria al evitar
    la creación de un __dict__ por instancia.
    """
    __slots__ = ['id', 'nombre', 'precio', 'stock']

    def __init__(self, id: int, nombre: str, precio: float, stock: int):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    def to_dict(self) -> dict:
        """Convierte el producto a diccionario para serialización JSON."""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'precio': self.precio,
            'stock': self.stock
        }

    @classmethod
    def from_dict(cls, datos: dict) -> 'Producto':
        """Crea un Producto desde un diccionario."""
        return cls(
            id=datos['id'],
            nombre=datos['nombre'],
            precio=datos['precio'],
            stock=datos['stock']
        )

    def __repr__(self):
        return f"Producto(id={self.id}, nombre='{self.nombre}', precio=${self.precio}, stock={self.stock})"


class Orden:
    """Representa una orden de compra de un cliente.
    
    Usa __slots__ para optimización de memoria.
    Prioridad: 0 = Express, 1 = Normal
    """
    __slots__ = ['id', 'producto_id', 'cantidad', 'destino', 'prioridad']

    def __init__(self, id: int, producto_id: int, cantidad: int, destino: str, prioridad: int = 1):
        self.id = id
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.destino = destino
        self.prioridad = prioridad  # 0 = Express, 1 = Normal

    def to_dict(self) -> dict:
        """Convierte la orden a diccionario para serialización JSON."""
        return {
            'id': self.id,
            'producto_id': self.producto_id,
            'cantidad': self.cantidad,
            'destino': self.destino,
            'prioridad': self.prioridad
        }

    @classmethod
    def from_dict(cls, datos: dict) -> 'Orden':
        """Crea una Orden desde un diccionario."""
        return cls(
            id=datos['id'],
            producto_id=datos['producto_id'],
            cantidad=datos['cantidad'],
            destino=datos['destino'],
            prioridad=datos.get('prioridad', 1)
        )

    def __lt__(self, otro):
        """Comparación para heapq: menor prioridad = más urgente."""
        return self.prioridad < otro.prioridad

    def __repr__(self):
        tipo = "Express" if self.prioridad == 0 else "Normal"
        return f"Orden(id={self.id}, producto_id={self.producto_id}, destino='{self.destino}', tipo={tipo})"

    @property
    def tipo_prioridad(self):
        """Retorna el tipo de prioridad como texto legible."""
        return "Express" if self.prioridad == 0 else "Normal"
