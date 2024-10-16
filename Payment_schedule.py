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
   
    ### Validaciones de los argumentos

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
    
    ### Calcular cuota mensual usando la fórmula de amortización

    cuotas = []

    cuota_mensual = (monto_prestamo * tasa_interes) / (1 - (1 + tasa_interes) ** -num_cuotas)

    saldo_pendiente = monto_prestamo

    for i in range(1, num_cuotas + 1): # num_cuotas iteraciones empezando en 1 y terminando en num_cuotas

        #### Cálculo del interés por cada periodo:

        interes = saldo_pendiente * tasa_interes

        #### Cálculo del capital amortiado

        capital_amortizado = cuota_mensual - interes

        #### Cálculo del saldo pendiente:

        saldo_pendiente -= capital_amortizado

        #### Fecha de pago de cada cuota

        fecha_pago = fecha_inicio + relativedelta(months = i)  # Sumar i meses a la fecha_inicio_prestamo

        #### Estructura del cronograma:

        cuotas.append({

            'Fecha de Pago': fecha_pago.strftime('%d-%m-%Y'),

            'Cuota': round(cuota_mensual, 2),

            'Interés': round(interes, 2),

            'Capital': round(capital_amortizado, 2),

            'Saldo Pendiente': round(saldo_pendiente if saldo_pendiente > 0 else 0, 2)  # Evitar saldo negativo al final
        })
    
    return pd.DataFrame(cuotas)

#---------------------------------------------------------------------------------------------

# CONVERTIR EL CRONOGRAMA EN IMAGEN

## Función para convertir el cronograma a una imagen:

def cronograma_a_imagen(cronograma_df):

    ### Crear una figura y ejes con matplotlib

    fig, ax = plt.subplots(figsize=(10, 6))

    ### Ocultar los ejes

    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_frame_on(False)

    ### Crear una tabla a partir del DataFrame y mostrarla

    tabla = ax.table(cellText=cronograma_df.values, colLabels=cronograma_df.columns, cellLoc='center', loc='center')

    ### Ajustar el tamaño de las celdas

    tabla.auto_set_font_size(False)
    tabla.set_fontsize(10)
    tabla.scale(1.2, 1.2)

    ### Guardar la imagen en un objeto BytesIO

    image_buffer = BytesIO()
    plt.savefig(image_buffer, format='png', bbox_inches='tight')
    plt.close(fig)
    
    ### Mover el puntero al inicio

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
def enviar_correo_con_imagen(correo_destino, asunto, cuerpo, cronograma_df):

    # Generar la imagen del cronograma
    imagen_buffer = cronograma_a_imagen(cronograma_df)

    # Convertir la imagen a base64
    encoded_image = base64.b64encode(imagen_buffer.getvalue()).decode()

    # Crear el cuerpo del mensaje

    if sendgrid_api_key is None:
        print("Error: No se pudo cargar la API Key.")
    else:   
        message = Mail(
            from_email='prestamouniversal.pe@outlook.com',
            to_emails=correo_destino,
            subject=asunto,
            html_content=cuerpo
        )

    # Crear el adjunto de imagen

    attachment = Attachment(
        FileContent(encoded_image),
        FileName('cronograma.png'),
        FileType('image/png'),
        Disposition('attachment')
    )

    # Adjuntar la imagen al correo

    message.add_attachment(attachment)

    # Enviar el correo usando SendGrid

    try:
        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(message)
        print(emoji.emojize(f"Correo enviado exitosamente con el estado: {response.status_code} :check_mark_button:"))
    except Exception as e:
        print(emoji.emojize(f"Error al enviar el correo: {e} :no_entry:"))

#---------------------------------------------------------------------------------------------

# Generar el cronograma de pagos

cronograma_df = generar_cronograma_prestatario(10000, 0.05, 12, '2024-10-31')

# Imprimir el cronograma de pagos

print(cronograma_df)

# Enviar el correo con el cronograma como imagen adjunta
enviar_correo_con_imagen(
    correo_destino='barbaragabriela2820@gmail.com',
    asunto='Cronograma de Pagos del Préstamo',
    cuerpo='<p>Adjunto encontrarás el cronograma de pagos del préstamo solicitado.</p>',
    cronograma_df=cronograma_df
)

