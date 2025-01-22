def calcular_tasa_interes(tasa_referencial, inflacion, id_cat_cliente, garantia_prestamo, score_crediticio, monto_prestamo, num_cuotas, id_profesion, edad):

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
    if monto_prestamo > 10352:
        ajuste_monto = 0.0116
    elif 9955 <= monto_prestamo < 10352:
        ajuste_monto = 0.0464
    elif 9558 <= monto_prestamo < 9955:
        ajuste_monto = 0.0813
    elif 9161 <= monto_prestamo < 9558:
        ajuste_monto = 0.1161
    elif 8764 <= monto_prestamo < 9161:
        ajuste_monto = 0.1509
    elif 8367 <= monto_prestamo < 8764:
        ajuste_monto = 0.1857
    elif 7970 <= monto_prestamo < 8367:
        ajuste_monto = 0.2206
    elif 7573 <= monto_prestamo < 7970:
        ajuste_monto = 0.2554
    elif 7176 <= monto_prestamo < 7573:
        ajuste_monto = 0.2902
    elif 6779 <= monto_prestamo < 7176:
        ajuste_monto = 0.3250
    elif 6382 <= monto_prestamo < 6779:
        ajuste_monto = 0.3599
    elif 5985 <= monto_prestamo < 6382:
        ajuste_monto = 0.3947
    elif 5588 <= monto_prestamo < 5985:
        ajuste_monto = 0.4295
    elif 5191 <= monto_prestamo < 5588:
        ajuste_monto = 0.4644
    elif 4794 <= monto_prestamo < 5191:
        ajuste_monto = 0.4992
    elif 4397 <= monto_prestamo < 4794:
        ajuste_monto = 0.5340
    elif 4000 <= monto_prestamo < 4397:
        ajuste_monto = 0.5688
    elif 3603 <= monto_prestamo < 4000:
        ajuste_monto = 0.6037
    elif 3206 <= monto_prestamo < 3603:
        ajuste_monto = 0.6385
    elif 2809 <= monto_prestamo < 3206:
        ajuste_monto = 0.6733
    elif 2412 <= monto_prestamo < 2809:
        ajuste_monto = 0.7081
    elif 2015 <= monto_prestamo < 2412:
        ajuste_monto = 0.7430
    elif 1618 <= monto_prestamo < 2015:
        ajuste_monto = 0.7778
    elif 1221 <= monto_prestamo < 1618:
        ajuste_monto = 0.8126
    elif 824 <= monto_prestamo < 1221:
        ajuste_monto = 0.8474
    elif 427 <= monto_prestamo < 824:
        ajuste_monto = 0.8823
    elif 100 <= monto_prestamo < 427:
        ajuste_monto = 0.9171
    else:  # 0.01 <= monto_prestamo < 30
        raise ValueError("El monto debe ser mayor o igual a S/100.")

    # Ajuste por número de cuotas
    if 1 <= num_cuotas < 2:
        ajuste_cuotas = 0.0116
    elif 2 <= num_cuotas < 3:
        ajuste_cuotas = 0.0464
    elif 3 <= num_cuotas < 4:
        ajuste_cuotas = 0.0813
    elif 4 <= num_cuotas < 5:
        ajuste_cuotas = 0.1161
    elif 5 <= num_cuotas < 7:
        ajuste_cuotas = 0.1509
    elif 7 <= num_cuotas < 8:
        ajuste_cuotas = 0.1857
    elif 8 <= num_cuotas < 9:
        ajuste_cuotas = 0.2206
    elif 9 <= num_cuotas < 10:
        ajuste_cuotas = 0.2554
    elif 10 <= num_cuotas < 11:
        ajuste_cuotas = 0.2902
    elif 11 <= num_cuotas < 12:
        ajuste_cuotas = 0.32050
    elif 12 <= num_cuotas < 13:
        ajuste_cuotas = 0.3599
    elif 13 <= num_cuotas < 14:
        ajuste_cuotas = 0.3947
    elif 14 <= num_cuotas < 15:
        ajuste_cuotas = 0.4295
    elif 15 <= num_cuotas < 16:
        ajuste_cuotas = 0.4644
    elif 16 <= num_cuotas < 18:
        ajuste_cuotas = 0.4992
    elif 18 <= num_cuotas < 19:
        ajuste_cuotas = 0.5340
    elif 19 <= num_cuotas < 20:
        ajuste_cuotas = 0.5688
    elif 20 <= num_cuotas < 21:
        ajuste_cuotas = 0.6037
    elif 21 <= num_cuotas < 22:
        ajuste_cuotas = 0.6385
    elif 22 <= num_cuotas < 23:
        ajuste_cuotas = 0.6733
    elif 23 <= num_cuotas < 24:
        ajuste_cuotas = 0.7081
    elif 24 <= num_cuotas < 25:
        ajuste_cuotas = 0.7430
    elif 25 <= num_cuotas < 26:
        ajuste_cuotas = 0.7778
    elif 26 <= num_cuotas < 27:
        ajuste_cuotas = 0.8126
    elif 27 <= num_cuotas < 29:
        ajuste_cuotas = 0.8474
    elif 29 <= num_cuotas < 30:
        ajuste_cuotas = 0.8823
    elif 30 <= num_cuotas < 31:
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
    if garantia_prestamo == "Garantía Material":
        ajuste_garantia = 0.0116
    elif garantia_prestamo == "Garantía Personal":
        ajuste_garantia = 0.4644
    else:  # Sin garantía
        ajuste_garantia = 0.9171

    # Calcular la tasa final
    tasa_interes = (
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

    return round(tasa_interes, 4)


#DATOS

#Datos del préstamo
monto_prestamo = 1500  # Monto del préstamo solicitado
num_cuotas = 4  # Número de cuotas del préstamo
garantia_prestamo = "Garantía Personal"  # Garantía ofrecida

#Datos del prestatario
id_cat_cliente = 2  # Categoría del cliente (C+)
score_crediticio = 920  # Score de Sentinel o Equifax
edad = 30  # Edad del cliente
id_profesion = "ingeniero"  # Profesión del cliente


#Constantes:
tasa_referencial = 4.75 / 100  # BRCP
inflacion = 2.45 / 100  # Inflación actual en porcentaje

# Calcular la tasa de interés
tasa = calcular_tasa_interes(
    tasa_referencial,
    inflacion,
    id_cat_cliente,
    garantia_prestamo,
    score_crediticio,
    monto_prestamo,
    num_cuotas,
    id_profesion,
    edad
)

print(f"La tasa de interés asignada es: {tasa}")