import pandas as pd
import os
import pyodbc
#-----------------------------------------------------------------------------------------
#CONEXIÓN A SQL SERVER

connection = pyodbc.connect('DRIVER={SQL Server};'
                          'SERVER=DESKTOP-UAGKOK6;'
                          'DATABASE=Prestamo_universal;'
                          'Trusted_Connection=yes;')

cursor = connection.cursor()

#-----------------------------------------------------------------------------------------
#DEFINICIÓN DE LA RUTA DEL PROYECTO:
ruta_proyecto = r'C:\Users\User\Desktop\Disco D\My_Projects\Prestamo_universal'

#Ruta para la carpeta Bases:

ruta_bases = os.path.join(ruta_proyecto,'Bases')

#-----------------------------------------------------------------------------------------
#LECTURA DE ARCHIVOS CSV

#lectura del archivo Clientes.csv

clientes_df = pd.read_csv(os.path.join(ruta_bases,'Clientes.csv'), delimiter=';')

#lectura del archivo Inversionistas.csv

inversionistas_df = pd.read_csv(os.path.join(ruta_bases,'Inversionistas.csv'), delimiter=';')

#------------------------------------------------------
# VALIDAR ESTRUCTURA DE LOS DATAFRAME
#Validar clientes_df
clientes_columnas = ['ti_documento', 'nu_documento', 'nombre_cliente', 'email_cliente', 'telefono_cliente', 
                     'direccion_cliente', 'id_ubigeo', 'id_pais_docu', 'id_ti_persona', 'ti_sexo', 
                     'fe_nacimiento', 'nu_cant_pres', 'id_profesion', 'id_esta_civil', 'id_estado', 
                     'id_cat_cliente']

if list(clientes_df.columns) != set(clientes_columnas):
    raise ValueError(f"Las columnas del archivo Clientes.csv no coinciden con las esperadas: {clientes_columnas}")

#Validar inversionistas_df
inversionistas_columnas = ['ti_documento', 'nu_documento', 'nombre_inversionista', 'email_inversionista', 'telefono_inversionista', 
                           'direccion_inversionista', 'id_ubigeo', 'id_pais_docu', 'id_ti_persona', 'ti_sexo', 
                           'fe_nacimiento', 'nu_cant_pres', 'id_profesion', 'id_esta_civil', 'id_estado', 
                           'id_niv_inversionista']

if list(inversionistas_df.columns) != set(inversionistas_columnas):
    raise ValueError(f"Las columnas del archivo Inversionistas.csv no coinciden con las esperadas: {inversionistas_columnas}")

#------------------------------------------------------

# CONVERTIR DATOS

# Convertir columnas de fecha

clientes_df['fe_nacimiento'] = pd.to_datetime(clientes_df['fe_nacimiento'], errors='coerce', format='%Y-%m-%d')
inversionistas_df['fe_nacimiento'] = pd.to_datetime(inversionistas_df['fe_nacimiento'], errors='coerce', format='%Y-%m-%d')


#------------------------------------------------------
#MIGRAR DATOS AL SQL

#Formatear nulos:
def formatear_valor(valor):
    if pd.isna(valor):
        return "NULL"
    elif isinstance(valor, str):
        return f"'{valor}'"
    elif isinstance(valor, pd.Timestamp):
        return f"'{valor.strftime('%Y-%m-%d')}'"  # Formato de fecha
    else:
        return str(valor)  # Para números
    
# Función para insertar los datos en las tablas SQL
def insertar_datos(df, tabla_sql):
    try:
        cursor.fast_executemany = True
        valores = [tuple(row) for _, row in df.iterrows()]
        placeholders = ', '.join(['?'] * len(df.columns))
        query = f"INSERT INTO {tabla_sql} VALUES ({placeholders})"
        
        print(f"Insertando {len(df)} filas en la tabla {tabla_sql}...")

        cursor.executemany(query, valores)
        connection.commit()
        
        print(f"Insertadas correctamente {len(df)} filas en {tabla_sql}.")

    except Exception as e:
        connection.rollback()  # Revertir cambios si algo falla
        raise e  # Lanzar el error para que lo puedas manejar

# Insertar los datos en la tabla MD_clientes
insertar_datos(clientes_df, 'MD_clientes')

# Insertar los datos en la tabla MD_inversionistas
insertar_datos(inversionistas_df, 'MD_inversionistas')

print("Migración completada exitosamente.")

# Cerrar la conexión
cursor.close()
connection.close()