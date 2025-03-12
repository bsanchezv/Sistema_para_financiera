import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from datetime import datetime
from dateutil.relativedelta import relativedelta

# ---------------------------------------------------------------------------------------------
# GENERAR EL CRONOGRAMA DE PAGOS DEL PRESTATARIO
# ---------------------------------------------------------------------------------------------

# Configuración de pandas para mostrar números con 2 decimales
pd.options.display.float_format = '{:,.2f}'.format


def calcular_tea(tasa_referencial, inflacion, id_cat_cliente, tipo_garantia, score_crediticio, importe_desembolsado, p, id_profesion, edad):
    """
    Calcula la Tasa Efectiva Anual (TEA) basada en varios factores de ajuste.
    """
    # Ajuste por tasa referencial e inflación
    ajuste_tasa_referencial = tasa_referencial
    ajuste_inflacion = inflacion

    # Ajuste por categoría del cliente
    if id_cat_cliente == 11:  # Categoría F
        raise ValueError(
            "El cliente tiene más de 10 atrasos y no puede generar un préstamo hasta que termine el semestre actual.")
    elif id_cat_cliente == 10:  # Categoría D
        ajuste_categoria = 0.9678
    elif id_cat_cliente == 9:  # Categoría D+
        ajuste_categoria = 0.8622
    elif id_cat_cliente == 8:  # Categoría C-
        ajuste_categoria = 0.7565
    elif id_cat_cliente == 7:  # Categoría C
        ajuste_categoria = 0.6509
    elif id_cat_cliente == 6:  # Categoría C+
        ajuste_categoria = 0.5452
    elif id_cat_cliente == 5:  # Categoría B-
        ajuste_categoria = 0.4396
    elif id_cat_cliente == 4:  # Categoría B
        ajuste_categoria = 0.3339
    elif id_cat_cliente == 3:  # Categoría B+
        ajuste_categoria = 0.2283
    elif id_cat_cliente == 2:  # Categoría A-
        ajuste_categoria = 0.1226
    else:  # Categoría A
        ajuste_categoria = 0.0170

    # Ajuste por score crediticio
    if 877 <= score_crediticio <= 999:
        ajuste_score = 0.0170
    elif 722 <= score_crediticio <= 876:
        ajuste_score = 0.2547
    elif 598 <= score_crediticio <= 721:
        ajuste_score = 0.4924
    elif 477 <= score_crediticio <= 597:
        ajuste_score = 0.7301
    else:
        ajuste_score = 0.9678

    # Ajuste por monto del préstamo
    if importe_desembolsado > 10352:
        ajuste_monto = 0.0170
    elif 9555 <= importe_desembolsado <= 10352:
        ajuste_monto = 0.0536
    elif 9161 <= importe_desembolsado < 9555:
        ajuste_monto = 0.1267
    elif 8764 <= importe_desembolsado < 9161:
        ajuste_monto = 0.1633
    elif 8367 <= importe_desembolsado < 8764:
        ajuste_monto = 0.1998
    elif 7970 <= importe_desembolsado < 8367:
        ajuste_monto = 0.2364
    elif 7573 <= importe_desembolsado < 7970:
        ajuste_monto = 0.2730
    elif 7176 <= importe_desembolsado < 7573:
        ajuste_monto = 0.3096
    elif 6779 <= importe_desembolsado < 7176:
        ajuste_monto = 0.3461
    elif 6382 <= importe_desembolsado < 6779:
        ajuste_monto = 0.3827
    elif 5985 <= importe_desembolsado < 6382:
        ajuste_monto = 0.4193
    elif 5588 <= importe_desembolsado < 5985:
        ajuste_monto = 0.4558
    elif 5191 <= importe_desembolsado < 5588:
        ajuste_monto = 0.4924
    elif 4794 <= importe_desembolsado < 5191:
        ajuste_monto = 0.5290
    elif 4397 <= importe_desembolsado < 4794:
        ajuste_monto = 0.5655
    elif 4000 <= importe_desembolsado < 4397:
        ajuste_monto = 0.6021
    elif 3603 <= importe_desembolsado < 4000:
        ajuste_monto = 0.6387
    elif 3206 <= importe_desembolsado < 3603:
        ajuste_monto = 0.6752
    elif 2809 <= importe_desembolsado < 3206:
        ajuste_monto = 0.7118
    elif 2412 <= importe_desembolsado < 2809:
        ajuste_monto = 0.7484
    elif 2015 <= importe_desembolsado < 2412:
        ajuste_monto = 0.7850
    elif 1618 <= importe_desembolsado < 2015:
        ajuste_monto = 0.8215
    elif 1221 <= importe_desembolsado < 1618:
        ajuste_monto = 0.8581
    elif 824 <= importe_desembolsado < 1221:
        ajuste_monto = 0.8947
    elif 427 <= importe_desembolsado < 824:
        ajuste_monto = 0.9312
    elif 100 <= importe_desembolsado < 427:
        ajuste_monto = 0.9678
    else:  # Caso en que importe_desembolsado sea menor a 100
        raise ValueError("El monto debe ser mayor o igual a S/100.")

    # Ajuste por número de cuotas
    if 1 <= p < 2:
        ajuste_cuotas = 0.0170
    elif 2 <= p < 3:
        ajuste_cuotas = 0.0536
    elif 3 <= p < 4:
        ajuste_cuotas = 0.0901
    elif 4 <= p < 5:
        ajuste_cuotas = 0.1267
    elif 5 <= p < 7:
        ajuste_cuotas = 0.1633
    elif 7 <= p < 8:
        ajuste_cuotas = 0.1998
    elif 8 <= p < 9:
        ajuste_cuotas = 0.2364
    elif 9 <= p < 10:
        ajuste_cuotas = 0.2730
    elif 10 <= p < 11:
        ajuste_cuotas = 0.3096
    elif 11 <= p < 12:
        ajuste_cuotas = 0.3461
    elif 12 <= p < 13:
        ajuste_cuotas = 0.3827
    elif 13 <= p < 14:
        ajuste_cuotas = 0.4193
    elif 14 <= p < 15:
        ajuste_cuotas = 0.4558
    elif 15 <= p < 16:
        ajuste_cuotas = 0.4924
    elif 16 <= p < 18:
        ajuste_cuotas = 0.5290
    elif 18 <= p < 19:
        ajuste_cuotas = 0.5655
    elif 19 <= p < 20:
        ajuste_cuotas = 0.6021
    elif 20 <= p < 21:
        ajuste_cuotas = 0.6387
    elif 21 <= p < 22:
        ajuste_cuotas = 0.6752
    elif 22 <= p < 23:
        ajuste_cuotas = 0.7118
    elif 23 <= p < 24:
        ajuste_cuotas = 0.7484
    elif 24 <= p < 25:
        ajuste_cuotas = 0.7850
    elif 25 <= p < 26:
        ajuste_cuotas = 0.8215
    elif 26 <= p < 27:
        ajuste_cuotas = 0.8581
    elif 27 <= p < 29:
        ajuste_cuotas = 0.8947
    elif 29 <= p < 30:
        ajuste_cuotas = 0.9312
    elif 30 <= p < 31:
        ajuste_cuotas = 0.9678
    else:
        raise ValueError("El número de cuotas está fuera del rango permitido.")

    # Ajuste por edad
    if 18 <= edad < 24:
        ajuste_edad = 0.4924
    elif 24 <= edad < 51:
        ajuste_edad = 0.0170
    elif 51 <= edad < 65:
        ajuste_edad = 0.9678
    else:
        raise ValueError("La edad del cliente está fuera del rango permitido.")

    # Ajuste por profesión
    if id_profesion in ["medico", "ingeniero", "empleado_publico"]:
        ajuste_profesion = 0.0170
    elif id_profesion in ["comerciante", "emprendedor"]:
        ajuste_profesion = 0.4924
    else:
        ajuste_profesion = 0.9678

    # Ajuste por garantía ofrecida
    if tipo_garantia == "Garantía Material":
        ajuste_garantia = 0.0170
    elif tipo_garantia == "Garantía Personal":
        ajuste_garantia = 0.4924
    else:  # Sin garantía
        ajuste_garantia = 0.9678

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
    tna = (((1 + tea) ** (1 / 12) - 1) * 12) * (365 / 360)
    return tna


