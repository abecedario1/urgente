from flask import request, jsonify
from database.connection import dbConnection

# ======================= OBTENER TODOS LOS EMPLEADOS ======================= #
def get_all_empleados():
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM empleados ORDER BY primer_nombre, primer_apellido")
        empleados = cursor.fetchall()
        cursor.close()
        mydb.close()
        return jsonify(empleados), 200

    except Exception as ex:
        return jsonify({'message': f'Error al obtener los empleados: {ex}'}), 500


# ======================= OBTENER EMPLEADO POR ID ======================= #
def get_empleado_by_id(id_empleado):
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM empleados WHERE id_empleado = %s", (id_empleado,))
        empleado = cursor.fetchone()
        cursor.close()
        mydb.close()

        if empleado:
            return jsonify(empleado), 200
        else:
            return jsonify({'message': 'Empleado no encontrado'}), 404

    except Exception as ex:
        return jsonify({'message': f'Error al obtener empleado: {ex}'}), 500


# ======================= CREAR EMPLEADO ======================= #
def create_empleado():
    data = request.json
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        query = """
        INSERT INTO empleados (id_empleado, dpi, primer_nombre, segundo_nombre,
            primer_apellido, segundo_apellido, fecha_nacimiento, fecha_contratacion,
            direccion, correo_electronico, telefono, salario_q, estado)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            data['id_empleado'],
            data['dpi'],
            data['primer_nombre'],
            data.get('segundo_nombre'),
            data['primer_apellido'],
            data.get('segundo_apellido'),
            data['fecha_nacimiento'],
            data['fecha_contratacion'],
            data.get('direccion'),
            data.get('correo_electronico'),
            data.get('telefono'),
            data.get('salario_q'),
            data.get('estado', 'Nuevo'),
        )

        cursor = mydb.cursor()
        cursor.execute(query, values)
        mydb.commit()
        cursor.close()
        mydb.close()

        return jsonify({'message': 'Empleado creado exitosamente'}), 201

    except Exception as ex:
        return jsonify({'message': f'Error al crear empleado: {ex}'}), 400


# ======================= ACTUALIZAR EMPLEADO ======================= #
def update_empleado(id_empleado):
    data = request.json
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        query = """
        UPDATE empleados SET
            dpi = %s,
            primer_nombre = %s,
            segundo_nombre = %s,
            primer_apellido = %s,
            segundo_apellido = %s,
            fecha_nacimiento = %s,
            fecha_contratacion = %s,
            direccion = %s,
            correo_electronico = %s,
            telefono = %s,
            salario_q = %s,
            estado = %s
        WHERE id_empleado = %s
        """
        values = (
            data['dpi'],
            data['primer_nombre'],
            data.get('segundo_nombre'),
            data['primer_apellido'],
            data.get('segundo_apellido'),
            data['fecha_nacimiento'],
            data['fecha_contratacion'],
            data.get('direccion'),
            data.get('correo_electronico'),
            data.get('telefono'),
            data.get('salario_q'),
            data.get('estado', 'Activo'),
            id_empleado
        )

        cursor = mydb.cursor()
        cursor.execute(query, values)
        mydb.commit()
        cursor.close()
        mydb.close()

        return jsonify({'message': 'Empleado actualizado exitosamente'}), 200

    except Exception as ex:
        return jsonify({'message': f'Error al actualizar empleado: {ex}'}), 400


# ======================= ELIMINAR EMPLEADO ======================= #
def delete_empleado(id_empleado):
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        cursor = mydb.cursor()
        cursor.execute("DELETE FROM empleados WHERE id_empleado = %s", (id_empleado,))
        mydb.commit()
        cursor.close()
        mydb.close()

        return jsonify({'message': 'Empleado eliminado correctamente'}), 200

    except Exception as ex:
        return jsonify({'message': f'Error al eliminar empleado: {ex}'}), 400

# ======================= BUSCAR EMPLEADO POR DPI ======================= #
def get_empleado_by_dpi(dpi):
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM empleados WHERE dpi = %s", (dpi,))
        empleado = cursor.fetchone()
        cursor.close()
        mydb.close()

        if empleado:
            return jsonify(empleado), 200
        else:
            return jsonify({'message': 'Empleado no encontrado'}), 404

    except Exception as ex:
        return jsonify({'message': f'Error al buscar por DPI: {ex}'}), 500

# ======================= BUSCAR POR NOMBRE ======================= #
def search_empleados_by_nombre():
    palabra_clave = request.args.get('q', '')  # ?q=valor
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        query = """
        SELECT * FROM empleados
        WHERE primer_nombre LIKE %s OR segundo_nombre LIKE %s 
           OR primer_apellido LIKE %s OR segundo_apellido LIKE %s
           OR CONCAT(primer_nombre, ' ', primer_apellido) LIKE %s
        ORDER BY primer_nombre, primer_apellido
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

# ======================= VERIFICAR EXISTENCIA DE EMPLEADO ======================= #
def check_empleado_exists(id_empleado):
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        cursor = mydb.cursor()
        cursor.execute("SELECT COUNT(*) FROM empleados WHERE id_empleado = %s", (id_empleado,))
        exists = cursor.fetchone()[0] > 0
        cursor.close()
        mydb.close()

        return jsonify({'exists': exists}), 200

    except Exception as ex:
        return jsonify({'message': f'Error al verificar empleado: {ex}'}), 500

# ======================= BUSCAR EMPLEADOS POR ESTADO ======================= #
def get_empleados_by_estado(estado):
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM empleados WHERE estado = %s ORDER BY primer_nombre, primer_apellido", (estado,))
        empleados = cursor.fetchall()
        cursor.close()
        mydb.close()

        if empleados:
            return jsonify(empleados), 200
        else:
            return jsonify({'message': f'No se encontraron empleados con estado {estado}'}), 404

    except Exception as ex:
        return jsonify({'message': f'Error al buscar por estado: {ex}'}), 500

# ======================= BUSCAR EMPLEADOS POR RANGO DE SALARIO ======================= #
def get_empleados_by_salario_range():
    salario_min = request.args.get('min', 0)  # ?min=1000
    salario_max = request.args.get('max', 999999)  # ?max=5000
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        query = """
        SELECT * FROM empleados 
        WHERE salario_q BETWEEN %s AND %s 
        ORDER BY salario_q DESC, primer_nombre, primer_apellido
        """
        cursor = mydb.cursor(dictionary=True)
        cursor.execute(query, (salario_min, salario_max))
        empleados = cursor.fetchall()
        cursor.close()
        mydb.close()

        if empleados:
            return jsonify(empleados), 200
        else:
            return jsonify({'message': f'No se encontraron empleados en el rango de salario Q{salario_min} - Q{salario_max}'}), 404

    except Exception as ex:
        return jsonify({'message': f'Error al buscar por rango de salario: {ex}'}), 500
