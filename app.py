from flask import Flask, render_template, request, flash
import pymssql

# Configuración de la conexión
server = 'localhost'  # Cambiar por la dirección de tu servidor SQL
user = 'sa'  # Usuario de la base de datos
password = 'JoseRamos1101.'  # Contraseña de la base de datos
database = 'Agroquimicos'  # Nombre de tu base de datos

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Función para conectarse a la base de datos
def get_db_connection():
    return pymssql.connect(server, user, password, database)

@app.route('/')
def index():
    return render_template('layout.html')

@app.route('/altas', methods=['GET', 'POST'])
def altas():
    mensaje = None
    sucursales = []

    # Consulta para obtener las sucursales existentes
    try:
        conn = pymssql.connect(server, user, password, database)
        cursor = conn.cursor()
        cursor.execute("SELECT id_sucursal, nombre_sucursal, direccion_sucursal FROM Sucursal")
        sucursales = cursor.fetchall()
    except pymssql.Error as e:
        print(f"Error al consultar sucursales: {e}")
    finally:
        conn.close()

    if request.method == 'POST':
        # Procesar datos del formulario de Altas
        id_sucursal = request.form.get('id_sucursal')
        nombre = request.form.get('nombre')
        direccion = request.form.get('direccion')

        try:
            conn = pymssql.connect(server, user, password, database)
            cursor = conn.cursor()
            cursor.callproc('AgregarSucursal', (id_sucursal, nombre, direccion))
            conn.commit()
            mensaje = f"Sucursal '{nombre}' añadida correctamente."
        except pymssql.Error as e:
            mensaje = f"Error al añadir sucursal: {e}"
        finally:
            conn.close()

    return render_template('altas.html', mensaje=mensaje, sucursales=sucursales)


@app.route('/bajas_empleado', methods=['GET', 'POST'])
def bajas_empleado():
    mensaje = None
    empleados = []

    # Consulta para obtener todos los empleados
    try:
        conn = pymssql.connect(server, user, password, database)
        cursor = conn.cursor()
        cursor.execute("SELECT id_empleado, nombre_empleado FROM Empleado")  # Ajusta según las columnas reales
        empleados = cursor.fetchall()
    except pymssql.Error as e:
        print(f"Error al consultar empleados: {e}")
    finally:
        conn.close()

    if request.method == 'POST':
        id_empleado = request.form.get('id')
        try:
            conn = pymssql.connect(server, user, password, database)
            cursor = conn.cursor()
            cursor.callproc('EliminarEmpleado', (id_empleado,))
            conn.commit()
            mensaje = f"Empleado con ID {id_empleado} eliminado correctamente."
        except pymssql.Error as e:
            mensaje = f"Error al eliminar empleado: {e}"
        finally:
            conn.close()

    return render_template('bajas_empleado.html', mensaje=mensaje, empleados=empleados)

#consultas pendient
@app.route('/consultas', methods=['GET', 'POST'])
def consultas():
    sucursales = None
    if request.method == 'POST':
        filtro = request.form.get('filtro')
        try:
            conn = get_db_connection()
            cursor = conn.cursor(as_dict=True)
            query = f"SELECT * FROM Sucursal WHERE nombre_sucursal LIKE '%{filtro}%'"
            cursor.execute(query)
            sucursales = cursor.fetchall()
        except pymssql.Error as e:
            flash(f"Error en la base de datos: {e}", 'error')
        finally:
            conn.close()
    return render_template('consultas.html', sucursales=sucursales)

@app.route('/cambios', methods=['GET', 'POST'])
def cambios():
    mensaje = None
    empleados = []
    puestos = ["Gerente", "Asistente", "Vendedor", "Supervisor", "Almacenista"]

    # Consultar empleados existentes con CEDIS o Sucursal
    try:
        conn = pymssql.connect(server, user, password, database)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                id_empleado, 
                nombre_empleado, 
                puesto_empleado, 
                CASE 
                    WHEN id_cedis IS NOT NULL THEN 'CEDIS'
                    WHEN id_sucursal IS NOT NULL THEN 'Sucursal'
                    ELSE 'N/A'
                END AS tipo
            FROM Empleado
        """)
        empleados = cursor.fetchall()
    except pymssql.Error as e:
        print(f"Error al consultar empleados: {e}")
    finally:
        conn.close()

    if request.method == 'POST':
        id_empleado = request.form.get('id_empleado')
        nuevo_puesto = request.form.get('nuevo_puesto')

        try:
            conn = pymssql.connect(server, user, password, database)
            cursor = conn.cursor()
            cursor.callproc('ActualizarPuestoEmpleado', (id_empleado, nuevo_puesto))
            conn.commit()
            mensaje = f"El puesto del empleado con ID {id_empleado} ha sido actualizado a '{nuevo_puesto}'."
        except pymssql.Error as e:
            mensaje = f"Error: {e}"
        finally:
            conn.close()

    return render_template('cambios.html', mensaje=mensaje, empleados=empleados, puestos=puestos)


if __name__ == '__main__':
    app.run(debug=True)
