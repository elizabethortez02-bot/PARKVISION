# PARKVISION - Deteccion de la maqueta real
# Responsable: David

from pathlib import Path
import cv2
import numpy as np

BASE = Path(__file__).resolve().parent.parent
CARPETA = BASE / "calibracion_maqueta"

RUTA_VACIA = CARPETA / "maqueta_vacia.jpg"

# Coordenadas reales obtenidas por David
ESPACIOS = [
    (311, 319, 67, 101),
    (397, 321, 63, 98),
    (481, 322, 63, 96),
    (546, 251, 92, 68),
    (547, 163, 92, 68),
    (545, 77, 93, 67)
]

# Umbrales calibrados con las fotografias
UMBRALES = [
    0.106,
    0.173,
    0.156,
    0.131,
    0.113,
    0.129
]

_referencia = None


def cargar_referencia():
    global _referencia

    if _referencia is None:
        imagen = cv2.imread(str(RUTA_VACIA))

        if imagen is None:
            raise ValueError(
                f"No se encontro la referencia: {RUTA_VACIA}"
            )

        _referencia = imagen

    return _referencia


def obtener_puntajes_maqueta(imagen):
    if imagen is None or imagen.size == 0:
        raise ValueError("Imagen no valida")

    referencia = cargar_referencia()

    if imagen.shape != referencia.shape:
        raise ValueError(
            "La imagen no coincide con la resolucion "
            "de la referencia"
        )

    alto, ancho = imagen.shape[:2]
    puntajes = []

    for numero, (x, y, w, h) in enumerate(ESPACIOS, 1):
        if x < 0 or y < 0 or x+w > ancho or y+h > alto:
            raise ValueError(
                f"Coordenadas incorrectas en espacio {numero}"
            )

        vacio = referencia[y:y+h, x:x+w]
        actual = imagen[y:y+h, x:x+w]

        gris_vacio = cv2.cvtColor(
            vacio, cv2.COLOR_BGR2GRAY
        )
        gris_actual = cv2.cvtColor(
            actual, cv2.COLOR_BGR2GRAY
        )

        gris_vacio = cv2.GaussianBlur(
            gris_vacio, (5, 5), 0
        )
        gris_actual = cv2.GaussianBlur(
            gris_actual, (5, 5), 0
        )

        diferencia = cv2.absdiff(
            gris_vacio, gris_actual
        )

        _, mascara = cv2.threshold(
            diferencia, 25, 255, cv2.THRESH_BINARY
        )

        puntaje = (
            np.count_nonzero(mascara) / mascara.size
        )

        puntajes.append(float(puntaje))

    return puntajes


def clasificar_espacios_maqueta(imagen):
    """
    True = Ocupado
    False = Libre
    """

    puntajes = obtener_puntajes_maqueta(imagen)

    return [
        puntaje > umbral
        for puntaje, umbral in zip(
            puntajes, UMBRALES
        )
    ]


if __name__ == "__main__":
    ruta = CARPETA / "maqueta_validacion.jpg"
    imagen = cv2.imread(str(ruta))

    if imagen is None:
        raise SystemExit(
            f"No se encontro: {ruta}"
        )

    estados = clasificar_espacios_maqueta(imagen)

    print("\nPARKVISION - MAQUETA REAL")

    for numero, ocupado in enumerate(estados, 1):
        estado = "Ocupado" if ocupado else "Libre"
        print(f"Espacio {numero}: {estado}")

    print("Total:", len(estados))
    print("Disponibles:", estados.count(False))
    print("Ocupados:", estados.count(True))