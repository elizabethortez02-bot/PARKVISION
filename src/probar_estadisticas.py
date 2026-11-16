# PARKVISION
# Pruebas del modulo de estadisticas

from estadisticas import calcular_estadisticas


# PRUEBA 1: Dos ocupados
estados = [False, False, False, True, False, True]
resultado = calcular_estadisticas(estados)

assert resultado["total"] == 6
assert resultado["ocupados"] == 2
assert resultado["disponibles"] == 4
assert resultado["porcentaje_ocupacion"] == 33.33
assert resultado["porcentaje_disponibilidad"] == 66.67

print("PRUEBA 1 APROBADA: Dos ocupados")


# PRUEBA 2: Todos libres
estados = [False, False, False, False, False, False]
resultado = calcular_estadisticas(estados)

assert resultado["ocupados"] == 0
assert resultado["disponibles"] == 6
assert resultado["porcentaje_ocupacion"] == 0.0
assert resultado["porcentaje_disponibilidad"] == 100.0

print("PRUEBA 2 APROBADA: Todos libres")


# PRUEBA 3: Todos ocupados
estados = [True, True, True, True, True, True]
resultado = calcular_estadisticas(estados)

assert resultado["ocupados"] == 6
assert resultado["disponibles"] == 0
assert resultado["porcentaje_ocupacion"] == 100.0
assert resultado["porcentaje_disponibilidad"] == 0.0

print("PRUEBA 3 APROBADA: Todos ocupados")


# PRUEBA 4: Mitad ocupados
estados = [True, False, True, False, True, False]
resultado = calcular_estadisticas(estados)

assert resultado["ocupados"] == 3
assert resultado["disponibles"] == 3
assert resultado["porcentaje_ocupacion"] == 50.0
assert resultado["porcentaje_disponibilidad"] == 50.0

print("PRUEBA 4 APROBADA: Mitad ocupados")


# PRUEBA 5: Lista vacia
resultado = calcular_estadisticas([])

assert resultado["total"] == 0
assert resultado["ocupados"] == 0
assert resultado["disponibles"] == 0
assert resultado["porcentaje_ocupacion"] == 0.0
assert resultado["porcentaje_disponibilidad"] == 0.0

print("PRUEBA 5 APROBADA: Lista vacia")


# PRUEBA 6: Datos invalidos
try:
    calcular_estadisticas(["ocupado", "libre"])
    assert False, "Debio lanzar ValueError con strings"
except ValueError:
    print("PRUEBA 6 APROBADA: Datos invalidos")

print("TODAS LAS PRUEBAS APROBADAS")