import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import emoji
import base64

#from io import BytesIO
#from sendgrid import SendGridAPIClient
#from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
from dotenv import load_dotenv
from datetime import datetime
from dateutil.relativedelta import relativedelta

#---------------------------------------------------------------------------------------------
# GENERAR EL CRONOGRAMA DE PAGOS DEL PRESTATARIO
#---------------------------------------------------------------------------------------------
def calcular_tea(tasa_referencial, inflacion, id_cat_cliente, tipo_garantia, score_crediticio, importe_desembolsado, p, id_profesion, edad):

    # Ajuste por tasa referencial
    ajuste_tasa_referencial = tasa_referencial

    # Ajuste por inflación
    ajuste_inflacion = inflacion  

    # Ajuste por categoría del cliente
    if id_cat_cliente == 11:  # Categoría F
        raise ValueError("El cliente tiene más de 4 atrasos y no puede generar un préstamo hasta que termine el semestre actual.")
    elif id_cat_cliente == 10:  # Categoría D
        ajuste_categoria = 0.9171
    elif id_cat_cliente == 9:  # Categoría D+
        ajuste_categoria = 0.8165
    elif id_cat_cliente == 8:  # Categoría C-
        ajuste_categoria = 0.7159
    elif id_cat_cliente == 7:  # Categoría C
        ajuste_categoria = 0.6153
    elif id_cat_cliente == 6:  # Categoría C+
        ajuste_categoria = 0.5147
    elif id_cat_cliente == 5:  # Categoría B-
        ajuste_categoria = 0.4140
    elif id_cat_cliente == 4:  # Categoría B
        ajuste_categoria = 0.3134
    elif id_cat_cliente == 3:  # Categoría B+
        ajuste_categoria = 0.2128
    elif id_cat_cliente == 2:  # Categoría A-
        ajuste_categoria = 0.1122
    else:  # Categoría A
        ajuste_categoria = 0.0116

    # Ajuste por score crediticio
    if 979 <= score_crediticio <= 1000:
        ajuste_score = 0.0116
    elif 924 <= score_crediticio < 979:
        ajuste_score = 0.2380
    elif 900 <= score_crediticio < 924:
        ajuste_score = 0.4644
    elif 675 <= score_crediticio < 900:
        ajuste_score = 0.6907
    else:
        ajuste_score = 0.9171

    # Ajuste por monto del préstamo
    if importe_desembolsado > 10352:
        ajuste_monto = 0.0116
    elif 9955 <= importe_desembolsado < 10352:
        ajuste_monto = 0.0464
    elif 9558 <= importe_desembolsado < 9955:
        ajuste_monto = 0.0813
    elif 9161 <= importe_desembolsado < 9558:
        ajuste_monto = 0.1161
    elif 8764 <= importe_desembolsado < 9161:
        ajuste_monto = 0.1509
    elif 8367 <= importe_desembolsado < 8764:
        ajuste_monto = 0.1857
    elif 7970 <= importe_desembolsado < 8367:
        ajuste_monto = 0.2206
    elif 7573 <= importe_desembolsado < 7970:
        ajuste_monto = 0.2554
    elif 7176 <= importe_desembolsado < 7573:
        ajuste_monto = 0.2902
    elif 6779 <= importe_desembolsado < 7176:
        ajuste_monto = 0.3250
    elif 6382 <= importe_desembolsado < 6779:
        ajuste_monto = 0.3599
    elif 5985 <= importe_desembolsado < 6382:
        ajuste_monto = 0.3947
    elif 5588 <= importe_desembolsado < 5985:
        ajuste_monto = 0.4295
    elif 5191 <= importe_desembolsado < 5588:
        ajuste_monto = 0.4644
    elif 4794 <= importe_desembolsado < 5191:
        ajuste_monto = 0.4992
    elif 4397 <= importe_desembolsado < 4794:
        ajuste_monto = 0.5340
    elif 4000 <= importe_desembolsado < 4397:
        ajuste_monto = 0.5688
    elif 3603 <= importe_desembolsado < 4000:
        ajuste_monto = 0.6037
    elif 3206 <= importe_desembolsado < 3603:
        ajuste_monto = 0.6385
    elif 2809 <= importe_desembolsado < 3206:
        ajuste_monto = 0.6733
    elif 2412 <= importe_desembolsado < 2809:
        ajuste_monto = 0.7081
    elif 2015 <= importe_desembolsado < 2412:
        ajuste_monto = 0.7430
    elif 1618 <= importe_desembolsado < 2015:
        ajuste_monto = 0.7778
    elif 1221 <= importe_desembolsado < 1618:
        ajuste_monto = 0.8126
    elif 824 <= importe_desembolsado < 1221:
        ajuste_monto = 0.8474
    elif 427 <= importe_desembolsado < 824:
        ajuste_monto = 0.8823
    elif 100 <= importe_desembolsado < 427:
        ajuste_monto = 0.9171
    else:  # 0.01 <= importe_desembolsado < 30
        raise ValueError("El monto debe ser mayor o igual a S/100.")

    # Ajuste por número de cuotas
    if 1 <= p < 2:
        ajuste_cuotas = 0.0116
    elif 2 <= p < 3:
        ajuste_cuotas = 0.0464
    elif 3 <= p < 4:
        ajuste_cuotas = 0.0813
    elif 4 <= p < 5:
        ajuste_cuotas = 0.1161
    elif 5 <= p < 7:
        ajuste_cuotas = 0.1509
    elif 7 <= p < 8:
        ajuste_cuotas = 0.1857
    elif 8 <= p < 9:
        ajuste_cuotas = 0.2206
    elif 9 <= p < 10:
        ajuste_cuotas = 0.2554
    elif 10 <= p < 11:
        ajuste_cuotas = 0.2902
    elif 11 <= p < 12:
        ajuste_cuotas = 0.32050
    elif 12 <= p < 13:
        ajuste_cuotas = 0.3599
    elif 13 <= p < 14:
        ajuste_cuotas = 0.3947
    elif 14 <= p < 15:
        ajuste_cuotas = 0.4295
    elif 15 <= p < 16:
        ajuste_cuotas = 0.4644
    elif 16 <= p < 18:
        ajuste_cuotas = 0.4992
    elif 18 <= p < 19:
        ajuste_cuotas = 0.5340
    elif 19 <= p < 20:
        ajuste_cuotas = 0.5688
    elif 20 <= p < 21:
        ajuste_cuotas = 0.6037
    elif 21 <= p < 22:
        ajuste_cuotas = 0.6385
    elif 22 <= p < 23:
        ajuste_cuotas = 0.6733
    elif 23 <= p < 24:
        ajuste_cuotas = 0.7081
    elif 24 <= p < 25:
        ajuste_cuotas = 0.7430
    elif 25 <= p < 26:
        ajuste_cuotas = 0.7778
    elif 26 <= p < 27:
        ajuste_cuotas = 0.8126
    elif 27 <= p < 29:
        ajuste_cuotas = 0.8474
    elif 29 <= p < 30:
        ajuste_cuotas = 0.8823
    elif 30 <= p < 31:
        ajuste_cuotas = 0.9171
    else:
        raise ValueError("El número de cuotas está fuera del rango permitido.")

    # Ajuste por edad
    if 18 <= edad < 24:
        ajuste_edad = 0.4644
    elif 24 <= edad < 51:
        ajuste_edad = 0.0116
    elif 51 <= edad < 65:
        ajuste_edad = 0.9171
    else:
        raise ValueError("La edad del cliente está fuera del rango permitido.")

    # Ajuste por profesión
    if id_profesion in ["medico", "ingeniero", "empleado_publico"]:
        ajuste_profesion = 0.0116
    elif id_profesion in ["comerciante", "emprendedor"]:
        ajuste_profesion = 0.4644
    else:
        ajuste_profesion = 0.9171


    # Ajuste por garantía ofrecida
    if tipo_garantia == "Garantía Material":
        ajuste_garantia = 0.0116
    elif tipo_garantia == "Garantía Personal":
        ajuste_garantia = 0.4644
    else:  # Sin garantía
        ajuste_garantia = 0.9171

    # Calcular la tasa final
    tea = (
        ajuste_tasa_referencial * 1
        + ajuste_inflacion * 2
        + ajuste_categoria * 1.000
        + ajuste_garantia * 0.8571
        + ajuste_score * 0.7143
        + ajuste_monto * 0.5714
        + ajuste_cuotas * 0.4286
        + ajuste_profesion * 0.2857
        + ajuste_edad * 0.1429
    )

    return round(tea, 4)

