
# PARKVISION - Prueba de fotografia real de DroidCam
# Integracion: Xiomara

from pathlib import Path
import cv2

try:
    from src.deteccion_maqueta import (
        clasificar_espacios_maqueta,
        obtener_puntajes_maqueta,
        ESPACIOS,
        UMBRALES
    )
except ModuleNotFoundError as error:
    if error.name != "src":
        raise
    from deteccion_maqueta import (
        clasificar_espacios_maqueta,
        obtener_puntajes_maqueta,
        ESPACIOS,
        UMBRALES
    )

BASE = Path(__file__).resolve().parent.parent
RUTA = BASE / "calibracion_maqueta" / "maqueta_camara.jpg"

imagen = cv2.imread(str(RUTA))

if imagen is None:
    raise SystemExit(
        f"No se encontro la fotografia: {RUTA}"
    )

print("\nPARKVISION - PRUEBA DE CAMARA REAL")
print("Resolucion:", imagen.shape[1], "x", imagen.shape[0])

try:
    estados = clasificar_espacios_maqueta(imagen)
    puntajes = obtener_puntajes_maqueta(imagen)

except ValueError as error:
    raise SystemExit(f"ERROR: {error}")

print("\nRESULTADOS DE DETECCION")
print("--------------------------------")

for numero, (ocupado, puntaje, umbral) in enumerate(
    zip(estados, puntajes, UMBRALES), 1
):
    estado = "OCUPADO" if ocupado else "LIBRE"

    print(
        f"Espacio {numero}: {estado} | "
        f"Cambio: {puntaje:.3f} | "
        f"Umbral: {umbral:.3f}"
    )

print("--------------------------------")
print("Total:", len(estados))
print("Disponibles:", estados.count(False))
print("Ocupados:", estados.count(True))

vista = imagen.copy()

for numero, (x, y, w, h) in enumerate(ESPACIOS, 1):
    ocupado = estados[numero - 1]
    color = (0, 0, 255) if ocupado else (0, 255, 0)

    cv2.rectangle(
        vista, (x, y), (x + w, y + h), color, 2
    )

    cv2.putText(
        vista,
        str(numero),
        (x + 5, y + 25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        color,
        2
    )

SALIDA = BASE / "calibracion_maqueta" / "resultado_camara.jpg"

cv2.imwrite(str(SALIDA), vista)

print("\nImagen de resultados guardada en:")
print(SALIDA)
