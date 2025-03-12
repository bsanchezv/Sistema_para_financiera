def calcular_tna(tea):
    tna = (((1 + tea) ** (1 / 12) - 1) * 12) * (365 / 360)
    return tna

print(calcular_tna(0.12))  # Ejemplo de uso