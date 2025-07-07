from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector
from config import config
from controllers import clientes, empleados, categorias, productos, slides

# ===================== VARIABLES GLOBALES ====================== #

db = config['database']()

app = Flask(__name__)
CORS(app)

# ===================== CONEXIÓN A MySQL ======================== #
def dbConnection():
    try:
        mydb = mysql.connector.connect(
             host="212.1.211.1",
            user="u138453277_expo",
            password="Expo2025@*",
            database="u138453277_expo_tec"
        )
        return mydb, None
    except Exception as ex:
        return None, ex

# ============================ RUTAS ============================ #

# Ruta raíz
@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Servidor Python de IMPORCOMGUA funcionando'}), 200

# Ruta de error 404
def rutaNoEncontrada(error):
    return jsonify({'message': 'La página no existe'}), 404

@app.route('/test-db', methods=['GET'])
def test_db():
    mydb, err = dbConnection()
    if err:
        return jsonify({'error': f'No se pudo conectar: {err}'}), 500
    else:
        mydb.close()
        return jsonify({'message': '✅ Conexión exitosa con la base de datos'}), 200

# ================================= CLIENTES ========================================
app.add_url_rule('/api/clientes', view_func=clientes.get_all_clientes, methods=['GET'])
app.add_url_rule('/api/clientes/<id_cliente>', view_func=clientes.get_cliente_by_id, methods=['GET'])
app.add_url_rule('/api/clientes', view_func=clientes.create_cliente, methods=['POST'])
app.add_url_rule('/api/clientes/<id_cliente>', view_func=clientes.update_cliente, methods=['PUT'])
app.add_url_rule('/api/clientes/<id_cliente>', view_func=clientes.delete_cliente, methods=['DELETE'])
app.add_url_rule('/api/clientes/dpi/<dpi>', view_func=clientes.get_cliente_by_dpi, methods=['GET'])
app.add_url_rule('/api/clientes/nit/<nit>', view_func=clientes.get_cliente_by_nit, methods=['GET'])
app.add_url_rule('/api/clientes/search', view_func=clientes.search_clientes_by_nombre, methods=['GET'])  # ?q=texto
app.add_url_rule('/api/clientes/<id_cliente>/exists', view_func=clientes.check_cliente_exists, methods=['GET'])
app.add_url_rule('/api/clientes/estado/<estado>', view_func=clientes.get_clientes_by_estado, methods=['GET'])

# ================================== EMPLEADOS =============================================
# Rutas para CRUD de Empleados
app.add_url_rule('/api/empleados', view_func=empleados.get_all_empleados, methods=['GET'])
app.add_url_rule('/api/empleados/<id_empleado>', view_func=empleados.get_empleado_by_id, methods=['GET'])
app.add_url_rule('/api/empleados', view_func=empleados.create_empleado, methods=['POST'])
app.add_url_rule('/api/empleados/<id_empleado>', view_func=empleados.update_empleado, methods=['PUT'])
app.add_url_rule('/api/empleados/<id_empleado>', view_func=empleados.delete_empleado, methods=['DELETE'])
app.add_url_rule('/api/empleados/dpi/<dpi>', view_func=empleados.get_empleado_by_dpi, methods=['GET'])
app.add_url_rule('/api/empleados/search', view_func=empleados.search_empleados_by_nombre, methods=['GET'])  # ?q=texto
app.add_url_rule('/api/empleados/<id_empleado>/exists', view_func=empleados.check_empleado_exists, methods=['GET'])
app.add_url_rule('/api/empleados/estado/<estado>', view_func=empleados.get_empleados_by_estado, methods=['GET'])
app.add_url_rule('/api/empleados/salario', view_func=empleados.get_empleados_by_salario_range, methods=['GET'])  # ?min=1000&max=5000

