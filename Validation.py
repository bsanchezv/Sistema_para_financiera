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
#---------------------------------------------------------------------------------------------

#VALIDAR ESTRUCTURA DE LOS DATAFRAME

## Definir las columnas esperadas ANTES de la función de validación

### Columnas esperadas para Clientes.csv

clientes_columnas = ['ti_documento', 'nu_documento', 'nombre_cliente', 'email_cliente', 'telefono_cliente', 'direccion_cliente', 'id_pais_docu', 'id_ti_persona', 'ti_sexo', 'fe_nacimiento', 'nu_cant_pres', 'id_profesion', 'id_esta_civil', 'id_estado', 'id_cat_cliente', 'fe_apertura', 'fe_aper_prim_cre']

### Columnas esperadas para Inversionistas.csv

inversionistas_columnas = ['ti_documento', 'nu_documento', 'nombre_inversionista', 'email_inversionista', 'telefono_inversionista', 'direccion_inversionista', 'id_pais_docu', 'id_ti_persona', 'ti_sexo', 'fe_nacimiento', 'nu_cant_pres', 'id_profesion', 'id_esta_civil', 'id_estado', 'id_niv_inversionista' , 'fe_apertura', 'fe_aper_prim_inv']

#---------------------------------------------------------------------------------------------

## Función para validar columnas

def validar_columnas(df,columnas_esperadas, nombre_archivo):

    ### Validar por columnas por conjunto

    if set(df.columns) != set(columnas_esperadas):

        #### Mostrar las columnas faltantes y adicionales para mejor depuración

        columnas_faltantes = set(columnas_esperadas) - set(df.columns)
        columnas_adicionales = set(df.columns) - set(columnas_esperadas)

        if columnas_faltantes:
            print(f"Advertencia: Columnas faltantes en '{nombre_archivo}': {columnas_faltantes}")

        if columnas_adicionales:
            print(f"Advertencia: Columnas adicionales en '{nombre_archivo}': {columnas_adicionales}")
        
        raise ValueError(emoji.emojize(f"Las columnas del archivo '{nombre_archivo}' no coinciden (en conjunto) con las esperadas. :double_exclamation_mark:"))

    else:
        print(emoji.emojize(f"La estructura de las columnas en '{nombre_archivo}' es correcta :thumbs_up:"))

    ### Validar columnas por orden

    if df.columns.tolist() != columnas_esperadas:
        raise ValueError(emoji.emojize(f"Las columnas del archivo '{nombre_archivo}' no coinciden (en orden) con las esperadas. :double_exclamation_mark:"
                     f"Actuales: {df.columns.tolist()}. "
                     f"Esperadas: {columnas_esperadas}"))
    ### Validar existencia de filas en el archivo .csv   
     
    if df.empty:
        raise ValueError(emoji.emojize(f"El archivo '{nombre_archivo}' está vacío. :cross_mark:"))
#---------------------------------------------------------------------------------------------

## Función para validar email:

def validar_email(email):

    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(patron, email))

### Aplicar validación a la columna de correos en los dataframes

def validar_emails(df, columna_email, nombre_archivo):

    emails_invalidos = df[~df[columna_email].apply(validar_email)]

    if not emails_invalidos.empty:

        print(emoji.emojize(f"Advertencia: Los siguientes correos electrónicos en '{nombre_archivo}' son inválidos :double_exclamation_mark: :"))

        print(emails_invalidos[[columna_email]])

#---------------------------------------------------------------------------------------------

## Función para validar fecha:

def validar_fecha(fecha):
    try:
        datetime.strptime(fecha, '%Y-%m-%d')
        return True
    except ValueError:
        return False

### Aplicar validación a la columna de fechas en los dataframes

def validar_fechas(df, columna_fecha, nombre_archivo, permitir_nat = False):

    #### Identificar filas con fechas inválidas

    fechas_invalidas = df[~df[columna_fecha].apply(validar_fecha)]

    #### Si permitir_nat es True, las fechas inválidas serán reemplazadas con NaT (solo para columnas donde NaT es aceptable).

    if permitir_nat:

        ##### Reemplazar fechas inválidas con NaT si está permitido

        df.loc[~df[columna_fecha].apply(validar_fecha), columna_fecha] = pd.NaT

    #### Si hay fechas inválidas:
    
    if (not permitir_nat and not fechas_invalidas.empty):
        print(emoji.emojize(f"Advertencia: Las siguientes fechas en '{nombre_archivo}' son inválidas :double_exclamation_mark:"))
        print(fechas_invalidas[[columna_fecha]])

    if (permitir_nat and not fechas_invalidas.empty) :
        print(emoji.emojize(f"Las fechas inválidas han sido reemplazadas con NaT en '{nombre_archivo}' :thumbs_up:"))
        print(fechas_invalidas[[columna_fecha]])

#---------------------------------------------------------------------------------------------


## Validar columnas

validar_columnas(clientes_df, clientes_columnas, "Clientes.csv")
validar_columnas(inversionistas_df, inversionistas_columnas, "Inversionistas.csv")

## Validar emails

validar_emails(clientes_df, 'email_cliente', "Clientes.csv")
validar_emails(inversionistas_df, 'email_inversionista', "Inversionistas.csv")

## Validar fechas

### Validar fechas para 'fe_nacimiento' (permitimos NaT para fechas de nacimiento)

validar_fechas(clientes_df, 'fe_nacimiento', "Clientes.csv", permitir_nat=True)
validar_fechas(inversionistas_df, 'fe_nacimiento', "Inversionistas.csv", permitir_nat=True)

### Validar fechas en otras columnas donde NO se permite NaT

validar_fechas(clientes_df, 'fe_apertura', "Clientes.csv", permitir_nat=False)
validar_fechas(clientes_df, 'fe_aper_prim_cre', "Clientes.csv", permitir_nat=False)

validar_fechas(inversionistas_df, 'fe_apertura', "Inversionistas.csv", permitir_nat=False)
validar_fechas(inversionistas_df, 'fe_aper_prim_inv', "Inversionistas.csv", permitir_nat=False)

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
