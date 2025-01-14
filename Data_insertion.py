import pyodbc
import os
import pandas as pd
import emoji


#-------------------------------------------------------------------------------------------

# RUTAS:

# Ruta de la carpeta del proyecto:
ruta_proyecto = r'C:\Users\User\Desktop\Disco_D\My_Projects\Prestamo_universal'

# Ruta para la carpeta Bases:
ruta_bases = os.path.join(ruta_proyecto, 'Bases')

#-------------------------------------------------------------------------------------------

# Función para conectar a SQL Server
def conectar_bd():
    try:
        conn = pyodbc.connect(
            'DRIVER={SQL Server};'
            'SERVER=DESKTOP-UAGKOK6;'
            'DATABASE=Prestamo_universal;'
            'Trusted_Connection=yes;'
        )
        print(emoji.emojize(f"Conexión a la base de datos exitosa. :thumbs_up:"))
        return conn
    except pyodbc.Error as e:
        print("Error al conectar a la base de datos:", e)
        return None

# Función para crear la tabla temporal
def crear_tabla_temporal_clientes(cursor):
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

    # Función para crear la tabla temporal de inversionistas
def crear_tabla_temporal_inversionistas(cursor):
    sql_create_temp = """
        CREATE TABLE #temp_inversionistas (
            ti_documento CHAR(2),
            nu_documento VARCHAR(15),
            nombre_inversionista NVARCHAR(100),
            email_inversionista NVARCHAR(100),
            telefono_inversionista VARCHAR(15),
            direccion_inversionista VARCHAR(200),
            id_pais_docu CHAR(4),
            id_ti_persona CHAR(1),
            ti_sexo CHAR(1),
            fe_nacimiento DATE,
            id_profesion INT,
            id_esta_civil INT,
            id_estado CHAR(1),
            id_niv_inversionista INT,
            fe_apertura DATE NOT NULL DEFAULT GETDATE(),
            fe_aper_prim_inver DATE NOT NULL DEFAULT GETDATE()
        )
    """
    cursor.execute(sql_create_temp)


# Función para insertar los datos en la tabla temporal de clientes

def insertar_datos_clientes(cursor, data):
    sql_insert_temp = """
        INSERT INTO #temp_clientes 
        (ti_documento, nu_documento, nombre_cliente, email_cliente, telefono_cliente, direccion_cliente, id_pais_docu, id_ti_persona, ti_sexo, fe_nacimiento, id_profesion, id_esta_civil, id_estado, id_cat_cliente, fe_apertura, fe_aper_prim_prest)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.executemany(sql_insert_temp, data)

# Función para insertar datos en la tabla temporal de inversionistas

def insertar_datos_inversionistas(cursor, data):
    sql_insert_temp = """
        INSERT INTO #temp_inversionistas 
        (ti_documento, nu_documento, nombre_inversionista, email_inversionista, telefono_inversionista, direccion_inversionista, id_pais_docu, id_ti_persona, ti_sexo, fe_nacimiento, id_profesion, id_esta_civil, id_estado, id_niv_inversionista, fe_apertura, fe_aper_prim_inver)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.executemany(sql_insert_temp, data)

# Función para verificar y mostrar datos de las tablas temporales

def verificar_tabla_temporal(cursor):

    # Verificar #temp_clientes

    print("\nDatos en #temp_clientes:")
    cursor.execute("SELECT * FROM #temp_clientes")
    rows_clientes = cursor.fetchall()
    
    if rows_clientes:

        for row in rows_clientes:

            print(row)
    else:

        print("La tabla #temp_clientes está vacía.")

    # Verificar #temp_inversionistas

    print("\nDatos en #temp_inversionistas:")
    cursor.execute("SELECT * FROM #temp_inversionistas")
    rows_inversionistas = cursor.fetchall()

    if rows_inversionistas:

        for row in rows_inversionistas:

            print(row)

    else:

        print("La tabla #temp_inversionistas está vacía.")

# LLAMADA DE FUNCIONES
# Función principal
if __name__ == "__main__":
    try:
        # Conectar a la base de datos
        conexion = conectar_bd()
        # Crear cursor
        cursor = conexion.cursor()

        # Crear tablas temporales
        print("Creando tabla temporal de clientes...")
        crear_tabla_temporal_clientes(cursor)

        print("Creando tabla temporal de inversionistas...")
        crear_tabla_temporal_inversionistas(cursor)

        # Cargar datos desde archivos CSV
        archivo_clientes = os.path.join(ruta_bases, 'Clientes.csv')
        archivo_inversionistas = os.path.join(ruta_bases, 'Inversionistas.csv')

        print("Cargando datos de clientes desde CSV...")
        data_clientes = pd.read_csv(archivo_clientes, delimiter=';', encoding='utf-8').values.tolist()
        insertar_datos_clientes(cursor, data_clientes)

        print("Cargando datos de inversionistas desde CSV...")
        data_inversionistas = pd.read_csv(archivo_inversionistas, delimiter=';', encoding='utf-8').values.tolist()
        insertar_datos_inversionistas(cursor, data_inversionistas)

        # Verificar las tablas temporales
        print("Verificando datos en tablas temporales...")
        verificar_tabla_temporal(cursor)

        # Confirmar cambios
        conexion.commit()
        print("Datos insertados y confirmados correctamente.")

    except Exception as e:
        print("Error:", e)
    finally:
        # Cerrar la conexión
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()
        print("Conexión cerrada.")
#---------
        print("Estructura de los datos de clientes:", data_clientes[:1])  # Muestra las primeras 5 filas para verificar