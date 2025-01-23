import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import emoji
import base64

from io import BytesIO
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
from dotenv import load_dotenv
from datetime import datetime
from dateutil.relativedelta import relativedelta

#---------------------------------------------------------------------------------------------
# GENERAR EL CRONOGRAMA DE PAGOS DEL PRESTATARIO
#---------------------------------------------------------------------------------------------

def calcular_tna(tea):
    """
    Calcula la TNA (Tasa Nominal Anual) a partir de la TEA (Tasa Efectiva Anual).
    """
    return (((1 + tea) ** (1 / 12) - 1) * 12) * (365 / 360)

def calcular_cronograma(fecha_desembolso, importe_desembolsado, tea, td, p, nombre_cliente, tipo_garantia):
    """
    Genera el cronograma de pagos para un crédito efectivo.

    Parámetros:
    - fecha_desembolso (str): Fecha del desembolso en formato '%d/%m/%Y'.
    - importe_desembolsado (float): Monto del préstamo.
    - tea (float): Tasa efectiva anual (en formato decimal, ej. 0.35 para 35%).
    - td (float): Tasa de seguro desgravamen mensual (en formato decimal, ej. 0.00115).
    - p (int): Número de cuotas.
    - nombre_cliente (str): Nombre del cliente.
    - tipo_garantia (str): Tipo de garantía ofrecida.

    Retorna:
    - DataFrame con el cronograma de pagos.
    - DataFrame con el resumen del préstamo.
    """
    # Convertir la fecha de desembolso a un objeto datetime
    fecha_desembolso = datetime.strptime(fecha_desembolso, '%d/%m/%Y')

    # Calcular TNA
    tna = calcular_tna(tea)

    # Inicializar variables
    saldo = importe_desembolsado
    interes_acumulado = 0
    seguro_desgravamen_acumulado = 0
    cronograma = []

    # Calcular la cuota referencial (cuota constante)
    cuota_referencial = None

    for i in range(1, p + 1):
        # Calcular días del periodo
        if i == 1:
            dias_periodo = (fecha_desembolso + relativedelta(months=1) - fecha_desembolso).days + 1
        else:
            dias_periodo = (fecha_desembolso + relativedelta(months=i) - (fecha_desembolso + relativedelta(months=i - 1))).days

        # Calcular tasa ajustada al periodo (i)
        tasa_ajustada = (tna / 365) * dias_periodo

        # Calcular seguro de desgravamen ajustado al periodo (d)
        tda = td * 12
        tasa_seguro = (tda / 360) * dias_periodo

        # Si no se ha calculado la cuota referencial, calcularla
        if cuota_referencial is None:
            cuota_referencial = saldo * ((tasa_ajustada + tasa_seguro) / (1 - (1 + tasa_ajustada + tasa_seguro) ** -p))

        # Calcular interés mensual
        interes_mensual = saldo * tasa_ajustada

        # Calcular seguro de desgravamen mensual
        seguro_desgravamen_mensual = saldo * tasa_seguro

        # Calcular amortización mensual
        amortizacion_mensual = cuota_referencial - interes_mensual - seguro_desgravamen_mensual

        # Actualizar saldo
        saldo -= amortizacion_mensual

        # Actualizar acumulados
        interes_acumulado += interes_mensual
        seguro_desgravamen_acumulado += seguro_desgravamen_mensual

        # Agregar datos al cronograma
        cronograma.append({
            "N° Cuota": i,
            "Fecha de Pago": (fecha_desembolso + relativedelta(months=i)).strftime('%d/%m/%Y'),
            "Días del Periodo": dias_periodo,
            "Saldo (S/)": round(saldo if saldo > 0 else 0, 2),
            "Interés Mensual (S/)": round(interes_mensual, 2),
            "Seguro Desgravamen (S/)": round(seguro_desgravamen_mensual, 2),
            "Amortización (S/)": round(amortizacion_mensual, 2),
            "Cuota (S/)": round(cuota_referencial, 2)
        })
    
    # Calcular la fecha final del pago
    fecha_final_pago = (fecha_desembolso + relativedelta(months=p)).strftime('%d/%m/%Y')

    # Crear el resumen del préstamo
    resumen = {
        "Nombre del Cliente:": nombre_cliente,
        "Tipo de Garantía:": tipo_garantia,
        "Importe del Préstamo (S/):": round(importe_desembolsado, 2),
        "Intereses Totales (S/):": round(interes_acumulado, 2),
        "Importe Total a Pagar (S/):": round(cuota_referencial * p, 2),
        "Fecha del Préstamo:": fecha_desembolso.strftime('%d/%m/%Y'),
        "Fecha Final de Pago.": fecha_final_pago,
        "Cuotas por Pagar:": p,
        "Periodicidad:": "Mensual",
        "TEA (%):": round(tea * 100, 2)
    }

    # Convertir el cronograma a un DataFrame
    cronograma_prestatario_df = pd.DataFrame(cronograma)

    resumen_cronograma_prestatario_df = pd.DataFrame([resumen]).T
    resumen_cronograma_prestatario_df.columns = [""]
    
    return cronograma_prestatario_df, resumen_cronograma_prestatario_df

