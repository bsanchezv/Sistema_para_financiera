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

def cronograma_desembolsos(monto, trea, num_desembolsos, tipo_desembolso, fecha_inicio_inversion):

    """
    Calcula el cronograma de desembolsos para un inversionista.
    """

    # Validaciones de entrada
    if monto <= 0:
        raise ValueError("El monto debe ser mayor a 0.")
    if trea <= 0:
        raise ValueError("La TREA debe ser mayor a 0.")
    if num_desembolsos <= 0 or not isinstance(num_desembolsos, int):
        raise ValueError("El número de desembolsos debe ser un entero positivo.")
    if tipo_desembolso not in ["único", "mensual"]:
        raise ValueError("El tipo de desembolso debe ser 'único' o 'mensual'.")
    
    # Calcular la TREM
    trem = calcular_trem(trea)

    # Convertir fecha de inicio a objeto datetime
    fecha_inicio = datetime.strptime(fecha_inicio_inversion, '%d/%m/%Y')

    # Inicializar variables
    capital = monto
    interes_acumulado = 0
    cronograma = []

    # Caso de desembolso único
    if tipo_desembolso == "único":
        for i in range(1, num_desembolsos + 1):
            # Calcular interés mensual
            interes_mensual = capital * trem

            # Acumular el interés
            interes_acumulado += interes_mensual

            # Actualizar el dinero acumulado
            dinero_acumulado = capital + interes_mensual

            # Agregar al cronograma
            cronograma.append({
                "N°": i,
                "Fecha": (fecha_inicio + relativedelta(months=i)).strftime('%d/%m/%Y'),
                "Capital (S/)": round(capital, 2),
                "Interés mensual (S/)": round(interes_mensual, 2),
                "Interés acumulado mensual (S/)": round(interes_acumulado, 2),
                "Dinero acumulado mensual (S/)": round(dinero_acumulado, 2)
            })

            # Actualizar capital
            capital = dinero_acumulado

        # Resumen
        resumen = {
            "N° Desembolso": num_desembolsos,
            "Fecha de pago (S/)": cronograma[-1]["Fecha"],
            "Interés total (S/)": round(interes_acumulado, 2),
            "Monto final acumulado (S/)": round(dinero_acumulado, 2)
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

            # Agregar al cronograma
            cronograma.append({
                "N° Desembolso": i,
                "Fecha de pago": (fecha_inicio + relativedelta(months=i)).strftime('%d/%m/%Y'),
                "Capital (S/)": round(dinero_acumulado - interes_mensual, 2),
                "Interés mensual (S/)": round(interes_mensual, 2),
                "Interés acumulado mensual (S/)": round(interes_acumulado, 2),
                "Dinero acumulado mensual (S/)": round(dinero_acumulado, 2),
                "Desembolso (S/)": round(desembolso, 2)
            })

        # Resumen
        resumen = {
            "N° de desembolsos": num_desembolsos,
            "Fecha final de pago": cronograma[-1]["Fecha de pago"],
            "Interés total (S/)": round(interes_acumulado, 2),
            "Monto final acumulado (S/)": round(sum([row["Desembolso (S/)"] for row in cronograma]), 2)
        }


    return pd.DataFrame(cronograma), pd.DataFrame([resumen])

def cronograma_a_imagen(cronograma_df, resumen):
    """
    Convierte el cronograma a una imagen y la muestra con el resumen.
    """
    # Crear figura
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.axis('off')  # Ocultar los ejes

    # Mostrar el resumen primero
    ax.text(0.5, 0.9, "Resumen del Cronograma", fontsize=14, ha="center", va="top", weight="bold")
    tabla_resumen = ax.table(cellText=resumen.values, colLabels=resumen.columns, cellLoc='center', loc='center', bbox=[0, 0.7, 1, 0.15])
    tabla_resumen.auto_set_font_size(False)
    tabla_resumen.set_fontsize(10)
    tabla_resumen.scale(1.2, 1.2)

     # Mostrar el cronograma después
    ax.text(0.5, 0.6, "Cronograma de Desembolsos", fontsize=14, ha="center", va="top", weight="bold")
    tabla_cronograma = ax.table(cellText=cronograma_df.values, colLabels=cronograma_df.columns, cellLoc='center', loc='center', bbox=[0, 0, 1, 0.6])
    tabla_cronograma.auto_set_font_size(False)
    tabla_cronograma.set_fontsize(8)
    tabla_cronograma.scale(1.0, 1.0)


    # Mostrar la imagen
    plt.show()

# Ejemplo de uso
monto = 1000  # Monto invertido
trea = 0.1  # TREA en decimal
num_desembolsos = 4  # Número de desembolsos
tipo_desembolso = "mensual"  # Tipo de desembolso ("único" o "mensual")
fecha_inicio_inversion = "01/01/2024"  # Fecha de inicio

# Calcular cronograma
cronograma_df, resumen = cronograma_desembolsos(monto, trea, num_desembolsos, tipo_desembolso, fecha_inicio_inversion)

# Mostrar cronograma
print("Cronograma de desembolsos:")
print(cronograma_df)

# Mostrar resumen
print("\nResumen:")

print(resumen)


# Mostrar el cronograma como imagen
cronograma_a_imagen(cronograma_df, resumen)