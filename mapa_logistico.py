"""
Módulo Mapa Logístico — Unidad IV
Grafo ponderado con algoritmo de Dijkstra para cálculo de rutas óptimas.
"""

import heapq
import math
from persistencia import cargar_datos


class MapaLogistico:
    """Representa el mapa de la ciudad como un grafo ponderado.
    
    Los pesos representan el costo de combustible (combinación de
    distancia, tráfico promedio y topografía).
    Se implementa como una Lista de Adyacencia (diccionario de diccionarios).
    """

    def __init__(self, archivo_mapa: str = None):
        self.grafo = {}         # Lista de adyacencia: {nodo: {vecino: {'gasolina': costo, 'tiempo': costo}, ...}, ...}
        self.coordenadas = {}   # Coordenadas geográficas: {nodo: {'lat': lat, 'lng': lng}}
        self.descripciones = {} # Descripciones de las aristas

        
        if archivo_mapa:
            self.cargar_mapa(archivo_mapa)

    def cargar_mapa(self, archivo: str) -> None:
        """Carga el mapa desde un archivo JSON y construye la lista de adyacencia.
        
        Args:
            archivo: Ruta al archivo JSON con la definición del grafo.
        """
        datos = cargar_datos(archivo)
        
        if not datos:
            return

        # Si es una lista, tomar el primer elemento (compatibilidad)
        if isinstance(datos, list):
            datos = datos[0] if datos else {}

        # Inicializar todos los nodos y sus coordenadas
        nodos_data = datos.get('nodos', {})
        if isinstance(nodos_data, dict):
            for nodo, coords in nodos_data.items():
                if nodo not in self.grafo:
                    self.grafo[nodo] = {}
                self.coordenadas[nodo] = coords
        else:
            # Fallback en caso de que aún sea una lista vieja
            for nodo in nodos_data:
                if nodo not in self.grafo:
                    self.grafo[nodo] = {}

        # Agregar aristas (bidireccionales)
        for arista in datos.get('aristas', []):
            origen = arista['origen']
            destino = arista['destino']
            costo_gasolina = arista.get('costo_gasolina', arista.get('costo', 1))
            tiempo = arista.get('tiempo', costo_gasolina)
            descripcion = arista.get('descripcion', '')

            # Asegurar que los nodos existen
            if origen not in self.grafo:
                self.grafo[origen] = {}
            if destino not in self.grafo:
                self.grafo[destino] = {}

            # Grafo bidireccional
            self.grafo[origen][destino] = {'gasolina': costo_gasolina, 'tiempo': tiempo}
            self.grafo[destino][origen] = {'gasolina': costo_gasolina, 'tiempo': tiempo}

            # Guardar descripciones
            self.descripciones[(origen, destino)] = descripcion
            self.descripciones[(destino, origen)] = descripcion

    def _distancia_haversine(self, coord_a: dict, coord_b: dict) -> float:
        """Calcula la distancia en kilómetros entre dos coordenadas.

        Args:
            coord_a: Diccionario con 'lat' y 'lng'.
            coord_b: Diccionario con 'lat' y 'lng'.

        Returns:
            Distancia aproximada en kilómetros.
        """
        radio_tierra = 6371.0
        lat1, lon1 = math.radians(coord_a['lat']), math.radians(coord_a['lng'])
        lat2, lon2 = math.radians(coord_b['lat']), math.radians(coord_b['lng'])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return radio_tierra * c

    def _estimacion_tiempo_directo(self, distancia_km: float) -> float:
        """Estima tiempo de viaje directo en minutos para la ruta más rápida."""
        velocidad_promedio_kmh = 40.0
        minutos = (distancia_km / velocidad_promedio_kmh) * 60
        return round(max(minutos, 2), 1)

    def calcular_ruta(self, origen: str, destino: str, estrategia: str = 'gasolina') -> tuple:
        """Calcula la ruta de menor costo usando el algoritmo de Dijkstra.
        
        Args:
            origen: Nodo de origen (ej: 'Almacen_Central').
            destino: Nodo de destino (ej: 'Sector_C').
            estrategia: 'gasolina' o 'tiempo'.
        
        Returns:
            Tupla (costo_total, camino, detalles) donde:
            - costo_total: Costo total (combustible o tiempo) de la ruta.
            - camino: Lista de nodos en orden ['Almacen_Central', 'Sector_A', 'Sector_C'].
            - detalles: Lista de diccionarios con info de cada tramo.
            Retorna (float('inf'), [], []) si no hay ruta posible.
        """
        if estrategia == 'tiempo':
            if origen not in self.coordenadas or destino not in self.coordenadas:
                return (float('inf'), [], [])
            if origen == destino:
                return (0, [origen], [])

            distancia = self._distancia_haversine(self.coordenadas[origen], self.coordenadas[destino])
            tiempo_est = self._estimacion_tiempo_directo(distancia)
            detalles = [{
                'desde': origen,
                'hasta': destino,
                'costo': tiempo_est,
                'pesos_completos': {'gasolina': None, 'tiempo': tiempo_est},
                'descripcion': 'Ruta directa más rápida sin paradas intermedias.'
            }]
            return (tiempo_est, [origen, destino], detalles)

        if origen not in self.grafo or destino not in self.grafo:
            return (float('inf'), [], [])

        # Tabla de distancias mínimas
        distancias = {nodo: float('inf') for nodo in self.grafo}
        distancias[origen] = 0

        # Nodo predecesor para reconstruir el camino
        predecesores = {nodo: None for nodo in self.grafo}

        # Cola de prioridad: (costo_acumulado, nodo)
        cola = [(0, origen)]

        # Conjunto de nodos ya procesados
        visitados = set()

        while cola:
            costo_actual, nodo_actual = heapq.heappop(cola)

            # Si ya procesamos este nodo, saltar
            if nodo_actual in visitados:
                continue

            visitados.add(nodo_actual)

            # Si llegamos al destino, terminar
            if nodo_actual == destino:
                break

            # Explorar vecinos
            for vecino, pesos in self.grafo[nodo_actual].items():
                if vecino in visitados:
                    continue

                costo_arista = pesos.get(estrategia, pesos['gasolina'])
                nuevo_costo = costo_actual + costo_arista

                if nuevo_costo < distancias[vecino]:
                    distancias[vecino] = nuevo_costo
                    predecesores[vecino] = nodo_actual
                    heapq.heappush(cola, (nuevo_costo, vecino))

        # Reconstruir el camino
        if distancias[destino] == float('inf'):
            return (float('inf'), [], [])

        camino = []
        nodo = destino
        while nodo is not None:
            camino.append(nodo)
            nodo = predecesores[nodo]
        camino.reverse()

        # Construir detalles del camino
        detalles = []
        for i in range(len(camino) - 1):
            tramo_origen = camino[i]
            tramo_destino = camino[i + 1]
            pesos = self.grafo[tramo_origen][tramo_destino]
            costo = pesos.get(estrategia, pesos['gasolina'])
            desc = self.descripciones.get((tramo_origen, tramo_destino), '')
            detalles.append({
                'desde': tramo_origen,
                'hasta': tramo_destino,
                'costo': costo,
                'pesos_completos': pesos,
                'descripcion': desc
            })

        return (distancias[destino], camino, detalles)

    def obtener_nodos(self) -> list:
        """Retorna la lista de todos los nodos (sectores) del grafo.
        
        Returns:
            Lista de strings con los nombres de los nodos.
        """
        return list(self.grafo.keys())

    def obtener_aristas(self) -> list:
        """Retorna la lista de todas las aristas del grafo.
        
        Returns:
            Lista de diccionarios con origen, destino y costo.
        """
        aristas = []
        visitadas = set()
        for origen in self.grafo:
            for destino, pesos in self.grafo[origen].items():
                par = tuple(sorted([origen, destino]))
                if par not in visitadas:
                    visitadas.add(par)
                    desc = self.descripciones.get((origen, destino), '')
                    aristas.append({
                        'origen': origen,
                        'destino': destino,
                        'costo_gasolina': pesos.get('gasolina', 0),
                        'tiempo': pesos.get('tiempo', 0),
                        'descripcion': desc
                    })
        return aristas

    def obtener_destinos(self) -> list:
        """Retorna todos los nodos excepto el Almacén Central (destinos posibles).
        
        Returns:
            Lista de strings con los nombres de los destinos.
        """
        return [n for n in self.grafo.keys() if n != 'Almacen_Central']