#---------------------------------------------------------------------------------------------

# CONVERTIR EL CRONOGRAMA EN IMAGEN

## Función para convertir el cronograma a una imagen:

def cronograma_a_imagen(cronograma_prestatario_df, resumen_cronograma_prestatario_df, total_intereses, p):
    """
    Convierte el cronograma a una imagen y la muestra con el resumen.
    """
    # Crear figura y ejes
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.axis('on')  # Mostrar los ejes

    # Mostrar el resumen primero
    ax.text(0.5, 0.95, "Resumen del Cronograma", fontsize=12, ha="center", va="top", weight="bold")
    tabla_resumen = ax.table(
        cellText=resumen_cronograma_prestatario_df.values,
        rowLabels=resumen_cronograma_prestatario_df.index,
        cellLoc='center',
        loc='center',
        bbox=[0.5, 0.7, 0.2, 0.2]  # [left, bottom, width, height]
    )
    tabla_resumen.auto_set_font_size(False)
    tabla_resumen.set_fontsize(10)
    tabla_resumen.scale(1.2, 1.2)

    # Eliminar bordes de las celdas en la tabla de resumen
    for key, cell in tabla_resumen.get_celld().items():
        cell.set_linewidth(0)  # Establecer el ancho del borde en 0

    # Mostrar el cronograma después
    ax.text(0.5, 0.65, "Cronograma de Pagos", fontsize=12, ha="center", va="center", weight="bold")
    tabla_cronograma = ax.table(
        cellText=cronograma_prestatario_df.values,
        colLabels=cronograma_prestatario_df.columns,
        cellLoc='center',
        loc='center',
        bbox=[0.1, 0.25, 0.8, 0.3]  # [left, bottom, width, height]
    )
    tabla_cronograma.auto_set_font_size(False)
    tabla_cronograma.set_fontsize(8)
    tabla_cronograma.scale(1.0, 1.0)
    
    # Agregar términos y condiciones en el pie de página
    terminos_condiciones = (
        f"- No incluye el ITF en caso de requerir.\n"
        f"- La tasa de interés es fija.\n"
        f"- Cargo por pago atrasado (S/): {round(total_intereses * 0.01 / p, 2)} por día.\n"
        f"- Máximo 7 días de espera después de vencida la cuota."
    )
    # Agregar los términos y condiciones al footer:
    plt.text(0.5, 0.05, terminos_condiciones, ha='center', va='center', fontsize=8, wrap=True)

    # Ajustar diseño
    plt.tight_layout()
    plt.show()

    # Guardar la imagen en un objeto BytesIO (para enviar por correo)

    image_buffer = BytesIO()
    plt.savefig(image_buffer, format='png', bbox_inches='tight')
    plt.close(fig)

    # Mover el puntero al inicio

    image_buffer.seek(0)

    return image_buffer

def exportar_a_excel(cronograma_prestatario_df, resumen_cronograma_prestatario_df, nombre_archivo):
    """
    Exporta el cronograma y el resumen a un archivo de Excel con el nombre especificado.
    """
    # Agregar la columna "Estado de la cuota" al cronograma
    cronograma_prestatario_df["Estado de la cuota"] = "Pendiente"

    with pd.ExcelWriter(nombre_archivo, engine='xlsxwriter') as writer:
        # Exportar el resumen al primer sheet
        resumen_cronograma_prestatario_df.to_excel(writer, sheet_name="Resumen", startrow=0, startcol=0, header=False)

        # Exportar el cronograma al segundo sheet
        cronograma_prestatario_df.to_excel(writer, sheet_name="Cronograma", index=False)

    print(f"Archivo Excel '{nombre_archivo}' generado exitosamente.")
