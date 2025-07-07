from flask import request, jsonify
from database.connection import dbConnection

# ======================= OBTENER TODOS LOS SLIDES ======================= #
def get_all_slides():
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM slides_carrusel ORDER BY orden_slide ASC, fecha_creacion DESC")
        slides = cursor.fetchall()
        cursor.close()
        mydb.close()
        return jsonify(slides), 200

    except Exception as ex:
        return jsonify({'message': f'Error al obtener los slides: {ex}'}), 500


# ======================= OBTENER SLIDE POR ID ======================= #
def get_slide_by_id(id_slide):
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM slides_carrusel WHERE id_slide = %s", (id_slide,))
        slide = cursor.fetchone()
        cursor.close()
        mydb.close()

        if slide:
            return jsonify(slide), 200
        else:
            return jsonify({'message': 'Slide no encontrado'}), 404

    except Exception as ex:
        return jsonify({'message': f'Error al obtener slide: {ex}'}), 500


# ======================= CREAR SLIDE ======================= #
def create_slide():
    data = request.json
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        query = """
        INSERT INTO slides_carrusel (titulo, descripcion, texto_boton, imagen_base64, 
                                   activo, orden_slide)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            data['titulo'],
            data.get('descripcion'),
            data.get('texto_boton'),
            data.get('imagen_base64'),
            data.get('activo', True),
            data.get('orden_slide', 0)
        )

        cursor = mydb.cursor()
        cursor.execute(query, values)
        mydb.commit()
        cursor.close()
        mydb.close()

        return jsonify({'message': 'Slide creado exitosamente'}), 201

    except Exception as ex:
        return jsonify({'message': f'Error al crear slide: {ex}'}), 400


# ======================= ACTUALIZAR SLIDE ======================= #
def update_slide(id_slide):
    data = request.json
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        query = """
        UPDATE slides_carrusel SET
            titulo = %s,
            descripcion = %s,
            texto_boton = %s,
            imagen_base64 = %s,
            activo = %s,
            orden_slide = %s
        WHERE id_slide = %s
        """
        values = (
            data['titulo'],
            data.get('descripcion'),
            data.get('texto_boton'),
            data.get('imagen_base64'),
            data.get('activo', True),
            data.get('orden_slide', 0),
            id_slide
        )

        cursor = mydb.cursor()
        cursor.execute(query, values)
        mydb.commit()
        cursor.close()
        mydb.close()

        return jsonify({'message': 'Slide actualizado exitosamente'}), 200

    except Exception as ex:
        return jsonify({'message': f'Error al actualizar slide: {ex}'}), 400


# ======================= ELIMINAR SLIDE ======================= #
def delete_slide(id_slide):
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        cursor = mydb.cursor()
        cursor.execute("DELETE FROM slides_carrusel WHERE id_slide = %s", (id_slide,))
        mydb.commit()
        cursor.close()
        mydb.close()

        return jsonify({'message': 'Slide eliminado correctamente'}), 200

    except Exception as ex:
        return jsonify({'message': f'Error al eliminar slide: {ex}'}), 400

# ======================= OBTENER SLIDES ACTIVOS ======================= #
def get_slides_activos():
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM slides_carrusel WHERE activo = TRUE ORDER BY orden_slide ASC")
        slides = cursor.fetchall()
        cursor.close()
        mydb.close()

        if slides:
            return jsonify(slides), 200
        else:
            return jsonify({'message': 'No se encontraron slides activos'}), 404

    except Exception as ex:
        return jsonify({'message': f'Error al obtener slides activos: {ex}'}), 500

# ======================= BUSCAR POR TÍTULO ======================= #
def search_slides_by_titulo():
    palabra_clave = request.args.get('q', '')  # ?q=valor
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        query = """
        SELECT * FROM slides_carrusel
        WHERE titulo LIKE %s OR descripcion LIKE %s
        ORDER BY orden_slide ASC, fecha_creacion DESC
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

# ======================= VERIFICAR EXISTENCIA DE SLIDE ======================= #
def check_slide_exists(id_slide):
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        cursor = mydb.cursor()
        cursor.execute("SELECT COUNT(*) FROM slides_carrusel WHERE id_slide = %s", (id_slide,))
        exists = cursor.fetchone()[0] > 0
        cursor.close()
        mydb.close()

        return jsonify({'exists': exists}), 200

    except Exception as ex:
        return jsonify({'message': f'Error al verificar slide: {ex}'}), 500

# ======================= ACTIVAR/DESACTIVAR SLIDE ======================= #
def toggle_slide_activo(id_slide):
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        # Primero obtener el estado actual
        cursor = mydb.cursor()
        cursor.execute("SELECT activo FROM slides_carrusel WHERE id_slide = %s", (id_slide,))
        result = cursor.fetchone()
        
        if not result:
            cursor.close()
            mydb.close()
            return jsonify({'message': 'Slide no encontrado'}), 404
        
        nuevo_estado = not result[0]  # Cambiar el estado
        
        # Actualizar el estado
        cursor.execute("UPDATE slides_carrusel SET activo = %s WHERE id_slide = %s", (nuevo_estado, id_slide))
        mydb.commit()
        cursor.close()
        mydb.close()

        estado_texto = "activado" if nuevo_estado else "desactivado"
        return jsonify({'message': f'Slide {estado_texto} exitosamente', 'activo': nuevo_estado}), 200

    except Exception as ex:
        return jsonify({'message': f'Error al cambiar estado del slide: {ex}'}), 400

# ======================= REORDENAR SLIDES ======================= #
def reorder_slides():
    data = request.json  # Esperamos un array de objetos con id_slide y orden_slide
    try:
        mydb, err = dbConnection()
        if mydb is None:
            return jsonify({'message': f'Error de conexión: {err}'}), 503

        cursor = mydb.cursor()
        
        # Actualizar el orden de cada slide
        for slide_order in data:
            cursor.execute(
                "UPDATE slides_carrusel SET orden_slide = %s WHERE id_slide = %s",
                (slide_order['orden_slide'], slide_order['id_slide'])
            )
        
        mydb.commit()
        cursor.close()
        mydb.close()

        return jsonify({'message': 'Orden de slides actualizado exitosamente'}), 200

    except Exception as ex:
        return jsonify({'message': f'Error al reordenar slides: {ex}'}), 400
