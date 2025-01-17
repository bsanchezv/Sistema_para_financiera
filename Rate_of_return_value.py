def calcular_tasa_rendimiento(
    tasa_base,  # Tasa base mínima de rendimiento
    id_niv_inversionista,  # Nivel del inversionista
    monto_inversion,  # Monto invertido
    num_cuotas,  # Número de cuotas del préstamo
    tipo_desembolso  # Tipo de desembolso: único o mensual
):
    # Ajuste por nivel del inversionista
    if id_niv_inversionista == 5:  # Nivel Bronce
        ajuste_nivel = 0.0
    elif id_niv_inversionista == 4:  # Nivel Plata
        ajuste_nivel = 0.5
    elif id_niv_inversionista == 3:  # Nivel Oro
        ajuste_nivel = 1
    elif id_niv_inversionista == 2:  # Nivel Platino
        ajuste_nivel = 1.5
    elif id_niv_inversionista == 1:  # Nivel Diamante
        ajuste_nivel = 2
    else:
        raise ValueError("El nivel del inversionista no es válido.")

    # Ajuste por monto de la inversión
    if monto_inversion > 10000:
        ajuste_monto = 5.0
    elif 5000.01 <= monto_inversion <= 10000:
        ajuste_monto = 4.0
    elif 3000.01 <= monto_inversion <= 5000:
        ajuste_monto = 3.0
    elif 1000.01 <= monto_inversion <= 3000:
        ajuste_monto = 2.0
    elif 500.01 <= monto_inversion <= 1000:
        ajuste_monto = 1.0
    else:  # 0.01 <= monto_inversion <= 500
        ajuste_monto = 0.0

    # Ajuste por número de cuotas del préstamo
    if 1 <= num_cuotas <= 6:
        ajuste_desembolsos = 0.0
    elif 7 <= num_cuotas <= 12:
        ajuste_desembolsos = 0.5
    elif 13 <= num_cuotas <= 18:
        ajuste_desembolsos = 1.0
    elif 19 <= num_cuotas <= 24:
        ajuste_desembolsos = 1.5
    elif 25 <= num_cuotas <= 30:
        ajuste_desembolsos = 2.0
    else:
        raise ValueError("El número de desembolsos está fuera del rango permitido.")

    # Ajuste por tipo de desembolso
    if tipo_desembolso == "único":
        factor_tipo_desembolso = 1.0
    elif tipo_desembolso == "mensual":
        factor_tipo_desembolso = 0.75
    else:
        raise ValueError("El tipo de desembolso no es válido.")

    # Calcular la tasa final
    tasa_rendimiento = (
        tasa_base
        + ajuste_nivel
        + ajuste_monto
        + ajuste_desembolsos
    ) * factor_tipo_desembolso

    return round(tasa_rendimiento, 2)



# Datos de ejemplo
tasa_base = 47.5/2  # La mitad de la tasa base de interés
id_niv_inversionista = 1  # Nivel del inversionista (Oro)
monto_inversion = 2000  # Monto invertido
num_cuotas = 4  # Número de cuotas del préstamo
tipo_desembolso = "único"  # Tipo de desembolso: único o mensual

# Calcular la tasa de rendimiento
tasa = calcular_tasa_rendimiento(
    tasa_base,
    id_niv_inversionista,
    monto_inversion,
    num_cuotas,
    tipo_desembolso
)

print(f"La tasa de rendimiento asignada es: {tasa}%")
