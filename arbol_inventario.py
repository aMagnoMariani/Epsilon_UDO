"""
Módulo Árbol de Inventario — Unidad V
Árbol Binario de Búsqueda (BST) para búsqueda eficiente de productos.
"""

from models import Producto


class NodoBST:
    """Nodo del Árbol Binario de Búsqueda.
    
    Contiene un objeto Producto y punteros al hijo izquierdo y derecho.
    """
    __slots__ = ['producto', 'izquierdo', 'derecho']

    def __init__(self, producto: Producto):
        self.producto = producto
        self.izquierdo = None
        self.derecho = None


class ArbolInventario:
    """Árbol Binario de Búsqueda para gestionar el inventario de productos.
    
    Las operaciones de búsqueda e inserción se basan en el ID del producto.
    """

    def __init__(self):
        self.raiz = None
        self._tamano = 0

    def insertar(self, producto: Producto) -> None:
        """Inserta un producto en el árbol basándose en su ID.
        
        Args:
            producto: Objeto Producto a insertar.
        """
        if self.raiz is None:
            self.raiz = NodoBST(producto)
            self._tamano += 1
        else:
            self._insertar_recursivo(self.raiz, producto)

    def _insertar_recursivo(self, nodo: NodoBST, producto: Producto) -> None:
        """Inserción recursiva en el subárbol."""
        if producto.id < nodo.producto.id:
            if nodo.izquierdo is None:
                nodo.izquierdo = NodoBST(producto)
                self._tamano += 1
            else:
                self._insertar_recursivo(nodo.izquierdo, producto)
        elif producto.id > nodo.producto.id:
            if nodo.derecho is None:
                nodo.derecho = NodoBST(producto)
                self._tamano += 1
            else:
                self._insertar_recursivo(nodo.derecho, producto)
        else:
            # Si el ID ya existe, actualizar el producto
            nodo.producto = producto

    def buscar(self, id: int) -> Producto:
        """Busca un producto por su ID en el árbol.
        
        Args:
            id: ID del producto a buscar.
        
        Returns:
            El objeto Producto si se encuentra, None en caso contrario.
        """
        return self._buscar_recursivo(self.raiz, id)

    def _buscar_recursivo(self, nodo: NodoBST, id: int) -> Producto:
        """Búsqueda recursiva en el subárbol."""
        if nodo is None:
            return None

        if id == nodo.producto.id:
            return nodo.producto
        elif id < nodo.producto.id:
            return self._buscar_recursivo(nodo.izquierdo, id)
        else:
            return self._buscar_recursivo(nodo.derecho, id)

    def actualizar_stock(self, id: int, cantidad: int) -> bool:
        """Modifica el stock de un producto en el árbol.
        
        Args:
            id: ID del producto.
            cantidad: Cantidad a restar (positiva) o sumar (negativa) al stock.
        
        Returns:
            True si la operación fue exitosa, False si no hay stock suficiente
            o el producto no existe.
        """
        producto = self.buscar(id)
        if producto is None:
            return False
        
        nuevo_stock = producto.stock - cantidad
        if nuevo_stock < 0:
            return False
        
        producto.stock = nuevo_stock
        return True

    def restaurar_stock(self, id: int, cantidad: int) -> bool:
        """Restaura stock de un producto (para operación de deshacer).
        
        Args:
            id: ID del producto.
            cantidad: Cantidad a sumar al stock.
        
        Returns:
            True si la operación fue exitosa.
        """
        producto = self.buscar(id)
        if producto is None:
            return False
        
        producto.stock += cantidad
        return True

    def obtener_todos(self) -> list:
        """Recorrido inorden del árbol. Retorna todos los productos ordenados por ID.
        
        Returns:
            Lista de objetos Producto en orden ascendente de ID.
        """
        resultado = []
        self._inorden(self.raiz, resultado)
        return resultado

    def _inorden(self, nodo: NodoBST, resultado: list) -> None:
        """Recorrido inorden recursivo."""
        if nodo is not None:
            self._inorden(nodo.izquierdo, resultado)
            resultado.append(nodo.producto)
            self._inorden(nodo.derecho, resultado)

    @property
    def tamano(self) -> int:
        """Retorna la cantidad de productos en el árbol."""
        return self._tamano

    def __len__(self):
        return self._tamano
