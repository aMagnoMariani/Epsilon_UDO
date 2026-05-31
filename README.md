# Epsilon_UDO

SistemaEnvios — Epsilon_UDO

Descripción
-----------
Epsilon_UDO es una aplicación educativa y funcional para gestionar inventario y despachos en una operación de última milla. Implementa estructuras de datos y algoritmos comunes (árboles binarios de búsqueda, colas de prioridad, pilas, grafos y Dijkstra) para ofrecer:

- Búsqueda eficiente de productos por ID.
- Cola de despacho con prioridad (Express vs Normal) y posibilidad de deshacer el último despacho.
- Cálculo de rutas óptimas según costo de combustible o tiempo usando un grafo ponderado.
- Persistencia simple en JSON para productos, órdenes y mapa.

Lenguaje y herramientas
-----------------------
- Lenguaje: Python 3.8+
- Framework web: Flask
- Persistencia: JSON (módulo `json`)
- Recomendadas: `python-dotenv`, `gunicorn` (despliegue)

Integrantes
-----------
- Alejandro Mariani
- Jose Felix Cedeño
- Diana Yegüez

Instalación rápida
------------------
1. Crear y activar un entorno virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Iniciar la aplicación en desarrollo:

```bash
python app.py
```

Archivos relevantes
------------------
- `app.py`: Rutas y orquestación del sistema (Flask).
- `models.py`: Clases `Producto` y `Orden`.
- `persistencia.py`: Lectura/escritura JSON.
- `arbol_inventario.py`: Árbol Binario de Búsqueda para productos.
- `cola_despacho.py`: Cola de prioridad para órdenes y pila de historial.
- `mapa_logistico.py`: Grafo y algoritmo de Dijkstra para rutas.
- `datos/`: JSON de ejemplo (`productos.json`, `ordenes.json`, `mapa.json`).
- `templates/` y `static/`: Frontend simple usando Jinja2 y CSS.

Uso y pruebas
------------
- La aplicación expone rutas web (por defecto `http://127.0.0.1:5000/`).
- Para pruebas unitarias, usar `pytest` (ya incluido en `requirements.txt`).

Contribuciones
--------------
- Seguir el estilo de código con `black` y habilitar `pre-commit` si se desea.
- Abrir issues y pull requests indicando el propósito y pruebas realizadas.

