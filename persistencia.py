"""
Módulo de Persistencia — Unidad II
Funciones genéricas para cargar y guardar datos en archivos JSON.
"""

import json
import os


def cargar_datos(archivo: str) -> list:
    """Carga datos desde un archivo JSON.
    
    Args:
        archivo: Ruta al archivo JSON a leer.
    
    Returns:
        Lista de diccionarios con los datos leídos.
        Retorna una lista vacía si el archivo no existe.
    """
    if not os.path.exists(archivo):
        print(f"⚠️  Archivo '{archivo}' no encontrado. Se retorna lista vacía.")
        return []

    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            datos = json.load(f)
        print(f"✅ Datos cargados desde '{archivo}' ({len(datos)} registros)")
        return datos
    except json.JSONDecodeError as e:
        print(f"❌ Error al decodificar JSON en '{archivo}': {e}")
        return []
    except Exception as e:
        print(f"❌ Error inesperado al leer '{archivo}': {e}")
        return []


def guardar_datos(datos: list, archivo: str) -> bool:
    """Guarda datos en un archivo JSON.
    
    Args:
        datos: Lista de diccionarios a guardar.
        archivo: Ruta al archivo JSON destino.
    
    Returns:
        True si se guardó exitosamente, False en caso de error.
    """
    try:
        # Crear directorio si no existe
        directorio = os.path.dirname(archivo)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio, exist_ok=True)

        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
        print(f"💾 Datos guardados en '{archivo}' ({len(datos)} registros)")
        return True
    except Exception as e:
        print(f"❌ Error al guardar en '{archivo}': {e}")
        return False