def validar_datos(fecha_desembolso, importe_desembolsado, p):
    """
    Valida los datos de entrada para asegurar que sean correctos.
    """
    try:
        datetime.strptime(fecha_desembolso, '%d/%m/%Y')
    except ValueError:
        raise ValueError(
            "La fecha de desembolso no tiene el formato correcto (dd/mm/yyyy).")

    if importe_desembolsado <= 0:
        raise ValueError("El importe desembolsado debe ser mayor que 0.")

    if p <= 0:
        raise ValueError("El número de cuotas debe ser mayor que 0.")


def calcular_cronograma(fecha_desembolso, importe_desembolsado, tea, td, p, nombre_cliente, tipo_garantia, dias_periodo, dias_mes):
    """
    Genera el cronograma de pagos para un crédito efectivo.
    """
    # Validar datos de entrada
    validar_datos(fecha_desembolso, importe_desembolsado, p)

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

    # 7. Calcular la cuota referencial (usando la fórmula de cuota constante)
    tasa_total = tasa_ajustada + tasa_seguro
    cuota_referencial = saldo * (tasa_total / (1 - (1 + tasa_total) ** (-p)))

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
        amortizacion_mensual = cuota_referencial - \
            (interes_mensual + seguro_desgravamen_mensual)

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
            "Saldo (S/)": round(saldo if saldo > 0 else 0, 2),
            "Interés Mensual (S/)": round(interes_mensual, 2),
            "Seguro Desgravamen (S/)": round(seguro_desgravamen_mensual, 2),
            "Amortización (S/)": round(amortizacion_mensual, 2),
            "Cuota (S/)": round(cuota_referencial, 2)
        })

    # Calcular la fecha final del pago
    fecha_final_pago = (fecha_desembolso +
                        relativedelta(months=p)).strftime('%d/%m/%Y')

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

