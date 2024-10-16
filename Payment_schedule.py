import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta


# Definir función para calcular el cronograma de cuotas del prestatario

def generar_cronograma_prestatario(monto_prestamo, tasa_interes, num_cuotas, fecha_inicio_prestamo):
   
    ## Validaciones de los argumentos

    if not (isinstance(monto_prestamo, (int, float)) and monto_prestamo > 0):
        raise ValueError("El monto debe ser un número positivo.")
    if not (0 <= tasa_interes <= 1):
        raise ValueError("La tasa de interés debe ser un número entre 0 y 1.")
    if not (isinstance(num_cuotas, int) and num_cuotas > 0):
        raise ValueError("El número de cuotas debe ser un entero positivo.")
    
    try:
        fecha_inicio = datetime.strptime(fecha_inicio_prestamo, '%Y-%m-%d') # string parse time
    except ValueError as e:
        raise ValueError(f"La fecha de inicio del préstamo no tiene el formato correcto (YYYY-MM-DD): {e}")

    cuotas = []

    ## Calcular cuota mensual usando la fórmula de amortización

    cuota_mensual = (monto_prestamo * tasa_interes) / (1 - (1 + tasa_interes) ** -num_cuotas)

    saldo_pendiente = monto_prestamo

    for i in range(1, num_cuotas + 1): # num_cuotas iteraciones empezando en 1 y terminando en num_cuotas

        ### Fecha de pago de cada cuota

        fecha_pago = fecha_inicio + relativedelta(months = i)  # Sumar i meses a la fecha_inicio_prestamo

        ### Cálculo del interés por cada periodo:

        interes = saldo_pendiente * tasa_interes

        #### Cálculo del capital amortiado

        capital_amortizado = cuota_mensual - interes

        ### Cálculo del saldo pendiente:

        saldo_pendiente -= capital_amortizado

        ### Estructura del cronograma:

        cuotas.append({

            'Fecha de Pago': fecha_pago.strftime('%d-%m-%Y'),

            'Cuota': round(cuota_mensual, 2),

            'Interés': round(interes, 2),

            'Capital': round(capital_amortizado, 2),

            'Saldo Pendiente': round(saldo_pendiente if saldo_pendiente > 0 else 0, 2)  # Evitar saldo negativo al final
        })
    
    return pd.DataFrame(cuotas)

# Generar el cronograma
cronograma_df = generar_cronograma_prestatario(10000, 0.05, 12, '2024-10-31')

# Mostrar el cronograma
print(cronograma_df)

# Exportar a Excel
cronograma_df.to_excel('cronograma_prestamo.xlsx', index=False)


import yagmail

def enviar_correo(destinatario, asunto, cuerpo, adjuntos):
    yag = yagmail.SMTP("barbaragabriela2820@gmail.com", "")
    yag.send(to=destinatario, subject=asunto, contents=cuerpo, attachments=adjuntos)

# Ejemplo de uso
enviar_correo("destinatario@correo.com", "Cronograma de Préstamo", "Adjunto el cronograma de tu préstamo.", ["cronograma_prestamo.xlsx", "cronograma_prestamo.pdf"])
