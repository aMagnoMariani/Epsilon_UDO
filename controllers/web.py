"""
Controlador web (rutas) — implementa la capa Controller en MVC.
"""
import os
import time
from flask import Flask, render_template, request, redirect, url_for, flash

from core import arbol, cola, mapa, inicializar_sistema, guardar_estado
from persistencia import guardar_datos
from models.product import Producto
from models.order import Orden


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# Create Flask app pointing to root templates/static so render_template finds files in project root
app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)
app.secret_key = 'logistica-ultima-milla-2026'


# Inicializar estado (carga desde JSON)
inicializar_sistema()


@app.route('/')
def index():
    productos = arbol.obtener_todos()
    stock_total = sum(p.stock for p in productos)
    valor_inventario = sum(p.precio * p.stock for p in productos)

    metricas = {
        'total_productos': arbol.tamano,
        'ordenes_pendientes': cola.pendientes,
        'despachos_realizados': cola.despachos_realizados,
        'nodos_mapa': len(mapa.obtener_nodos()),
        'stock_total': stock_total,
        'valor_inventario': valor_inventario,
    }
    return render_template('index.html', metricas=metricas)


@app.route('/productos')
def productos():
    todos_productos = arbol.obtener_todos()
    return render_template('productos.html', productos=todos_productos)


@app.route('/productos/buscar', methods=['POST'])
def buscar_producto():
    try:
        id_buscar = int(request.form.get('id', 0))
    except ValueError:
        flash('El ID debe ser un número entero.', 'warning')
        return redirect(url_for('productos'))

    inicio = time.perf_counter()
    producto = arbol.buscar(id_buscar)
    fin = time.perf_counter()
    tiempo_ms = (fin - inicio) * 1000

    todos_productos = arbol.obtener_todos()

    if producto:
        flash(f"Encontrado: {producto.nombre} — ${producto.precio} — Stock: {producto.stock} (Búsqueda: {tiempo_ms:.4f} ms)", 'success')
    else:
        flash(f"Producto con ID {id_buscar} no encontrado. (Búsqueda: {tiempo_ms:.4f} ms)", 'danger')

    return render_template('productos.html', productos=todos_productos, resultado=producto, tiempo_busqueda=tiempo_ms, id_buscado=id_buscar)


@app.route('/ordenes')
def ordenes():
    ordenes_pendientes = cola.ver_cola()
    destinos = mapa.obtener_destinos()
    todos_productos = arbol.obtener_todos()
    return render_template('ordenes.html', ordenes=ordenes_pendientes, destinos=destinos, productos=todos_productos)


@app.route('/ordenes/nueva', methods=['POST'])
def nueva_orden():
    try:
        producto_id = int(request.form.get('producto_id', 0))
        cantidad = int(request.form.get('cantidad', 1))
        destino = request.form.get('destino', '')
        prioridad = int(request.form.get('prioridad', 1))
    except ValueError:
        flash('Datos inválidos. Verifica los campos.', 'warning')
        return redirect(url_for('ordenes'))

    producto = arbol.buscar(producto_id)
    if not producto:
        flash(f'Producto con ID {producto_id} no existe.', 'danger')
        return redirect(url_for('ordenes'))

    if producto.stock < cantidad:
        flash(f'Stock insuficiente. Disponible: {producto.stock}, Solicitado: {cantidad}.', 'warning')
        return redirect(url_for('ordenes'))

    historial = cola.ver_historial()
    pendientes = cola.ver_cola()
    todos_ids = [o.id for o in historial + pendientes]
    nuevo_id = max(todos_ids) + 1 if todos_ids else 1001

    orden = Orden(id=nuevo_id, producto_id=producto_id, cantidad=cantidad, destino=destino, prioridad=prioridad)

    cola.agregar_orden(orden)
    tipo = "Express" if prioridad == 0 else "Normal"
    flash(f'Orden #{nuevo_id} agregada ({tipo}) — {producto.nombre} x{cantidad} -> {destino}', 'success')
    return redirect(url_for('ordenes'))


@app.route('/despacho')
def despacho():
    ordenes_pendientes = cola.ver_cola()
    return render_template('despacho.html', ordenes=ordenes_pendientes)