def calcular_tna(tea):
    """
    Calcula la TNA (Tasa Nominal Anual) a partir de la TEA (Tasa Efectiva Anual).
    """
    tea = calcular_tea(tasa_referencial, inflacion, id_cat_cliente, tipo_garantia, score_crediticio, importe_desembolsado, p, id_profesion, edad)
    tna = (((1 + tea) ** (1 / 12) - 1) * 12) * (365 / 360)
    return tna

def calcular_cronograma(fecha_desembolso, importe_desembolsado, tea, td, p, nombre_cliente, tipo_garantia, dias_periodo, dias_mes):
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
    - dias_periodo (int): Número de días del período.
    - dias_mes (int): Número de días del mes.

    Retorna:
    - DataFrame con el cronograma de pagos.
    - DataFrame con el resumen del préstamo.
    """
    # Convertir la fecha de desembolso a un objeto datetime
    fecha_desembolso = datetime.strptime(fecha_desembolso, '%d/%m/%Y')

    # Definir saldo inicial
    saldo = importe_desembolsado

    # 1. Calcular la tasa nominal
    tna = calcular_tna(tea)

    # 2. Calcular la tasa ajustada al plazo
    tasa_ajustada = (tna / 365) * dias_periodo

    # 4. Calcular la TDA (tasa de seguro de desgravamen anual)
    tda = td * 12

    # 5. Calcular la tasa ajustada al plazo para el seguro de desgravamen (d)
    tasa_seguro = (tda / 360) * dias_mes

    # 3. Calcular el interés mensual
    interes_mensual = saldo * tasa_ajustada

    # 7. Calcular la cuota referencial (usando la fórmula de cuota constante)
    cuota_referencial = saldo * ((tasa_ajustada + tasa_seguro) / (1 - (1 + tasa_ajustada + tasa_seguro) ** (-p)))

    # Inicializar variables para el cronograma:
    interes_acumulado = 0
    seguro_desgravamen_acumulado = 0
    cronograma = []

    for i in range(1, p + 1):
        
        # 1. Calcular interés mensual
        interes_mensual = saldo * tasa_ajustada

        # 2. Calcular seguro de desgravamen mensual
        seguro_desgravamen_mensual = saldo * tasa_seguro

        # 3. Calcular amortización mensual
        amortizacion_mensual = cuota_referencial - (interes_mensual + seguro_desgravamen_mensual)

        # Evitar saldo negativo en la última cuota
        if saldo - amortizacion_mensual < 0:
            amortizacion_mensual = saldo
        
        # 4. Actualizar saldo
        saldo -= amortizacion_mensual

        # 5. Actualizar acumulados
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

def cronograma_a_imagen(cronograma_prestatario_df, resumen_cronograma_prestatario_df, total_intereses):
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
        bbox=[0.1, 0.25, 0.8, 0.1]  # [left, bottom, width, height]
    )
    tabla_cronograma.auto_set_font_size(False)
    tabla_cronograma.set_fontsize(10)
    tabla_cronograma.scale(1.2, 1.2)
    
    # Agregar términos y condiciones en el pie de página
    terminos_condiciones = (
        f"- No incluye el ITF en caso de requerir.\n"
        f"- La tasa de interés es fija.\n"
        f"- Cargo por pago atrasado (S/): {round(total_intereses * 0.033, 2)} por día.\n"
        f"- Máximo 7 días de espera después de vencida la cuota."
    )
    # Agregar los términos y condiciones al footer:
    plt.text(0.5, 0.07, terminos_condiciones, ha='center', va='center', fontsize=9, wrap=True)

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

def enviar_correo_con_imagen(correo_destinatario,correo_destino, asunto, cuerpo, cronograma_cuotas_df, importe_desembolsado, tasa_interes_anual, p, fecha_inicio_prestamo, cuota_mensual, total_intereses, total_a_pagar, mostrar_imagen):

    ### Generar la imagen del cronograma

    imagen_buffer = cronograma_a_imagen(cronograma_cuotas_df, importe_desembolsado, tasa_interes_anual, p, fecha_inicio_prestamo, cuota_mensual, total_intereses, total_a_pagar, mostrar_imagen)

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

# DATOS DE ENTRADA
# Datos del prestatario:
nombre_cliente = "Marcos Leonardo Ronceros Ramírez"
id_profesion = "ingeniero"  # Profesión del cliente
id_cat_cliente = 3  # Categoría del cliente (C+)
score_crediticio = 700  # Score de Sentinel o Equifax
edad = 30  # Edad del cliente

# Datos del préstamo:
importe_desembolsado = 8500
p = 24 #Número de cuotas
fecha_desembolso = "27/01/2025"
tipo_garantia = "Garantía Personal"

# Constantes:
tasa_referencial = 4.75 / 100  # BRCP
inflacion = 2.45 / 100  # Inflación actual en porcentaje
td = 0 / 100 # 0.00115 en los bancos
dias_periodo = 32
dias_mes = 31


# Calcular la tasa de interés
tea = calcular_tea(
    tasa_referencial,
    inflacion,
    id_cat_cliente,
    tipo_garantia,
    score_crediticio,
    importe_desembolsado,
    p,
    id_profesion,
    edad
)
print(f"La tasa de interés asignada es: {tea}")

cronograma_prestatario_df, resumen_cronograma_prestatario_df = calcular_cronograma(
    fecha_desembolso,
    importe_desembolsado,
    tea,
    td,
    p,
    nombre_cliente,
    tipo_garantia,
    dias_periodo,
    dias_mes
    )


# Mostrar el resumen del préstamo
print("Resumen del Préstamo:")
print(resumen_cronograma_prestatario_df)

# Mostrar el cronograma de pagos
print("\nCronograma de Pagos:")
print(cronograma_prestatario_df)

# Mostrar la imagen antes de enviar el correo
total_intereses = cronograma_prestatario_df["Interés Mensual (S/)"].sum()

cronograma_a_imagen(cronograma_prestatario_df, resumen_cronograma_prestatario_df,total_intereses)

# Nombre del archivo
nombre_archivo = "Cronograma de cuotas - LR20250127.xlsx"

# Exportar a Excel
exportar_a_excel(cronograma_prestatario_df,resumen_cronograma_prestatario_df, nombre_archivo)


# Enviar el correo con el cronograma como imagen adjunta

enviar_correo_con_imagen(

    correo_destinatario = 'prestamouniversal.pe@outlook.com',
    correo_destino = 'barbaragabriela2820@gmail.com',
    asunto = 'Cronograma de Pagos del Préstamo',
    cuerpo = '<p>Adjunto encontrarás el cronograma de pagos del préstamo solicitado.</p>',
    cronograma_df = cronograma_prestatario_df,
    importe_desembolsado=importe_desembolsado,
    tasa_interes_anual=tasa_interes_anual,
    p=p,
    fecha_inicio_prestamo=fecha_inicio_prestamo,
    cuota_mensual=cuota_mensual,
    total_intereses=total_intereses,
    total_a_pagar=total_a_pagar,
    mostrar_imagen=False

)


# Mostrar la curva del interés
mostrar_curva_interes(cronograma_prestatario_df)

