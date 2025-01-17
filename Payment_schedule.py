import os
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
from dotenv import load_dotenv
from datetime import datetime
from dateutil.relativedelta import relativedelta
import emoji

#---------------------------------------------------------------------------------------------

# GENERAR EL CRONOGRAMA DE PAGOS DEL PRESTATARIO

## Función para calcular el cronograma de cuotas del prestatario

def generar_cronograma_prestatario(monto_prestamo, tasa_interes, num_cuotas, fecha_inicio_prestamo):
    """
    Genera el cronograma de pagos para un prestatario.
    """

    if not (isinstance(monto_prestamo, (int, float)) and monto_prestamo >= 0):
        raise ValueError("El monto debe ser mayor a 0.")
    
    if not (0 < tasa_interes <= 1):
        raise ValueError("La tasa de interés debe er un número mayor a 0 y menor a 1.")
    
    if not (isinstance(num_cuotas, int) and num_cuotas > 0):
        raise ValueError("El número de cuotas debe ser un entero positivo.")
    
    try:
        fecha_inicio = datetime.strptime(fecha_inicio_prestamo, '%Y-%m-%d') # string parse time
    except ValueError as e:
        raise ValueError(f"La fecha de inicio del préstamo no tiene el formato correcto (YYYY-MM-DD): {e}")
    
    ### Calcular cuota mensual usando la fórmula de amortización

    cronograma_prestatario = []

    cuota_mensual = (monto_prestamo * tasa_interes) / (1 - (1 + tasa_interes) ** -num_cuotas)

    saldo_pendiente = monto_prestamo

    total_intereses = 0

    for i in range(1, num_cuotas + 1): # num_cuotas iteraciones empezando en 1 y terminando en num_cuotas

        #### Cálculo del interés por cada periodo:
        interes_mensual = saldo_pendiente * tasa_interes

        #### Cálculo del capital amortiado
        capital_amortizado = cuota_mensual - interes_mensual

        #### Cálculo del saldo pendiente:
        saldo_pendiente -= capital_amortizado

        #### Cálculo del total de intereses:
        total_intereses += interes_mensual

        #### Fecha de pago de cada cuota
        fecha_pago = fecha_inicio + relativedelta(months = i)  # Sumar i meses a la fecha_inicio_prestamo

        #### Estructura del cronograma:
        cronograma_prestatario.append({

            'Fecha de Pago': fecha_pago.strftime('%d/%m/%Y'),
            'Cuota (S/)': round(cuota_mensual, 2),
            'Interés (S/)': round(interes_mensual, 2),
            'Capital (S/)': round(capital_amortizado, 2),
            'Saldo Pendiente (S/)': round(saldo_pendiente if saldo_pendiente > 0 else 0, 2)  # Evitar saldo negativo al final
        })

    # Resumen
    resumen_cronograma_prestatario = {
        "Monto del préstamo (S/)": monto_prestamo,
        "Tasa de interés (%)": round(tasa_interes * 100, 2),
        "Fecha de préstamo": fecha_inicio.strftime('%d/%m/%Y'),
        "Frecuencia de pago": 'Mensual',
        "Cantidad de cuotas": num_cuotas,
        "Total Intereses (S/)": round(total_intereses ,2),
        "Total a Pagar (S/)": round(cuota_mensual * num_cuotas, 2)
    }

    return pd.DataFrame(cronograma_prestatario), pd.DataFrame([resumen_cronograma_prestatario])

#---------------------------------------------------------------------------------------------

# CONVERTIR EL CRONOGRAMA EN IMAGEN

## Función para convertir el cronograma a una imagen:

def cronograma_a_imagen(cronograma_prestatario_df, resumen_cronograma_prestatario_df, total_intereses, num_cuotas):

    """
    Convierte el cronograma a una imagen y la muestra con el resumen.
    """
    # Crear figura y ejes
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.axis('on')  # Ocultar los ejes en off

    # Mostrar el resumen primero
    ax.text(0.5, 0.97, "Resumen del Cronograma", fontsize=14, ha="center", va="center", weight="bold")
    tabla_resumen = ax.table(
        cellText=resumen_cronograma_prestatario_df.values,
        colLabels=resumen_cronograma_prestatario_df.columns,
        cellLoc='center',
        loc='center',
        bbox=[0.1, 0.75, 0.8, 0.2]  # [left, bottom, width, height]
    )
    tabla_resumen.auto_set_font_size(False)
    tabla_resumen.set_fontsize(10)
    tabla_resumen.scale(1.2, 1.2)

    # Mostrar el cronograma después
    ax.text(0.5, 0.72, "Cronograma de Pagos", fontsize=14, ha="center", va="center", weight="bold")
    tabla_cronograma = ax.table(
        cellText=cronograma_prestatario_df.values,
        colLabels=cronograma_prestatario_df.columns,
        cellLoc='center',
        loc='center',
        bbox=[0.1, 0.2, 0.8, 0.5]  # [left, bottom, width, height]
    )
    tabla_cronograma.auto_set_font_size(False)
    tabla_cronograma.set_fontsize(8)
    tabla_cronograma.scale(1.0, 1.0)
    
    # Agregar términos y condiciones en el pie de página
    terminos_condiciones = (
        f"- No incluye el ITF en caso de requerir.\n"
        f"- La tasa de interés es fija.\n"
        f"- Cargo por pago atrasado (S/): {round(total_intereses * 0.01 / num_cuotas, 2)} por día.\n"
        f"- Máximo 7 días de espera después de vencida la cuota."
    )
    ### Agregar los términos y condiciones al footer:
    ax.text(0.5, 0.05, terminos_condiciones, ha='center', va='center', fontsize=10, wrap=True)

    # Mostrar la imagen directamente
    plt.tight_layout()
    plt.show()

    # Guardar la imagen en un objeto BytesIO (para enviar por correo)

    image_buffer = BytesIO()
    plt.savefig(image_buffer, format='png', bbox_inches='tight')
    plt.close(fig)

    # Mover el puntero al inicio

    image_buffer.seek(0)

    return image_buffer

