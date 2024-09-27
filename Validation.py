import pandas as pd
import os
import emoji
#-------------------------------------------------------------------------------------------------

#RUTA DEL PROYECTO:
ruta_proyecto = r'C:\Users\User\Desktop\Disco D\My_Projects\Prestamo_universal'

#Ruta para la carpeta Bases:
ruta_bases = os.path.join(ruta_proyecto, 'Bases')

#-------------------------------------------------------------------------------------------------

#LECTURA DE ARCHIVOS .CSV

clientes_df = pd.read_csv(os.path.join(ruta_bases, 'Clientes.csv'), delimiter = ';')

inversionistas_df = pd.read_csv(os.path.join(ruta_bases, 'Inversionistas.csv'), delimiter = ';')

#-------------------------------------------------------------------------------------------------

#VALIDAR ESTRUCTURA DE LOS DATAFRAME

# Validar columnas de clientes_df:

clientes_columnas = ['ti_documento', 'nu_documento', 'nombre_cliente', 'email_cliente', 'telefono_cliente', 'direccion_cliente', 'id_pais_docu', 'id_ti_persona', 'ti_sexo', 'fe_nacimiento', 'nu_cant_pres', 'id_profesion', 'id_esta_civil', 'id_estado', 'id_cat_cliente']

# Verificar si todas las columnas están presentes

if set(clientes_df.columns) != set(clientes_columnas):

    # Mostrar las columnas faltantes y adicionales para mejor depuración

    columnas_faltantes_cli = set(clientes_columnas) - set(clientes_df.columns)
    columnas_adicionales_cli = set(clientes_df.columns) - set(clientes_columnas)
    raise ValueError(f"Las columnas del archivo Clientes.csv no coinciden con las esperadas."
                     f"Faltantes: {columnas_faltantes_cli}, Adicionales: {columnas_adicionales_cli}")
else:
    print(emoji.emojize("La estructura de las columnas en 'Clientes.csv' es correcta :thumbs_up:"))

#Validar columnas de inversionistas_columnas:

inversionistas_columnas = ['ti_documento', 'nu_documento', 'nombre_inversionista', 'email_inversionista', 'telefono_inversionista', 'direccion_inversionista', 'id_pais_docu', 'id_ti_persona', 'ti_sexo', 'fe_nacimiento', 'nu_cant_pres', 'id_profesion', 'id_esta_civil', 'id_estado', 'id_niv_inversionista']

# Verificar si todas las columnas están presentes

if set(inversionistas_df.columns) != set(inversionistas_columnas):
    # Mostrar las columnas faltantes y adicionales para mejor depuración
    columnas_faltantes_inv = set(inversionistas_columnas) - set(inversionistas_df.columns)
    columnas_adicionales_inv = set(inversionistas_df.columns) - set(inversionistas_columnas)
    raise ValueError(f"Las columnas del archivo Inversionistas.csv no coinciden con las esperadas."
                     f"Faltantes: {columnas_faltantes_inv}, Adicionales: {columnas_adicionales_inv}")
else:
    print(emoji.emojize("La estructura de las columnas en 'Inversionistas.csv' es correcta :thumbs_up:"))

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
