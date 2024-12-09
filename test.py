import pymssql

# Configuración de la conexión
server = 'localhost'  # Cambia esto por la dirección de tu servidor SQL
user = 'sa'  # Usuario de la base de datos
password = 'JoseRamos1101.'  # Contraseña de la base de datos
database = 'Agroquimicos'  # Nombre de tu base de datos

try:
    # Establecer la conexión
    conn = pymssql.connect(server, user, password, database)
    cursor = conn.cursor()
    
    # Realizar la inserción manualmente
    query = """
    INSERT INTO Sucursal (id_sucursal, nombre_sucursal, direccion_sucursal)
    VALUES (%s, %s, %s)
    """
    values = (30, 'Sucursal X', 'Direccion X')
    cursor.execute(query, values)
    
    # Confirmar la transacción
    conn.commit()
    print("Sucursal añadida correctamente.")
except pymssql.Error as e:
    print(f"Error en la base de datos: {e}")
finally:
    # Cerrar la conexión
    conn.close()
