from flask import request, jsonify
from database.connection import dbConnection

# ======================= OBTENER TODOS LOS PRODUCTOS ======================= #
def get_all_productos():
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        cursor = mydb.cursor(dictionary=True)
        query = """
        SELECT p.*, c.nombre_categoria 
        FROM productos p 
        LEFT JOIN categorias c ON p.id_categoria = c.id_categoria 
        ORDER BY p.nombre_producto
        """
        cursor.execute(query)
        productos = cursor.fetchall()
        cursor.close()
        mydb.close()
        return jsonify(productos), 200

    except Exception as ex:
        return jsonify({'message': f'Error al obtener los productos: {ex}'}), 500


# ======================= OBTENER PRODUCTO POR ID ======================= #
def get_producto_by_id(id_producto):
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        cursor = mydb.cursor(dictionary=True)
        query = """
        SELECT p.*, c.nombre_categoria 
        FROM productos p 
        LEFT JOIN categorias c ON p.id_categoria = c.id_categoria 
        WHERE p.id_producto = %s
        """
        cursor.execute(query, (id_producto,))
        producto = cursor.fetchone()
        cursor.close()
        mydb.close()

        if producto:
            return jsonify(producto), 200
        else:
            return jsonify({'message': 'Producto no encontrado'}), 404

    except Exception as ex:
        return jsonify({'message': f'Error al obtener producto: {ex}'}), 500


