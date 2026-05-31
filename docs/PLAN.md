| Estructura | En dónde se usa | Operaciones requeridas | Biblioteca | Integrante encargado |
| :--- | :---: | :---: | :---: | :---: |
| Pila | En el historial de acciones del operador para revertir el último despacho | Registrar movimiento (append), deshacer último movimiento (pop) | Ninguna | Jose Felix
| Cola | En el modulo de despacho para procesar los paquetes VIP | Insertar con prioridad, Extraer el de mayor prioridad | headpq | Diana
| Arbol B | En el sistema de almacenamiento fisico para organizar los índices en el disco duro | Crear índice, Buscar clave en disco, Insertar clave, Balancear páginas | sqlite3 (Utiliza Arboles B internamente para manejar archivos eficientes | Ariadna
| Grafo | En el modulo de mapas y rutas | Agregar ciudad/punto, Agregar ruta con peso, Calcular camino minimo (Algoritmo de Dijkstra) | networkx (para gestionar el grafo), scipy.spatial (para calculos geometricos) | Alejandro
| Hashing | En el modulo de inventario para encontrar un producto de forma inmediata | Insertar producto(), Buscar producto(), Eliminar producto() | Ninguna | Victoria
