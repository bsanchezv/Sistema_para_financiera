import pandas as pd
import matplotlib.pyplot as plt
import emoji

from datetime import datetime
from dateutil.relativedelta import relativedelta

# Configuración de pandas para mostrar números con 2 decimales
pd.options.display.float_format = '{:,.2f}'.format

def calcular_trea(inflacion, id_niv_inversionista, monto_inversion, num_meses, tipo_desembolso):

    # Ajuste por la inflación esperada (BCRP)
    ajuste_inflacion = inflacion

    # Ajuste por nivel del inversionista
    if id_niv_inversionista == 5:  # Nivel Bronce
        ajuste_nivel = 0.0000
    elif id_niv_inversionista == 4:  # Nivel Plata
        ajuste_nivel = 0.0189
    elif id_niv_inversionista == 3:  # Nivel Oro
        ajuste_nivel = 0.0378
    elif id_niv_inversionista == 2:  # Nivel Platino
        ajuste_nivel = 0.0566
    elif id_niv_inversionista == 1:  # Nivel Diamante
        ajuste_nivel = 0.0755
    else:
        raise ValueError("🚨 El nivel del inversionista no es válido.")

    # Ajuste por monto de la inversión
    if monto_inversion > 10352:
        ajuste_monto = 0.0000
    elif 9955 <= monto_inversion < 10352:
        ajuste_monto = 0.0029
    elif 9558 <= monto_inversion < 9955:
        ajuste_monto = 0.0058
    elif 9161 <= monto_inversion < 9558:
        ajuste_monto = 0.0087
    elif 8764 <= monto_inversion < 9161:
        ajuste_monto = 0.0116
    elif 8367 <= monto_inversion < 8764:
        ajuste_monto = 0.0145
    elif 7970 <= monto_inversion < 8367:
        ajuste_monto = 0.0174
    elif 7573 <= monto_inversion < 7970:
        ajuste_monto = 0.0203
    elif 7176 <= monto_inversion < 7573:
        ajuste_monto = 0.0232
    elif 6779 <= monto_inversion < 7176:
        ajuste_monto = 0.0261
    elif 6382 <= monto_inversion < 6779:
        ajuste_monto = 0.0290
    elif 5985 <= monto_inversion < 6382:
        ajuste_monto = 0.0319
    elif 5588 <= monto_inversion < 5985:
        ajuste_monto = 0.0348
    elif 5191 <= monto_inversion < 5588:
        ajuste_monto = 0.0378
    elif 4794 <= monto_inversion < 5191:
        ajuste_monto = 0.0407
    elif 4397 <= monto_inversion < 4794:
        ajuste_monto = 0.0436
    elif 4000 <= monto_inversion < 4397:
        ajuste_monto = 0.0465
    elif 3603 <= monto_inversion < 4000:
        ajuste_monto = 0.0494
    elif 3206 <= monto_inversion < 3603:
        ajuste_monto = 0.0523
    elif 2809 <= monto_inversion < 3206:
        ajuste_monto = 0.0552
    elif 2412 <= monto_inversion < 2809:
        ajuste_monto = 0.0581
    elif 2015 <= monto_inversion < 2412:
        ajuste_monto = 0.0610
    elif 1618 <= monto_inversion < 2015:
        ajuste_monto = 0.0639
    elif 1221 <= monto_inversion < 1618:
        ajuste_monto = 0.0668
    elif 824 <= monto_inversion < 1221:
        ajuste_monto = 0.0697
    elif 427 <= monto_inversion < 824:
        ajuste_monto = 0.0726
    elif 100 <= monto_inversion < 427:
        ajuste_monto = 0.0755
    else:  # 0.01 <= monto_prestamo < 30
        raise ValueError("🚨 El monto debe ser mayor o igual a S/100.")

    # Ajuste por número de desembolsos o cuotas del préstamo
    if 1 <= num_meses < 2:
        ajuste_desembolsos = 0.0755
    elif 2 <= num_meses < 3:
        ajuste_desembolsos = 0.0726
    elif 3 <= num_meses < 4:
        ajuste_desembolsos = 0.0697
    elif 4 <= num_meses < 5:
        ajuste_desembolsos = 0.0668
    elif 5 <= num_meses < 7:
        ajuste_desembolsos = 0.0639
    elif 7 <= num_meses < 8:
        ajuste_desembolsos = 0.0610
    elif 8 <= num_meses < 9:
        ajuste_desembolsos = 0.0581
    elif 9 <= num_meses < 10:
        ajuste_desembolsos = 0.0552
    elif 10 <= num_meses < 11:
        ajuste_desembolsos = 0.0523
    elif 11 <= num_meses < 12:
        ajuste_desembolsos = 0.0494
    elif 12 <= num_meses < 13:
        ajuste_desembolsos = 0.0465
    elif 13 <= num_meses < 14:
        ajuste_desembolsos = 0.0436
    elif 14 <= num_meses < 15:
        ajuste_desembolsos = 0.0407
    elif 15 <= num_meses < 16:
        ajuste_desembolsos = 0.0378
    elif 16 <= num_meses < 18:
        ajuste_desembolsos = 0.0348
    elif 18 <= num_meses < 19:
        ajuste_desembolsos = 0.0319
    elif 19 <= num_meses < 20:
        ajuste_desembolsos = 0.0290
    elif 20 <= num_meses < 21:
        ajuste_desembolsos = 0.0261
    elif 21 <= num_meses < 22:
        ajuste_desembolsos = 0.0232
    elif 22 <= num_meses < 23:
        ajuste_desembolsos = 0.0203
    elif 23 <= num_meses < 24:
        ajuste_desembolsos = 0.0174
    elif 24 <= num_meses < 25:
        ajuste_desembolsos = 0.0145
    elif 25 <= num_meses < 26:
        ajuste_desembolsos = 0.0116
    elif 26 <= num_meses < 27:
        ajuste_desembolsos = 0.0087
    elif 27 <= num_meses < 29:
        ajuste_desembolsos = 0.0058
    elif 29 <= num_meses < 30:
        ajuste_desembolsos = 0.0029
    elif 30 <= num_meses < 31:
        ajuste_desembolsos = 0.0000
    else:
        raise ValueError("🚨 El número de desembolsos está fuera del rango permitido.")

    # Ajuste por tipo de desembolso
    if tipo_desembolso == "único":
        ajuste_tipo_desembolso = 0.0755
    elif tipo_desembolso == "mensual":
        ajuste_tipo_desembolso = 0.0000
    else:
        raise ValueError("🚨 El tipo de desembolso no es válido.")

    # Calcular la tasa final
    trea = (
        ajuste_inflacion * 1.00
        + ajuste_nivel * 0.4
        + ajuste_monto * 0.3
        + ajuste_desembolsos * 0.2
        + ajuste_tipo_desembolso * 0.1
    )

    return round(trea,4)