# ======================= CREAR PRODUCTO ======================= #
def create_producto():
    data = request.json
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        query = """
        INSERT INTO productos (codigo, nombre_producto, id_categoria, stock, 
                             precio_q, estado, imagen)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            data['codigo'],
            data['nombre_producto'],
            data['id_categoria'],
            data.get('stock', 0),
            data['precio_q'],
            data.get('estado', 'Activo'),
            data.get('imagen')
        )

        cursor = mydb.cursor()
        cursor.execute(query, values)
        mydb.commit()
        cursor.close()
        mydb.close()

        return jsonify({'message': 'Producto creado exitosamente'}), 201

    except Exception as ex:
        return jsonify({'message': f'Error al crear producto: {ex}'}), 400


# ======================= ACTUALIZAR PRODUCTO ======================= #
def update_producto(id_producto):
    data = request.json
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        query = """
        UPDATE productos SET
            codigo = %s,
            nombre_producto = %s,
            id_categoria = %s,
            stock = %s,
            precio_q = %s,
            estado = %s,
            imagen = %s
        WHERE id_producto = %s
        """
        values = (
            data['codigo'],
            data['nombre_producto'],
            data['id_categoria'],
            data.get('stock', 0),
            data['precio_q'],
            data.get('estado', 'Activo'),
            data.get('imagen'),
            id_producto
        )

        cursor = mydb.cursor()
        cursor.execute(query, values)
        mydb.commit()
        cursor.close()
        mydb.close()

        return jsonify({'message': 'Producto actualizado exitosamente'}), 200

    except Exception as ex:
        return jsonify({'message': f'Error al actualizar producto: {ex}'}), 400


# ======================= ELIMINAR PRODUCTO ======================= #
def delete_producto(id_producto):
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        cursor = mydb.cursor()
        cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id_producto,))
        mydb.commit()
        cursor.close()
        mydb.close()

        return jsonify({'message': 'Producto eliminado correctamente'}), 200

    except Exception as ex:
        return jsonify({'message': f'Error al eliminar producto: {ex}'}), 400

# ======================= BUSCAR PRODUCTO POR CÓDIGO ======================= #
def get_producto_by_codigo(codigo):
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        cursor = mydb.cursor(dictionary=True)
        query = """
        SELECT p.*, c.nombre_categoria 
        FROM productos p 
        LEFT JOIN categorias c ON p.id_categoria = c.id_categoria 
        WHERE p.codigo = %s
        """
        cursor.execute(query, (codigo,))
        producto = cursor.fetchone()
        cursor.close()
        mydb.close()

        if producto:
            return jsonify(producto), 200
        else:
            return jsonify({'message': 'Producto no encontrado'}), 404

    except Exception as ex:
        return jsonify({'message': f'Error al buscar por código: {ex}'}), 500

# ======================= BUSCAR PRODUCTOS POR CATEGORÍA ======================= #
def get_productos_by_categoria(id_categoria):
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        cursor = mydb.cursor(dictionary=True)
        query = """
        SELECT p.*, c.nombre_categoria 
        FROM productos p 
        LEFT JOIN categorias c ON p.id_categoria = c.id_categoria 
        WHERE p.id_categoria = %s 
        ORDER BY p.nombre_producto
        """
        cursor.execute(query, (id_categoria,))
        productos = cursor.fetchall()
        cursor.close()
        mydb.close()

        if productos:
            return jsonify(productos), 200
        else:
            return jsonify({'message': 'No se encontraron productos en esta categoría'}), 404

    except Exception as ex:
        return jsonify({'message': f'Error al buscar por categoría: {ex}'}), 500

# ======================= BUSCAR POR NOMBRE ======================= #
def search_productos_by_nombre():
    palabra_clave = request.args.get('q', '')  # ?q=valor
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        query = """
        SELECT p.*, c.nombre_categoria 
        FROM productos p 
        LEFT JOIN categorias c ON p.id_categoria = c.id_categoria 
        WHERE p.nombre_producto LIKE %s OR p.codigo LIKE %s
        ORDER BY p.nombre_producto
        """
        like_value = f"%{palabra_clave}%"
        cursor = mydb.cursor(dictionary=True)
        cursor.execute(query, (like_value, like_value))
        resultados = cursor.fetchall()
        cursor.close()
        mydb.close()

        if resultados:
            return jsonify(resultados), 200
        else:
            return jsonify({'message': 'No se encontraron coincidencias'}), 404

    except Exception as ex:
        return jsonify({'message': f'Error en búsqueda: {ex}'}), 500

# ======================= VERIFICAR EXISTENCIA DE PRODUCTO ======================= #
def check_producto_exists(id_producto):
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        cursor = mydb.cursor()
        cursor.execute("SELECT COUNT(*) FROM productos WHERE id_producto = %s", (id_producto,))
        exists = cursor.fetchone()[0] > 0
        cursor.close()
        mydb.close()

        return jsonify({'exists': exists}), 200

    except Exception as ex:
        return jsonify({'message': f'Error al verificar producto: {ex}'}), 500

# ======================= BUSCAR PRODUCTOS POR ESTADO ======================= #
def get_productos_by_estado(estado):
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        cursor = mydb.cursor(dictionary=True)
        query = """
        SELECT p.*, c.nombre_categoria 
        FROM productos p 
        LEFT JOIN categorias c ON p.id_categoria = c.id_categoria 
        WHERE p.estado = %s 
        ORDER BY p.nombre_producto
        """
        cursor.execute(query, (estado,))
        productos = cursor.fetchall()
        cursor.close()
        mydb.close()

        if productos:
            return jsonify(productos), 200
        else:
            return jsonify({'message': f'No se encontraron productos con estado {estado}'}), 404

    except Exception as ex:
        return jsonify({'message': f'Error al buscar por estado: {ex}'}), 500

# ======================= BUSCAR PRODUCTOS POR RANGO DE PRECIO ======================= #
def get_productos_by_precio_range():
    precio_min = request.args.get('min', 0)  # ?min=10
    precio_max = request.args.get('max', 999999)  # ?max=100
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        query = """
        SELECT p.*, c.nombre_categoria 
        FROM productos p 
        LEFT JOIN categorias c ON p.id_categoria = c.id_categoria 
        WHERE p.precio_q BETWEEN %s AND %s 
        ORDER BY p.precio_q ASC, p.nombre_producto
        """
        cursor = mydb.cursor(dictionary=True)
        cursor.execute(query, (precio_min, precio_max))
        productos = cursor.fetchall()
        cursor.close()
        mydb.close()

        if productos:
            return jsonify(productos), 200
        else:
            return jsonify({'message': f'No se encontraron productos en el rango de precio Q{precio_min} - Q{precio_max}'}), 404

    except Exception as ex:
        return jsonify({'message': f'Error al buscar por rango de precio: {ex}'}), 500

# ======================= BUSCAR PRODUCTOS POR STOCK ======================= #
def get_productos_by_stock():
    stock_min = request.args.get('min', 0)  # ?min=5
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        query = """
        SELECT p.*, c.nombre_categoria 
        FROM productos p 
        LEFT JOIN categorias c ON p.id_categoria = c.id_categoria 
        WHERE p.stock >= %s 
        ORDER BY p.stock DESC, p.nombre_producto
        """
        cursor = mydb.cursor(dictionary=True)
        cursor.execute(query, (stock_min,))
        productos = cursor.fetchall()
        cursor.close()
        mydb.close()

        if productos:
            return jsonify(productos), 200
        else:
            return jsonify({'message': f'No se encontraron productos con stock mínimo de {stock_min}'}), 404

    except Exception as ex:
        return jsonify({'message': f'Error al buscar por stock: {ex}'}), 500
