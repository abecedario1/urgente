from flask import request, jsonify
from database.connection import dbConnection

# ======================= OBTENER TODAS LAS CATEGORÍAS ======================= #
def get_all_categorias():
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM categorias ORDER BY nombre_categoria")
        categorias = cursor.fetchall()
        cursor.close()
        mydb.close()
        return jsonify(categorias), 200

    except Exception as ex:
        return jsonify({'message': f'Error al obtener las categorías: {ex}'}), 500


# ======================= OBTENER CATEGORÍA POR ID ======================= #
def get_categoria_by_id(id_categoria):
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM categorias WHERE id_categoria = %s", (id_categoria,))
        categoria = cursor.fetchone()
        cursor.close()
        mydb.close()

        if categoria:
            return jsonify(categoria), 200
        else:
            return jsonify({'message': 'Categoría no encontrada'}), 404

    except Exception as ex:
        return jsonify({'message': f'Error al obtener categoría: {ex}'}), 500


# ======================= CREAR CATEGORÍA ======================= #
def create_categoria():
    data = request.json
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        query = """
        INSERT INTO categorias (nombre_categoria, codigo, estado, fecha_fin)
        VALUES (%s, %s, %s, %s)
        """
        values = (
            data['nombre_categoria'],
            data['codigo'],
            data.get('estado', 'Activo'),
            data.get('fecha_fin')
        )

        cursor = mydb.cursor()
        cursor.execute(query, values)
        mydb.commit()
        cursor.close()
        mydb.close()

        return jsonify({'message': 'Categoría creada exitosamente'}), 201

    except Exception as ex:
        return jsonify({'message': f'Error al crear categoría: {ex}'}), 400


# ======================= ACTUALIZAR CATEGORÍA ======================= #
def update_categoria(id_categoria):
    data = request.json
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        query = """
        UPDATE categorias SET
            nombre_categoria = %s,
            codigo = %s,
            estado = %s,
            fecha_fin = %s
        WHERE id_categoria = %s
        """
        values = (
            data['nombre_categoria'],
            data['codigo'],
            data.get('estado', 'Activo'),
            data.get('fecha_fin'),
            id_categoria
        )

        cursor = mydb.cursor()
        cursor.execute(query, values)
        mydb.commit()
        cursor.close()
        mydb.close()

        return jsonify({'message': 'Categoría actualizada exitosamente'}), 200

    except Exception as ex:
        return jsonify({'message': f'Error al actualizar categoría: {ex}'}), 400


# ======================= ELIMINAR CATEGORÍA ======================= #
def delete_categoria(id_categoria):
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        cursor = mydb.cursor()
        cursor.execute("DELETE FROM categorias WHERE id_categoria = %s", (id_categoria,))
        mydb.commit()
        cursor.close()
        mydb.close()

        return jsonify({'message': 'Categoría eliminada correctamente'}), 200

    except Exception as ex:
        return jsonify({'message': f'Error al eliminar categoría: {ex}'}), 400

# ======================= BUSCAR CATEGORÍA POR CÓDIGO ======================= #
def get_categoria_by_codigo(codigo):
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM categorias WHERE codigo = %s", (codigo,))
        categoria = cursor.fetchone()
        cursor.close()
        mydb.close()

        if categoria:
            return jsonify(categoria), 200
        else:
            return jsonify({'message': 'Categoría no encontrada'}), 404

    except Exception as ex:
        return jsonify({'message': f'Error al buscar por código: {ex}'}), 500

# ======================= BUSCAR POR NOMBRE ======================= #
def search_categorias_by_nombre():
    palabra_clave = request.args.get('q', '')  # ?q=valor
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        query = """
        SELECT * FROM categorias
        WHERE nombre_categoria LIKE %s OR codigo LIKE %s
        ORDER BY nombre_categoria
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

# ======================= VERIFICAR EXISTENCIA DE CATEGORÍA ======================= #
def check_categoria_exists(id_categoria):
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        cursor = mydb.cursor()
        cursor.execute("SELECT COUNT(*) FROM categorias WHERE id_categoria = %s", (id_categoria,))
        exists = cursor.fetchone()[0] > 0
        cursor.close()
        mydb.close()

        return jsonify({'exists': exists}), 200

    except Exception as ex:
        return jsonify({'message': f'Error al verificar categoría: {ex}'}), 500

# ======================= BUSCAR CATEGORÍAS POR ESTADO ======================= #
def get_categorias_by_estado(estado):
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM categorias WHERE estado = %s ORDER BY nombre_categoria", (estado,))
        categorias = cursor.fetchall()
        cursor.close()
        mydb.close()

        if categorias:
            return jsonify(categorias), 200
        else:
            return jsonify({'message': f'No se encontraron categorías con estado {estado}'}), 404

    except Exception as ex:
        return jsonify({'message': f'Error al buscar por estado: {ex}'}), 500

# ======================= OBTENER CATEGORÍAS VIGENTES ======================= #
def get_categorias_vigentes():
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        query = """
        SELECT * FROM categorias 
        WHERE estado = 'Activo' 
        AND (fecha_fin IS NULL OR fecha_fin >= CURDATE())
        ORDER BY nombre_categoria
        """
        cursor = mydb.cursor(dictionary=True)
        cursor.execute(query)
        categorias = cursor.fetchall()
        cursor.close()
        mydb.close()

        if categorias:
            return jsonify(categorias), 200
        else:
            return jsonify({'message': 'No se encontraron categorías vigentes'}), 404

    except Exception as ex:
        return jsonify({'message': f'Error al obtener categorías vigentes: {ex}'}), 500