def calcular_trem(trea):
    """
    Calcula la TREM (Tasa de Rendimiento Efectiva Mensual) a partir de la TREA (Tasa de Rendimiento Efectiva Anual).
    """
    trea = calcular_trea(inflacion, id_niv_inversionista, monto_inversion, num_meses, tipo_desembolso)
    trem = (1 + trea) ** (1 / 12) - 1

    return trem

def generar_cronograma_inversionista(monto_inversion, trea, num_meses, tipo_desembolso, fecha_inicio_inversion, nombre_inversionista, categoria_inversionista):
    

    """
    Calcula el cronograma de desembolsos para un inversionista.
    """

    # Validaciones de entrada
    if not(0 < trea <= 1):
        raise ValueError("La TREA debe ser un número mayor a 0 y menor a 1.")

    # Calcular la TREM
    trem = calcular_trem(trea)
    
    # Convertir fecha de inicio a objeto datetime
    fecha_inicio = datetime.strptime(fecha_inicio_inversion, '%d/%m/%Y')

    # Inicializar variables
    capital = monto_inversion
    interes_acumulado = 0
    cronograma_inversionista = []

    # Caso de desembolso único
    if tipo_desembolso == "único":
        for i in range(1, num_meses + 1):
            # Calcular interés mensual
            interes_mensual = capital * trem

            # Acumular el interés
            interes_acumulado += interes_mensual

            # Actualizar el dinero acumulado
            dinero_acumulado = capital + interes_mensual

            # Fecha de desembolso
            fecha_desembolso = fecha_inicio + relativedelta(months=i)

            # Agregar al cronograma
            cronograma_inversionista.append({
                "N° mes": i,
                "Fecha": fecha_desembolso.strftime('%d/%m/%Y'),
                "Saldo (S/)": round(capital, 2),
                "Rendimiento (S/)": round(interes_mensual, 2),
                "Rendimiento acumulado (S/)": round(interes_acumulado, 2),
                "Importe acumulado (S/)": round(dinero_acumulado, 2)
            })

            # Actualizar capital
            capital = dinero_acumulado

        # Resumen
        resumen_cronograma_inversionista = {
            "Nombre del inversionista:": nombre_inversionista,
            "Team:": categoria_inversionista,   
            "Fecha de inversión:":fecha_inicio_inversion,
            "N° de desembolsos:": '1',
            "Fecha de desembolso:": cronograma_inversionista[-1]["Fecha"],
            "Importe invertido (S/):": monto_inversion,
            "Rendimiento total (S/):": round(interes_acumulado, 2),
            "Importe desembolsado (S/):": round(dinero_acumulado, 2),
            "TREA (%):": round(trea * 100, 2)
        }

    # Caso de desembolsos mensuales
    elif tipo_desembolso == "mensual":
        for i in range(1, num_meses + 1):
            # Calcular interés mensual

            interes_mensual = capital * trem

            # Acumular el interés
            interes_acumulado += interes_mensual

            # Calcular dinero acumulado mensual
            dinero_acumulado = capital + interes_mensual

            # Calcular desembolso
            desembolso = dinero_acumulado / (num_meses - i + 1)

            # Actualizar capital
            capital = dinero_acumulado - desembolso

            # Fecha de desembolso
            fecha_desembolso = fecha_inicio + relativedelta(months=i)

            # Agregar al cronograma
            cronograma_inversionista.append({
                "N° Desembolso": i,
                "Fecha": fecha_desembolso.strftime('%d/%m/%Y'),
                "Saldo (S/)": round(dinero_acumulado - interes_mensual, 2),
                "Rendimiento (S/)": round(interes_mensual, 2),
                "Rendimiento acumulado (S/)": round(interes_acumulado, 2),
                "Importe acumulado (S/)": round(dinero_acumulado, 2),
                "Desembolso (S/)": round(desembolso, 2)
            })

        # Resumen
        resumen_cronograma_inversionista = {
            "Nombre del inversionista:": nombre_inversionista,
            "Team:": categoria_inversionista,           
            "Fecha de inversión:":fecha_inicio_inversion,
            "N° de desembolsos:": num_meses,
            "Fecha final de desembolso:": cronograma_inversionista[-1]["Fecha"],
            "Importe invertido (S/):": monto_inversion,
            "Rendimiento total (S/):": round(interes_acumulado, 2),
            "Importe total desembolsado (S/):": round(sum([row["Desembolso (S/)"] for row in cronograma_inversionista]), 2),
            "TREA (%):": round(trea * 100, 2)
        }

    cronograma_inversionista_df = pd.DataFrame(cronograma_inversionista)

    resumen_cronograma_inversionista_df = pd.DataFrame([resumen_cronograma_inversionista]).T
    resumen_cronograma_inversionista_df.columns = [""]
    
    return cronograma_inversionista_df, resumen_cronograma_inversionista_df 