@app.route('/despacho/siguiente', methods=['POST'])
def despachar_siguiente():
    if cola.esta_vacia():
        flash('No hay órdenes pendientes para despachar.', 'warning')
        return redirect(url_for('despacho'))

    orden = cola.despachar_siguiente()

    producto = arbol.buscar(orden.producto_id)
    if producto:
        exito = arbol.actualizar_stock(orden.producto_id, orden.cantidad)
        if not exito:
            flash(f'Stock insuficiente para {producto.nombre}. Despacho registrado pero stock no actualizado.', 'warning')

    costo, camino, detalles = mapa.calcular_ruta('Almacen_Central', orden.destino, 'gasolina')

    nombre_producto = producto.nombre if producto else f'ID:{orden.producto_id}'
    ruta_str = ' → '.join(camino) if camino else 'Sin ruta disponible'

    ordenes_pendientes = cola.ver_cola()

    return render_template('despacho.html', ordenes=ordenes_pendientes, orden_despachada=orden, producto_despachado=producto, ruta_camino=camino, ruta_costo=costo, ruta_detalles=detalles, estrategia_seleccionada='gasolina', ruta_str=ruta_str)


@app.route('/historial')
def historial():
    historial_despachos = cola.ver_historial()
    historial_enriquecido = []
    for orden in reversed(historial_despachos):
        producto = arbol.buscar(orden.producto_id)
        historial_enriquecido.append({'orden': orden, 'producto': producto})
    return render_template('historial.html', historial=historial_enriquecido)


@app.route('/historial/deshacer', methods=['POST'])
def deshacer_despacho():
    orden = cola.deshacer_ultimo_despacho()

    if orden is None:
        flash('No hay despachos para deshacer.', 'warning')
        return redirect(url_for('historial'))

    exito = arbol.restaurar_stock(orden.producto_id, orden.cantidad)
    producto = arbol.buscar(orden.producto_id)
    nombre = producto.nombre if producto else f'ID:{orden.producto_id}'

    if exito:
        flash(f'Despacho deshecho: Orden #{orden.id} — {nombre} x{orden.cantidad}. Stock restaurado.', 'success')
    else:
        flash(f'Despacho deshecho: Orden #{orden.id}, pero no se pudo restaurar el stock.', 'warning')

    return redirect(url_for('historial'))


@app.route('/guardar', methods=['POST'])
def guardar():
    guardar_estado()
    flash('Datos guardados exitosamente en archivos JSON.', 'success')
    return redirect(url_for('index'))


@app.route('/mapa')
def ver_mapa():
    nodos = mapa.obtener_nodos()
    aristas = mapa.obtener_aristas()
    coordenadas = mapa.coordenadas
    productos_dicts = [p.to_dict() for p in arbol.obtener_todos()]
    return render_template('mapa.html', nodos=nodos, aristas=aristas, coordenadas=coordenadas, productos=productos_dicts, origen_seleccionado='Almacen_Central', destino_seleccionado='', estrategia_seleccionada='gasolina')


@app.route('/mapa/calcular', methods=['POST'])
def calcular_ruta_mapa():
    origen = request.form.get('origen', 'Almacen_Central')
    destino = request.form.get('destino', '')
    estrategia = request.form.get('estrategia', 'gasolina')

    if not destino:
        flash('Selecciona un destino.', 'warning')
        return redirect(url_for('ver_mapa'))

    costo, camino, detalles = mapa.calcular_ruta(origen, destino, estrategia)
    nodos = mapa.obtener_nodos()
    aristas = mapa.obtener_aristas()
    coordenadas = mapa.coordenadas
    productos_dicts = [p.to_dict() for p in arbol.obtener_todos()]

    if camino:
        tipo_str = 'unidades de combustible' if estrategia == 'gasolina' else 'minutos'
        if estrategia == 'tiempo':
            origen_texto = origen.replace('_', ' ')
            destino_texto = destino.replace('_', ' ')
            flash(f'Ruta directa más rápida: {origen_texto} -> {destino_texto} (Tiempo estimado: {costo} {tipo_str})', 'success')
        else:
            ruta_str = ' -> '.join([n.replace('_', ' ') for n in camino])
            flash(f'Ruta óptima ({estrategia}): {ruta_str} (Costo total: {costo} {tipo_str})', 'success')
    else:
        flash(f'No se encontró ruta de {origen} a {destino}.', 'danger')

    return render_template('mapa.html', nodos=nodos, aristas=aristas, coordenadas=coordenadas, productos=productos_dicts, ruta_camino=camino, ruta_costo=costo, ruta_detalles=detalles, origen_seleccionado=origen, destino_seleccionado=destino, estrategia_seleccionada=estrategia)