#---------------------------------------------------------------------------------------------

# ENVIAR LA IMAGEN DEL CRONOGRAMA DE PAGOS POR CORREO (SENDGRID)

## Cargar variables de entorno desde el archivo .env

load_dotenv()

## Obtener la API key de SendGrid

sendgrid_api_key = os.getenv('SENDGRID_API_KEY')

print("API Key:", sendgrid_api_key)  # Para asegurarte de que se cargó correctamente

## Función para enviar el correo con la imagen adjunta

def enviar_correo_con_imagen(correo_destinatario,correo_destino, asunto, cuerpo, cronograma_cuotas_df, monto_prestamo, tasa_interes, num_cuotas, fecha_inicio_prestamo, cuota_mensual, total_intereses, total_a_pagar, mostrar_imagen):

    ### Generar la imagen del cronograma

    imagen_buffer = cronograma_a_imagen(cronograma_cuotas_df, monto_prestamo, tasa_interes, num_cuotas, fecha_inicio_prestamo, cuota_mensual, total_intereses, total_a_pagar, mostrar_imagen)

    ### Convertir la imagen a base64

    encoded_image = base64.b64encode(imagen_buffer.getvalue()).decode()

    ### Crear el cuerpo del mensaje

    if sendgrid_api_key is None:
        print("Error: No se pudo cargar la API Key.")
    else:   
        message = Mail(
            from_email=correo_destinatario,
            to_emails=correo_destino,
            subject=asunto,
            html_content=cuerpo
        )

    ### Crear el adjunto de imagen

    attachment = Attachment(
        FileContent(encoded_image),
        FileName('cronograma.png'),
        FileType('image/png'),
        Disposition('attachment')
    )

    ### Adjuntar la imagen al correo

    message.add_attachment(attachment)

    ### Enviar el correo usando SendGrid

    try:
        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(message)
        print(emoji.emojize(f"Correo enviado exitosamente con el estado: {response.status_code} :check_mark_button:"))
    except Exception as e:
        print(emoji.emojize(f"Error al enviar el correo: {e} :no_entry:"))

#---------------------------------------------------------------------------------------------

# LLAMADA A LAS FUNCIONES

# Generar el cronograma de pagos

# Ejemplo de uso
monto_prestamo = 10000  # Monto del préstamo
tasa_interes = 0.05  # Tasa de interés (5%)
num_cuotas = 12  # Número de cuotas
fecha_inicio_prestamo = "2024-01-01"  # Fecha de inicio del préstamo

# Generar cronograma y resumen
cronograma_prestatario_df, resumen_cronograma_prestatario_df = generar_cronograma_prestatario(monto_prestamo, tasa_interes, num_cuotas, fecha_inicio_prestamo)

# Imprimir el cronograma de pagos

print(cronograma_prestatario_df)
print(resumen_cronograma_prestatario_df)


# Mostrar la imagen antes de enviar el correo

cronograma_a_imagen(cronograma_prestatario_df, resumen_cronograma_prestatario_df, resumen_cronograma_prestatario_df["Total Intereses (S/)"][0], num_cuotas)

# Enviar el correo con el cronograma como imagen adjunta

enviar_correo_con_imagen(

    correo_destinatario = 'prestamouniversal.pe@outlook.com',
    correo_destino = 'barbaragabriela2820@gmail.com',
    asunto = 'Cronograma de Pagos del Préstamo',
    cuerpo = '<p>Adjunto encontrarás el cronograma de pagos del préstamo solicitado.</p>',
    cronograma_df = cronograma_prestatario_df,
    monto_prestamo=monto_prestamo,
    tasa_interes=tasa_interes,
    num_cuotas=num_cuotas,
    fecha_inicio_prestamo=fecha_inicio_prestamo,
    cuota_mensual=cuota_mensual,
    total_intereses=total_intereses,
    total_a_pagar=total_a_pagar,
    mostrar_imagen=False

)