def cronograma_a_imagen(cronograma_inversionista_df, resumen_cronograma_inversionista_df):
    """
    Convierte el cronograma a una imagen y la muestra con el resumen.
    """
    # Crear figura
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.axis('on')  # Ocultar los ejes

    # Mostrar el resumen primero
    ax.text(0.5, 0.95, "Resumen del Cronograma", fontsize=12, ha="center", va="top", weight="bold")
    tabla_resumen = ax.table(
        cellText=resumen_cronograma_inversionista_df.values,
        rowLabels=resumen_cronograma_inversionista_df.index,
        cellLoc='center',
        loc='center',
        bbox=[0.45, 0.7, 0.25, 0.2]  # [left, bottom, width, height]
    )
    tabla_resumen.auto_set_font_size(False)
    tabla_resumen.set_fontsize(10)
    tabla_resumen.scale(1.2, 1.2)

    # Eliminar bordes de las celdas en la tabla de resumen
    for key, cell in tabla_resumen.get_celld().items():
        cell.set_linewidth(0)  # Establecer el ancho del borde en 0

    # Mostrar el cronograma después
    ax.text(0.5, 0.65, "Cronograma", fontsize=12, ha="center", va="top", weight="bold")
    tabla_cronograma = ax.table(
        cellText=cronograma_inversionista_df.values,
        colLabels=cronograma_inversionista_df.columns,
        cellLoc='center',
        loc='center',
        bbox=[0.03, 0.15, 0.95, 0.4]  # [left, bottom, width, height]
    )
    tabla_cronograma.auto_set_font_size(False)
    tabla_cronograma.set_fontsize(10)
    tabla_cronograma.scale(1.2, 1.2)

    # Ajustar diseño y mostrar
    plt.tight_layout()
    plt.show()

