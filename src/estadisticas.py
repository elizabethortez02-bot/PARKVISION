# PARKVISION
# Modulo de estadisticas
# Responsable: Erick


def calcular_estadisticas(estados):
    """
    Recibe los estados de los estacionamientos.

    True = Ocupado
    False = Disponible

    Devuelve cantidades y porcentajes.
    """

    # Validar que los datos sean una lista o tupla
    if not isinstance(estados, (list, tuple)):
        raise ValueError("Se esperaba una lista de estados.")

    # Validar que todos los valores sean booleanos
    if not all(type(estado) is bool for estado in estados):
        raise ValueError("Los estados deben ser True o False.")

    # Calcular cantidades
    total = len(estados)
    ocupados = estados.count(True)
    disponibles = estados.count(False)

    # Calcular porcentajes
    if total > 0:
        porcentaje_ocupacion = round(
            (ocupados / total) * 100, 2
        )

        porcentaje_disponibilidad = round(
            (disponibles / total) * 100, 2
        )
    else:
        porcentaje_ocupacion = 0.0
        porcentaje_disponibilidad = 0.0

    return {
        "total": total,
        "ocupados": ocupados,
        "disponibles": disponibles,
        "porcentaje_ocupacion": porcentaje_ocupacion,
        "porcentaje_disponibilidad": porcentaje_disponibilidad
    }


# PRUEBA DEL MODULO DE ESTADISTICAS
if __name__ == "__main__":

    estados_prueba = [
        False, False, False,
        True, False, True
    ]

    resultado = calcular_estadisticas(estados_prueba)

    print("PARKVISION - ESTADISTICAS")
    print("------------------------")

    print("Total:", resultado["total"])
    print("Ocupados:", resultado["ocupados"])
    print("Disponibles:", resultado["disponibles"])

    print(
        "Ocupacion:",
        f'{resultado["porcentaje_ocupacion"]:.2f}%'
    )

    print(
        "Disponibilidad:",
        f'{resultado["porcentaje_disponibilidad"]:.2f}%'
    )