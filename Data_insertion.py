import pyodbc
import os
import pandas as pd

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
            fe_apertura DATE,
            fe_aper_prim_prest DATE
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
            id_nivel_inversionista INT,
            fe_apertura DATE,
            fe_aper_prim_inver DATE

        )
    """
    cursor.execute(sql_create_temp)

# Función para insertar los datos en la tabla temporal

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
        (ti_documento;nu_documento;nombre_inversionista;email_inversionista;telefono_inversionista;direccion_inversionista;id_pais_docu;id_ti_persona;ti_sexo;fe_nacimiento;id_profesion;id_esta_civil;id_estado;id_niv_inversionista;fe_apertura;fe_aper_prim_inv)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.executemany(sql_insert_temp, data)

# Función para verificar y mostrar datos de las tablas temporales

def verificar_tabla_temporal(cursor):

    # Mostrar #temp_clientes

    print("\nDatos en #temp_clientes:")

    # Consulta para verificar la tabla temporal #temp_clientes

    cursor.execute("SELECT * FROM #temp_clientes")
    rows_clientes = cursor.fetchall()
    
    if rows_clientes:

        print("Datos en #temp_clientes:")

        for row in rows_clientes:

            print(row)
    else:

        print("La tabla #temp_clientes está vacía.")

    # Mostrar #temp_inversionistas

    print("\nDatos en #temp_inversionistas:")

    # Consulta para verificar la tabla temporal #temp_clientes

    cursor.execute("SELECT * FROM #temp_inversionistas")
    rows_inversionistas = cursor.fetchall()
    if rows_inversionistas:
        for row in rows_inversionistas:
            print(row)
    else:
        print("La tabla #temp_inversionistas está vacía.")
# LLAMADA DE FUNCIONES
#######################################################
##### FALTA CORREGIR ESTA PARTE #####
#######################################################
if __name__ == "__main__":
        
    # Paso 2: Conectar a la base de datos
    conexion = conectar_bd()
    
    # Crear un cursor
    cursor = conexion.cursor()
    
    # Crear la tabla temporal

    crear_tabla_temporal_clientes(cursor)
    crear_tabla_temporal_inversionistas(cursor)

    
    # Paso 3: Insertar los datos en la tabla temporal
    insertar_datos(cursor, data_clientes)

    # Verificar la tabla temporal
    verificar_tabla_temporal(cursor)

    # Confirmar cambios y cerrar la conexión
    conexion.commit()
    cursor.close()
    conexion.close()
