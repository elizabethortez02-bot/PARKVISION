# PARKVISION
# Modulo de deteccion de estacionamientos

import cv2
from procesamiento import procesar_imagen

TOTAL_ESPACIOS = 6

# Coordenadas de los seis estacionamientos
# Formato: (x, y, ancho, alto)

ESPACIOS = [
    (189, 156, 64, 120),
    (253, 155, 60, 120),
    (313, 157, 61, 117),
    (373, 158, 61, 117),
    (436, 158, 58, 117),
    (494, 160, 64, 116)
]
def analizar_imagen(imagen):
    procesada = procesar_imagen(imagen)
    resultados = []

    for x, y, ancho, alto in ESPACIOS:
        zona = procesada[y:y + alto, x:x + ancho]

        if zona.size == 0:
            resultados.append(0)
            continue

        bordes = cv2.Canny(zona, 50, 150)
        cantidad_bordes = cv2.countNonZero(bordes)

        resultados.append(cantidad_bordes)

    return resultados

def clasificar_espacios(imagen):
    cantidades = analizar_imagen(imagen)

    UMBRAL = 500

    estados = []

    for cantidad in cantidades:
        ocupado = cantidad > UMBRAL
        estados.append(ocupado)

    return estados


def detectar_espacios():
    # True = ocupado, False = libre
    estados = [False, True, False, True, False, False]
    return estados
 
 
if __name__ == "__main__":
    from pathlib import Path

    ruta = Path(__file__).resolve().parent.parent / "prueba.jpg"
    imagen = cv2.imread(str(ruta))

    if imagen is None:
        print("No se pudo cargar prueba.jpg")
    else:
        estados = clasificar_espacios(imagen)

        for numero, ocupado in enumerate(estados, start=1):
            estado = "Ocupado" if ocupado else "Libre"
            print(f"Espacio {numero}: {estado}")

        print("Disponibles:", estados.count(False))
        print("Ocupados:", estados.count(True))