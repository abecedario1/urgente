from flask import request, jsonify
from database.connection import dbConnection

# ======================= OBTENER TODOS LOS CLIENTES ======================= #
def get_all_clientes():
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM clientes")
        clientes = cursor.fetchall()
        cursor.close()
        mydb.close()
        return jsonify(clientes), 200

    except Exception as ex:
        return jsonify({'message': f'Error al obtener los clientes: {ex}'}), 500


# ======================= OBTENER CLIENTE POR ID ======================= #
def get_cliente_by_id(id_cliente):
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM clientes WHERE id_cliente = %s", (id_cliente,))
        cliente = cursor.fetchone()
        cursor.close()
        mydb.close()

        if cliente:
            return jsonify(cliente), 200
        else:
            return jsonify({'message': 'Cliente no encontrado'}), 404

    except Exception as ex:
        return jsonify({'message': f'Error al obtener cliente: {ex}'}), 500


# ======================= CREAR CLIENTE ======================= #
def create_cliente():
    data = request.json
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        query = """
        INSERT INTO clientes (id_cliente, dpi, nit, primer_nombre, segundo_nombre,
            primer_apellido, segundo_apellido, fecha_nacimiento, direccion,
            correo_electronico, telefono, estado)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            data['id_cliente'],
            data['dpi'],
            data.get('nit'),
            data['primer_nombre'],
            data.get('segundo_nombre'),
            data['primer_apellido'],
            data.get('segundo_apellido'),
            data['fecha_nacimiento'],
            data.get('direccion'),
            data.get('correo_electronico'),
            data.get('telefono'),
            data.get('estado', 'Activo'),
        )

        cursor = mydb.cursor()
        cursor.execute(query, values)
        mydb.commit()
        cursor.close()
        mydb.close()

        return jsonify({'message': 'Cliente creado exitosamente'}), 201

    except Exception as ex:
        return jsonify({'message': f'Error al crear cliente: {ex}'}), 400


# ======================= ACTUALIZAR CLIENTE ======================= #
def update_cliente(id_cliente):
    data = request.json
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        query = """
        UPDATE clientes SET
            dpi = %s,
            nit = %s,
            primer_nombre = %s,
            segundo_nombre = %s,
            primer_apellido = %s,
            segundo_apellido = %s,
            fecha_nacimiento = %s,
            direccion = %s,
            correo_electronico = %s,
            telefono = %s,
            estado = %s
        WHERE id_cliente = %s
        """
        values = (
            data['dpi'],
            data.get('nit'),
            data['primer_nombre'],
            data.get('segundo_nombre'),
            data['primer_apellido'],
            data.get('segundo_apellido'),
            data['fecha_nacimiento'],
            data.get('direccion'),
            data.get('correo_electronico'),
            data.get('telefono'),
            data.get('estado', 'Activo'),
            id_cliente
        )

        cursor = mydb.cursor()
        cursor.execute(query, values)
        mydb.commit()
        cursor.close()
        mydb.close()

        return jsonify({'message': 'Cliente actualizado exitosamente'}), 200

    except Exception as ex:
        return jsonify({'message': f'Error al actualizar cliente: {ex}'}), 400


# ======================= ELIMINAR CLIENTE ======================= #
def delete_cliente(id_cliente):
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        cursor = mydb.cursor()
        cursor.execute("DELETE FROM clientes WHERE id_cliente = %s", (id_cliente,))
        mydb.commit()
        cursor.close()
        mydb.close()

        return jsonify({'message': 'Cliente eliminado correctamente'}), 200

    except Exception as ex:
        return jsonify({'message': f'Error al eliminar cliente: {ex}'}), 400

# ======================= BUSCAR CLIENTE POR DPI ======================= #
def get_cliente_by_dpi(dpi):
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM clientes WHERE dpi = %s", (dpi,))
        cliente = cursor.fetchone()
        cursor.close()
        mydb.close()

        if cliente:
            return jsonify(cliente), 200
        else:
            return jsonify({'message': 'Cliente no encontrado'}), 404

    except Exception as ex:
        return jsonify({'message': f'Error al buscar por DPI: {ex}'}), 500

# ======================= BUSCAR CLIENTE POR NIT ======================= #
def get_cliente_by_nit(nit):
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM clientes WHERE nit = %s", (nit,))
        cliente = cursor.fetchone()
        cursor.close()
        mydb.close()

        if cliente:
            return jsonify(cliente), 200
        else:
            return jsonify({'message': 'Cliente no encontrado'}), 404

    except Exception as ex:
        return jsonify({'message': f'Error al buscar por NIT: {ex}'}), 500

# ======================= BUSCAR POR NOMBRE ======================= #
def search_clientes_by_nombre():
    palabra_clave = request.args.get('q', '')  # ?q=valor
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        query = """
        SELECT * FROM clientes
        WHERE primer_nombre LIKE %s OR segundo_nombre LIKE %s 
           OR primer_apellido LIKE %s OR segundo_apellido LIKE %s
           OR CONCAT(primer_nombre, ' ', primer_apellido) LIKE %s
        """
        like_value = f"%{palabra_clave}%"
        cursor = mydb.cursor(dictionary=True)
        cursor.execute(query, (like_value, like_value, like_value, like_value, like_value))
        resultados = cursor.fetchall()
        cursor.close()
        mydb.close()

        if resultados:
            return jsonify(resultados), 200
        else:
            return jsonify({'message': 'No se encontraron coincidencias'}), 404

    except Exception as ex:
        return jsonify({'message': f'Error en búsqueda: {ex}'}), 500

# ======================= VERIFICAR EXISTENCIA DE CLIENTE ======================= #
def check_cliente_exists(id_cliente):
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        cursor = mydb.cursor()
        cursor.execute("SELECT COUNT(*) FROM clientes WHERE id_cliente = %s", (id_cliente,))
        exists = cursor.fetchone()[0] > 0
        cursor.close()
        mydb.close()

        return jsonify({'exists': exists}), 200

    except Exception as ex:
        return jsonify({'message': f'Error al verificar cliente: {ex}'}), 500

# ======================= BUSCAR CLIENTES POR ESTADO ======================= #
def get_clientes_by_estado(estado):
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM clientes WHERE estado = %s", (estado,))
        clientes = cursor.fetchall()
        cursor.close()
        mydb.close()

        if clientes:
            return jsonify(clientes), 200
        else:
            return jsonify({'message': f'No se encontraron clientes con estado {estado}'}), 404

    except Exception as ex:
        return jsonify({'message': f'Error al buscar por estado: {ex}'}), 500