def exportar_a_excel(cronograma_inversionista_df, resumen_cronograma_inversionista_df, nombre_archivo):
    """
    Exporta el cronograma y el resumen a un archivo de Excel con el nombre especificado.
    """

    with pd.ExcelWriter(nombre_archivo, engine='xlsxwriter') as writer:
        # Exportar el resumen al primer sheet
        resumen_cronograma_inversionista_df.to_excel(writer, sheet_name="Resumen", startrow=0, startcol=0, header=False)

        # Exportar el cronograma al segundo sheet
        cronograma_inversionista_df.to_excel(writer, sheet_name="Cronograma", index=False)

    print(f"Archivo Excel '{nombre_archivo}' generado exitosamente.")

#---------------------------------------------------------------------------------------------

# DATOS DE ENTRADA
#---------------------------------------------------------------------------------------------

# Datos del inversionista:
id_niv_inversionista = 3  # Nivel del inversionista (Oro)
nombre_inversionista = "Edwin N. Huacchillo T."
categoria_inversionista = "Oro"

# Datos de la inversión:
monto_inversion =200 # Monto invertido
num_meses = 1  # Número de desembolsos
tipo_desembolso = "único"  # Tipo de desembolso ("único" o "mensual")
fecha_inicio_inversion = "12/03/2025"  # Fecha de inicio

# Constantes:
inflacion = 2.45 / 100 # La inflación

#---------------------------------------------------------------------------------------------

# Calcular cronograma
trea = calcular_trea(
    inflacion,
    id_niv_inversionista,
    monto_inversion,
    num_meses,
    tipo_desembolso
)

cronograma_inversionista_df, resumen_cronograma_inversionista_df = generar_cronograma_inversionista(
    monto_inversion,
    trea,
    num_meses,
    tipo_desembolso,
    fecha_inicio_inversion,
    nombre_inversionista,
    categoria_inversionista
    )

# Mostrar resumen
print("\nResumen:")
print(resumen_cronograma_inversionista_df)

# Mostrar cronograma
print("Cronograma de desembolsos:")
print(cronograma_inversionista_df)


# Mostrar el cronograma como imagen
cronograma_a_imagen(cronograma_inversionista_df, resumen_cronograma_inversionista_df)

# Nombre del archivo
nombre_archivo = "Cronograma de desembolsos - LR20250312.xlsx"
# Agregar la columna "Estado del desembolso" solo para el archivo de Excel
cronograma_inversionista_df["Estado del desembolso"] = "Pendiente"
# Exportar a Excel
exportar_a_excel(cronograma_inversionista_df, resumen_cronograma_inversionista_df, nombre_archivo)