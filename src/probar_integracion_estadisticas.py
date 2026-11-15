# PARKVISION
# Integracion del modulo de deteccion y estadisticas

from pathlib import Path
import cv2

from deteccion import clasificar_espacios
from estadisticas import calcular_estadisticas


# Buscar la imagen de prueba
ruta = Path(__file__).resolve().parent.parent / "prueba.jpg"

imagen = cv2.imread(str(ruta))

if imagen is None:
    raise FileNotFoundError("No se encontro prueba.jpg")


# Obtener los estados de los estacionamientos
estados = clasificar_espacios(imagen)


# Calcular estadisticas
resultado = calcular_estadisticas(estados)


# Mostrar resultados
print("PARKVISION - INTEGRACION")
print("-----------------------")

print("Estados:", estados)
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