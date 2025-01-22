import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Configuración de pandas para mostrar números con 2 decimales
pd.options.display.float_format = '{:,.2f}'.format

def calcular_trem(trea):
    """
    Calcula la TREM (Tasa de Rendimiento Efectiva Mensual) a partir de la TREA (Tasa de Rendimiento Efectiva Anual).
    """
    return (1 + trea) ** (1 / 12) - 1

def generar_cronograma_inversionista(monto_inversion, trea, num_desembolsos, tipo_desembolso, fecha_inicio_inversion):
    

    """
    Calcula el cronograma de desembolsos para un inversionista.
    """

    # Validaciones de entrada
    if not (isinstance(monto_inversion, (int, float)) and monto_inversion >= 0):
        raise ValueError("El monto de inversión debe ser mayor a 0.")
    if not(0 < trea <= 1):
        raise ValueError("La TREA debe ser un número mayor a 0 y menor a 1.")
    if num_desembolsos <= 0 or not isinstance(num_desembolsos, int):
        raise ValueError("El número de meses debe ser un entero positivo.")
    if tipo_desembolso not in ["único", "mensual"]:
        raise ValueError("El tipo de desembolso debe ser 'único' o 'mensual'.")
    
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
        for i in range(1, num_desembolsos + 1):
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
                "Rendimiento mensual (S/)": round(interes_mensual, 2),
                "Rendimiento acumulado mensual (S/)": round(interes_acumulado, 2),
                "Dinero acumulado mensual (S/)": round(dinero_acumulado, 2)
            })

            # Actualizar capital
            capital = dinero_acumulado

        # Resumen
        resumen_cronograma_inversionista = {
            "N° de desembolsos:": '1',
            "Fecha de desembolso:": cronograma_inversionista[-1]["Fecha"],
            "Importe invertido (S/):": monto_inversion,
            "Rendimiento total (S/):": round(interes_acumulado, 2),
            "Importe desembolsado (S/):": round(dinero_acumulado, 2)
        }

    # Caso de desembolsos mensuales
    elif tipo_desembolso == "mensual":
        for i in range(1, num_desembolsos + 1):
            # Calcular interés mensual

            interes_mensual = capital * trem

            # Acumular el interés
            interes_acumulado += interes_mensual

            # Calcular dinero acumulado mensual
            dinero_acumulado = capital + interes_mensual

            # Calcular desembolso
            desembolso = dinero_acumulado / (num_desembolsos - i + 1)

            # Actualizar capital
            capital = dinero_acumulado - desembolso

            # Fecha de desembolso
            fecha_desembolso = fecha_inicio + relativedelta(months=i)

            # Agregar al cronograma
            cronograma_inversionista.append({
                "N° Desembolso": i,
                "Fecha": fecha_desembolso.strftime('%d/%m/%Y'),
                "Saldo (S/)": round(dinero_acumulado - interes_mensual, 2),
                "Rendimiento mensual (S/)": round(interes_mensual, 2),
                "Rendimiento acumulado mensual (S/)": round(interes_acumulado, 2),
                "Importe acumulado mensual (S/)": round(dinero_acumulado, 2),
                "Desembolso (S/)": round(desembolso, 2)
            })

        # Resumen
        resumen_cronograma_inversionista = {
            "N° de desembolsos:": num_desembolsos,
            "Fecha final de desembolso:": cronograma_inversionista[-1]["Fecha de pago"],
            "Importe invertido (S/):": monto_inversion,
            "Rendimiento total (S/):": round(interes_acumulado, 2),
            "Importe total desembolsado (S/):": round(sum([row["Desembolso (S/)"] for row in cronograma_inversionista]), 2)
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
    ax.axis('off')  # Ocultar los ejes

    # Mostrar el resumen primero
    ax.text(0.5, 0.95, "Resumen del Cronograma", fontsize=16, ha="center", va="top", weight="bold")
    tabla_resumen = ax.table(
        cellText=resumen_cronograma_inversionista_df.values,
        rowLabels=resumen_cronograma_inversionista_df.index,
        cellLoc='center',
        loc='center',
        bbox=[0.45, 0.7, 0.25, 0.2]  # [left, bottom, width, height]
    )
    tabla_resumen.auto_set_font_size(False)
    tabla_resumen.set_fontsize(12)
    tabla_resumen.scale(1.2, 1.2)

    # Eliminar bordes de las celdas en la tabla de resumen
    for key, cell in tabla_resumen.get_celld().items():
        cell.set_linewidth(0)  # Establecer el ancho del borde en 0

    # Mostrar el cronograma después
    ax.text(0.5, 0.65, "Cronograma", fontsize=14, ha="center", va="top", weight="bold")
    tabla_cronograma = ax.table(
        cellText=cronograma_inversionista_df.values,
        colLabels=cronograma_inversionista_df.columns,
        cellLoc='center',
        loc='center',
        bbox=[0, 0.0, 1, 0.6]  # [left, bottom, width, height]
    )
    tabla_cronograma.auto_set_font_size(False)
    tabla_cronograma.set_fontsize(10)
    tabla_cronograma.scale(1.0, 1.0)

    # Ajustar diseño y mostrar
    plt.tight_layout()
    plt.show()

def exportar_a_excel(cronograma_inversionista_df, resumen_cronograma_inversionista_df, nombre_archivo):
    """
    Exporta el cronograma y el resumen a un archivo de Excel con el nombre especificado.
    """
    # Agregar la columna "Estado de la cuota" al cronograma
    cronograma_inversionista_df["Estado de la cuota"] = "Pendiente"

    with pd.ExcelWriter(nombre_archivo, engine='xlsxwriter') as writer:
        # Exportar el resumen al primer sheet
        resumen_cronograma_inversionista_df.to_excel(writer, sheet_name="Resumen", startrow=0, startcol=0, header=False)

        # Exportar el cronograma al segundo sheet
        cronograma_inversionista_df.to_excel(writer, sheet_name="Cronograma", index=False)

    print(f"Archivo Excel '{nombre_archivo}' generado exitosamente.")

#---------------------------------------------------------------------------------------------

# DATOS DE ENTRADA
#---------------------------------------------------------------------------------------------

monto_inversion = 1500  # Monto invertido
trea = 0.0765 # TREA en decimal
num_desembolsos = 4  # Número de desembolsos
tipo_desembolso = "único"  # Tipo de desembolso ("único" o "mensual")
fecha_inicio_inversion = "01/01/2024"  # Fecha de inicio
#---------------------------------------------------------------------------------------------

# Calcular cronograma
cronograma_inversionista_df, resumen_cronograma_inversionista_df = generar_cronograma_inversionista(monto_inversion, trea, num_desembolsos, tipo_desembolso, fecha_inicio_inversion)

# Mostrar resumen
print("\nResumen:")
print(resumen_cronograma_inversionista_df)

# Mostrar cronograma
print("Cronograma de desembolsos:")
print(cronograma_inversionista_df)


# Mostrar el cronograma como imagen
cronograma_a_imagen(cronograma_inversionista_df, resumen_cronograma_inversionista_df)

# Nombre del archivo
nombre_archivo = "Cronograma_Inversionista_prueba.xlsx"

# Exportar a Excel
exportar_a_excel(cronograma_inversionista_df, resumen_cronograma_inversionista_df, nombre_archivo)