#---------------------------------------------------------------------------------------------

# ENVIAR LA IMAGEN DEL CRONOGRAMA DE PAGOS POR CORREO (SENDGRID)

## Cargar variables de entorno desde el archivo .env

load_dotenv()

## Obtener la API key de SendGrid

sendgrid_api_key = os.getenv('SENDGRID_API_KEY')

print("API Key:", sendgrid_api_key)  # Para asegurarte de que se cargó correctamente

## Función para enviar el correo con la imagen adjunta

def enviar_correo_con_imagen(correo_destinatario,correo_destino, asunto, cuerpo, cronograma_cuotas_df, monto_prestamo, tasa_interes_anual, num_cuotas, fecha_inicio_prestamo, cuota_mensual, total_intereses, total_a_pagar, mostrar_imagen):

    ### Generar la imagen del cronograma

    imagen_buffer = cronograma_a_imagen(cronograma_cuotas_df, monto_prestamo, tasa_interes_anual, num_cuotas, fecha_inicio_prestamo, cuota_mensual, total_intereses, total_a_pagar, mostrar_imagen)

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


def mostrar_curva_interes(cronograma_prestatario_df):
    """
    Muestra la curva del interés a lo largo de las cuotas, asegurando que se muestren todas las cuotas en el eje X.
    """
    # Extraer los datos
    cuotas = cronograma_prestatario_df["N° Cuota"]
    intereses = cronograma_prestatario_df["Interés Mensual (S/)"]

    # Crear la figura y el eje
    plt.figure(figsize=(10, 6))
    plt.plot(cuotas, intereses, marker='o', label="Interés mensual (S/)", color='b')

    # Configurar el gráfico
    plt.title("Curva del Interés Mensual")
    plt.xlabel("N° de Cuota")
    plt.ylabel("Interés Mensual (S/)")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()

    # Configurar los ticks del eje X para mostrar todas las cuotas
    plt.xticks(ticks=cuotas, labels=cuotas, rotation=45)

    plt.tight_layout()

    # Mostrar la curva
    plt.show()

#---------------------------------------------------------------------------------------------

# LLAMADA A LAS FUNCIONES

# Generar el cronograma de pagos

# Datos de entrada
fecha_desembolso = "30/09/2024"
importe_desembolsado = 1500
tea = 1.4575
p = 4 #Número de cuotas
nombre_cliente = "Leonardo"
tipo_garantia = "Garantía Personal"
td = 0 # 0.00115 en los bancos

cronograma_prestatario_df, resumen_cronograma_prestatario_df = calcular_cronograma(fecha_desembolso, importe_desembolsado, tea, td, p, nombre_cliente, tipo_garantia)

# Mostrar el resumen del préstamo
print("Resumen del Préstamo:")
print(resumen_cronograma_prestatario_df)

# Mostrar el cronograma de pagos
print("\nCronograma de Pagos:")
print(cronograma_prestatario_df)

# Mostrar la imagen antes de enviar el correo
total_intereses = cronograma_prestatario_df["Interés Mensual (S/)"].sum()

cronograma_a_imagen(cronograma_prestatario_df, resumen_cronograma_prestatario_df,total_intereses, p)

# Nombre del archivo
nombre_archivo = "Cronograma_Prestatario_Prueba.xlsx"

# Exportar a Excel
exportar_a_excel(cronograma_prestatario_df,resumen_cronograma_prestatario_df, nombre_archivo)


# Enviar el correo con el cronograma como imagen adjunta

enviar_correo_con_imagen(

    correo_destinatario = 'prestamouniversal.pe@outlook.com',
    correo_destino = 'barbaragabriela2820@gmail.com',
    asunto = 'Cronograma de Pagos del Préstamo',
    cuerpo = '<p>Adjunto encontrarás el cronograma de pagos del préstamo solicitado.</p>',
    cronograma_df = cronograma_prestatario_df,
    monto_prestamo=monto_prestamo,
    tasa_interes_anual=tasa_interes_anual,
    num_cuotas=num_cuotas,
    fecha_inicio_prestamo=fecha_inicio_prestamo,
    cuota_mensual=cuota_mensual,
    total_intereses=total_intereses,
    total_a_pagar=total_a_pagar,
    mostrar_imagen=False

)


# Mostrar la curva del interés
mostrar_curva_interes(cronograma_prestatario_df)

