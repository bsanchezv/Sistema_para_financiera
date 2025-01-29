def calcular_tasa_rendimiento(
    inflacion,  # Tasa base mínima de rendimiento
    id_niv_inversionista,  # Nivel del inversionista
    monto_inversion,  # Monto invertido
    num_meses,  # Número de cuotas del préstamo
    tipo_desembolso  # Tipo de desembolso: único o mensual
):
    ajuste_inflacion = inflacion

    # Ajuste por nivel del inversionista
    if id_niv_inversionista == 5:  # Nivel Bronce
        ajuste_nivel = 0.0000
    elif id_niv_inversionista == 4:  # Nivel Plata
        ajuste_nivel = 0.0189
    elif id_niv_inversionista == 3:  # Nivel Oro
        ajuste_nivel = 0.0378
    elif id_niv_inversionista == 2:  # Nivel Platino
        ajuste_nivel = 0.0566
    elif id_niv_inversionista == 1:  # Nivel Diamante
        ajuste_nivel = 0.0755
    else:
        raise ValueError("El nivel del inversionista no es válido.")

    # Ajuste por monto de la inversión
    if monto_inversion > 10352:
        ajuste_monto = 0.0000
    elif 9955 <= monto_inversion < 10352:
        ajuste_monto = 0.0029
    elif 9558 <= monto_inversion < 9955:
        ajuste_monto = 0.0058
    elif 9161 <= monto_inversion < 9558:
        ajuste_monto = 0.0087
    elif 8764 <= monto_inversion < 9161:
        ajuste_monto = 0.0116
    elif 8367 <= monto_inversion < 8764:
        ajuste_monto = 0.0145
    elif 7970 <= monto_inversion < 8367:
        ajuste_monto = 0.0174
    elif 7573 <= monto_inversion < 7970:
        ajuste_monto = 0.0203
    elif 7176 <= monto_inversion < 7573:
        ajuste_monto = 0.0232
    elif 6779 <= monto_inversion < 7176:
        ajuste_monto = 0.0261
    elif 6382 <= monto_inversion < 6779:
        ajuste_monto = 0.0290
    elif 5985 <= monto_inversion < 6382:
        ajuste_monto = 0.0319
    elif 5588 <= monto_inversion < 5985:
        ajuste_monto = 0.0348
    elif 5191 <= monto_inversion < 5588:
        ajuste_monto = 0.0378
    elif 4794 <= monto_inversion < 5191:
        ajuste_monto = 0.0407
    elif 4397 <= monto_inversion < 4794:
        ajuste_monto = 0.0436
    elif 4000 <= monto_inversion < 4397:
        ajuste_monto = 0.0465
    elif 3603 <= monto_inversion < 4000:
        ajuste_monto = 0.0494
    elif 3206 <= monto_inversion < 3603:
        ajuste_monto = 0.0523
    elif 2809 <= monto_inversion < 3206:
        ajuste_monto = 0.0552
    elif 2412 <= monto_inversion < 2809:
        ajuste_monto = 0.0581
    elif 2015 <= monto_inversion < 2412:
        ajuste_monto = 0.0610
    elif 1618 <= monto_inversion < 2015:
        ajuste_monto = 0.0639
    elif 1221 <= monto_inversion < 1618:
        ajuste_monto = 0.0668
    elif 824 <= monto_inversion < 1221:
        ajuste_monto = 0.0697
    elif 427 <= monto_inversion < 824:
        ajuste_monto = 0.0726
    elif 100 <= monto_inversion < 427:
        ajuste_monto = 0.0755
    else:  # 0.01 <= monto_prestamo < 30
        raise ValueError("El monto debe ser mayor o igual a S/100.")

    # Ajuste por número de desembolsos o cuotas del préstamo
    if 1 <= num_meses < 2:
        ajuste_desembolsos = 0.0755
    elif 2 <= num_meses < 3:
        ajuste_desembolsos = 0.0726
    elif 3 <= num_meses < 4:
        ajuste_desembolsos = 0.0697
    elif 4 <= num_meses < 5:
        ajuste_desembolsos = 0.0668
    elif 5 <= num_meses < 7:
        ajuste_desembolsos = 0.0639
    elif 7 <= num_meses < 8:
        ajuste_desembolsos = 0.0610
    elif 8 <= num_meses < 9:
        ajuste_desembolsos = 0.0581
    elif 9 <= num_meses < 10:
        ajuste_desembolsos = 0.0552
    elif 10 <= num_meses < 11:
        ajuste_desembolsos = 0.0523
    elif 11 <= num_meses < 12:
        ajuste_desembolsos = 0.0494
    elif 12 <= num_meses < 13:
        ajuste_desembolsos = 0.0465
    elif 13 <= num_meses < 14:
        ajuste_desembolsos = 0.0436
    elif 14 <= num_meses < 15:
        ajuste_desembolsos = 0.0407
    elif 15 <= num_meses < 16:
        ajuste_desembolsos = 0.0378
    elif 16 <= num_meses < 18:
        ajuste_desembolsos = 0.0348
    elif 18 <= num_meses < 19:
        ajuste_desembolsos = 0.0319
    elif 19 <= num_meses < 20:
        ajuste_desembolsos = 0.0290
    elif 20 <= num_meses < 21:
        ajuste_desembolsos = 0.0261
    elif 21 <= num_meses < 22:
        ajuste_desembolsos = 0.0232
    elif 22 <= num_meses < 23:
        ajuste_desembolsos = 0.0203
    elif 23 <= num_meses < 24:
        ajuste_desembolsos = 0.0174
    elif 24 <= num_meses < 25:
        ajuste_desembolsos = 0.0145
    elif 25 <= num_meses < 26:
        ajuste_desembolsos = 0.0116
    elif 26 <= num_meses < 27:
        ajuste_desembolsos = 0.0087
    elif 27 <= num_meses < 29:
        ajuste_desembolsos = 0.0058
    elif 29 <= num_meses < 30:
        ajuste_desembolsos = 0.0029
    elif 30 <= num_meses < 31:
        ajuste_desembolsos = 0.0000
    else:
        raise ValueError("El número de desembolsos está fuera del rango permitido.")

    # Ajuste por tipo de desembolso
    if tipo_desembolso == "único":
        ajuste_tipo_desembolso = 0.0755
    elif tipo_desembolso == "mensual":
        ajuste_tipo_desembolso = 0.0000
    else:
        raise ValueError("El tipo de desembolso no es válido.")

    # Calcular la tasa final
    tasa_rendimiento = (
        ajuste_inflacion * 1.00
        + ajuste_nivel * 0.4
        + ajuste_monto * 0.3
        + ajuste_desembolsos * 0.2
        + ajuste_tipo_desembolso * 0.1
    )

    return round(tasa_rendimiento,4)



# Datos de ejemplo

id_niv_inversionista = 3  # Nivel del inversionista (Oro)
monto_inversion = 100  # Monto invertido
num_meses = 1  # Número de cuotas del préstamo
tipo_desembolso = "único"  # Tipo de desembolso: único o mensual

#Constantes
inflacion = 2.45 / 100 # La inflación

# Calcular la tasa de rendimiento
tasa = calcular_tasa_rendimiento(
    inflacion,
    id_niv_inversionista,
    monto_inversion,
    num_meses,
    tipo_desembolso
)

print(f"La tasa de rendimiento asignada es: {tasa}")

