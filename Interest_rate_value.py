def calcular_tasa_interes(
    tasa_base,  # Tasa de referencia del BCRP
    id_cat_cliente,  # Categoría del cliente
    score_crediticio,  # Score de Sentinel o Equifax
    edad,  # Edad del cliente
    id_profesion,  # Profesión del cliente
    inflacion,  # Inflación actual en porcentaje
    monto_prestamo,  # Monto del préstamo solicitado
    num_cuotas,  # Número de cuotas del préstamo
    garantia_prestamo  # Garantía ofrecida
):
    # Ajuste por categoría del cliente
    if id_cat_cliente == 11:  # Categoría F
        raise ValueError("El cliente tiene más de 4 atrasos y no puede generar un préstamo hasta que termine el semestre actual.")
    elif id_cat_cliente == 10:  # Categoría D
        ajuste_categoria = 2
    elif id_cat_cliente == 9:  # Categoría D+
        ajuste_categoria = 1.5
    elif id_cat_cliente == 8:  # Categoría C-
        ajuste_categoria = 1
    elif id_cat_cliente == 7:  # Categoría C
        ajuste_categoria = 0.6
    elif id_cat_cliente == 6:  # Categoría C+
        ajuste_categoria = 0.5
    elif id_cat_cliente == 5:  # Categoría B-
        ajuste_categoria = 0.4
    elif id_cat_cliente == 4:  # Categoría B
        ajuste_categoria = 0.3
    elif id_cat_cliente == 3:  # Categoría B+
        ajuste_categoria = 0.2
    elif id_cat_cliente == 2:  # Categoría A-
        ajuste_categoria = 0.1
    else:  # Categoría A
        ajuste_categoria = 0

    # Ajuste por score crediticio
    if 979 <= score_crediticio <= 1000:
        ajuste_score = 0
    elif 924 <= score_crediticio <= 978:
        ajuste_score = 0.5
    elif 900 <= score_crediticio <= 924:
        ajuste_score = 1
    elif 675 <= score_crediticio <= 899:
        ajuste_score = 2
    else:
        ajuste_score = 2.5

    # Ajuste por edad
    if 18 <= edad <= 24:
        ajuste_edad = 1
    elif 25 <= edad <= 50:
        ajuste_edad = 0
    elif 51 <= edad <= 65:
        ajuste_edad = 1.5
    else:
        raise ValueError("La edad del cliente está fuera del rango permitido.")

    # Ajuste por profesión
    if id_profesion in ["medico", "ingeniero", "empleado_publico"]:
        ajuste_profesion = 0.00
    elif id_profesion in ["comerciante", "emprendedor"]:
        ajuste_profesion = 1
    else:
        ajuste_profesion = 2

    # Ajuste por inflación
    ajuste_inflacion = inflacion

    # Ajuste por monto del préstamo
    if monto_prestamo > 10000:
        ajuste_monto = -3
    elif 5000.01 <= monto_prestamo <= 10000:
        ajuste_monto = -2
    elif 3000.01 <= monto_prestamo <= 5000:
        ajuste_monto = -1
    elif 1000.01 <= monto_prestamo <= 3000:
        ajuste_monto = 0.0
    elif 500.01 <= monto_prestamo <= 1000:
        ajuste_monto = +2
    else:  # 0.01 <= monto_prestamo <= 500
        ajuste_monto = +3

    # Ajuste por número de cuotas
    if 1 <= num_cuotas <= 6:
        ajuste_cuotas = 0.0
    elif 7 <= num_cuotas <= 12:
        ajuste_cuotas = 0.5
    elif 13 <= num_cuotas <= 18:
        ajuste_cuotas = 1
    elif 19 <= num_cuotas <= 24:
        ajuste_cuotas = 1.5
    elif 25 <= num_cuotas <= 30:
        ajuste_cuotas = 2
    else:
        raise ValueError("El número de cuotas está fuera del rango permitido.")

    # Ajuste por garantía ofrecida
    if garantia_prestamo == "solida":
        ajuste_garantia = -1
    elif garantia_prestamo == "personal":
        ajuste_garantia = -0.5
    else:  # Sin garantía
        ajuste_garantia = 0.2

    # Calcular la tasa final
    tasa_interes = (
        tasa_base / 100
        + ajuste_categoria / 100
        + ajuste_score / 100
        + ajuste_edad / 100
        + ajuste_profesion / 100
        + ajuste_inflacion / 100
        + ajuste_monto / 100
        + ajuste_cuotas / 100
        + ajuste_garantia / 100
    )

    return round(tasa_interes, 2)


# Datos de ejemplo

id_cat_cliente = 1  # Categoría del cliente (C+)
score_crediticio = 920  # Score de Sentinel o Equifax
edad = 32  # Edad del cliente
id_profesion = "ingeniero"  # Profesión del cliente
monto_prestamo = 160  # Monto del préstamo solicitado
num_cuotas = 1  # Número de cuotas del préstamo
garantia_prestamo = "personal"  # Garantía ofrecida

#Constantes:
tasa_base = 10  # Inflación actual en porcentaje
inflacion = 1.97  # Inflación actual en porcentaje

# Calcular la tasa de interés
tasa = calcular_tasa_interes(
    tasa_base,
    id_cat_cliente,
    score_crediticio,
    edad,
    id_profesion,
    inflacion,
    monto_prestamo,
    num_cuotas,
    garantia_prestamo
)

print(f"La tasa de interés asignada es: {tasa}")