# ==================================== CATEGORIAS ========================================================
# Rutas para CRUD de Categorías
app.add_url_rule('/api/categorias', view_func=categorias.get_all_categorias, methods=['GET'])
app.add_url_rule('/api/categorias/<int:id_categoria>', view_func=categorias.get_categoria_by_id, methods=['GET'])
app.add_url_rule('/api/categorias', view_func=categorias.create_categoria, methods=['POST'])
app.add_url_rule('/api/categorias/<int:id_categoria>', view_func=categorias.update_categoria, methods=['PUT'])
app.add_url_rule('/api/categorias/<int:id_categoria>', view_func=categorias.delete_categoria, methods=['DELETE'])
app.add_url_rule('/api/categorias/codigo/<codigo>', view_func=categorias.get_categoria_by_codigo, methods=['GET'])
app.add_url_rule('/api/categorias/search', view_func=categorias.search_categorias_by_nombre, methods=['GET'])  # ?q=texto
app.add_url_rule('/api/categorias/<int:id_categoria>/exists', view_func=categorias.check_categoria_exists, methods=['GET'])
app.add_url_rule('/api/categorias/estado/<estado>', view_func=categorias.get_categorias_by_estado, methods=['GET'])
app.add_url_rule('/api/categorias/vigentes', view_func=categorias.get_categorias_vigentes, methods=['GET'])

# ====================================== PRODUCTOS ===========================================================
# Rutas para CRUD de Productos
app.add_url_rule('/api/productos', view_func=productos.get_all_productos, methods=['GET'])
app.add_url_rule('/api/productos/<int:id_producto>', view_func=productos.get_producto_by_id, methods=['GET'])
app.add_url_rule('/api/productos', view_func=productos.create_producto, methods=['POST'])
app.add_url_rule('/api/productos/<int:id_producto>', view_func=productos.update_producto, methods=['PUT'])
app.add_url_rule('/api/productos/<int:id_producto>', view_func=productos.delete_producto, methods=['DELETE'])
app.add_url_rule('/api/productos/codigo/<codigo>', view_func=productos.get_producto_by_codigo, methods=['GET'])
app.add_url_rule('/api/productos/categoria/<int:id_categoria>', view_func=productos.get_productos_by_categoria, methods=['GET'])
app.add_url_rule('/api/productos/search', view_func=productos.search_productos_by_nombre, methods=['GET'])  # ?q=texto
app.add_url_rule('/api/productos/<int:id_producto>/exists', view_func=productos.check_producto_exists, methods=['GET'])
app.add_url_rule('/api/productos/estado/<estado>', view_func=productos.get_productos_by_estado, methods=['GET'])
app.add_url_rule('/api/productos/precio', view_func=productos.get_productos_by_precio_range, methods=['GET'])  # ?min=10&max=100
app.add_url_rule('/api/productos/stock', view_func=productos.get_productos_by_stock, methods=['GET'])  # ?min=5

# ========================================= SLIDES CARRUSEL =====================================================
# Rutas para CRUD de Slides del Carrusel
app.add_url_rule('/api/slides', view_func=slides.get_all_slides, methods=['GET'])
app.add_url_rule('/api/slides/<int:id_slide>', view_func=slides.get_slide_by_id, methods=['GET'])
app.add_url_rule('/api/slides', view_func=slides.create_slide, methods=['POST'])
app.add_url_rule('/api/slides/<int:id_slide>', view_func=slides.update_slide, methods=['PUT'])
app.add_url_rule('/api/slides/<int:id_slide>', view_func=slides.delete_slide, methods=['DELETE'])
app.add_url_rule('/api/slides/activos', view_func=slides.get_slides_activos, methods=['GET'])
app.add_url_rule('/api/slides/search', view_func=slides.search_slides_by_titulo, methods=['GET'])  # ?q=texto
app.add_url_rule('/api/slides/<int:id_slide>/exists', view_func=slides.check_slide_exists, methods=['GET'])
app.add_url_rule('/api/slides/<int:id_slide>/toggle', view_func=slides.toggle_slide_activo, methods=['PATCH'])
app.add_url_rule('/api/slides/reorder', view_func=slides.reorder_slides, methods=['PUT'])


# =============== INICIALIZACIÓN DEL SERVIDOR ================== #
if __name__ == '__main__':
    app.register_error_handler(404, rutaNoEncontrada)
    app.run(host='0.0.0.0',port=5000, debug=True)