# ---------------------------------------------------------------------------------------------

# CONVERTIR EL CRONOGRAMA EN IMAGEN


def cronograma_a_imagen(cronograma_prestatario_df, resumen_cronograma_prestatario_df, cargo_pago_atrasado):
    """
    Convierte el cronograma a una imagen y la muestra con el resumen.
    """
    # Crear figura y ejes
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.axis('off')  # Ocultar los ejes

    # Mostrar el resumen primero
    ax.text(0.5, 0.95, "Resumen del Cronograma", fontsize=12,
            ha="center", va="top", weight="bold")
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
    ax.text(0.5, 0.65, "Cronograma de Pagos", fontsize=12,
            ha="center", va="center", weight="bold")
    tabla_cronograma = ax.table(
        cellText=cronograma_prestatario_df.values,
        colLabels=cronograma_prestatario_df.columns,
        cellLoc='center',
        loc='center',
        bbox=[0.1, 0.25, 0.8, 0.3]  # [left, bottom, width, height]
    )
    tabla_cronograma.auto_set_font_size(False)
    tabla_cronograma.set_fontsize(10)
    tabla_cronograma.scale(1.2, 1.2)

    # Agregar términos y condiciones en el pie de página
    terminos_condiciones = (
        f"- No incluye el ITF en caso de requerir. Transferir en cantidades menores a S/ 1,000.00.\n"
        f"- La tasa de interés es fija.\n"
        f"- Cargo por pago atrasado (S/):  {round(cargo_pago_atrasado, 2)} por día.\n"
        f"- Máximo 7 días de espera después de vencida la cuota."
    )
    # Agregar los términos y condiciones al footer:
    plt.text(0.5, 0.07, terminos_condiciones, ha='center',
             va='center', fontsize=9, wrap=True)

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
        resumen_cronograma_prestatario_df.to_excel(
            writer, sheet_name="Resumen", startrow=0, startcol=0, header=False)

        # Exportar el cronograma al segundo sheet
        cronograma_prestatario_df.to_excel(
            writer, sheet_name="Cronograma", index=False)

        # Obtener el libro y las hojas
        workbook = writer.book
        worksheet_resumen = writer.sheets['Resumen']
        worksheet_cronograma = writer.sheets['Cronograma']

        # Formatear las celdas
        format_header = workbook.add_format(
            {'bold': True, 'align': 'center', 'bg_color': '#D7E4BC'})
        format_cells = workbook.add_format({'align': 'center'})

        # Aplicar formato a las celdas
        worksheet_resumen.set_column('A:A', 30)
        worksheet_resumen.set_column('B:B', 20)
        worksheet_cronograma.set_column('A:G', 20)

        # Aplicar formato a los encabezados
        for col_num, value in enumerate(cronograma_prestatario_df.columns.values):
            worksheet_cronograma.write(0, col_num, value, format_header)

    print(f"Archivo Excel '{nombre_archivo}' generado exitosamente.")


