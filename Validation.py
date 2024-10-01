import pandas as pd
import os
import emoji
import re
from datetime import datetime
#---------------------------------------------------------------------------------------------

#RUTA DEL PROYECTO:
ruta_proyecto = r'C:\Users\User\Desktop\Disco_D\My_Projects\Prestamo_universal'

#Ruta para la carpeta Bases:
ruta_bases = os.path.join(ruta_proyecto, 'Bases')

#---------------------------------------------------------------------------------------------

#LECTURA DE ARCHIVOS .CSV

clientes_df = pd.read_csv(os.path.join(ruta_bases, 'Clientes.csv'), delimiter = ';')

inversionistas_df = pd.read_csv(os.path.join(ruta_bases, 'Inversionistas.csv'), delimiter = ';')

#---------------------------------------------------------------------------------------------

#VALIDAR ESTRUCTURA DE LOS DATAFRAME

#CLIENTES:

# Validar columnas de clientes_df:

clientes_columnas = ['ti_documento', 'nu_documento', 'nombre_cliente', 'email_cliente', 'telefono_cliente', 'direccion_cliente', 'id_pais_docu', 'id_ti_persona', 'ti_sexo', 'fe_nacimiento', 'nu_cant_pres', 'id_profesion', 'id_esta_civil', 'id_estado', 'id_cat_cliente']

# Verificar si todas las columnas están presentes

if set(clientes_df.columns) != set(clientes_columnas):

    # Mostrar las columnas faltantes y adicionales para mejor depuración

    columnas_faltantes_cli = set(clientes_columnas) - set(clientes_df.columns)
    columnas_adicionales_cli = set(clientes_df.columns) - set(clientes_columnas)

    if columnas_faltantes_cli != 0:
        print(f"Advertencia: Columnas faltantes en 'Clientes.csv': {columnas_faltantes}")
    if columnas_adicionales_cli != 0:
        print(f"Advertencia: Columnas adicionales en 'Clientes.csv': {columnas_adicionales}")
    
    raise ValueError(f"Las columnas del archivo Clientes.csv no coinciden con las esperadas.")

else:
    print(emoji.emojize("La estructura de las columnas en 'Clientes.csv' es correcta :thumbs_up:"))

# Verificar si las columnas están en el mismo orden:

if clientes_df.columns.tolist() != clientes_columnas:
    raise ValueError(f"Las columnas del archivo Clientes.csv no coinciden con las esperadas. "
                     f"Actuales: {clientes_df.columns.tolist()}. "
                     f"Esperadas: {clientes_columnas}")
# Validar email:
def validar_email(email):
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(patron, email):
        return False
    return True

# Aplicar validación a la columna de correos en clientes_df

emails_invalidos = clientes_df[~clientes_df['email_cliente'].apply(validar_email)]
if not emails_invalidos.empty:
    print("Advertencia: Los siguientes correos electrónicos son inválidos:")
    print(emails_invalidos[['nombre_cliente', 'email_cliente']])

# Validar fecha
def validar_fecha(fecha):
    try:
        datetime.strptime(fecha, '%Y-%m-%d')
        return True
    except ValueError:
        return False

# Aplicar validación a la columna de fechas en clientes_df
fechas_invalidas = clientes_df[~clientes_df['fe_nacimiento'].apply(validar_fecha)]
if not fechas_invalidas.empty:
    print("Advertencia: Las siguientes fechas son inválidas:")
    print(fechas_invalidas[['nombre_cliente', 'fe_nacimiento']])

# INVERSIONISTAS:

#Validar columnas de inversionistas_columnas:

inversionistas_columnas = ['ti_documento', 'nu_documento', 'nombre_inversionista', 'email_inversionista', 'telefono_inversionista', 'direccion_inversionista', 'id_pais_docu', 'id_ti_persona', 'ti_sexo', 'fe_nacimiento', 'nu_cant_pres', 'id_profesion', 'id_esta_civil', 'id_estado', 'id_niv_inversionista']

# Verificar si todas las columnas están presentes

if set(inversionistas_df.columns) != set(inversionistas_columnas):

    # Mostrar las columnas faltantes y adicionales para mejor depuración

    columnas_faltantes_inv = set(inversionistas_columnas) - set(inversionistas_df.columns)
    columnas_adicionales_inv = set(inversionistas_df.columns) - set(inversionistas_columnas)

    if columnas_faltantes_inv != 0:
        print(f"Advertencia: Columnas faltantes en 'Inversionistas.csv': {columnas_faltantes_inv}")
    if columnas_adicionales_inv != 0:
        print(f"Advertencia: Columnas adicionales en 'Inversionistas.csv': {columnas_adicionales_inv}")
    
    raise ValueError(f"Las columnas del archivo Inversionistas.csv no coinciden con las esperadas.")
else:
    print(emoji.emojize("La estructura de las columnas en 'Inversionistas.csv' es correcta :thumbs_up:"))

# Verificar si las columnas están en el mismo orden:

if inversionistas_df.columns.tolist() != inversionistas_columnas:
    raise ValueError(f"Las columnas del archivo Inversionistas.csv no coinciden con las esperadas. "
                     f"Actuales: {inversionistas_df.columns.tolist()}. "
                     f"Esperadas: {inversionistas_columnas}")

# Validar email:
def validar_email(email):
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(patron, email):
        return False
    return True

# Aplicar validación a la columna de correos en inversionistas_df

emails_invalidos = inversionistas_df[~inversionistas_df['email_inversionista'].apply(validar_email)]
if not emails_invalidos.empty:
    print("Advertencia: Los siguientes correos electrónicos son inválidos:")
    print(emails_invalidos[['nombre_inversionista', 'email_inversionista']])

# Validar fecha
def validar_fecha(fecha):
    try:
        datetime.strptime(fecha, '%Y-%m-%d')
        return True
    except ValueError:
        return False

# Aplicar validación a la columna de fechas en inversionistas_df
fechas_invalidas = inversionistas_df[~inversionistas_df['fe_nacimiento'].apply(validar_fecha)]
if not fechas_invalidas.empty:
    print("Advertencia: Las siguientes fechas son inválidas:")
    print(fechas_invalidas[['nombre_inversionista', 'fe_nacimiento']])
# #-------------------------------------------------------------------------------------------------

# # GARANTIZAR ORDEN PARA BULK INSERT

# # Orden correcto de columnas para coincidir con la tabla en SQL Server
# clientes_ordenadas_columnas = ['ti_documento', 'nu_documento', 'nombre_cliente', 'email_cliente',
#                                'telefono_cliente', 'direccion_cliente', 'id_pais_docu', 'id_ti_persona',
#                                'ti_sexo', 'fe_nacimiento', 'nu_cant_pres', 'id_profesion',
#                                'id_esta_civil', 'id_estado', 'id_cat_cliente']

# # Reorganizar las columnas en el DataFrame
# clientes_df = clientes_df[clientes_ordenadas_columnas]

# # Escribir el archivo CSV en el orden correcto
# clientes_df.to_csv(os.path.join(ruta_bases, 'Clientes_reorganizado.csv'), sep=';', index=False)



#print(clientes_df.columns)
#print(clientes_columnas)
