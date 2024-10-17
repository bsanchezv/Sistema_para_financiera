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

    total_intereses = 0

    for i in range(1, num_cuotas + 1): # num_cuotas iteraciones empezando en 1 y terminando en num_cuotas

        #### Cálculo del interés por cada periodo:

        interes = saldo_pendiente * tasa_interes

        #### Cálculo del capital amortiado

        capital_amortizado = cuota_mensual - interes

        #### Cálculo del saldo pendiente:

        saldo_pendiente -= capital_amortizado

        #### Cálculo del total de intereses:
        
        total_intereses += interes

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
    
    cronograma_df = pd.DataFrame(cuotas)

    total_a_pagar = round(cuota_mensual * num_cuotas, 2)

    return cronograma_df, round(cuota_mensual, 2), round(total_intereses, 2), total_a_pagar

#---------------------------------------------------------------------------------------------

# CONVERTIR EL CRONOGRAMA EN IMAGEN

## Función para convertir el cronograma a una imagen:

def cronograma_a_imagen(cronograma_df, monto_prestamo, tasa_interes, num_cuotas, fecha_inicio_prestamo, cuota_mensual, total_intereses, total_a_pagar, mostrar_imagen):

    ### Crear una figura y ejes con matplotlib

    fig, ax = plt.subplots(figsize=(10, 9))

    ### Ocultar los ejes

    ax.xaxis.set_visible(True)
    ax.yaxis.set_visible(True)
    ax.set_frame_on(True)

    ### Crear una tabla a partir del DataFrame y mostrarla

    tabla = ax.table(cellText=cronograma_df.values, colLabels=cronograma_df.columns, cellLoc='center', loc='center', bbox=[0, 0.2, 1, 0.5])

    ### Ajustar el tamaño de las celdas

    tabla.auto_set_font_size(False)
    tabla.set_fontsize(10)
    tabla.scale(1.2, 1.2)

    ### Estructura de la cabecera:

    resumen = f"""
    Monto del préstamo: {monto_prestamo} 
    Interés mensual: {round(tasa_interes * 100, 2)}% 
    Fecha de préstamo: {fecha_inicio_prestamo} 
    Frecuencia de pago: Mensual
    Cantidad de cuotas: {num_cuotas} 
    Cuota: {cuota_mensual} 
    Total intereses: {total_intereses} 
    Total a pagar: {total_a_pagar}
    \n
    CRONOGRAMA DE PAGOS:
    """

    ### Agregar la cabecera del resumen en la parte superior

    ax.text(0.5, 1, resumen, ha='center', va='top', fontsize=10, transform=ax.transAxes)

    ### Estructura de los términos y condiciones
    terminos_condiciones = f"""
    - No incluye el ITF en caso de requerir.
    - La tasa de interés es fija.
    - Cargo por pago atrasado: {round(total_intereses * 0.01 / num_cuotas, 2)} por día.
    - Máximo 7 días de espera después de vencida la cuota.
    """

    ### Agregar los términos y condiciones al footer:

    ax.text(0.5, 0.15, terminos_condiciones, ha='center', va='top', fontsize=10, transform=ax.transAxes)

    # Mostrar la imagen directamente

    if mostrar_imagen:

        # Mostrar la imagen directamente

        plt.show()

    else:

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

def enviar_correo_con_imagen(correo_destinatario,correo_destino, asunto, cuerpo, cronograma_df, monto_prestamo, tasa_interes, num_cuotas, fecha_inicio_prestamo, cuota_mensual, total_intereses, total_a_pagar, mostrar_imagen):

    ### Generar la imagen del cronograma

    imagen_buffer = cronograma_a_imagen(cronograma_df, monto_prestamo, tasa_interes, num_cuotas, fecha_inicio_prestamo, cuota_mensual, total_intereses, total_a_pagar, mostrar_imagen)

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

monto_prestamo = 10000
tasa_interes = 0.05
num_cuotas = 12
fecha_inicio_prestamo = '2024-10-31'

cronograma_df, cuota_mensual, total_intereses, total_a_pagar = generar_cronograma_prestatario(monto_prestamo, tasa_interes, num_cuotas, fecha_inicio_prestamo)

# Imprimir el cronograma de pagos

print(cronograma_df)

# Mostrar la imagen antes de enviar el correo

cronograma_a_imagen(

    cronograma_df=cronograma_df,
    monto_prestamo=monto_prestamo,
    tasa_interes=tasa_interes,
    num_cuotas=num_cuotas,
    fecha_inicio_prestamo=fecha_inicio_prestamo,
    cuota_mensual=cuota_mensual,
    total_intereses=total_intereses,
    total_a_pagar=total_a_pagar,
    mostrar_imagen = False #Cambiar si se quiere mostrar o no
)

# Enviar el correo con el cronograma como imagen adjunta

enviar_correo_con_imagen(

    correo_destinatario = 'prestamouniversal.pe@outlook.com',
    correo_destino = 'barbaragabriela2820@gmail.com',
    asunto = 'Cronograma de Pagos del Préstamo',
    cuerpo = '<p>Adjunto encontrarás el cronograma de pagos del préstamo solicitado.</p>',
    cronograma_df = cronograma_df,
    monto_prestamo=monto_prestamo,
    tasa_interes=tasa_interes,
    num_cuotas=num_cuotas,
    fecha_inicio_prestamo=fecha_inicio_prestamo,
    cuota_mensual=cuota_mensual,
    total_intereses=total_intereses,
    total_a_pagar=total_a_pagar,
    mostrar_imagen=False

)