def exportar_a_excel(cronograma_prestatario_df, resumen_cronograma_prestatario_df, nombre_archivo):
    """
    Exporta el cronograma y el resumen a un archivo de Excel con el nombre especificado.
    """
    # Agregar la columna "Estado de la cuota" al cronograma
    cronograma_prestatario_df["Estado de la cuota"] = "Pendiente"

    with pd.ExcelWriter(nombre_archivo, engine='xlsxwriter') as writer:
        # Exportar el resumen al primer sheet
        resumen_cronograma_prestatario_df.to_excel(
            writer, sheet_name="Resumen", startrow=0, startcol=0, header=False)

        # Exportar el cronograma al segundo sheet
        cronograma_prestatario_df.to_excel(
            writer, sheet_name="Cronograma", index=False)

        # Obtener el libro y las hojas
        workbook = writer.book
        worksheet_resumen = writer.sheets['Resumen']
        worksheet_cronograma = writer.sheets['Cronograma']

        # Formatear las celdas
        format_header = workbook.add_format(
            {'bold': True, 'align': 'center', 'bg_color': '#D7E4BC'})
        format_cells = workbook.add_format({'align': 'center'})

        # Aplicar formato a las celdas
        worksheet_resumen.set_column('A:A', 30)
        worksheet_resumen.set_column('B:B', 20)
        worksheet_cronograma.set_column('A:G', 20)

        # Aplicar formato a los encabezados
        for col_num, value in enumerate(cronograma_prestatario_df.columns.values):
            worksheet_cronograma.write(0, col_num, value, format_header)

    print(f"Archivo Excel '{nombre_archivo}' generado exitosamente.")

# ---------------------------------------------------------------------------------------------


# DATOS DE ENTRADA
# Datos del prestatario:
nombre_cliente = "Marcos L. Ronceros R."
id_profesion = "ingeniero"  # Profesión del cliente
id_cat_cliente = 7  # Categoría del cliente (C+)
score_crediticio = 461  # Score de Sentinel o Equifax
edad = 30  # Edad del cliente

# Datos del préstamo:
importe_desembolsado = 200
p = 1  # Número de cuotas
fecha_desembolso = "12/03/2025"
tipo_garantia = "Garantía Personal"

# Constantes:
tasa_referencial = 4.75 / 100  # BRCP
inflacion = 2.45 / 100  # Inflación actual en porcentaje
td = 0 / 100  # 0.00115 en los bancos
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
cargo_pago_atrasado = 2  # Cargo fijo por día de atraso
cronograma_a_imagen(cronograma_prestatario_df, resumen_cronograma_prestatario_df, cargo_pago_atrasado)

# Nombre del archivo
nombre_archivo = "Cronograma de cuotas - LR20250312.xlsx"

# Exportar a Excel
exportar_a_excel(cronograma_prestatario_df, resumen_cronograma_prestatario_df, nombre_archivo)
