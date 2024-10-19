import pyodbc
import os

#-------------------------------------------------------------------------------------------

# RUTAS:

# Ruta de la carpeta del proyecto:
ruta_proyecto = r'C:\Users\User\Desktop\Disco_D\My_Projects\Prestamo_universal'

# Ruta para la carpeta Bases:
ruta_bases = os.path.join(ruta_proyecto, 'Bases')

#-------------------------------------------------------------------------------------------

# Función para conectar a SQL Server
def conectar_bd():
    conn = pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=DESKTOP-UAGKOK6;'
        'DATABASE=Prestamo_universal;'
        'Trusted_Connection=yes;'
    )
    return conn

# Función para crear la tabla temporal
def crear_tabla_temporal(cursor):
    sql_create_temp = """
        CREATE TABLE #temp_clientes (
            ti_documento CHAR(2),
            nu_documento VARCHAR(15),
            nombre_cliente NVARCHAR(100),
            email_cliente NVARCHAR(100),
            telefono_cliente VARCHAR(15),
            direccion_cliente NVARCHAR(200),
            id_pais_docu CHAR(4),
            id_ti_persona CHAR(1),
            ti_sexo CHAR(1),
            fe_nacimiento DATE,
            id_profesion INT,
            id_esta_civil INT,
            id_estado CHAR(1),
            id_cat_cliente INT,
            fe_apertura DATE NOT NULL DEFAULT GETDATE(),
            fe_aper_prim_prest DATE NOT NULL DEFAULT GETDATE()
        )
    """
    cursor.execute(sql_create_temp)

# Función para insertar los datos en la tabla temporal
def insertar_datos(cursor, data):
    sql_insert_temp = """
        INSERT INTO #temp_clientes 
        (ti_documento, nu_documento, nombre_cliente, email_cliente, telefono_cliente, direccion_cliente, id_pais_docu, id_ti_persona, ti_sexo, fe_nacimiento, id_profesion, id_esta_civil, id_estado, id_cat_cliente, fe_apertura, fe_aper_prim_prest)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.executemany(sql_insert_temp, data)

# Función para verificar la existencia de la tabla y consultar los datos
def verificar_tabla_temporal(cursor):
    # Consulta para verificar la tabla temporal
    cursor.execute("SELECT * FROM #temp_clientes")
    rows = cursor.fetchall()
    
    if rows:
        print("Datos en #temp_clientes:")
        for row in rows:
            print(row)
    else:
        print("La tabla #temp_clientes está vacía.")

# LLAMADA DE FUNCIONES


if __name__ == "__main__":
    # Paso 1: Crear una fila de prueba manualmente
    data_clientes = [
        ('01', '2338', 'Juan Perez', 'jpeasdfrez@gmail.com', '987654325', 'Calle Falsa 120', '9589', '1', 'M', '1985-07-12', 3, 1, 'V', 1, '2023-10-01', '2023-10-01')
    ]
    
    # Paso 2: Conectar a la base de datos
    conexion = conectar_bd()
    
    # Crear un cursor
    cursor = conexion.cursor()
    
    # Crear la tabla temporal
    crear_tabla_temporal(cursor)
    
    # Paso 3: Insertar los datos en la tabla temporal
    insertar_datos(cursor, data_clientes)

    # Verificar la tabla temporal
    verificar_tabla_temporal(cursor)

    # Confirmar cambios y cerrar la conexión
    conexion.commit()
    cursor.close()
    conexion.close()
