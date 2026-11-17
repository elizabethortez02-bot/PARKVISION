# PARKVISION
# Modulo de deteccion de estacionamientos
# Responsable: David

from pathlib import Path
import cv2

from procesamiento import procesar_imagen


TOTAL_ESPACIOS = 6

# Coordenadas correspondientes a prueba.jpg
# Formato: (x, y, ancho, alto)
ESPACIOS = [
    (189, 156, 64, 120),
    (253, 155, 60, 120),
    (313, 157, 61, 117),
    (373, 158, 61, 117),
    (436, 158, 58, 117),
    (494, 160, 64, 116)
]

UMBRAL = 500


def analizar_imagen(imagen):
    """
    Analiza los seis espacios de estacionamiento
    y calcula la cantidad de bordes de cada uno.
    """

    if imagen is None or imagen.size == 0:
        raise ValueError("La imagen no es valida.")

    procesada = procesar_imagen(imagen)

    alto_imagen, ancho_imagen = procesada.shape[:2]

    resultados = []

    for numero, (x, y, ancho, alto) in enumerate(ESPACIOS, 1):

        if (
            x < 0 or y < 0
            or x + ancho > ancho_imagen
            or y + alto > alto_imagen
        ):
            raise ValueError(
                f"Espacio {numero}: coordenadas fuera de la imagen."
            )

        zona = procesada[y:y + alto, x:x + ancho]

        bordes = cv2.Canny(zona, 50, 150)

        cantidad_bordes = cv2.countNonZero(bordes)

        resultados.append(cantidad_bordes)

    return resultados


def clasificar_espacios(imagen):
    """
    Clasifica los estacionamientos.

    True = Ocupado
    False = Libre
    """

    cantidades = analizar_imagen(imagen)

    estados = []

    for cantidad in cantidades:

        ocupado = cantidad > UMBRAL

        estados.append(ocupado)

    return estados


def detectar_espacios():
    """
    Funcion de compatibilidad con versiones
    anteriores del proyecto.
    """

    return [False, True, False, True, False, False]


def mostrar_resultados(estados):
    """
    Muestra los resultados de deteccion.
    """

    print("\nPARKVISION - DETECCION")
    print("-------------------------")

    for numero, ocupado in enumerate(estados, start=1):

        estado = "Ocupado" if ocupado else "Libre"

        print(f"Espacio {numero}: {estado}")

    print("-------------------------")
    print("Total:", len(estados))
    print("Disponibles:", estados.count(False))
    print("Ocupados:", estados.count(True))


if __name__ == "__main__":
    
    ruta_proyecto = Path(__file__).resolve().parent.parent

    ruta_imagen = ruta_proyecto / "prueba.jpg"

    imagen = cv2.imread(str(ruta_imagen))

    if imagen is None:

        print("ERROR: No se pudo cargar prueba.jpg")

    else:

        try:

            cantidades = analizar_imagen(imagen)

            print("Cantidad de bordes por espacio:")

            for numero, cantidad in enumerate(
                cantidades, start=1
            ):
                print(f"Espacio {numero}: {cantidad} bordes")

            estados = clasificar_espacios(imagen)

            mostrar_resultados(estados)

        except ValueError as error:

            print("ERROR:", error)