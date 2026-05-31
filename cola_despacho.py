"""
Módulo de Cola de Despacho — Unidad III
Cola de prioridad con heapq y pila de historial para operaciones de deshacer.
"""

import heapq
from models import Orden


class ColaDespacho:
    """Gestiona las órdenes de envío con una cola de prioridad.
    
    Las órdenes Express (prioridad 0) se despachan antes que las Normales (prioridad 1).
    Incluye una pila de historial para deshacer despachos.
    """

    def __init__(self):
        self._cola = []           # Cola de prioridad (heap)
        self._contador = 0        # Desempate para heapq (FIFO en misma prioridad)
        self.pila_historial = []  # Pila para deshacer despachos

    def agregar_orden(self, orden: Orden) -> None:
        """Agrega una orden a la cola de prioridad.
        
        Usa una tupla (prioridad, contador, orden) para el heap.
        El contador asegura orden FIFO cuando dos órdenes tienen la misma prioridad.
        
        Args:
            orden: Objeto Orden a agregar.
        """
        heapq.heappush(self._cola, (orden.prioridad, self._contador, orden))
        self._contador += 1

    def despachar_siguiente(self) -> Orden:
        """Despacha (extrae) la orden más urgente de la cola.
        
        Returns:
            La Orden con mayor prioridad (menor valor numérico).
            None si la cola está vacía.
        """
        if not self._cola:
            return None

        prioridad, _, orden = heapq.heappop(self._cola)
        # Guardar en la pila de historial
        self.pila_historial.append(orden)
        return orden

    def deshacer_ultimo_despacho(self) -> Orden:
        """Deshace el último despacho, extrayéndolo de la pila de historial.
        
        Returns:
            La última Orden despachada, o None si no hay historial.
        """
        if not self.pila_historial:
            return None

        orden = self.pila_historial.pop()
        # Reinsertarla en la cola
        self.agregar_orden(orden)
        return orden

    def ver_cola(self) -> list:
        """Retorna las órdenes pendientes ordenadas por prioridad.
        
        Returns:
            Lista de objetos Orden ordenados (no modifica el heap).
        """
        # Crear una copia ordenada sin modificar el heap original
        ordenes_ordenadas = sorted(self._cola, key=lambda x: (x[0], x[1]))
        return [item[2] for item in ordenes_ordenadas]

    def ver_historial(self) -> list:
        """Retorna el historial de despachos (el más reciente al final).
        
        Returns:
            Lista de objetos Orden despachados.
        """
        return list(self.pila_historial)

    @property
    def pendientes(self) -> int:
        """Cantidad de órdenes pendientes en la cola."""
        return len(self._cola)

    @property
    def despachos_realizados(self) -> int:
        """Cantidad de despachos en el historial."""
        return len(self.pila_historial)

    def esta_vacia(self) -> bool:
        """Verifica si la cola está vacía."""
        return len(self._cola) == 0

    def obtener_ordenes_pendientes_como_dicts(self) -> list:
        """Retorna las órdenes pendientes como lista de diccionarios para serialización."""
        ordenes = self.ver_cola()
        return [o.to_dict() for o in ordenes]
