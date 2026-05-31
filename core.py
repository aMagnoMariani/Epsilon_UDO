"""
Core del sistema: inicialización de estructuras y carga/guardado de datos.
Centraliza el estado (modelo) que luego usan los controladores (controllers).
"""
import os
import time
from persistencia import cargar_datos, guardar_datos
from arbol_inventario import ArbolInventario
from cola_despacho import ColaDespacho
from mapa_logistico import MapaLogistico
from models.product import Producto
from models.order import Orden

# Directorio de datos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATOS_DIR = os.path.join(BASE_DIR, 'datos')
PRODUCTOS_FILE = os.path.join(DATOS_DIR, 'productos.json')
ORDENES_FILE = os.path.join(DATOS_DIR, 'ordenes.json')
MAPA_FILE = os.path.join(DATOS_DIR, 'mapa.json')

# Estado global (modelo)
arbol = ArbolInventario()
cola = ColaDespacho()
mapa = MapaLogistico()


def inicializar_sistema():
    """Carga datos desde JSON e inicializa las estructuras globales.
    Diseñado para ser llamado una vez al arranque.
    """
    global arbol, cola, mapa

    # Cargar productos en el Árbol BST
    datos_productos = cargar_datos(PRODUCTOS_FILE)
    for datos in datos_productos:
        producto = Producto.from_dict(datos)
        arbol.insertar(producto)

    # Cargar órdenes en la Cola de Prioridad
    datos_ordenes = cargar_datos(ORDENES_FILE)
    for datos in datos_ordenes:
        orden = Orden.from_dict(datos)
        cola.agregar_orden(orden)

    # Cargar mapa logístico
    mapa.cargar_mapa(MAPA_FILE)

    print('=' * 50)
    print('Sistema de Logística de Última Milla (core)')
    print(f'   Productos cargados: {arbol.tamano}')
    print(f'   Órdenes pendientes: {cola.pendientes}')
    print(f'   Nodos del mapa:     {len(mapa.obtener_nodos())}')
    print('=' * 50)


def guardar_estado():
    """Guarda el estado actual (productos y órdenes pendientes) a JSON."""
    productos = arbol.obtener_todos()
    datos_productos = [p.to_dict() for p in productos]
    guardar_datos(datos_productos, PRODUCTOS_FILE)

    datos_ordenes = cola.obtener_ordenes_pendientes_como_dicts()
    guardar_datos(datos_ordenes, ORDENES_FILE)
